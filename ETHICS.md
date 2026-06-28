<!--
Copyright (c) 2026 [authors anonymised for double-blind review]
SPDX-License-Identifier: MIT
-->

# Responsible use

This artefact is a research probe, not an attack tool. It measures whether an
AI consumer grounds its answers in an engineering model or fabricates rationale
the model does not contain. The probe includes a "pressed" instruction cell
that pushes a model to be decisive under time pressure. That is an elicitation
technique, so this file states why it is here and how it should be used.

## Why this is published

The companion paper claims that epistemic metadata changes how an AI consumer
answers derivation questions over an MBSE model. That claim needs a measured
result a reviewer can inspect and a non-author can re-run. Publishing the
instrument, the substrate, and the raw verdicts is what makes the claim
falsifiable. Withholding it would leave the claim unauditable.

## Who it is for

Systems-engineering and AI-evaluation researchers studying grounding,
abstention, and training-leakage in model consumers; reviewers of the companion
paper; anyone replicating or extending the probe.

## What is deliberately excluded

- No jailbreak corpus and no catalogue of bypass techniques. The single
  "pressed" instruction is a documented experimental condition, not a method
  for defeating a safety policy.
- No private model internals, weights, or undisclosed endpoints. The probe runs
  against published, generally available model IDs through the public API.
- No real engineering programme data. The Apollo excerpt is public (Airbus,
  MPL-2.0); the Caldera vehicle and the EA sidecar are synthetic and labelled as
  such, so they cannot be mistaken for authoritative source data.

## What is expected of users

Use the probe to measure and improve grounding, not to manufacture
authoritative-sounding output that an engineering model does not support. The
"ungrounded_correct" and "ungrounded_incorrect" categories exist to make
fabrication visible; treat a model that scores there as a finding to fix, not a
capability to exploit. This statement governs misuse of the research artefact;
for code vulnerabilities see the security note in the README.
