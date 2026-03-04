private note: output was 384 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmptsYmz4 do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 
                    an_count += 1

    return all_jobs, aa_count, an_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search Germany job APIs (Arbeitsagentur, Arbeitnow)"
    )
    parser.add_argument(
        "--keywords",
        default="",
        help="Search keywords, comma-separated for multi-search (e.g. 'TPM,Product Manager')"
    )
    parser.add_argument(
        "--preset",
        choices=["tpm", "pm", "ai", "builder", "all"],
        help="Keyword preset: tpm, pm, ai, builder, or all"
    )
    parser.add_argument("--location", default="Frankfurt", help="Location (default: Frankfurt)")
    parser.add_argument("--limit", type=int, default=25, help="Max results per keyword per source (default: 25)")
    parser.add_argument("--remote", action="store_true", help="Filter remote/telework only")
    parser.add_argument("--output", choices=["csv", "json"], default="csv", help="Output format")
    parser.add_argument("--english-only", action="store_true", help="Filter out likely German-language-only jobs")
    parser.add_argument(
        "--sources",
        nargs="+",
        default=["arbeitsagentur", "arbeitnow"],
        help="Source APIs to query"
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="Print a rough fit score (1-5 stars) based on keyword signals"
    )
    args = parser.parse_args()

    # Determine keyword list
    keyword_list: list[str] = []
    if args.preset:
        if args.preset == "all":
            for kws in PRESETS.values():
                keyword_list.extend(kws)
        else:
            keyword_list = PRESETS[args.preset]
        print(f"Using preset '{args.preset}': {keyword_list}", file=sys.stderr)
    elif args.keywords:
        # Support comma-separated multi-keyword
        keyword_list = [k.strip() for k in args.keywords.split(",") if k.strip()]
    else:
        keyword_list = [""]  # empty search = broad fetch

    # Fetch jobs
    all_jobs, aa_total, an_total = fetch_all_for_keywords(
        keyword_list=keyword_list,
        location=args.location,
        limit=args.limit,
        remote=args.remote,
        sources=args.sources,
    )

    if not all_jobs:
        print("No jobs found.", file=sys.stderr)
        print(f"Found 0 jobs total (0 from Arbeitsagentur, 0 from Arbeitnow)", file=sys.stderr)
        return

    # Score all jobs
    for j in all_jobs:
        j["score"] = score_job(j)

    if args.output == "json":
        print(json.dumps(all_jobs, indent=2, ensure_ascii=False))
    else:
        # CSV output
        headers = ["source", "title", "company", "location", "url", "posted"]
        if args.score:
            headers.append("score")
        print(",".join(headers))
        for j in all_jobs:
            row = [str(j.get(h, "")).replace(",", ";") for h in headers if h != "score"]
            if args.score:
                row.append(str(j.get("score", 1)))
            print(",".join(row))

    # Summary line (always printed to stdout so it's visible)
    total = len(all_jobs)
    summary = f"Found {total} jobs total ({aa_total} from Arbeitsagentur, {an_total} from Arbeitnow)"
    if args.score:
        # Also print score breakdown
        score_dist = {}
        for j in all_jobs:
            s = j.get("score", 1)
            score_dist[s] = score_dist.get(s, 0) + 1
        score_str = " | ".join(f"{stars(s)}:{count}" for s, count in sorted(score_dist.items(), reverse=True))
        summary += f"  [{score_str}]"
    print(summary, file=sys.stderr)


if __name__ == "__main__":
    main()