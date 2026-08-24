# Obsidian Format

## Heading Rules

- Use `#` for the note title only.
- Use `##` for major sections.
- Use `###` only when a section genuinely needs internal structure.
- Do not flatten everything into bullet points.
- For method, system, benchmark, or clinical empirical papers, prefer meaningful `###` subheadings in technical sections instead of one long undifferentiated block.
- For method, framework, or system papers, default to `### Mechanism Flow` inside `Method Overview` and write it as a numbered 3 to 4 step flow.

## File Naming

Default file name:
- sanitized English title with underscores
- default note layout is folder-per-paper:
  - `<field>/<paper_slug>/<paper_slug>.md`
  - `<field>/<paper_slug>/images/...`
- when deciding `<field>`, prefer matching an existing first-level domain folder under the user's papers directory
- domain routing uses the editable taxonomy in `references/domain_rules.yaml`: application domains are checked before fallback method domains
- reuse existing first-level folders conservatively; method-only evidence should not force reuse of an unrelated application folder
- only create a new domain folder when no existing domain is a reasonable fit
- do not save new papers directly into the bare papers root
- always create the paper-local `images/` directory during final save, even if no real image is inserted
- the paper-local `images/` directory is part of the required note layout, not an optional optimization

If the user already has a vault convention, preserve it.

## Markdown Style

- Prefer short paragraphs over long bullet lists.
- Use bullets for metadata and sharply list-shaped content.
- Keep code or metric identifiers in backticks.
- Use backticks for literal identifiers when helpful, for example `GPT-4`, `SQuAD`, `BLEU`, or `87.3%`; do not wrap ordinary prose solely for visual separation.
- Preserve stable internal links where useful.
- Use normal LaTeX delimiters for math:
  - inline math: `$...$`
  - display math:
    `$$`
    `...`
    `$$`
- Do not wrap formulas in backticks or fenced code blocks unless you are literally showing source code.

## Core Info Block

`## Core Info` is a fixed metadata zone.

Formatting and scope rules:
- Core info field schema: use only the following fields, in this order, and no free prose:
  `Title`, `Title Translation`, `Authors`, `Affiliations`, `Published`, `Venue`, `DOI`, `arXiv`, `Paper Link`, `Code / Project`, `Data / Resources`, `Paper Type`
- keep each entry in `- Field name: value` form
- omit fields that are unavailable or not applicable; do not add placeholder rows just to fill the schema
- do not add interpretation, commentary, judgment, or takeaway lines inside `Core Info`
- do not use the last metadata bullet as a place to append extra analysis
- move explanatory content to `One-Sentence Summary`, `Deep Analysis`, `My Notes`, or another true analysis section

## YAML Frontmatter

Every note must start with an Obsidian properties block **above** the `#` title heading.

Required fields:
- `tags`: use `papers/<domain>` hierarchy, e.g. `papers/NLP`, `papers/CV`, `papers/multimodal`
- `aliases`: English short name or common abbreviation for wikilink resolution
- `date`: ISO publication date; use `YYYY` if only the year is known
- `doi`: DOI string without the `https://doi.org/` prefix; omit the field entirely if unavailable

Example:

```yaml
---
tags:
  - papers/NLP
aliases:
  - "Paper Short Name"
date: 2024-05-01
doi: 10.18653/v1/2024.acl-long.1
---
```

Rules:
- Do not invent placeholder values for missing fields; omit them instead.
- The `tags` field must always be present with at least one `papers/<domain>` tag.
- `aliases` should be the paper's short name or acronym (e.g. "GPT-4", "LoRA"), not a paraphrase.

## Figure Placeholder Style

Use this callout format only for placeholders that remain unresolved in the final note:

```md
> [!figure] Fig. 3 Data distribution and quality assessment
> Suggested Placement:Data and Task Definition
> Rationale: This figure shows sample composition, conversation-length statistics, and expert quality-control results, making it important for understanding the boundaries of the `PsyInterview` dataset.
> Current Status: Keep placeholder; extraction produced only local subfigures and cannot reliably reconstruct a complete, independently interpretable original figure.
```

Formatting rules:
- keep the original paper numbering, for example `Fig. 3` or `Table 2`
- keep a short human-readable label on the first line
- always include `Suggested Placement`
- always include `Rationale`
- always include `Current Status`

`Current Status` should be explicit, for example:
- `Keep placeholder; no high-confidence complete image was found.`
- `Keep placeholder; only possible local subfigures were matched, which is not reliable enough for replacement.`

The structured `[FIGURE_PLACEHOLDER] ... [/FIGURE_PLACEHOLDER]` block is legacy/internal only.
Do not use it in the final user-facing note unless you are debugging the pipeline.

If a real image has been selected and materialized into the vault, do not keep the `[!figure]` callout for that same figure.
Prefer an Obsidian embed, or use a Markdown image embed when that is the available path.
The embed must be followed immediately by exactly one italic caption line:

```md
![[Research/Papers/DeepPaperNote/paper_slug/images/page_003_img_01.png]]
*Original figure number: Fig. 2. Data-generation flowchart. Inserted here because it best supports the Method Overview.*
```

## Default Section Order

1. `Core Info`
2. `Abstract Translation`
3. `Key Innovations`
4. `One-Sentence Summary`
5. `Research Question`
6. `Data and Task Definition`
7. `Method Overview`
8. `Key Results`
9. `Deep Analysis`
10. `Limitations`
11. `My Notes`
12. `References`

When abstract metadata exists, `Abstract Translation` should be a single faithful English rendering of the original abstract rather than a bilingual subsection pair.

This order is the stable backbone, not a full outline.
When the paper is complex, add `###` subsections such as:
- `### Data source`
- `### task definition`
- `### Mechanism Flow`
- `### Why the result holds`
- `### Where are things easily misread?`

## References Section Format

Entries in `## References` should link to existing notes in the vault where possible.
If the synthesis bundle includes `references.candidates`, use confirmed candidate `wikilink` values when present. When `wikilink` is empty, treat `display_text` as the plain-text fallback.
Follow this priority order for each reference:

1. **Vault lookup first**: check whether the cited paper already has a note in the vault.
   - Match by note basename (the `<paper_slug>` part of the folder name).
   - Match by the `aliases` field in the note's YAML frontmatter.
2. **If a match is found**: write a wikilink that separates the target from the display text:
   ```
   - [[paper_slug_or_alias|Human Readable Title]]
   ```
3. **If no match is found**: do not invent a wikilink target. Write the reference as plain text instead:
   ```
   - Vaswani et al. (2017). Attention Is All You Need.
   ```
   Use the candidate `display_text` as the plain fallback when available.

Rules:
- Never use a raw English paper title as the wikilink target; it will not match vault filenames.
- To derive a likely slug from a title: lowercase the title and replace spaces and special characters with underscores — but only use the result as the target if you have confirmed the file exists.
- List only papers cited or directly relevant to this note.
- Do not add extra DOIs or author metadata when using wikilink format; the display text is enough.
