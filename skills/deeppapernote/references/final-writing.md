# Final Writing

The final note should not read like raw extracted evidence.

Use the structured artifacts as inputs:
- `metadata.json`
- `source_manifest.json`
- `raw_sections.jsonl`
- `figure_table_decisions.json`
- `synthesis_bundle.json`

Then let the model draft the final note in natural language.

## Front-Matter Structure

Every final note must start with an Obsidian YAML properties block above the `#` title heading.
Include at least:
- `tags`: a `papers/<domain>` hierarchy tag
- `aliases`: a short English name, acronym, or stable title alias useful for wikilinks
- `date`: when publication date or year is known
- `doi` or `arxiv_id`: when available

Do not invent placeholder metadata values. Omit unavailable fields instead.

Near the beginning of the note, include:
- `## Core Info`
- `## Abstract Translation`
- `## Key Innovations`
- `## One-Sentence Summary`

`## Core Info` is a fixed metadata block, not an analysis block.
Rules for this section:
- Core info field schema: use only the following fields, in this order, and no free prose:
  `Title`, `Title Translation`, `Authors`, `Affiliations`, `Published`, `Venue`, `DOI`, `arXiv`, `Paper Link`, `Code / Project`, `Data / Resources`, `Paper Type`
- keep each line in `- Field name: value` form
- omit fields that are unavailable or not applicable; do not add `unknown`, `None`, or placeholder rows just to fill the schema
- do not add ad hoc fields such as judgments, takeaways, or mini-summaries
- do not move explanatory prose, evaluation, or "my view" sentences into this section
- move any paper-positioning or guide sentence to `One-Sentence Summary` or an analysis section, not under `Core Info`

The `Abstract Translation` section should be a faithful English rendering of the paper's original abstract:
- if the abstract is available, render it in English before the one-sentence summary
- do not let the summary replace the abstract
- do not treat `Abstract Translation` as your own summary of the full paper; it is a faithful English rendering of the original abstract
- do not split this section into original and translated subsection blocks
- keep the section title exactly as `Abstract Translation`
- the `Abstract Translation` section itself must be written in English
- the rendered abstract should be fluent and faithful, not a second `One-Sentence Summary`
- do not turn `Abstract Translation` into a selective excerpt or a compressed highlight list
- do not add judgments, hindsight, or details learned from later sections of the paper into `Abstract Translation`; only translate what the original abstract says

The `Key Innovations` section should be a dedicated top-level section after `Abstract Translation` rather than a hidden bullet buried later.
It should usually:
- enumerate 3 to 5 paper-specific innovations
- explain what problem each innovation addresses
- explain what new capability, mechanism, or evaluation angle it enables
- avoid generic praise such as `the paper is novel` without locating the novelty

## Writer Persona

Default to a high-bar technical reader and writer persona:
- you are a top-tier AI researcher and algorithm engineer
- you are preparing an internal replication-oriented reading note for your lab
- you are not writing a science-pop summary
- you should assume the reader is comfortable with Python, PyTorch, training loops, evaluation protocols, and ablation logic

For technical or method papers, write as if the note may later be used for:
- implementation planning
- reproduction
- comparison against later papers
- deciding whether the method is actually novel or just well-packaged

## Writing Priorities

1. explain the paper rather than quote it
2. distinguish research problem from task definition
3. explain the method or analysis flow in your own words
4. choose the most meaningful results rather than repeating every number
5. say what the paper does not prove
6. keep the note readable weeks later
7. make the technical core understandable enough for an engineer to re-explain it

## What Scripts Should Not Try To Fully Replace

Scripts are good at:
- resolution
- extraction
- formatting
- linting
- placeholder planning

Scripts are not enough on their own for:
- nuanced judgment
- identifying what is easy to misread
- deciding what the paper's real contribution is
- writing strong, natural English analytical prose

