"""
Resilient job scraper with rate limiting, retries, and anti-detection.

Wraps existing scrapers (scraper.py, germany_jobs.py) and adds:
- Rate limiting with configurable delays between requests
- User-agent rotation
- Retry with exponential backoff on transient failures
- Optional headless browser fallback via Playwright
- Source prioritization (API-first, browser as fallback)
- Structured output for the daily pipeline

Usage:
    .venv/bin/python tools/scrape_resilient.py
    .venv/bin/python tools/scrape_resilient.py --sources api-only
    .venv/bin/python tools/scrape_resilient.py --sources all --hours 24
"""

from __future__ import annotations

import json
import logging
import os
import random
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# Add project root to path so we can import sibling modules
sys.path.insert(0, str(Path(__file__).parent))

import germany_jobs
from scraper import scrape_all as jobspy_scrape

logger = logging.getLogger("scrape_resilient")

# --- Configuration ---

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
]

# Delays between source scrapes (seconds)
MIN_DELAY = 2.0
MAX_DELAY = 5.0

# Retry config
MAX_RETRIES = 3
BACKOFF_BASE = 2.0


@dataclass
class ScrapedJob:
    """Normalized job record from any source."""
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str = ""
    posted: str = ""
    remote: bool = False
    salary: str = ""
    tags: list[str] = field(default_factory=list)
    search_keyword: str = ""
    scraped_at: str = ""

    def dedup_key(self) -> tuple[str, str]:
        return (self.title.lower().strip(), self.company.lower().strip())


def _random_delay():
    """Sleep for a random duration to avoid detection."""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    logger.debug(f"Rate limit delay: {delay:.1f}s")
    time.sleep(delay)


def _get_user_agent() -> str:
    return random.choice(USER_AGENTS)


