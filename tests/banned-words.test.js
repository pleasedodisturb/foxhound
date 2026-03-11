import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const BANNED = [
  /\bWolt\b/i,
  /\bDoorDash\b/i,
  /\bcreditornot\b/i,
  /\bMx[- ]CRM\b/i,
  /\bPedregal\b/i,
];

const EXCLUDED_PATHS = [
  'tests/',
  'CHANGELOG.md',
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

describe('No banned company references', () => {
  const files = findMarkdownFiles(ROOT);

  for (const file of files) {
    const rel = path.relative(ROOT, file);
    if (EXCLUDED_PATHS.some(ex => rel.startsWith(ex))) continue;

    it(`${rel} is clean`, () => {
      const content = fs.readFileSync(file, 'utf8');
      const lines = content.split('\n');

      for (let i = 0; i < lines.length; i++) {
        for (const pattern of BANNED) {
          const match = lines[i].match(pattern);
          if (match) {
            assert.fail(
              `Banned word "${match[0]}" found in ${rel}:${i + 1}: ${lines[i].trim()}`
            );
          }
        }
      }
    });
  }
});
