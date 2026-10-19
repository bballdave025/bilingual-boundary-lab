# Experiment 00 observations — 2026-10-18

## Recorded baseline

The Windows run passed 14 tests and generated the overview, run JSON,
and summary. Corpus: 2,895,061 characters; 450,660 normalized tokens;
2,746,016 normalized characters. There are 6,370 maximal script-class
runs: 3,122 Cyrillic, 2,094 Latin, 806 numeric, and 348 other.
These are run counts, not token totals or language percentages.

## Dave's observations and questions

Dave is excited by the visualization: the overview makes the alternation
and run-size structure visible, and a same-size prefix zoom should make
individual runs easier to inspect. One Latin run appeared to reach the
10^3 range. Inspection of the saved run JSON gives a maximum Latin run of 599 tokens;
four Latin runs map to rounded log radius 3 (no Latin run reaches 1,000).
The radius is round(log10(length)), not an exact power-of-ten length. Run lengths count tokens,
not characters; Latin does not establish French language identity.
German-looking text also occurs in generated output.

## Punctuation and mixed scripts

The 359 findings are original whitespace-delimited token occurrences
containing letters from multiple scripts, not all tokens with punctuation,
and not necessarily 359 distinct spellings. Only the first 50 are shown.
Punctuation remains in the displayed source token but is ignored when
collecting letter scripts. Examples include `m-llе` and `Ha-днях,`.
Mixed Latin/Cyrillic lookalikes deserve inspection, not automatic correction.

The plotting and generation paths already normalize separately: NFKD,
discard combining marks, and map punctuation to separators. This also
changes Russian й to и and ё to е, and removes French accents. Thus the
current generated strings are not faithful orthographic reproductions.
Keep this baseline unchanged for the first comparison; revisit normalization
in a separate controlled experiment.

## Generation already exists

`summary.samples` contains generated text, not corpus excerpts. Word contexts
use n=0,1,2,3 and generate 100 tokens; character contexts use n=0,1,2,3,5
and generate 500 characters. Seeds are fixed. The observed German-to-French
transition is in `character_n5`. Inspect the original corpus before making
claims about the exact source of any generated passage.

An n-gram model IS a statistical language model; it is not a neural language
model. With k preceding tokens, it estimates

$$P(w_t\mid w_{<t}) \approx P(w_t\mid w_{t-k},\ldots,w_{t-1}).$$

Here code n counts context tokens; conventional n-gram order is n+1.
Future experiment: generate longer samples and compare script-switch/run
statistics with the real corpus under identical preprocessing.

## Prefix zoom

`python scripts/run_first_experiment.py --num-language-changes 1000`

This plots 1,001 complete runs, including numeric/other transitions.
A request beyond the available transitions warns and uses all runs.
Overview and prefix use the same figure dimensions and full-corpus radius
limits. The prefix gets its own figure filename. Corpus statistics and
short generated samples still describe the full input corpus.

## Inspection commands and follow-ups

PowerShell equivalent of `head -n 60`:

```powershell
Get-Content outputs/first_experiment_summary.json -Encoding UTF8 -TotalCount 60
```

This limits lines, not characters; very long JSON lines can still be large.
Run JSON pairs are `[script_class, token_count]`: numeric=0, Cyrillic=1,
Latin=2, other=3. Initial runs include the builder's volume headings and
Roman-numeral chapter headings, not only narrative prose.

TODO: word/index slicing with explicit partial-run policies; six run-based
panels; exact long-Latin-run inspection; corpus completeness; explanatory
test strings for mentoring; dedicated generated-text comparison outputs.

`structure.ps1` makes directories with -Force but overwrites helper/profile
files via Set-Content. Repeating it restores its templates; it does not
create numbered per-experiment subdirectories. No rerun is needed here.
