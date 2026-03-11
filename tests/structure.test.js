import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');

const REQUIRED_FILES = [
  'README.md',
  'LICENSE',
  'AGENT.md',
  'CLAUDE.md',
  'CONTRIBUTING.md',
  '.goosehints',
  '.cursorrules',
  '.gitignore',
  'requirements.txt',
  'package.json',
  'profile/target-roles.md',
  'profile/README.md',
  'tracking/applications.csv.example',
  'cv/cv.yaml.example',
  '.mcp.json.example',
  'docs/SETUP.md',
  'docs/architecture.md',
];

const REQUIRED_DIRS = [
  'profile',
  'tracking',
  'tools',
  'cv',
  'docs',
  'recipes',
  'research',
  '.claude/commands',
  '.github/workflows',
];

describe('Project structure', () => {
  describe('Required files exist', () => {
    for (const file of REQUIRED_FILES) {
      it(file, () => {
        assert.ok(
          fs.existsSync(path.join(ROOT, file)),
          `Required file missing: ${file}`
        );
      });
    }
  });

  describe('Required directories exist', () => {
    for (const dir of REQUIRED_DIRS) {
      it(dir, () => {
        const full = path.join(ROOT, dir);
        assert.ok(
          fs.existsSync(full) && fs.statSync(full).isDirectory(),
          `Required directory missing: ${dir}`
        );
      });
    }
  });

  describe('Tools directory has Python scripts', () => {
    it('has at least 3 .py files', () => {
      const pyFiles = fs.readdirSync(path.join(ROOT, 'tools'))
        .filter(f => f.endsWith('.py'));
      assert.ok(pyFiles.length >= 3, `Expected 3+ .py files, found ${pyFiles.length}`);
    });
  });

  describe('Recipes directory has YAML workflows', () => {
    it('has at least 2 .yaml files', () => {
      const yamlFiles = fs.readdirSync(path.join(ROOT, 'recipes'))
        .filter(f => f.endsWith('.yaml'));
      assert.ok(yamlFiles.length >= 2, `Expected 2+ .yaml files, found ${yamlFiles.length}`);
    });
  });

  describe('Claude commands exist', () => {
    it('has at least 2 command files', () => {
      const cmds = fs.readdirSync(path.join(ROOT, '.claude', 'commands'))
        .filter(f => f.endsWith('.md'));
      assert.ok(cmds.length >= 2, `Expected 2+ command files, found ${cmds.length}`);
    });
  });
});
