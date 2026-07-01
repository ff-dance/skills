# Changelog

## 2026-07-01

### Added

- Added SkillOpt training assets under `evals/skillopt/` for schema, rubric, mapping, and split data.
- Added a repo-local SkillOpt overlay under `tooling/skillopt-overlay/` for configs, prompts, adapters, and model glue code.
- Added automation entry points with `README.md`, `Makefile`, `.env.skillopt.local.example`, and helper scripts for install, train, verify, and upgrade workflows.

### Changed

- Refined `SKILL.md` and the supporting references to align the Siemens slide skill with the new planning, evaluation, and verification loop.
- Updated `agents/openai.yaml`, `references/content-brief.md`, and `references/quality-checklist.md` to match the current spec-driven workflow.
- Expanded `.gitignore` to keep local env files and generated artifacts out of git.

### Fixed

- Replaced hardcoded repository file links in documentation with relative links.
- Removed direct machine-specific path references from documentation and SkillOpt helper defaults in favor of environment overrides and sibling checkout discovery.
