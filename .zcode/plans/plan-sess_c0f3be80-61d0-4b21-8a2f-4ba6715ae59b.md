# Clarity pass: RESULTS.md (light) + docs/index.html (lighter)

Same treatment as REPORT.md, scaled to each file's register. No numbers change, no instrument strings touched, HTML markup untouched.

## RESULTS.md (5 edits)

1. Item 3: split the double-colon sentence. "...historically plausible (`ungrounded_correct`), i.e. exactly the in-distribution masking..." becomes a new sentence: "That is exactly the in-distribution masking the paper describes: answers that look right and pass review while the substrate authorises none of them."
2. Item 3a: split "Where it works completely: ... to 3/3 grounded; with a derivation node..." at the semicolon.
3. Real-artefact finding: split the four-clause tail. "...CLR-R055 is absent from the model's own satisfy block. Two of the four figures sit below the minimum and one above it, with no construct to compute, flag, or disposition the conflict."
4. Errata: remove the "more interesting one" self-label. "The EV-002 error is the more interesting one, because it is an instance of the failure this probe studies." becomes "EV-002 is an instance of the failure this probe studies." (the next sentence already carries the why).
5. Indicator paragraph: strip the whole-clause bold ("**A moves... chain arithmetic**") and split the sentence; "structure alone already supports chain arithmetic" becomes its own clause.

Kept deliberately: the "The gap is not missing data. The data is present; the authorising chain over it is not." close (one instance per document, matching the report's kept instance), the bolded headline rates in the numbered findings (data emphasis, register-consistent), and the one-sentence summary block.

## docs/index.html (4 prose-span edits, markup untouched)

1. "What this is" lead: replace the old nested-parenthetical substrate/instruction sentence with the aligned phrasing from the edited report: arms and instructions each get their own short sentence.
2. Finding 1: "every unauthorised claim historically plausible" → "every unauthorised claim was historically plausible" (alignment with report).
3. Finding 3: end the card at "...compute, flag, or reconcile them." and drop the tacked-on appositive "a missing authorising chain over data already there" (the same info opens the Live Gap section below).
4. Scoring section: split "The check bounds inter-model judge bias; it does not establish..." into two sentences, matching the report.

Kept deliberately: the line-704 antithesis (the Live Gap section's thesis), the model sentences ("It had less to confabulate with."), the scope banner, all headings, all figures, SVG/chart markup, BibTeX, and metadata.

## Verification

Grep both files for the as-executed figures before/after (13.3%, 2.2%, 60%, 33%, 9/15, 5/15, 1/45, 44/45, 39/45, 79.7%, 73.5%, 113/120, 52/60, four thrust values), diff review to confirm only prose spans changed, prose_check.py on both files.

Estimate: 9 small edits across two files.
