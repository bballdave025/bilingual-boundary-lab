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

## Translation round-trip observation — 2026-10-18

Dave submitted the generated `word_n0` sample to Google Translate and
reported a fluent English narrative with connective events absent from
the incoherent source. Back-translation yielded another fluent Russian
passage, not a reconstruction of the source. The reported outputs are
user-supplied; service/model configuration was not independently verified.

This illustrates a risk: fluency can conceal reconstruction or invention.
Round-trip overlap measures surface preservation, not translation fidelity
or proof of a particular service architecture.

Using the original generated Russian as reference and the supplied
back-translation as candidate, scores below use NFC, case folding, Unicode
alphanumeric word tokenization, punctuation splitting, and no stemming or
lemmatization. Accents and ё/й are preserved. These choices differ from
the experiment's existing NFKD preprocessing.

Reference tokens: 100; candidate tokens: 105.

- ROUGE-1: precision 0.247619, recall 0.260000, F1 0.253659.
- ROUGE-2: precision 0.009615, recall 0.010101, F1 0.009852.
- ROUGE-L: precision 0.152381, recall 0.160000, F1 0.156098.

TODO: preserve the original/English/back-translated triplet and repeat
with controlled translation settings; compare lexical overlap with manual
checks of added events, relationships, and omitted fragments.

Dave uses 10^3 as the nearest geometric order-of-magnitude bin: 599
correctly belongs there because it exceeds sqrt(100*1000) ≈ 316.23.
The plot uses that same rounded-log convention; 599 is not an error.


## Starting contexts and reproducibility

Word models receive the first n corpus tokens as a supplied prefix and
random seed 1729+n. Character models receive the first n normalized
characters and random seed 2718+n. For n=0 the prefix is empty. Repeated
runs with the same input and environment therefore reproduce these samples.
These are opening-conditioned demonstrations, not a representative sample
of all possible generations. Longer comparisons should retain explicit
starting contexts and examine several random seeds.

## The penguin/typewriter effect — Dave's analogy

> There are two penguins in the bathtub. One turns to the other and asks
> for the soap. The one who was asked turns back and says, "What do I look
> like to you, a typewriter?"

When someone laughs as though they understand, Dave follows with:

> Most people don't get that joke. Including me. Explain it to me.

The analogy: fluent output can suggest an understanding unsupported by
incoherent input. The translation seemed to supply a narrative connecting
independently sampled words. Back-translation was useful for exposing the
rewrite; ROUGE measures surface overlap, not the truth of inferred events.
For family messages, Dave checks preservation of intended content rather
than identical wording.

## Visual exploration

Dave's annotated images are in `img/fun/`. The musical excerpt is identified
by Dave as the Russian national anthem, not the tsarist anthem. The
100/250/500/1000-change views make individual runs and recurring horizontal
arrangements easier to see. Top/bottom symmetry is imposed by the plotting
algorithm; repetition along the run-order axis is an empirical question.
Labels such as "Lotsa French" identify candidate passages for source
inspection; Latin-script classification alone is not language identification.
Small Numeric/Other/Latin runs interrupt longer Cyrillic passages. Extract
those passages before attributing causes to the interruptions.

## Safe scaffold refresh

Both structure scripts now default to `do_very_safe_structure=true`
(`$true` in PowerShell): create missing scaffold files and preserve existing
ones. Set false explicitly to restore the previous overwrite behavior.
Directory creation remains repeatable. No numbered experiment directories
are created. Newly written PowerShell templates use UTF-8 without BOM and
LF endings; existing files are left unchanged in safe mode.

## Next bounded work

- Regenerate the full overview so its x-axis label matches the detail views.
- Inspect source passages behind selected highlighted runs.
- Compare one longer generation with real text of matched token count,
  using the same preprocessing and visual scale. Measure switch counts
  rather than forcing a target number of switches.
- Separate follow-up: general-text generator and guiding Jupyter notebook,
  configurable maximum context order, optional thin CLI.
- Preserve existing punctuation/hyphen behavior for this baseline.
