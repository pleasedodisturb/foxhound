import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');

// Prompt templates — not standard markdown docs
const HEADING_EXCLUDED = [
  '.claude/commands/',
];

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

describe('Markdown quality', () => {
  const files = findMarkdownFiles(ROOT);

  describe('Files start with heading', () => {
    for (const file of files) {
      const rel = path.relative(ROOT, file);
      if (HEADING_EXCLUDED.some(ex => rel.startsWith(ex))) continue;
      it(rel, () => {
        const content = fs.readFileSync(file, 'utf8');
        assert.ok(
          content.startsWith('# '),
          `${rel} should start with a # heading`
        );
      });
    }
  });

  describe('Files end with newline', () => {
    for (const file of files) {
      const rel = path.relative(ROOT, file);
      it(rel, () => {
        const content = fs.readFileSync(file, 'utf8');
        assert.ok(
          content.endsWith('\n'),
          `${rel} should end with a newline`
        );
      });
    }
  });

  describe('No excessive blank lines', () => {
    for (const file of files) {
      const rel = path.relative(ROOT, file);
      it(rel, () => {
        const content = fs.readFileSync(file, 'utf8');
        assert.ok(
          !content.includes('\n\n\n\n'),
          `${rel} has 3+ consecutive blank lines`
        );
      });
    }
  });
});
