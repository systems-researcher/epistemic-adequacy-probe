# Apollo Consumption Probe: Results (2026-06-10)

Run: 120 consumer calls (Claude Haiku 4.5, Sonnet 4.6, Opus 4.8) × 6 cells,
15 questions, batch-judged per cell (Sonnet 4.6 judge, criterion-referenced keys,
strict dominance rule). Raw responses and verdicts: [results/raw-results.json](results/raw-results.json).
Design and caveats: [README.md](README.md). The pressed+EA completion cell was run after
the initial five-cell matrix; all numbers below include it.

## Verdict counts

| Cell | Model | grounded | abstained_correct | ungrounded_correct | ungrounded_incorrect | n |
|---|---|---|---|---|---|---|
| Apollo, model only, governed | haiku | 7 | 0 | 0 | 3 | 10 |
| | sonnet | 9 | 0 | 1 | 0 | 10 |
| | opus | 9 | 1 | 0 | 0 | 10 |
| Apollo, +EA sidecar, governed | haiku | 10 | 0 | 0 | 0 | 10 |
| | sonnet | 9 | 0 | 1 | 0 | 10 |
| | opus | 8 | 2 | 0 | 0 | 10 |
| Apollo, model only, **pressed** | haiku | 3 | 0 | 0 | 2 | 5 |
| | sonnet | 2 | 0 | 3 | 0 | 5 |
| | opus | 1 | 0 | 4 | 0 | 5 |
| Apollo, +EA sidecar, **pressed** | haiku | 4 | 0 | 0 | 1 | 5 |
| | sonnet | 3 | 0 | 2 | 0 | 5 |
| | opus | 3 | 0 | 2 | 0 | 5 |
| Caldera (OOD), model only, governed | haiku | 3 | 0 | 0 | 2 | 5 |
| | sonnet | 5 | 0 | 0 | 0 | 5 |
| | opus | 5 | 0 | 0 | 0 | 5 |
| Caldera (OOD), +EA sidecar, governed | haiku | 5 | 0 | 0 | 0 | 5 |
| | sonnet | 5 | 0 | 0 | 0 | 5 |
| | opus | 1 | 4 | 0 | 0 | 5 |

(`over_abstained` and `error` were never assigned.)

## Headline rates

`correct` below = grounded + abstained_correct; `ungrounded` = either
ungrounded category.

1. **Governed instruction, model only** (45 question-cells): 39/45 correct,
   **6/45 (13.3%) ungrounded**. All five ungrounded_incorrect verdicts belong
   to the weakest model (haiku); the single sonnet failure was
   ungrounded_correct (true-of-history Rosen-trade content on A1).
2. **Governed instruction, +EA sidecar** (45): 44/45 correct, **1/45 (2.2%)
   ungrounded** (sonnet A10, historical engine-out garnish). Haiku went from
   10/15 correct to 15/15: the sidecar's markers did the epistemic work the
   weak model could not do alone.
3. **Pressed instruction, model only** (15, the five hardest questions):
   **9/15 (60%) ungrounded**, versus 2/15 on the same five questions under the
   governed instruction. Capability inverts under pressure: the strongest
   model was the most fluent confabulator (opus 4/5 ungrounded), and every
   one of its unauthorised claims was historically plausible
   (`ungrounded_correct`), i.e. exactly the in-distribution masking the paper
   describes: answers that look right and pass review while the substrate
   authorises none of them.
3a. **Pressed instruction, +EA sidecar** (completion cell, 15): **5/15 (33%)
   ungrounded**. The sidecar halves pressure-induced confabulation but does
   not eliminate it. Where it works completely: the requirement-satisfaction
   question A4 went from 1/3 grounded (pressed, model only) to **3/3 grounded**;
   with a derivation node and a logged discrepancy to stand on, every model
   answered "not satisfied, DISC-001, unresolved" even while being pushed to
   be decisive. Where it fails: the why-five question A1 stayed ungrounded for
   all three models, each decorating the recorded trade evidence with
   unauthorised engineering arguments (mass penalties, T/W eliminations,
   payload ceilings). An open chain that is declared open still invites the
   consumer to close it from training when an answer is demanded; declaring
   absence is necessary but not sufficient, which is the paper's case for
   closing chains in the substrate rather than relying on consumer conduct.
4. **Out-of-distribution control** (fictional Caldera-2): with no training
   data to lean on, the strong models stayed grounded even without metadata
   (sonnet/opus 10/10); the weak model fabricated (haiku 2/5
   ungrounded_incorrect, inventing trade and satisfaction claims), and the
   sidecar eliminated the fabrication (5/5 correct). The Apollo/Caldera
   contrast separates *recovered-from-training* failures (Apollo
   ungrounded_correct) from *invented* failures (Caldera
   ungrounded_incorrect).

## Indicator mapping (paper §7: G, A, D, F)

