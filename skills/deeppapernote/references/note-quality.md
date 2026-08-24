# Note Quality

The note is high quality only if it satisfies most of the checks below.

## Minimum Bar

- It is not a paraphrase of the abstract.
- It distinguishes `research problem` from `task definition`.
- It explains how the method or analysis actually works.
- It reports the most meaningful results, not only the prettiest numbers.
- It includes at least one real limitation.
- It includes an explicit judgment about the paper's actual contribution.
- It includes at least one paper-specific technical subsection rather than only broad top-level sections.
- For method-heavy papers, it explains enough mechanism detail that an engineer could re-explain the pipeline without reopening the PDF.

## Structural Checks

The note should usually include:
- `Core Info`
- `Abstract Translation`
- `Key Innovations`
- `One-Sentence Summary`
- `Research Question`
- `Data and Task Definition`
- `Method Overview`
- `Key Results`
- `Deep Analysis`
- `Limitations`
- `My Notes`
- `References`

For non-trivial papers, it should usually also include multiple `###` subheadings inside:
- `Data and Task Definition`
- `Method Overview`
- `Key Results`
- `Deep Analysis`

Before the final note is written, the run should already have an inspectable, grounded plan whose analytical commitments are paper-specific.

Bad sign:
- the model jumps directly to a polished final note with no grounded plan at all

## Depth Checks

### Good signs

- The note explains the flow of information in the method.
- The note explains technical details with section-specific subheadings rather than one flat block.
- The note points out what the paper does not prove.
- The note identifies where labels, supervision, or evaluation may be weak.
- The note explains why the paper matters to later reading or research reuse.
- The note surfaces one paper-specific insight, not just generic praise.

### Bad signs

- It only repeats the introduction and abstract.
- It lists model names without explaining the pipeline.
- It copies metrics without noting the evaluation setting.
- It says the paper is innovative without locating the innovation.
- It has no dedicated `Key Innovations` section and leaves the paper's novelty scattered across the note.
- It uses generic limitations such as "future work can use more data" and nothing more specific.
- It flattens a technically rich paper into only `##` headings with no internal structure.

## Quality Gate

Fail closed if any of these are missing:
- method evidence
- result evidence
- a clear paper identity
- enough metadata to label the note responsibly

Also fail closed if:
- the final English note still contains residual non-English body prose outside quoted source text and citations
- body prose is not written in clear academic English
- figure placeholders include untranslated caption sentences that read like raw extraction rather than note prose

Strong notes should also clearly contain:
- the most important numbers
- the most important comparison
- the central evidence chain behind the paper's main claim
- a clear distinction between what the paper proves and what it does not prove
- at least one limiting, weak, negative, or explicitly unreported result that constrains the conclusion
- one paper-specific insight
- one honest limitation

For technical papers, strong notes should usually also contain:
- at least one method subsection that goes beyond summary into mechanism explanation
- at least one concrete training / inference / complexity detail
- at least one key formula or formal expression when the paper's contribution depends on it
- formulas rendered as math rather than code formatting

When abstract metadata exists, strong notes should also make `Abstract Translation` a faithful English rendering of the abstract:
- render the original abstract in English rather than rewriting it as your own summary
- avoid reducing it to a shorter interpretation-only summary
- keep this section as `Abstract Translation`, not a bilingual original-plus-translation block
- do not mix innovation takeaways, evaluation, or post-hoc interpretation into this section
