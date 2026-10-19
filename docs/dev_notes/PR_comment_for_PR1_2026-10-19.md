# Add script-switch prefix zoom and document Experiment 00

The full War and Peace script-run overview compresses individual runs.
Add `--num-language-changes N` to plot the first N switches (N+1 complete
runs), preserving overview dimensions and vertical scale. A request beyond
the available switches warns and uses all runs; negative requests error.
Prefix PNGs have distinct filenames and the x-axis identifies script-class
changes, including Numeric/Other transitions rather than language inference.

Includes 100/250/500/1000-change figures and Dave's annotated explorations,
README usage, virtual-environment/patch ignore rules, and Experiment 00
observations covering tokenization, mixed scripts, seeded generation,
rounded logarithmic bins, and translation round-trip overlap limitations.
Both scaffold scripts now preserve existing files by default while creating
missing templates. Add continuation documentation with reusable PCDP/context
header/body templates, a bbl lab-notebook checkpoint from Project Selection
Summary, and a README-linked TESTME checklist.

## Validation

- Windows: all 19 Python tests passed; full experiment regenerated 6,370 runs.
- User inspected prefix figures; full overview regenerated with updated label.
- Bash safe mode: isolated preservation and repeat-run checks passed.
- PowerShell scaffold preservation: isolated Windows check PASSED on
  2026-10-19; existing sentinel preserved, missing files created, all six
  hashes unchanged on repeat. Procedure retained in TESTME.

## Limits and follow-up

Script classes are not language labels; run lengths count normalized tokens.
Normalization still strips punctuation/combining marks. Corpus completeness
and source passages behind highlighted patterns are not yet verified.
Follow-ups: longer generated-text comparison, then general-text generation
with a guiding notebook. No generation-model redesign in this PR.

## Final validation and handoff

Latest Windows regression result: **19 passed in 0.64s**. The isolated
PowerShell check printed **PASS: existing edits preserved; missing files
created; second run unchanged.** This verifies default safe mode only.
The updated full overview was visually reviewed and accepted by Dave.

Context README retains reusable PCDP/header/body templates. The bbl LN
records the originating chat (Project Selection Summary), architecture,
measurements, seed semantics, normalization limitations, and remaining work.
A Termux PCDP and README-linked TESTME preserve continuation and validation.
README's obsolete pending-safety sentence is struck through temporarily;
remove it on the next branch.

Next branch proposal: portfolio-grade guiding Jupyter notebook plus a
reusable generator for arbitrary text input and maximum context order
(code n=context length; conventional n-gram order=n+1). Longer generation
comparisons remain follow-up work. README portfolio polish will be discussed
later; current artifact is intentionally bounded so other projects can
reach a comparable state. Corpus completeness/source-passage interpretation
and overwrite-mode tests are not claimed complete.

This note describes prepared changes and supplied validation. It does not
claim the branch is pushed, the PR exists, or a merge has occurred.
