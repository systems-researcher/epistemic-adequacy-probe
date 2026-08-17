# Licensing

Copyright (c) 2026 Jason D. Gower, Michael J. de C. Henshaw, Siyuan Ji

Everything in this repository authored by the copyright holders above is
released under **MIT** or **CC-BY-4.0**, as set out in sections 1 and 2. Two
categories of third-party material, listed in sections 3 and 4, are not ours to
license and are covered by their own terms.

## 1. Written work and data: CC-BY-4.0

Applies to the prose, results, and authored data:

- every `*.md` file in the repository except this one, including
  `report/REPORT.md`, `README.md`, `RESULTS.md`, `ETHICS.md`, and `CHANGELOG.md`
- `results/` (all recorded runs and verdicts)
- `substrate/apollo-ea-metadata.yaml`, `substrate/caldera-ea-metadata.yaml`,
  and `substrate/caldera-model.sysml` (the authored sidecars and the synthetic
  out-of-distribution model)

Licensed under the Creative Commons Attribution 4.0 International License
(CC-BY-4.0). You are free to share and adapt this material for any purpose,
including commercially, provided you give appropriate credit, link to the
licence, and indicate if changes were made.

Licence text: <https://creativecommons.org/licenses/by/4.0/legalcode>
Summary: <https://creativecommons.org/licenses/by/4.0/>

Attribution is satisfied by citing the companion paper and this artefact; see
`CITATION.cff` for the canonical citation metadata.

## 2. Everything else we wrote: MIT License

Applies to all remaining files authored by the copyright holders, that is,
every file not covered by section 1, 3, or 4. This includes `harness/`,
`probes.json`, `docs/index.html`, `requirements.txt`, `.github/workflows/`,
`.gitignore`, `docs/.nojekyll`, and the packaging and metadata files
(`CITATION.cff`, `COPYRIGHT`, `NOTICE`, `RELEASE-INFO.txt`, `LICENSE.md`).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 3. Third-party model, copyright Airbus: MPL-2.0

Neither of the following is our work and neither is covered by sections 1 or 2:

- `substrate/apollo-model-excerpt.sysml`, an excerpt of the elements bearing on
  S-IC first-stage propulsion
- `substrate/apollo-model-full-6e9c93f.sysml`, every `.sysml` file in the
  source repository concatenated in sorted path order

Both are reproduced from the Apollo 11 SysML v2 model, copyright Airbus,
licensed under the Mozilla Public License 2.0 (MPL-2.0), under that licence
with attribution. Airbus copyright and MPL-2.0 notices are retained in both
files.

    Source:  https://github.com/airbus/apollo-11-sysml-v2
    Commit:  6e9c93fe7d80c5ca3534bb14b10ab374a643ef2d
    Licence: https://www.mozilla.org/en-US/MPL/2.0/

Model content is unmodified. The excerpt selects elements and adds a provenance
header; the full file adds a provenance header and per-file boundary markers.

## 4. Third-party image, NASA

`docs/assets/apollo-11-liftoff-nasa-6900540.jpg` is a NASA photograph
(NASA ID 6900540). NASA still images are generally not protected by copyright
in the United States and may be used for educational or informational purposes
with NASA acknowledged as the source. NASA does not endorse this work. See
`NOTICE` for the full statement.

## Note on prior releases

Version 0.1.0 described its own licensing as MIT, alongside the same MPL-2.0
carve-out for the Airbus model that appears in section 3. Whatever permissions
were granted under that release remain granted for the material distributed
under it; the split above applies from version 0.2.0 onward, reclassifies only
the copyright holders' own work, and withdraws nothing previously given.
