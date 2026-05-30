# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

`aiogram_tests` uses independent SemVer and is released alongside aiogram:
each release declares the supported aiogram range via its dependency constraint.

<!-- BEGIN RELEASES -->

## [1.1.0] - 2026-05-29

**Supported aiogram:** `>=3.28,<4`

### Security
- Refresh the dependency lock so all transitive dependencies resolve to
  non-vulnerable versions (aiohttp `3.13.5`, certifi `2026.5.20`, idna `3.17`,
  pydantic `2.13.4`).
- Bump dev tooling past known advisories: pytest `>=9.0.3` (tmpdir handling)
  and pytest-asyncio `>=1.4.0`.

### Changed
- Track the latest aiogram release: bump the constraint to `^3.28`.
- Move `pytest`, `pytest-asyncio` and `tox` out of the runtime dependencies into
  the `dev` group — the published package now only requires `aiogram`.
- Modernize type hints (pyupgrade) and apply consistent formatting.

### Tooling
- Replace black / pyupgrade / reorder-python-imports / autoflake with
  [ruff](https://docs.astral.sh/ruff/) (lint + format) in pre-commit and CI.
- Add GitHub Actions CI (ruff + pytest on Python 3.12 / 3.13).
- Add a tag-triggered release workflow that publishes to PyPI via
  Trusted Publishing (OIDC).
- Enable Dependabot version and security updates.