def _retry_with_backoff(func, *args, **kwargs):
    """Execute func with exponential backoff on failure."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            wait = BACKOFF_BASE ** attempt + random.uniform(0, 1)
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}. Retrying in {wait:.1f}s")
            time.sleep(wait)
    logger.error(f"All {MAX_RETRIES} retries failed: {last_error}")
    return None


# --- Source: Germany APIs (Arbeitsagentur + Arbeitnow) ---

def scrape_germany_apis(
    presets: list[str] | None = None,
    location: str = "Berlin",
    limit: int = 25,
    remote: bool = False,
) -> list[ScrapedJob]:
    """Scrape German job APIs — pure API, no browser needed."""
    presets = presets or ["all"]
    jobs: list[ScrapedJob] = []
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    for preset in presets:
        keyword_list = []
        if preset == "all":
            for kws in germany_jobs.PRESETS.values():
                keyword_list.extend(kws)
        elif preset in germany_jobs.PRESETS:
            keyword_list = germany_jobs.PRESETS[preset]
        else:
            keyword_list = [preset]

        def _fetch():
            return germany_jobs.fetch_all_for_keywords(
                keyword_list=keyword_list,
                location=location,
                limit=limit,
                remote=remote,
                sources=["arbeitsagentur", "arbeitnow"],
            )

        result = _retry_with_backoff(_fetch)
        if result is None:
            continue

        raw_jobs, aa_count, an_count = result
        logger.info(f"Germany APIs ({preset}): {len(raw_jobs)} jobs ({aa_count} AA, {an_count} AN)")

        for j in raw_jobs:
            if germany_jobs.is_likely_german_only(j):
                continue
            jobs.append(ScrapedJob(
                title=j.get("title", ""),
                company=j.get("company", ""),
                location=j.get("location", ""),
                url=j.get("url", ""),
                source=j.get("source", "germany_api"),
                posted=j.get("posted", ""),
                remote=j.get("remote", False),
                tags=j.get("tags", []),
                scraped_at=now,
            ))
        _random_delay()

    return jobs


# --- Source: JobSpy (LinkedIn, Indeed, Glassdoor, Google) ---

def scrape_jobspy(
    keywords: list[str] | None = None,
    location: str | None = None,
    hours_old: int = 24,
    results_per_keyword: int = 20,
    sites: list[str] | None = None,
) -> list[ScrapedJob]:
    """
    Scrape via python-jobspy. This uses HTTP requests (not a browser)
    to search LinkedIn, Indeed, Glassdoor, and Google Jobs.

    NOTE: LinkedIn scraping via jobspy uses public listing pages. For
    authenticated access (saved jobs, Easy Apply), you'd need browser
    automation — but that's fragile and against ToS. We intentionally
    stick to public-facing data.
    """
    jobs: list[ScrapedJob] = []
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def _fetch():
        return jobspy_scrape(
            keywords=keywords,
            location=location or "Your City, Country",
            hours_old=hours_old,
            results_per_keyword=results_per_keyword,
            sites=sites,
        )

    df = _retry_with_backoff(_fetch)
    if df is None or df.empty:
        logger.info("JobSpy: no results")
        return jobs

    logger.info(f"JobSpy: {len(df)} unique jobs")

    for _, row in df.iterrows():
        jobs.append(ScrapedJob(
            title=str(row.get("title", "")),
            company=str(row.get("company", "")),
            location=str(row.get("location", "")),
            url=str(row.get("job_url", row.get("link", ""))),
            source=str(row.get("site", "jobspy")),
            description=str(row.get("description", "")),
            posted=str(row.get("date_posted", "")),
            search_keyword=str(row.get("search_keyword", "")),
            scraped_at=now,
        ))

    return jobs


# --- Source: Headless browser (Playwright) — fallback only ---

def scrape_with_browser(
    urls: list[str],
    extract_selector: str = "body",
) -> list[dict]:
    """
    Headless browser scraping via Playwright — USE SPARINGLY.

    This is the fallback for sites that:
    1. Require JavaScript rendering
    2. Block HTTP scrapers
    3. Have data behind client-side rendering

    Anti-detection measures:
    - Random viewport sizes
    - Human-like delays between actions
    - Stealth mode (no webdriver flag)
    - Random user agents

    IMPORTANT: This should NOT be used for LinkedIn or Indeed at scale.
    Those sites actively detect and block headless browsers. Use their
    public listings via python-jobspy instead.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("Playwright not installed. Skipping browser scraping. Install: pip install playwright && playwright install chromium")
        return []

    results = []
    viewports = [
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 1440, "height": 900},
        {"width": 1536, "height": 864},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        for url in urls:
            try:
                context = browser.new_context(
                    viewport=random.choice(viewports),
                    user_agent=_get_user_agent(),
                )
                page = context.new_page()

                # Remove webdriver flag
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                """)

                page.goto(url, wait_until="networkidle", timeout=30000)

                # Human-like delay
                time.sleep(random.uniform(2, 5))

                content = page.query_selector(extract_selector)
                text = content.inner_text() if content else page.content()

                results.append({
                    "url": url,
                    "content": text,
                    "title": page.title(),
                    "scraped_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                })

                context.close()
                _random_delay()

            except Exception as e:
                logger.error(f"Browser scrape failed for {url}: {e}")
                results.append({"url": url, "content": "", "error": str(e)})

        browser.close()

    return results


# --- Deduplication ---

def deduplicate(jobs: list[ScrapedJob]) -> list[ScrapedJob]:
    """Remove duplicate jobs by (title, company) key."""
    seen: set[tuple[str, str]] = set()
    unique: list[ScrapedJob] = []
    for job in jobs:
        key = job.dedup_key()
        if key not in seen:
            seen.add(key)
            unique.append(job)
    logger.info(f"Dedup: {len(jobs)} → {len(unique)} unique jobs")
    return unique


# --- Main orchestrator ---

def scrape_all_sources(
    mode: str = "api-only",
    keywords: list[str] | None = None,
    location: str | None = None,
    hours_old: int = 24,
    germany_presets: list[str] | None = None,
    jobspy_sites: list[str] | None = None,
    browser_urls: list[str] | None = None,
) -> list[ScrapedJob]:
    """
    Scrape all configured sources and return deduplicated jobs.

    Modes:
        api-only   — Germany APIs + JobSpy HTTP only (safest, fastest)
        api-plus   — Above + career page browser scraping
        all        — All sources including browser fallback
    """
    all_jobs: list[ScrapedJob] = []

    # 1. Germany APIs (always — pure API, zero risk)
    logger.info("=== Source: Germany APIs ===")
    try:
        germany_results = scrape_germany_apis(
            presets=germany_presets or ["all"],
            location=location or "Berlin",
            remote=True,
        )
        all_jobs.extend(germany_results)
    except Exception as e:
        logger.error(f"Germany APIs failed: {e}")

    _random_delay()

    # 2. JobSpy HTTP scraper (LinkedIn, Indeed, Glassdoor, Google)
    logger.info("=== Source: JobSpy ===")
    try:
        jobspy_results = scrape_jobspy(
            keywords=keywords,
            location=location,
            hours_old=hours_old,
            sites=jobspy_sites,
        )
        all_jobs.extend(jobspy_results)
    except Exception as e:
        logger.error(f"JobSpy failed: {e}")

    # 3. Browser scraping (only in api-plus or all mode)
    if mode in ("api-plus", "all") and browser_urls:
        logger.info("=== Source: Browser (career pages) ===")
        _random_delay()
        raw = scrape_with_browser(browser_urls)
        for item in raw:
            if item.get("content") and not item.get("error"):
                all_jobs.append(ScrapedJob(
                    title=item.get("title", ""),
                    company="",
                    location="",
                    url=item["url"],
                    source="browser",
                    description=item["content"][:5000],
                    scraped_at=item.get("scraped_at", ""),
                ))

    # Deduplicate
    all_jobs = deduplicate(all_jobs)
    logger.info(f"Total after all sources: {len(all_jobs)} jobs")

    return all_jobs


def save_results(jobs: list[ScrapedJob], output_dir: Path) -> Path:
    """Save scraped jobs to JSON for downstream processing."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"scraped_raw_{date_str}.json"

    data = [asdict(j) for j in jobs]
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.info(f"Saved {len(data)} jobs to {output_path}")
    return output_path


def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Resilient multi-source job scraper")
    parser.add_argument("--mode", choices=["api-only", "api-plus", "all"], default="api-only",
                        help="Scraping mode (default: api-only)")
    parser.add_argument("--keywords", nargs="+", help="Search keywords for JobSpy")
    parser.add_argument("--location", help="Location filter")
    parser.add_argument("--hours", type=int, default=24, help="Max posting age in hours (default: 24)")
    parser.add_argument("--germany-presets", nargs="+", default=["all"],
                        help="Germany job presets (default: all)")
    parser.add_argument("--jobspy-sites", nargs="+", help="JobSpy sites to search")
    parser.add_argument("--browser-urls", nargs="+", help="Career page URLs for browser scraping")
    parser.add_argument("--output-dir", default="tracking", help="Output directory")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    output_dir = project_root / args.output_dir

    jobs = scrape_all_sources(
        mode=args.mode,
        keywords=args.keywords,
        location=args.location,
        hours_old=args.hours,
        germany_presets=args.germany_presets,
        jobspy_sites=args.jobspy_sites,
        browser_urls=args.browser_urls,
    )

    if jobs:
        output_path = save_results(jobs, output_dir)
        print(f"\nDone. {len(jobs)} jobs saved to {output_path}")
    else:
        print("\nNo jobs found across any source.")


if __name__ == "__main__":
    main()
