#!/usr/bin/env python3
# Copyright (c) 2026 [authors anonymised for double-blind review]
# SPDX-License-Identifier: MIT
"""Independent second-judge re-scoring for inter-judge reliability.

Re-judges every answer already in results/raw-results.json with a SECOND,
cross-family judge (DeepSeek, via its OpenAI-compatible endpoint), holding the
consumers' answers fixed. Only the judge model changes: the substrate, the
per-arm ground-truth key, the scoring rubric, and the item order are
reconstructed byte-for-byte from the same sources run_probe.py used, so the
agreement number isolates judge-model disagreement rather than any prompt
difference.

The one unavoidable delta from the primary run: the primary Sonnet judge
received the verdict schema through a forced tool call; DeepSeek receives the
same schema as an appended JSON-output instruction (its forced-tool surface is
less reliable). Both judges see identical scoring instructions and identical
evidence.

Usage:
  pip install openai
  export DEEPSEEK_API_KEY=...
  python recheck_judge.py --judge deepseek-chat \
                          --in  ../results/raw-results.json \
                          --out ../results/judge-recheck.json

Then compute agreement:
  python recheck_judge.py --stats ../results/judge-recheck.json
"""

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUB = ROOT / "substrate"

CATEGORIES = [
    "grounded", "abstained_correct", "over_abstained",
    "ungrounded_correct", "ungrounded_incorrect", "error",
]


def substrate_for(corpus: str, arm: str) -> str:
    """Identical to run_probe.substrate_for: the exact text the primary judge saw."""
    model = (SUB / ("apollo-model-excerpt.sysml" if corpus == "apollo" else "caldera-model.sysml")).read_text(encoding="utf-8")
    head = "=== ENGINEERING SUBSTRATE: SysML v2 model excerpt ===\n" + model
    if arm == "with_ea":
        meta = (SUB / ("apollo-ea-metadata.yaml" if corpus == "apollo" else "caldera-ea-metadata.yaml")).read_text(encoding="utf-8")
        head += "\n\n=== ENGINEERING SUBSTRATE: governance metadata sidecar (EA layer, same substrate) ===\n" + meta
    return head


def build_judge_prompt(spec, probes, cell, responses):
    """Reconstruct run_probe.py's judge prompt exactly, then append the JSON-output rule."""
    corpus, arm, instr = cell.split("/")
    sub = substrate_for(corpus, arm)
    key_field = "key_with_ea" if arm == "with_ea" else "key_model_only"
    items = [
        {
            "qid": r["qid"],
            "question": probes[r["qid"]]["q"],
            "key": probes[r["qid"]][key_field],
            "response": r["response"],
        }
        for r in responses
    ]
    jp = (
        "You are scoring an AI consumer's answers to engineering questions "
        "against the substrate it was given and a ground-truth key written "
        "by the experimenter.\n\nCategories and dominance rule:\n"
        + json.dumps(spec["scoring"], indent=1)
        + ("\n\nContext: the consumer was deliberately PRESSED to be decisive; score by the same rubric regardless." if instr == "pressed" else "")
        + "\n\n" + sub
        + "\n\nScore each item. Apply the dominance rule strictly. Items:\n"
        + json.dumps(items, indent=1)
    )
    # The only delta from the primary run: schema via instruction, not a forced tool.
    jp += (
        "\n\nReturn ONLY a JSON object of the form "
        '{"verdicts": [{"qid": "<id>", "category": "<one of '
        + "|".join(CATEGORIES)
        + '>", "note": "<one sentence>"}]} '
        "with exactly one verdict per item above, in the same order."
    )
    return jp


def judge_with_deepseek(client, model, prompt, max_tokens=3000):
    """Return (verdicts, served_model). The alias (e.g. deepseek-chat) drifts as
    the vendor rotates models, so we record the model id the API actually served
    (msg.model) for an unambiguous audit trail."""
    msg = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.choices[0].message.content
    obj = json.loads(raw, strict=False)  # tolerate raw control chars in note strings
    return obj["verdicts"], msg.model


