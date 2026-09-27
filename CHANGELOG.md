# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

`aiogram_tests` uses independent SemVer and is released alongside aiogram:
each release declares the supported aiogram range via its dependency constraint.

## [1.2.0](https://github.com/k0te1ch/aiogram_tests/compare/v1.1.0...v1.2.0) (2026-09-27)


### Features

* BotTester for whole routers and a pytest plugin ([#9](https://github.com/k0te1ch/aiogram_tests/issues/9)) ([e77608c](https://github.com/k0te1ch/aiogram_tests/commit/e77608c3e681f910bb2ab1771fa33090d5ce81e6))
* **deps:** support aiogram 3.23+ and test the whole range in CI ([#6](https://github.com/k0te1ch/aiogram_tests/issues/6)) ([d9adaa7](https://github.com/k0te1ch/aiogram_tests/commit/d9adaa7b41eed09600f661b08f1823d53695cea5))
* handlers for every update type ([#8](https://github.com/k0te1ch/aiogram_tests/issues/8)) ([6d467ca](https://github.com/k0te1ch/aiogram_tests/commit/6d467cad04b9db46a3003947d72f2cc24157e12a))
* **requester:** return aiogram method objects and add call assertions ([#7](https://github.com/k0te1ch/aiogram_tests/issues/7)) ([b856af3](https://github.com/k0te1ch/aiogram_tests/commit/b856af39abfaf047215bc3a28c0af2c243b7d374))


### Bug Fixes

* handler registration, FSM context and call collection ([#4](https://github.com/k0te1ch/aiogram_tests/issues/4)) ([3b30f21](https://github.com/k0te1ch/aiogram_tests/commit/3b30f21309af71714ce6e52b12c03b1ccf0e9201))

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
