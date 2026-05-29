# Changelog

All notable changes to this project are documented in this file.

## Versioning policy

`aiogram_tests` follows [Semantic Versioning](https://semver.org/) with its own
independent version numbers. Because the library is tightly coupled to aiogram
internals, a new release is cut **alongside aiogram releases**: each release
declares the supported aiogram range via its dependency constraint, and the
supported aiogram version is recorded in the entry below.

## [1.1.0]

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