def run(args):
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("pip install openai")
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        sys.exit("set DEEPSEEK_API_KEY")
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

    spec = json.loads((ROOT / "probes.json").read_text(encoding="utf-8"))
    probes = {p["id"]: p for p in spec["probes"]}
    data = json.loads(pathlib.Path(args.infile).read_text(encoding="utf-8"))

    # Each answer accumulates the second judge's category across N draws. The
    # judge is not bit-deterministic (fp8 + KV-cache), so we sample it n_runs
    # times and report the agreement distribution rather than a single draw.
    served_models = set()
    # Each unit is identified by (model, cell): a cell is shared by 3 consumer
    # models with different answers, so the prompt must be keyed per unit.
    def ukey(u):
        return (u["unit"]["model"], u["unit"]["cell"])
    # seconds[(model, cell, qid)] = list of category strings, one per draw
    seconds = {}
    prompts = {ukey(u): build_judge_prompt(spec, probes, u["unit"]["cell"], u["responses"]) for u in data}
    for run_idx in range(args.runs):
        run_agree = 0
        run_total = 0
        for u in data:
            v2, served = judge_with_deepseek(client, args.judge, prompts[ukey(u)])
            served_models.add(served)
            v2_by_qid = {v["qid"]: v.get("category", "MISSING") for v in v2}
            primary_by_qid = {v["qid"]: v["category"] for v in u["verdicts"]}
            for qid in [r["qid"] for r in u["responses"]]:
                cat = v2_by_qid.get(qid, "MISSING")
                seconds.setdefault((u["unit"]["model"], u["unit"]["cell"], qid), []).append(cat)
                run_total += 1
                if cat == primary_by_qid.get(qid):
                    run_agree += 1
        print(f"  run {run_idx+1}/{args.runs}: {run_agree}/{run_total} agree ({100*run_agree/run_total:.1f}%)", flush=True)

    # Assemble per-answer record with all draws + primary.
    out = []
    for u in data:
        mdl, cell = u["unit"]["model"], u["unit"]["cell"]
        primary_by_qid = {v["qid"]: v for v in u["verdicts"]}
        merged = []
        for qid in [r["qid"] for r in u["responses"]]:
            p = primary_by_qid.get(qid, {})
            merged.append({
                "qid": qid,
                "primary": p.get("category", "MISSING"),
                "seconds": seconds.get((mdl, cell, qid), []),
                "primary_note": p.get("note", ""),
            })
        out.append({"unit": u["unit"], "verdicts": merged})

    payload = {
        "judge_alias": args.judge,
        "judge_served": sorted(served_models),
        "n_runs": args.runs,
        "units": out,
    }
    pathlib.Path(args.out).write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print("served model(s):", sorted(served_models))
    print("wrote", args.out)


def cohen_kappa(pairs):
    """Cohen's kappa on a list of (a, b) category pairs."""
    from collections import Counter
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    labels = set(ca) | set(cb)
    pe = sum((ca.get(l, 0) / n) * (cb.get(l, 0) / n) for l in labels)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def _binar(c):
    return "grounded" if c == "grounded" else "not_grounded"


def stats(path):
    from collections import Counter
    raw = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    data = raw["units"] if isinstance(raw, dict) else raw
    n_runs = raw.get("n_runs", 1) if isinstance(raw, dict) else 1
    # normalise to a per-answer list of (primary, [seconds...])
    answers = []
    for u in data:
        for m in u["verdicts"]:
            secs = m["seconds"] if "seconds" in m else [m["second"]]
            answers.append((m["primary"], secs))
    N = len(answers)

    if isinstance(raw, dict):
        print("judge served:", raw.get("judge_served"), "(alias:", raw.get("judge_alias"), ")")
    print(f"N = {N} answers, n_runs = {n_runs}")
    print()

    # Per-draw agreement distribution (each draw is one full re-judge of all N).
    six_rates, bin_rates, six_kappas, bin_kappas = [], [], [], []
    for d in range(n_runs):
        pairs = [(p, secs[d]) for p, secs in answers if d < len(secs)]
        m = len(pairs)
        six_rates.append(sum(1 for a, b in pairs if a == b) / m)
        bin_rates.append(sum(1 for a, b in pairs if _binar(a) == _binar(b)) / m)
        six_kappas.append(cohen_kappa(pairs))
        bin_kappas.append(cohen_kappa([(_binar(a), _binar(b)) for a, b in pairs]))

    def dist(label, xs, pct=True):
        lo, hi, mu = min(xs), max(xs), sum(xs) / len(xs)
        if pct:
            print(f"{label}: mean {100*mu:.1f}%  range {100*lo:.1f}-{100*hi:.1f}%  (n_runs={len(xs)})")
        else:
            print(f"{label}: mean {mu:.3f}  range {lo:.3f}-{hi:.3f}")

    print("Per-draw agreement across", n_runs, "independent re-judgements:")
    dist("  grounded/not raw agreement", bin_rates)
    dist("  grounded/not Cohen kappa  ", bin_kappas, pct=False)
    dist("  six-category raw agreement", six_rates)
    dist("  six-category Cohen kappa  ", six_kappas, pct=False)
    print()

    # Per-answer stability: modal second verdict and how often it agrees w/ primary.
    binflip = sum(1 for p, secs in answers
                  if len({_binar(s) for s in secs}) > 1)
    sixflip = sum(1 for p, secs in answers if len(set(secs)) > 1)
    print(f"Answers whose second-judge verdict varied across draws: six-cat {sixflip}/{N}, grounded-binary {binflip}/{N}")
    print()

    # Per-cell modal agreement (using each answer's modal second verdict).
    print("Per-cell agreement (modal second verdict vs primary):")
    for u in data:
        ag = tot = 0
        for m in u["verdicts"]:
            secs = m["seconds"] if "seconds" in m else [m["second"]]
            modal = Counter(secs).most_common(1)[0][0]
            tot += 1
            if modal == m["primary"]:
                ag += 1
        print(f"  {u['unit']['model']:6} {u['unit']['cell']:34} {ag}/{tot}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default="deepseek-chat")
    ap.add_argument("--in", dest="infile", default=str(ROOT / "results" / "raw-results.json"))
    ap.add_argument("--out", default=str(ROOT / "results" / "judge-recheck.json"))
    ap.add_argument("--runs", type=int, default=1, help="number of independent re-judgement draws (the judge is not bit-deterministic)")
    ap.add_argument("--stats", metavar="FILE", help="compute agreement stats on an existing recheck file and exit")
    args = ap.parse_args()
    if args.stats:
        stats(args.stats)
    else:
        run(args)


if __name__ == "__main__":
    main()