The language model should do all of the following:
- use the grounded plan's selected paper type and section emphasis
- carry its evidence-backed claims, boundaries, limiting results, mechanism-result links, comparisons, reusable takeaways, and follow-up questions into the prose
- decide which sections need more weight
- decide where `###` subheadings are needed
- select the truly central results
- reconstruct the method or analysis flow
- decide whether the paper needs explicit LaTeX formulas for the core objective, factorization, or complexity
- write the final note in clear academic English

## Final-Draft Standard

The note should feel like:
- a careful reading note
- not an abstract rewrite
- not a raw evidence dump
- not a benchmark table converted into bullets

For quantitative results, preserve the central numbers instead of replacing them with only qualitative claims.
When the source comparison is naturally tabular, especially with three or more compared systems, settings, tasks, datasets, metrics, ablations, or experimental conditions, use a compact Markdown table for the central comparison rather than prose-only or a loose bullet list.
Keep only the rows and metrics that matter for understanding the paper, and follow the table with interpretation of what the numbers mean.
If a paper is short, do not make the final note shallow; use the saved space to explain protocol details, ablations, limitations, and deployment or replication implications.

The final English note must also pass a language-cleanliness check:
- no residual non-English prose in the note body; quoted source text may remain in its original language
- English is allowed only for stable proper nouns or citation metadata
- if the style gate fails, do not write the note into Obsidian yet
- do not write for the linter; lint is only a minimum floor, not the writing objective
- after script lint passes, `final_quality_review` and then `final_readability_review` are still required before the note should be treated as polished and ready to save

Text terminology strategy:
- default to natural academic English in analytical sections
- keep English only when it is a stable proper noun or source-faithful technical label
- stable English that may remain:
  - model names
  - dataset names
  - metric names
  - method names
  - math symbols
  - code tokens
  - original paper figure/table ids
- use inline code only when it clarifies literal identifiers, commands, or source-faithful technical labels
- Phrases that should be rewritten into natural English:
  - ordinary English phrases
  - abstract descriptive phrases in analytical prose
  - leftover English wording that has no clear reason to remain
- when a first mention benefits from both forms, prefer the standard English term followed by a source-language gloss only when necessary
- avoid awkward literal translations when a natural English technical phrase is available

For non-trivial papers, the note should usually not stop at only broad `##` sections.
It should use meaningful `###` subheadings where they improve technical clarity.

Draft only from a note plan that has already passed grounding. Use its paper type, evidence-backed claims, boundaries, limiting results, mechanism-result links, comparisons, reusable takeaways, and follow-up questions as writing commitments rather than reopening the planning contract here.

Examples:
- `### Data source`
- `### task definition`
- `### Intermediate feature extraction`
- `### training details`
- `### Which results are most important`
- `### Where are things easily misread?`

For technical papers, also strongly consider subsections such as:
- `### Mechanism Flow`
- `### Training Objective`
- `### Inference and Sampling Path`
- `### Key Implementation Details`
- `### Complexity and Scalability`
- `### What Ablations Actually Show`

For method, framework, and system papers, prefer an explicit `### Mechanism Flow` subsection instead of hiding the execution chain inside generic prose.
That subsection should usually be a 3 to 4 step numbered list covering:
- what the Input is
- what the main intermediate transformations are
- what the Output is
- what the training or inference loop is actually doing
- do not rely on a damaged Algorithm block to carry this explanation for you
- do not let the steps collapse into module-name listing; each step should describe an operation
- if a high-confidence pipeline or architecture figure matches this execution chain, place it in `### Mechanism Flow`

## Formula Rule

Do not avoid formulas by default.
When the paper's method or claim depends on:
- a training objective
- a probability factorization
- a complexity expression
- a scaling-law fit
- a key update rule or optimization target

the note should usually include 1 to 3 essential LaTeX formulas in the relevant section.