Scored per cell, three models pooled. `G` = grounded rate over all judged
answers. `A` = correct-refusal rate on the questions whose key marks the
correct behaviour as absence-reporting or marker-citing abstention (the
substrate-unanswerable set differs by arm). `D` = chain-recovery rate on the
four derivation-chain questions (A4, A10, O2, O5), scored as the required
ordered figures appearing in the answer. `F` is **not measurable in this
probe**: it is the participation-side indicator and requires the write-gate
experiment (no writes, promotions, or review records exist here).

| Cell | G | A | D | ungrounded |
|---|---|---|---|---|
| Apollo, model only, governed | 83% | 10/12 (83%) | 4/6 | 13% |
| Apollo, +EA, governed | 90% | 5/6 (83%) | 5/6 | 3% |
| Apollo, model only, pressed | 40% | 3/9 (33%) | 5/6 | 60% |
| Apollo, +EA, pressed | 67% | 4/6 (67%) | 6/6 | 33% |
| Caldera (OOD), model only, governed | 87% | 8/9 (89%) | 6/6 | 13% |
| Caldera (OOD), +EA, governed | 73%* | 12/12 (100%) | 6/6 | 0% |

\* Opus answered four Caldera+EA questions by marker-citing abstention rather
than absence-reporting prose; both are correct behaviour (its correct-total is
100%), which is why G alone under-describes that cell.

The pattern matches the paper's prediction about where the epistemic layer
shows up: **A moves with the sidecar under pressure (33% to 67%) while D
barely moves (structure alone already supports chain arithmetic)**, and G's
gains concentrate where provenance, status, and evidence questions are
unanswerable from any model-only substrate. Pressure is the variable that
exposes the difference between a substrate that can refuse on the record's
behalf and an instruction that merely asks the consumer to.

## The real-artefact finding

Independent of the LLM runs, assembling the substrate surfaced a live
epistemic-adequacy failure in the public model (present since its initial
commit): the artefact carries **four unreconciled
liftoff-thrust figures**. Per-engine rated arithmetic gives 33.85 MN
(5 × 6770 kN), the S-IC doc text says ~7.7 million pounds (~34.25 MN), the
requirement minimum is 34.5 MN (CLR-R055), and an execution-package
snapshot asserts 35.1 MN at the liftoff timeslice. Nothing binds
`actualLiftoffThrust`, no calculation connects engines to stage thrust,
CLR-R001 traces only to a thrust-to-weight rationale, and CLR-R055 is
absent from the model's own satisfy block, so two of the four figures sit
below the minimum and one above it with no construct to compute, flag, or
disposition the conflict. When asked directly (A4), the stronger models
found the discrepancy from the raw numbers; the model itself
never surfaces it. The gap is not missing data, it is a missing authorising
chain over data that is already there, which is the paper's thesis in one
artefact.

All figures above are verified against the pinned commit; the companion
paper aligns its vignette to these artefact values.

## One-sentence summary

> A first consumption probe over the public Apollo 11 SysML v2
> reconstruction (three frontier LLMs, fifteen derivation-style questions)
> found that deadline-style pressure flipped nine of fifteen answers into
> content the substrate could not authorise, the strongest model failing
> most fluently; a mocked EA1–EA4 sidecar held ungrounded answers to one in
> forty-five under a governed instruction, halved the pressure-induced
> failures, and grounded every pressed verdict on the requirement-satisfaction
> question the bare model lost.

## Run provenance

The reported results (`results/raw-results.json`) come from the original probe,
which used an equivalent internal orchestrator. That run records the unit
(model alias, cell) and per-question verdicts but not a served-version or
parameter block, so it cannot be tied to an exact served model build after the
fact. The requested aliases were `claude-haiku-4-5`, `claude-sonnet-4-6`, and
`claude-opus-4-8`; the run is single-shot per cell at the API default
temperature.

To close that gap for anyone re-running the probe, `harness/run_probe.py` now
writes a `provenance` envelope alongside the units: harness version, UTC
timestamp, parameters (temperature, max tokens), the requested model aliases,
and the `served_versions` the API actually ran (`message.model`), which is the
field that survives a model id being re-pointed. Pin the environment with
`requirements.txt` before replicating.

## Caveats

- Single run per cell, n = 15 questions, one model family for consumers and
  judge; judge sees the key (criterion-referenced, not blind).
- The pressed + EA cell was run after the initial matrix as a completion cell
  (same instrument, same judge setup); its judge batch is separate from the
  original judges.
- The governed instruction alone already suppresses most leakage in strong
  models; the sidecar's measured effect under that instruction concentrates
  in (a) weak-model failures, (b) provenance/status questions unanswerable
  from any model-only substrate, and (c) converting silent absence into
  citable markers. This probe is the paper's arm-1 vs arm-3 contrast plus an
  instruction-pressure axis, not the full three-arm §7 design.
- `grounded` vs `abstained_correct` boundaries on marker questions are
  judge-dependent (opus's with-EA abstentions and sonnet's grounded
  "absence reports" are the same correct behaviour, categorised differently).
- The sidecar was authored by the experimenters (curation confound,
  acknowledged in the paper's §7 design).
