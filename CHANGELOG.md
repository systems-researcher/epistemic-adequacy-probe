# Changelog

All notable changes to this artefact are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-08-17

### Changed
- **Licensing: split from MIT-only to MIT plus CC-BY-4.0.** The report, recorded
  results, authored sidecars, synthetic model, and the other prose files are now
  CC-BY-4.0, which is the appropriate instrument for non-code research output
  and states the attribution expectation explicitly; MIT covers everything else
  the copyright holders wrote, including the harness, instrument, and landing
  page. `LICENSE.md` was restructured so that MIT is the catch-all rather than an
  enumerated list, which leaves no file uncovered. Third-party material is
  unaffected: both Apollo model files stay MPL-2.0 (Airbus) and the NASA
  photograph carries its own terms. Whatever 0.1.0 granted stays granted for the
  material distributed under it; this split applies from 0.2.0 onward,
  reclassifies only the copyright holders' own work, and withdraws nothing.
  Agreed by all three copyright holders.
- De-anonymised the artefact following acceptance of the companion paper at
  MODELS 2026 (NIER track, doi:10.1145/3822455.3838783): authorship, copyright,
  citation metadata, and contact channel now name the authors.
- Rewrote the landing-page self-containment CI check to separate assets from
  navigation: `src` must still be entirely local (no CDN scripts, fonts, or
  trackers), while `href` additionally permits the DOI resolver and canonical
  licence deeds.
- Restored `EV-002` in `substrate/apollo-ea-metadata.yaml` to the text the
  recorded run actually consumed. The shipped sidecar had been revised after the
  run (page reference changed to pp.192-193 and the content enriched to state
  the committee's recommendation), so the deposited substrate no longer matched
  either `results/raw-results.json`, whose archived answers quote the earlier
  text verbatim, or the scoring keys in `probes.json`, which still score against
  it. The revision also supplied the very rationale that question A1 is designed
  to lack. The correct page reference is recorded in the new errata table
  instead.
- Removed the claim that the companion paper's vignette misstates the minimum
  thrust requirement. `README.md` asserted the paper "currently states" 33.4 MN
  and needed a correction this probe forces, while `RESULTS.md` recorded that
  the paper aligns with the artefact values. Both predate acceptance; the
  published paper aligns, so the stale assertions are gone and the artefact
  facts they were attached to are unchanged.

### Removed
- Anonymity tripwire step in `.github/workflows/validate.yml`, which enforced
  the double-blind constraint that no longer applies. The secrets/leak-sentinel
  scan is retained.
- `<meta name="robots" content="noindex">` from the landing page, which kept the
  artefact out of search indexes during double-blind review. The page is now
  deliberately indexable, and carries Dublin Core bibliographic metadata.

### Added
- `repository-code` and `url` fields in `CITATION.cff`.
- Statement of scope ("Status of this work") in `report/REPORT.md`, with
  matching notices in `README.md`, `RESULTS.md`, and the landing page, marking
  these as initial findings and describing the full susceptibility probe still
  being designed.
- Landing page: NASA launch photograph, per-cell ungrounded-rate chart,
  capability-inversion slope plot, cross-family judge agreement figures, and a
  copyable BibTeX citation block. Every figure shown is recomputed from
  `results/` and also stated in `RESULTS.md` or `report/REPORT.md`.
- Documentation of the exploratory full-model arm in `results/raw-fullmodel.json`
  (`RESULTS.md`, and a pointer in `report/REPORT.md`), which had shipped in 0.1.0
  without prose describing it. It is explicitly not claimed as a result.
- Airbus copyright and MPL-2.0 notices restored to the header of
  `substrate/apollo-model-excerpt.sysml`, which carried provenance but had lost
  the licence notice itself (MPL-2.0 section 3.4).
- An "Errata" section in `RESULTS.md` recording two citation errors in the
  hand-authored Apollo sidecar, both left uncorrected in the substrate on
  purpose so the artefact still reproduces its own run, and both flagged in
  comments at the point of use.

## [0.1.0] - 2026-06-10

First public release of the consumption probe, the companion artefact to the
MODELS 2026 NIER-track paper.

### Added
- Probe instrument: 15 derivation-style questions with ground-truth keys and scoring
  rubric (`probes.json`).
- `requirements.txt`: pinned harness dependencies (anthropic, PyYAML) for
  replicable re-runs (RR-R-01).
- `ETHICS.md`: responsible-use / dual-use statement (RR-R-06).
- Run-provenance envelope in `harness/run_probe.py` (harness version, UTC
  timestamp, parameters, and the served model versions the API actually ran)
  plus a "Run provenance" section in `RESULTS.md` (RR-R-02).
- Substrates: verbatim Apollo 11 SysML v2 excerpt (MPL-2.0, Airbus), a hand-authored
  epistemic-adequacy sidecar, and a fictional out-of-distribution control vehicle
  (`substrate/`).
- Reproducible harness: probe runner, cross-family judge recheck, and substrate builder
  (`harness/`).
- Results: raw per-question responses and verdicts, and the cross-family judge recheck
  (`results/`).
- Write-ups: scored analysis (`RESULTS.md`) and the full technical report
  (`report/REPORT.md`), hardened through two adversarial review rounds.
