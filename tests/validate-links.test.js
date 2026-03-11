import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');

function findMarkdownFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    if (entry.isDirectory()) {
      results.push(...findMarkdownFiles(full));
    } else if (entry.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

function extractLinks(content) {
  const links = [];
  const regex = /\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const href = match[2].split('#')[0].split('?')[0].trim();
    if (href && !href.startsWith('http') && !href.startsWith('mailto:')) {
      links.push({ text: match[1], href: match[2], raw: href });
    }
  }
  return links;
}

describe('Markdown relative links', () => {
  const files = findMarkdownFiles(ROOT);

  for (const file of files) {
    const rel = path.relative(ROOT, file);
    const content = fs.readFileSync(file, 'utf8');
    const links = extractLinks(content);

    for (const link of links) {
      it(`${rel} → ${link.raw}`, () => {
        const resolved = path.resolve(path.dirname(file), link.raw);
        assert.ok(
          fs.existsSync(resolved),
          `Broken link in ${rel}: [${link.text}](${link.href}) → ${link.raw} not found`
        );
      });
    }
  }
});