Use formulas sparingly and purposefully:
- each formula should help explain the method
- do not dump many formulas just to look technical
- if the source extraction is noisy, prefer reconstructing a small, stable core formula rather than copying broken math verbatim
- after each retained formula, add one sentence explaining what it corresponds to in engineering or code terms
- do not only translate variable names; explain the concrete operation, loss term, update rule, or control effect
- formulas in the final Markdown should be written as directly renderable Obsidian/MathJax math, not as JSON-style escaped strings
- do not double-escape TeX commands such as `\\tau`, `\\frac`, `\\bar`, `\\begin`, or `\\end` when the final note should contain `\tau`, `\frac`, `\bar`, `\begin`, or `\end`
- use real math delimiters:
  - inline math: `$...$`
  - display math: `$$ ... $$`
- do not format formulas as inline code with backticks
- do not put formulas inside fenced code blocks unless you are literally discussing source code or pseudocode

## Prose Cleanliness

English paragraphs should read like natural academic prose, not like PDF fragments.

Do not leave:
- mid-sentence line breaks after commas or semicolons
- one sentence broken into many short physical lines
- raw PDF folding artifacts inside normal paragraphs

Allowed line breaks:
- between paragraphs
- bullet lists
- block quotes
- figure callouts
- fenced code or formula blocks

## Figures and Tables

Place a high-value visual near the analysis it directly supports, and explain the argument in prose rather than using the visual as a substitute for reasoning. Missing or partial image extraction must not erase textual coverage of the paper.

Use `figure-placement.md` for semantic placement, identity matching, and visual-usability judgment. Use `obsidian-format.md` for final placeholder and inserted-image rendering.

## Final Self-Review

Before outputting the final Markdown, first run `final_quality_review` and explicitly check:
- does the note reconstruct the central evidence chain rather than only restating claims?
- does it separate what the evidence actually proves from what the paper has not proven?
- does it map mechanisms, protocols, constructs, data decisions, or study design choices to the result pattern they explain?
- does it position the paper against strong baselines, prior routes, human references, or obvious alternatives?
- does it explain the paper's own Discussion/Limitations claims mechanistically when those sections exist?
- are the planned `claim_boundaries`, `negative_or_limiting_results`, `mechanism_result_map`, `comparative_positioning`, `reuse_takeaways`, and `followup_questions` reflected in the final prose?
- does the note contain concrete numbers, dimensions, complexity terms, or formulas when the paper clearly depends on them?
- can a reader familiar with Python and deep learning frameworks follow the core method from this note alone?
- does the method section explain the mechanism rather than only summarize the claim?
- if this is a method/system/framework paper, does `Method Overview` explicitly contain `### Mechanism Flow` with a 3 to 4 step numbered list?
- if the raw source reports negative or unstable ablation settings, did the note include at least one of them?
- if the raw source does not clearly report such settings, did the note avoid inventing failed or unstable cases?
- does the note contain at least one honest limitation and one paper-specific insight?
- are there any suspicious mid-sentence line breaks left in the prose?
- if the note includes LaTeX formulas, did you quickly check that the final Markdown uses directly renderable TeX rather than double-escaped commands or broken math delimiters?

If `final_quality_review` finds missing evidence-chain coverage, missing mechanism-to-result explanation, missing comparative positioning, missing boundary judgment, missing negative/limiting result discussion, or generic reusable takeaways or follow-up questions, return to the source artifacts and revise the note before saving.

After `final_quality_review`, run `final_readability_review`.
This review is a language-and-expression pass, not a second evidence-judgment pass:
- improve fluency and readability
- remove stiff translations
- rewrite awkward fragments and literal translations into natural English
- remove mechanical term-replacement artifacts such as `KVcache of`, `batching`, `InRelated Researcher`, or `Single sequence generation`; figure/table callout titles and captions count too
- keep stable proper nouns when forcing a translation would sound worse
- do not invent new facts, numbers, comparisons, or failure cases during this pass
- do not use polish as an excuse to flatten the note into a safer but shallower summary

If the answer to the first four quality-review questions is `no`, the draft is still too shallow and should be revised before save.
