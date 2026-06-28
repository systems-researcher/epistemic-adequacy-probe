# Epistemic Adequacy Consumption Probe (Apollo 11 SysML v2)

> **Read the full technical report:** [report/REPORT.md](report/REPORT.md)

First probe of the research programme set out in the companion paper
(“Models as Governed Interfaces for AI-Native MBSE”, under review): does
epistemic metadata, beyond structured model access alone, change how an AI
consumer answers derivation-style questions over an MBSE model? The probe
converts the companion paper's central design claim into a first measured
result.

## Substrate

**Real model.** Verbatim excerpt ([substrate/apollo-model-excerpt.sysml](substrate/apollo-model-excerpt.sysml)) from
the public Airbus Apollo 11 SysML v2 reconstruction,
[github.com/airbus/apollo-11-sysml-v2](https://github.com/airbus/apollo-11-sysml-v2) @ [`6e9c93fe7d80c5ca3534bb14b10ab374a643ef2d`](https://github.com/airbus/apollo-11-sysml-v2/commit/6e9c93fe7d80c5ca3534bb14b10ab374a643ef2d)
(MPL-2.0): engine and stage part defs, the SaturnV assembly, CLR-R001 (five
F-1 engines), CLR-R002, CLR-R055 (34.5 MN minimum liftoff thrust), FLR-R008,
HLR-R062.

**Finding made while assembling the substrate** (verified against the repo's
initial commit, 2026-02-16, so present from first publication):

1. The model **does** carry per-engine F-1 thrust (`thrustSeaLevel = 6770 kN`)
   and **does** carry a stage thrust requirement (CLR-R055, **34.5 MN minimum**,
   not the 33.4 MN the paper's vignette currently states).
2. Nothing links them: `actualLiftoffThrust` is declared but never bound, no
   calculation computes stage thrust from the engines, and CLR-R001 traces only
   to FLR-R008 (TWR > 1), never to CLR-R055.
3. The unlinked numbers conflict: 5 × 6770 kN = **33.85 MN < 34.5 MN**. As
   modelled, the rated configuration cannot satisfy the stated minimum, and no
   construct in the model computes, flags, or dispositions this.

So the epistemic gap in the real artefact is sharper than the paper claims:
the ingredients are present, the authorising chain is absent, and the absence
conceals a live numerical discrepancy.

**EA sidecar (arm B).** [substrate/apollo-ea-metadata.yaml](substrate/apollo-ea-metadata.yaml) is a hand-authored
mock of the paper's EA1–EA4 layer: closed status vocabulary, provenance
records, reachable evidence anchors (real documents: the
[AS-506 flight evaluation report](https://archive.org/details/saturn-v-launch-vehicle-flight-evaluation-report-as-506)
(cited in the sidecar as NASA TM X-58058),
[Bilstein SP-4206](https://history.nasa.gov/SP-4206/sp4206.htm) pp.192–193), a derivation node computing 33.85 MN with a FAILS
consistency check, and AC1 `UNRESOLVED` markers for the open chains (basis of
the 34.5 MN figure, sizing chain, margin, engine-out).

**Out-of-distribution control.** [substrate/caldera-model.sysml](substrate/caldera-model.sysml) is a fictional
"Caldera-2" hopper (3 × 412 kN K-9 engines, 1.4 MN minimum, same planted
shape: unlinked, conflicting, 1.236 MN < 1.4 MN). No training corpus contains
this vehicle, so any specific rationale supplied for it is invented, which
separates "answers recovered from training" (Apollo) from "answers
fabricated" (Caldera). Its sidecar deliberately holds **no** trade evidence,
so the configuration-rationale question must be abstained on even in arm B.

## Design

15 questions ([probes.json](probes.json): A1–A10 Apollo, O1–O5 Caldera) × 3 consumers
(Claude Haiku 4.5, Sonnet 4.6, Opus 4.8, model IDs `claude-haiku-4-5`,
`claude-sonnet-4-6`, `claude-opus-4-8`) × cells:

| Cell | Substrate | Instruction |
|---|---|---|
| A | model only | governed (answer from substrate; report absences) |
| B | model + EA sidecar | governed |
| C (A1/A4/A5/A8/A10 only) | model only | pressed ("review in ten minutes, be decisive, do not say not-recorded") |
| D (A1/A4/A5/A8/A10 only) | model + EA sidecar | pressed (completion cell, run second) |
| OOD-A / OOD-B | Caldera, model only / + sidecar | governed |

120 consumer calls, batch-judged per (model × cell) by a Sonnet 4.6 judge against
per-question ground-truth keys with a strict dominance rule. Categories:
`grounded`, `abstained_correct`, `over_abstained`, `ungrounded_correct`
(true-of-history but unauthorised: training leakage), `ungrounded_incorrect`,
`error`.

Mapping to the paper's indicators: `grounded` ≈ G, `abstained_correct` /
`over_abstained` ≈ A's two failure directions, `ungrounded_*` is the failure
mode the architecture exists to make visible.

## Caveats (stated up front)

- Single run per cell; no prompt-sensitivity sweep; n = 15 questions.
- All consumers and the judge are one model family (Claude); judge sees the
  key (criterion-referenced scoring, not blind).
- The EA sidecar is authored by the experimenters; arm B partly measures
  "did a human encode the answer", which is the known curation confound the
  paper's three-arm §7 design exists to control. This probe is the paper's
  arm-1-vs-arm-3 contrast plus instruction pressure, not the full design.
- The governed instruction itself does epistemic work; cell C exists to
  separate instruction effects from substrate effects, but only on 5 questions.
- Probe agents had tool access disabled by instruction, not sandbox.
- Responsible-use / dual-use statement: [ETHICS.md](ETHICS.md).

## Reproduce

The original run used an equivalent internal orchestrator;
[harness/run_probe.py](harness/run_probe.py) re-runs the probe against the Anthropic API
with identical prompts, schemas, and judge rubric, and
[harness/recheck_judge.py](harness/recheck_judge.py) replays the cross-family judge check.

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python harness/run_probe.py --models claude-haiku-4-5,claude-sonnet-4-6,claude-opus-4-8 \
                            --out results/replication.json
```

The hosted models are non-deterministic and single-run per cell, so cell-level rates
should *track* the reported figures rather than match them exactly. See each script's
header for the full options.

## Files

- [substrate/](substrate/): substrate files (the Apollo excerpt is verbatim from the
  pinned commit; everything else hand-authored 2026-06-10)
- [probes.json](probes.json): questions, ground-truth keys, scoring rubric
- [harness/](harness/): the reproducible runner, the cross-family judge recheck, and the
  substrate builder
- [results/](results/): raw per-question responses and verdicts
  ([raw-results.json](results/raw-results.json)) plus the judge recheck
  ([judge-recheck.json](results/judge-recheck.json))
- [RESULTS.md](RESULTS.md): scored tables, analysis, indicator mapping, and the
  paper-vignette correction this probe forces
- [report/REPORT.md](report/REPORT.md): the full technical report
- [requirements.txt](requirements.txt): pinned harness dependencies (RR-R-01)
- [ETHICS.md](ETHICS.md): responsible-use / dual-use statement

## Licence & citation

MIT for the harness, instrument, sidecars, synthetic model, report, and results; the one
verbatim Apollo excerpt is MPL-2.0 (Airbus). See [LICENSE.md](LICENSE.md). Citation
metadata is in [CITATION.cff](CITATION.cff). Authorship is withheld for double-blind
review.

## Support & contact

During review, reach the authors through the double-blind review system; direct
contact and a security/support address will be restored on de-anonymisation. To
report a problem with the artefact, please route it through the review channel.