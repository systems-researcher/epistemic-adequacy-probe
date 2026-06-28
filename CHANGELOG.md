# Changelog

All notable changes to this artefact are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `requirements.txt`: pinned harness dependencies (anthropic, PyYAML) for
  replicable re-runs (RR-R-01).
- `ETHICS.md`: responsible-use / dual-use statement (RR-R-06).
- Run-provenance envelope in `harness/run_probe.py` (harness version, UTC
  timestamp, parameters, and the served model versions the API actually ran)
  plus a "Run provenance" section in `RESULTS.md` (RR-R-02).

## [0.1.0] - 2026-06-10

First public release of the consumption probe, prepared as an anonymised companion
artefact for double-blind review.

### Added
- Probe instrument: 15 derivation-style questions with ground-truth keys and scoring
  rubric (`probes.json`).
- Substrates: verbatim Apollo 11 SysML v2 excerpt (MPL-2.0, Airbus), a hand-authored
  epistemic-adequacy sidecar, and a fictional out-of-distribution control vehicle
  (`substrate/`).
- Reproducible harness: probe runner, cross-family judge recheck, and substrate builder
  (`harness/`).
- Results: raw per-question responses and verdicts, and the cross-family judge recheck
  (`results/`).
- Write-ups: scored analysis (`RESULTS.md`) and the full technical report
  (`report/REPORT.md`), hardened through two adversarial review rounds.
