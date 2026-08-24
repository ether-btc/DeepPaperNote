from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from lint_note import (
    core_info_structure_issues,
    figure_structure_issues,
    figure_structure_passes,
    find_missing_sections,
    front_matter_order_warnings,
    has_figure_marker,
    inspect_note_plan,
    inspect_figure_callouts,
    inspect_reference_hygiene,
    inspect_substantive_content,
    math_render_issues,
    mechanism_flow_warnings,
    mechanical_translation_artifact_issues,
    mixed_language_issues,
    strip_frontmatter,
    suspicious_code_formatted_math,
    suspicious_mid_sentence_linebreaks,
)


def _valid_note_text() -> str:
    return """# Paper

## Core Info

- Title: Paper
- Published: 2024
- DOI: 10.1234/example

## Abstract Translation

The paper focuses on the problem of error propagation in long-chain reasoning，Propose a way to retrieve evidence、A framework for joint modeling of tool call status and final answer，and reported the main experimental conclusions。

## Key Innovations

- The paper puts retrieval evidence selection and tool call planning in the same state transfer process to model，So that false evidence will not be regarded as reliable input by default in subsequent steps。
- The paper designs a traceback mechanism for failed calls，Explicitly record the confidence level and exception type returned by the tool at each step，This allows the final answer to differentiate between insufficient evidence and model inference errors.。

## One-Sentence Summary

This paper uses auditable tools to call state machines to reduce error accumulation in long-link question answering.。

## Research Question

The paper focuses on the incomplete retrieval of evidence in multi-step question answering systems.、When tool calls fail and intermediate states are misused，How to maintain traceability and reliability of final answers。

## Data and Task Definition

Task input includes user questions、List of candidate retrieval evidence and callable tools；The output includes the final answer、Each step of tool call record and failure reason annotation。

## Method Overview

### Mechanism Flow

Enter the question and enter the evidence screening module first.，Then the tool planner selects the next call，Finally, the answer generator combines the status log to output a traceable conclusion.。

> [!figure] Figure 1 Method overview
> Suggested Placement:Method Overview
> Rationale:Help understand the overall process。
> Current Status:Reserve placeholder；High confidence whole image not found。

## Key Results

On three multi-step question answering datasets，The method changes the answer accuracy from 71.2% promoted to 78.5%，and reduce the proportion of non-traceable errors from 18% down to 9%。

## Deep Analysis

The critical value of this work goes beyond improving the final score，Instead, it turns failed tool calls from hidden intermediate states into inspectable evidence.，Therefore, it is suitable for knowledge-intensive Q&A that requires audit links.。

## Limitations

The paper is mainly verified on English question and answer data，The tool set is also concentrated in two categories: retrieval and calculation.，This state machine has not been proven to be stable for covering multi-modal tools or high-latency external services。

## My Notes

I will focus on whether its failure backtracking mechanism can be transferred to the paper intensive reading process.，because DeepPaperNote It is also necessary to distinguish between missing evidence and insufficient model summary。

## References

- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example
"""


def _valid_plan_payload() -> dict:
    return {
        "paper_type": "AI_method",
        "paper_type_rationale": "The paper proposes a model mechanism and evaluates it experimentally.",
        "dominant_domain": "reasoning",
        "must_cover": ["Method Overview"],
        "key_numbers": ["78.5"],
        "real_comparisons": ["baseline"],
        "central_claims": [
            {
                "claim": "The method improves traceability.",
                "supporting_evidence": [{"section_id": "sec:method"}],
                "what_it_actually_proves": "The described mechanism records tool states.",
                "what_it_does_not_prove": "It does not prove production robustness.",
            }
        ],
        "claim_boundaries": ["The evidence is limited to the reported workflow."],
        "negative_or_limiting_results": ["The paper does not report multi-service failures."],
        "mechanism_result_map": ["The failure-state mechanism explains lower unrecoverable errors."],
        "comparative_positioning": ["The method is compared against answer-only baselines."],
        "reuse_takeaways": ["Track failure state explicitly."],
        "followup_questions": ["Check whether the mechanism survives missing tool outputs."],
        "section_plan": [{"section": "Method Overview", "evidence_sources": [{"section_id": "sec:method"}]}],
    }


def test_reference_hygiene_allows_images_doi_arxiv_and_urls() -> None:
    note = (
        _valid_note_text()
        + "\n![Figure 1](images/page_001_fig_figure_1.png)\n"
        + "*Original figure number:Fig. 1。Method diagram。*\n"
        + "\n- arXiv: 2401.00001\n"
        + "- Project: https://example.org/papers/demo\n"
    )

    assert inspect_reference_hygiene(note) == []


def test_reference_hygiene_gate_flags_runtime_artifact_references(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(
        _valid_note_text().replace(
            "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
            "- LLaMA source: /private/tmp/dpn-test-runs/candidate/artifacts/llama_source_manifest.json",
        ),
        encoding="utf-8",
    )
    plan_path.write_text(json.dumps(_valid_plan_payload()), encoding="utf-8")

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["passes_reference_hygiene_gate"] is False
    assert "runtime_artifact_references_present" in payload["warnings"]
    assert payload["reference_hygiene_issues"]
    assert payload["reference_hygiene_issues"][0]["reason"] == "runtime_artifact_reference"
    assert "llama_source_manifest.json" in payload["reference_hygiene_issues"][0]["match"]


def test_figure_callout_requires_status_line() -> None:
    note = """# Title

## Core Info

> [!figure] Fig. 1 Method diagram
> Suggested Placement:Method Overview
> Rationale:Help understand the overall process。
"""
    warnings = inspect_figure_callouts(note)
    assert "figure_callout_missing_status" in warnings


def test_legacy_placeholder_block_is_flagged() -> None:
    note = """# Title

[FIGURE_PLACEHOLDER]
id: Fig.1
[/FIGURE_PLACEHOLDER]
"""
    warnings = inspect_figure_callouts(note)
    assert "legacy_figure_placeholder_block_used" in warnings


def test_figure_bucket_heading_is_figure_structure_issue() -> None:
    note = """# Title

## Deep Analysis

### Remaining chart space

> [!figure] Fig. 6 Supplementary figure
> Suggested Placement:Deep Analysis
> Rationale:Help with understanding supplementary material。
> Current Status:Reserve placeholder；High confidence whole image not found。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_placeholder_bucket_heading" for issue in issues)
    assert figure_structure_passes(note) is False


def test_figure_callout_target_section_mismatch_is_flagged() -> None:
    note = """# Title

## Deep Analysis

> [!figure] Fig. 1 problem boundary diagram
> Suggested Placement:Research Question
> Rationale:Help define problem boundaries。
> Current Status:Reserve placeholder；High confidence whole image not found。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_callout_placement_mismatch" for issue in issues)


def test_figure_callout_inside_declared_section_passes() -> None:
    note = """# Title

## Method Overview

### Mechanism Flow

> [!figure] Fig. 2 Overall process
> Suggested Placement:Method Overview
> Rationale:Help understand the execution chain。
> Current Status:Reserve placeholder；High confidence whole image not found。

> [!figure] Fig. 3 Mechanism details
> Suggested Placement:Mechanism Flow
> Rationale:Help understand execution chain details。
> Current Status:Reserve placeholder；High confidence whole image not found。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_figure_callout_with_inserted_image_status_fails_figure_structure_gate() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 2 Overall process
> Suggested Placement:Method Overview
> Rationale:Help understand the execution chain。
> Current Status:Replaced with real picture；What is currently inserted is a partial panel of the original image of the paper.。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_redundant_callout" for issue in issues)
    assert figure_structure_passes(note) is False


def test_dqn_style_callout_plus_embed_fails_figure_structure_gate() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 1 Agent-environment loop
> Suggested Placement:Method Overview
> Rationale:Help understand the interactive closed loop of reinforcement learning。
> Current Status:Copied to images/figure_1.png，and insert it as a real picture。
![[Research/Papers/DQN/images/figure_1.png]]
*Original figure number:Fig. 1。Agent-environment loop。*
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_redundant_callout" for issue in issues)
    assert figure_structure_passes(note) is False


def test_non_figure_remaining_heading_is_not_flagged() -> None:
    note = """# Title

## Deep Analysis

### remaining questions

Here we discuss questions that have not yet been answered by the paper。
"""
    assert figure_structure_issues(note) == []


def test_figure_callout_missing_location_fails_figure_structure_gate() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 1 Method diagram
> Rationale:Help understand the overall process。
> Current Status:Reserve placeholder；High confidence whole image not found。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "figure_callout_missing_location" for issue in issues)
    assert figure_structure_passes(note) is False


def test_figure_callout_missing_title_fails_figure_structure_gate() -> None:
    note = """# Title

## Method Overview

> [!figure]
> Suggested Placement:Method Overview
> Rationale:Help understand the overall process。
> Current Status:Reserve placeholder；High confidence whole image not found。
"""
    warnings = inspect_figure_callouts(note)
    issues = figure_structure_issues(note)
    assert "figure_callout_missing_title" in warnings
    assert any(issue["reason"] == "figure_callout_missing_title" for issue in issues)
    assert figure_structure_passes(note) is False


def test_nonstandard_bracket_figure_placeholder_fails_figure_structure_gate() -> None:
    note = """# Title

## Research Question

[chart placeholder | Fig. 1] The overall task diagram given in the paper。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "nonstandard_figure_placeholder_format" for issue in issues)
    assert figure_structure_passes(note) is False


def test_nonstandard_colon_and_english_figure_placeholders_fail_gate() -> None:
    note = """# Title

## Key Results

chart placeholder: Table 2 Cross-dataset results.

Figure Placeholder | Fig. 3 reasoning example.
"""
    issues = figure_structure_issues(note)
    assert len([issue for issue in issues if issue["reason"] == "nonstandard_figure_placeholder_format"]) == 2
    assert figure_structure_passes(note) is False


def test_image_embed_without_italic_caption_fails_figure_structure_gate() -> None:
    note = """# Title

## Method Overview

![Fig. 2 Architecture](images/page_005_fig_figure_2.png)
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "inserted_figure_missing_caption" for issue in issues)
    assert figure_structure_passes(note) is False


def test_flashattention_style_embed_with_italic_caption_passes() -> None:
    note = """# Title

## Method Overview

![[Research/Papers/FlashAttention/images/page_005_fig_figure_2.png]]
*Original figure number:Fig. 2。FlashAttention The block calculation flow chart of。Inserted here because it best aids understandingMethod Overview。*
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True
    assert has_figure_marker(note) is True


def test_usable_candidate_soft_placeholder_reasons_fail_figure_structure_gate() -> None:
    statuses = [
        "Image cropped for readability，But the final note uses placeholders to keep it lightweight。",
        "High image matching，But the final note does not insert real pictures。",
        "The table is clearly cropped，But the main text has excerpted the core values。",
        "Although there are candidate images available，However, the table content is more suitable to directly transcribe the key values in the text.。",
        "Viewed manually，The cropping is clear and the image numbers match.；But Fig. 1 Has assumed the main process description，Therefore reserved as a low priority supplementary figure placeholder。",
        "Viewed manually，The image is clear and the drawing number matches；Since it serves an auxiliary set specification，rather than the main conclusion，Therefore reserved as a low priority supplementary figure placeholder。",
    ]
    for status in statuses:
        note = f"""# Title

## Method Overview

> [!figure] Fig. 2 candidate image
> Suggested Placement:Method Overview
> Rationale:Help understand the execution chain。
> Current Status:{status}
"""
        issues = figure_structure_issues(note)
        assert any(issue["reason"] == "usable_candidate_unresolved_decision" for issue in issues)
        assert figure_structure_passes(note) is False


def test_usable_candidate_visual_defect_placeholder_reason_passes() -> None:
    note = """# Title

## Method Overview

> [!figure] Table 5 Evaluation form
> Suggested Placement:Method Overview
> Rationale:Help understand the review protocol。
> Current Status:Candidate cropping available，but mixed into adjacent Table 6。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_usable_candidate_lower_priority_placeholder_reason_fails() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 3 Supplementary mechanism diagram
> Suggested Placement:Method Overview
> Rationale:Helps understand supplementation mechanisms。
> Current Status:Candidate cropping available；inserted Figure 2 As the core diagram of the same mechanism，Therefore, this picture has low priority。
"""
    issues = figure_structure_issues(note)
    assert any(issue["reason"] == "usable_candidate_unresolved_decision" for issue in issues)
    assert figure_structure_passes(note) is False


def test_usable_candidate_materialization_blocked_reason_passes() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 4 Tool chain diagram
> Suggested Placement:Method Overview
> Rationale:Help understanding the tool chain。
> Current Status:Candidate available but materialize_figure_asset.py Copy failed/Insufficient permissions。
"""
    assert figure_structure_issues(note) == []
    assert figure_structure_passes(note) is True


def test_missing_asset_must_not_be_reported_as_materialization_blocked() -> None:
    note = """# Title

## Method Overview

> [!figure] Fig. 4 System diagram
> Suggested Placement:Method Overview
> Rationale:Help understand the overall execution chain。
> Current Status:Reserve placeholder：Caused by missing corresponding image assets materialize_figure_asset.py Copy blocked；Keep the structure placeholders for reviewing the original image。
"""
    issues = figure_structure_issues(note)
    assert any(
        issue["reason"] == "missing_asset_misreported_as_materialization_blocked"
        for issue in issues
    )
    assert figure_structure_passes(note) is False


def test_chinese_placeholder_policy_prose_is_not_flagged_as_nonstandard_placeholder() -> None:
    note = """# Title

## Deep Analysis

Here we discuss why chart placement strategies cannot replace text analysis。
"""
    assert figure_structure_issues(note) == []


def test_mechanical_translation_detector_accepts_natural_english_figure_title() -> None:
    note = "> [!figure] Figure 7 Storing the KVcache of two requests at the same time in vLLM"

    issues = mechanical_translation_artifact_issues(note)

    assert issues == []


def test_mechanical_translation_detector_flags_metadata_artifacts() -> None:
    note = "- Affiliations: UC Berkeley, Stanford University, InRelated Researcher, UC San Diego"

    issues = mechanical_translation_artifact_issues(note)

    assert len(issues) == 1
    assert issues[0]["line_number"] == 1


def test_mechanical_translation_detector_accepts_stable_proper_nouns() -> None:
    note = "> [!figure] Fig. 2 Overview of the training pipeline，Training process overview。"

    assert mechanical_translation_artifact_issues(note) == []


def test_mixed_language_detector_flags_prose_line() -> None:
    note = "This paper uses a model, but contains stray \u4e2d\u6587 prose."
    issues = mixed_language_issues(note)
    assert len(issues) == 1


def test_mixed_language_detector_exempts_figure_status_lines() -> None:
    note = "> Current Status:Reserve placeholder；The current extraction results only get partial crop，Unable to recover stably。"
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_figure_callout_title_only() -> None:
    note = "> [!figure] Fig. 2 Overview of the training pipeline，Training process overview。"
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_blockquote_source_text() -> None:
    note = "> Quoted source excerpt: \u4e2d\u6587\u539f\u6587."
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_frontmatter_code_urls_and_references() -> None:
    note = """---
aliases:
  - \u4e2d\u6587\u522b\u540d
---

Inline `\u4e2d\u6587\u4ee3\u7801` and https://example.test/\u4e2d\u6587 are exempt.

```text
\u4e2d\u6587 fenced code
```

## References

- Zhang. \u4e2d\u6587\u8bba\u6587\u6807\u9898. 2024.
"""
    assert mixed_language_issues(note) == []


def test_mixed_language_detector_exempts_core_info_section() -> None:
    note = """## Core Info

- Title：
`AffectGPT: A New Dataset, Model, and Benchmark for Emotion Understanding with Multimodal Large Language Models`
- Authors：
Zheng Lian, Haoyu Chen, Lan Chen
- Affiliations：
Institute of Automation, Chinese Academy of Sciences
"""
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_exempts_core_info_wrapped_value_lines() -> None:
    note = """## Core Info

- Authors：
Zheng Lian, Haoyu Chen, Lan Chen, Haiyang Sun
and additional collaborators from multiple institutions
"""
    issues = mixed_language_issues(note)
    assert issues == []


def test_mixed_language_detector_flags_summary_section_when_mixed() -> None:
    note = """## Abstract Translation

This paper uses a multimodal framework but leaves \u4e2d\u6587 prose.
"""
    issues = mixed_language_issues(note)
    assert len(issues) == 1


def test_mid_sentence_linebreak_detector_flags_pdf_style_wrapping() -> None:
    note = "The most important contribution of this paper is,\nIt redefines the prediction order of visual autoregression."
    issues = suspicious_mid_sentence_linebreaks(note)
    assert len(issues) == 1


def test_mid_sentence_linebreak_detector_ignores_real_paragraph_breaks() -> None:
    note = "The most important contribution of this paper is to redefine the prediction order of visual autoregression.\n\n## Method Overview"
    issues = suspicious_mid_sentence_linebreaks(note)
    assert issues == []


def test_code_formatted_math_detector_flags_inline_code_formula() -> None:
    note = "The core decomposition can be written as `p(r_1, r_2)=\\prod_k p(r_k | r_{<k})`。"
    issues = suspicious_code_formatted_math(note)
    assert len(issues) == 1


def test_code_formatted_math_detector_flags_fenced_formula_block() -> None:
    note = """```
L = x + y
```"""
    issues = suspicious_code_formatted_math(note)
    assert len(issues) == 1


def test_math_render_detector_flags_double_escaped_tex_command() -> None:
    note = """## Method Overview

$$
\\\\tau = \\\\exp(x)
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "double_escaped_tex_command" for issue in issues)


def test_math_render_detector_flags_invalid_frac_arguments() -> None:
    note = r"""$$
\mathrm{Precision} =
\frac{a}
\left|b\right|}
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "invalid_frac_arguments" for issue in issues)


def test_math_render_detector_flags_environment_mismatch() -> None:
    note = r"""$$
\begin{cases}
a
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "environment_mismatch" for issue in issues)


def test_math_render_detector_flags_left_right_mismatch() -> None:
    note = r"""$$
\left| x + y
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "left_right_mismatch" for issue in issues)


def test_math_render_detector_flags_unbalanced_braces() -> None:
    note = r"""$$
\bar{R_t
$$
"""
    issues = math_render_issues(note)
    assert any(issue["reason"] == "unbalanced_braces" for issue in issues)


def test_math_render_detector_accepts_valid_cases_formula() -> None:
    note = r"""$$
\tau =
\begin{cases}
1, & \bar R_t^{(c)} \ge \bar R_t^{(w)} \\
\exp(\bar R_t^{(c)} - \bar R_t^{(w)}), & \bar R_t^{(c)} < \bar R_t^{(w)}
\end{cases}
$$
"""
    issues = math_render_issues(note)
    assert issues == []


def test_find_missing_sections_requires_innovation_section() -> None:
    note = """# Title

## Core Info

## Abstract Translation

## One-Sentence Summary

## Research Question

## Data and Task Definition

## Method Overview

## Key Results

## Deep Analysis

## Limitations

## My Notes

## References
"""
    missing = find_missing_sections(note)
    assert "Key Innovations" in missing


def test_substantive_gate_passes_specific_note() -> None:
    issues = inspect_substantive_content(_valid_note_text())

    assert issues == []


def test_substantive_gate_rejects_empty_shell_innovation() -> None:
    note = _valid_note_text().replace(
        "- The paper puts retrieval evidence selection and tool call planning in the same state transfer process to model，So that false evidence will not be regarded as reliable input by default in subsequent steps。\n"
        "- The paper designs a traceback mechanism for failed calls，Explicitly record the confidence level and exception type returned by the tool at each step，This allows the final answer to differentiate between insufficient evidence and model inference errors.。",
        "This article proposes a new method，innovative。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "innovation_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_warns_single_specific_innovation() -> None:
    note = _valid_note_text().replace(
        "- The paper puts retrieval evidence selection and tool call planning in the same state transfer process to model，So that false evidence will not be regarded as reliable input by default in subsequent steps。\n"
        "- The paper designs a traceback mechanism for failed calls，Explicitly record the confidence level and exception type returned by the tool at each step，This allows the final answer to differentiate between insufficient evidence and model inference errors.。",
        "- The paper puts retrieval evidence selection and tool call planning in the same state transfer process to model，So that false evidence will not be regarded as reliable input by default in subsequent steps。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "innovation_too_few_specific_points" for issue in issues)
    assert all(issue["severity"] != "error" for issue in issues)


def test_substantive_gate_rejects_generic_key_results() -> None:
    note = _valid_note_text().replace(
        "On three multi-step question answering datasets，The method changes the answer accuracy from 71.2% promoted to 78.5%，and reduce the proportion of non-traceable errors from 18% down to 9%。",
        "Experimental results show that the method is effective。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "key_results_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_common_generic_result_evasion() -> None:
    note = _valid_note_text()
    start = note.index("## Key Results") + len("## Key Results")
    end = note.index("\n## ", start)
    note = note[:start] + "\n\nResults show our method is effective.\n" + note[end:]

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "key_results_empty_shell" for issue in issues)


def test_substantive_gate_rejects_common_generic_innovation_evasions() -> None:
    for sentence in ("This paper proposes a new method.", "This paper proposes a novel approach."):
        note = _valid_note_text()
        start = note.index("## Key Innovations") + len("## Key Innovations")
        end = note.index("\n## ", start)
        note = note[:start] + f"\n\n{sentence}\n" + note[end:]

        issues = inspect_substantive_content(note)

        assert any(issue["reason"] == "innovation_empty_shell" for issue in issues)


def test_mechanism_flow_requires_precise_actions_and_is_case_insensitive() -> None:
    vague = """## Method Overview
The model architecture uses training and inference.

### Mechanism Flow
1. A feature receives a Query.
2. The feature receives an update.
3. Another feature receives an update.
"""
    assert "mechanism_flow_too_abstract" in mechanism_flow_warnings(vague)

    precise = """## Method Overview
The model architecture uses training and inference.

### Mechanism Flow
1. The INPUT is mapped into an EMBEDDING.
2. The encoder COMPUTES token representations.
3. The decoder PRODUCES the OUTPUT.
"""
    assert "mechanism_flow_too_abstract" not in mechanism_flow_warnings(precise)


def test_mixed_language_detector_exempts_cjk_in_list_nested_fences() -> None:
    note = """## Method Overview
- ```python
  label = "中文代码内容"
  ~~~ is not a matching closing fence
- ```
Natural English prose follows.
"""
    assert mixed_language_issues(note) == []


def test_substantive_gate_rejects_honest_missing_in_key_results() -> None:
    note = _valid_note_text().replace(
        "On three multi-step question answering datasets，The method changes the answer accuracy from 71.2% promoted to 78.5%，and reduce the proportion of non-traceable errors from 18% down to 9%。",
        "This article does not provide reproducible quantification benchmark；The basis is that both the main text and the appendix only report case analysis，No indicator table or baseline Contrast，Therefore, numerical conclusions cannot be forged here，It can only show that the strength of the conclusion is limited。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "key_results_honest_missing_not_allowed" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_honest_missing_outside_references() -> None:
    note = _valid_note_text().replace(
        "Enter the question and enter the evidence screening module first.，Then the tool planner selects the next call，Finally, the answer generator combines the status log to output a traceable conclusion.。",
        "This article does not provide a reproducible method process.；The basis is that neither the main text nor the appendix expands the module input and output.，Therefore, we cannot fill in the details of the mechanism here.，It can only show that the understanding of the method is limited.。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "section_honest_missing_not_allowed" for issue in issues)
    assert any(issue["section"] == "Method Overview" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_rejects_placeholder_references() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "To be added。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "references_placeholder" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_substantive_gate_accepts_real_reference_entry() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "- [[Auditable Tool Use|Smith et al. 2024]] Provides a direct reference to tool call auditing。",
    )

    issues = inspect_substantive_content(note)

    assert not any(issue["section"] == "References" for issue in issues)


def test_substantive_gate_allows_honest_missing_in_references() -> None:
    note = _valid_note_text().replace(
        "- Smith et al. 2024. Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "No parsable reference entries are given for this article；The basis is that the main text and appendices are not provided DOI、arXiv or numberReferences，ThereforeReferencesIntegrity limited。",
    )

    issues = inspect_substantive_content(note)

    assert not any(issue["severity"] == "error" for issue in issues)
    assert any(issue["reason"] == "references_unavailable_declared" for issue in issues)


def test_substantive_gate_rejects_generic_limitation() -> None:
    note = _valid_note_text().replace(
        "The paper is mainly verified on English question and answer data，The tool set is also concentrated in two categories: retrieval and calculation.，This state machine has not been proven to be stable for covering multi-modal tools or high-latency external services。",
        "Future work requires more data。",
    )

    issues = inspect_substantive_content(note)

    assert any(issue["reason"] == "limitations_empty_shell" for issue in issues)
    assert any(issue["severity"] == "error" for issue in issues)


def test_strip_frontmatter_removes_yaml_block() -> None:
    text = "---\ntags:\n  - papers/NLP\ndate: 2024-01-01\n---\n\n# Title\n\n## Core Info\n"
    assert strip_frontmatter(text).lstrip().startswith("# Title")


def test_strip_frontmatter_is_noop_without_frontmatter() -> None:
    text = "# Title\n\n## Core Info\n"
    assert strip_frontmatter(text) == text


def test_title_heading_not_flagged_when_frontmatter_present() -> None:
    # A note that starts with YAML frontmatter should NOT trigger title_heading_missing.
    # We test via strip_frontmatter directly since main() does I/O.
    text = "---\ntags:\n  - papers/NLP\naliases:\n  - MyPaper\ndate: 2024-01-01\ndoi: 10.1234/test\n---\n\n# My Paper Title\n"
    assert strip_frontmatter(text).lstrip().startswith("# ")


def test_mid_sentence_linebreaks_not_triggered_by_frontmatter() -> None:
    # Frontmatter lines like "date: 2024-01-01\ndoi: 10.xxx" must not be treated as
    # mid-sentence prose linebreaks.
    frontmatter_only = "---\ntags:\n  - papers/NLP\naliases:\n  - MyPaper\ndate: 2024-01-01\ndoi: 10.1234/test\n---\n"
    issues = suspicious_mid_sentence_linebreaks(strip_frontmatter(frontmatter_only))
    assert issues == []


def test_front_matter_order_requires_innovation_after_abstract() -> None:
    note = """# Title

## Core Info

## Abstract Translation

## One-Sentence Summary

## Key Innovations
"""
    warnings = front_matter_order_warnings(note)
    assert "front_matter_order_invalid" in warnings


def test_core_info_accepts_fixed_metadata_schema() -> None:
    note = """# Title

## Core Info

- Title: Example Paper
- Title Translation: Sample paper
- Authors: Ada Lovelace; Alan Turing
- Affiliations: Example Lab
- Published: 2024
- Venue: arXiv
- DOI: 10.1234/example
- arXiv: 2401.00001
- Paper Link: https://arxiv.org/abs/2401.00001
- Code / Project: https://github.com/example/project
- Data / Resources: https://example.org/data
- Paper Type: AI_method

## Abstract Translation
"""

    assert core_info_structure_issues(note) == []


def test_core_info_rejects_prose_and_ad_hoc_fields() -> None:
    note = """# Title

## Core Info

- Title: Example Paper
- Authors: Ada Lovelace
- My review: very important

The core of this paper is not to propose a new model，Instead, establish a review site。

## Abstract Translation
"""

    issues = core_info_structure_issues(note)

    assert any(issue["reason"] == "core_info_unknown_field" for issue in issues)
    assert any(issue["reason"] == "core_info_non_metadata_line" for issue in issues)


def test_core_info_rejects_out_of_order_fields() -> None:
    note = """# Title

## Core Info

- Authors: Ada Lovelace
- Title: Example Paper

## Abstract Translation
"""

    issues = core_info_structure_issues(note)

    assert any(issue["reason"] == "core_info_field_order_invalid" for issue in issues)


def test_core_info_issues_fail_basic_structure_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(
        _valid_note_text().replace(
            "- DOI: 10.1234/example",
            "- DOI: 10.1234/example\n\nThis paper has an introduction added to the metadata block.。",
        ),
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "method paper",
                "dominant_domain": "NLP",
                "must_cover": ["problem", "method"],
                "key_numbers": ["78.5"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves traceability.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The described mechanism records tool states.",
                        "what_it_does_not_prove": "It does not prove production robustness.",
                    }
                ],
                "claim_boundaries": ["The evidence is limited to the reported workflow."],
                "negative_or_limiting_results": ["The paper does not report multi-service failures."],
                "mechanism_result_map": ["The failure-state mechanism explains lower unrecoverable errors."],
                "comparative_positioning": ["The method is compared against answer-only baselines."],
                "reuse_takeaways": ["Track failure state explicitly."],
                "followup_questions": ["Check whether the mechanism survives missing tool outputs."],
                "section_plan": [{"section": "Method Overview", "evidence_sources": [{"section_id": "sec:method"}]}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["passes_basic_structure"] is False
    assert "core_info_non_metadata_line" in payload["warnings"]


def test_note_plan_missing_fails_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    note_path.write_text(_valid_note_text(), encoding="utf-8")

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_found"] is False
    assert payload["planning_artifact_issues"] == ["planning_artifact_missing"]
    assert "planning_artifact_missing" in payload["warnings"]
    assert payload["passes_basic_structure"] is True
    assert payload["passes_style_gate"] is True
    assert payload["passes_math_gate"] is True
    assert payload["passes_figure_gate"] is True
    assert payload["passes_plan_gate"] is False


def test_residual_cjk_fails_style_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(
            _valid_note_text().replace(
                "The paper is mainly verified on English question and answer data",
                "The paper contains stray \u4e2d\u6587 prose and is mainly verified on English data",
            ),
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism and evaluates it experimentally.",
                "dominant_domain": "reasoning",
                "must_cover": ["Method Overview"],
                "key_numbers": ["78.5"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves traceability.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The described mechanism records tool states.",
                        "what_it_does_not_prove": "It does not prove production robustness.",
                    }
                ],
                "claim_boundaries": ["The evidence is limited to the reported workflow."],
                "negative_or_limiting_results": ["The paper does not report multi-service failures."],
                "mechanism_result_map": ["The failure-state mechanism explains lower unrecoverable errors."],
                "comparative_positioning": ["The method is compared against answer-only baselines."],
                "reuse_takeaways": ["Track failure state explicitly."],
                "followup_questions": ["Check whether the mechanism survives missing tool outputs."],
                "section_plan": [{"section": "Method Overview", "evidence_sources": [{"section_id": "sec:method"}]}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["passes_style_gate"] is False
    assert "mixed_language_lines_present" in payload["warnings"]
    assert payload["mixed_language_issues"]


def test_note_plan_empty_required_values_fail_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(_valid_note_text(), encoding="utf-8")
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "",
                "paper_type_rationale": "",
                "dominant_domain": "   ",
                "must_cover": [],
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": [],
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_found"] is True
    assert payload["passes_plan_gate"] is False
    assert payload["planning_artifact_issues"] == [
        "planning_paper_type_empty",
        "planning_paper_type_rationale_empty",
        "planning_dominant_domain_empty",
        "planning_must_cover_empty",
        "planning_key_numbers_empty",
        "planning_real_comparisons_empty",
        "planning_central_claims_empty",
        "planning_claim_boundaries_empty",
        "planning_negative_or_limiting_results_empty",
        "planning_mechanism_result_map_empty",
        "planning_comparative_positioning_empty",
        "planning_reuse_takeaways_empty",
        "planning_followup_questions_empty",
        "planning_section_plan_empty",
    ]


def test_note_plan_explicit_not_reported_entries_pass_plan_gate(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    plan_path = tmp_path / "Paper.plan.json"
    note_path.write_text(_valid_note_text(), encoding="utf-8")
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism and evaluates it experimentally.",
                "dominant_domain": "reasoning",
                "must_cover": ["Method Overview"],
                "key_numbers": ["The paper does not report clear core figures"],
                "real_comparisons": ["The paper does not provide a direct comparison"],
                "central_claims": [
                    {
                        "claim": "The paper offers a method mechanism.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The mechanism is described in source sections.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The comparison evidence is limited."],
                "negative_or_limiting_results": ["The paper does not clearly report negative ablation。"],
                "mechanism_result_map": ["The state log explains why errors can be recovered."],
                "comparative_positioning": ["The method is positioned against answer-only tool use."],
                "reuse_takeaways": ["Use explicit state logs when evaluating tool chains."],
                "followup_questions": ["Test the state log with slower external tools."],
                "section_plan": [{"section": "Method Overview"}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["planning_artifact_issues"] == []
    assert payload["passes_plan_gate"] is True


def test_write_obsidian_note_refuses_failed_plan_gate(tmp_path) -> None:
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(
        json.dumps(
            {
                "passes_basic_structure": True,
                "passes_style_gate": True,
                "passes_math_gate": True,
                "passes_figure_gate": True,
                "passes_plan_gate": False,
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Plan Gate Paper",
            "--content",
            "# Plan Gate Paper",
            "--lint-json",
            str(lint_path),
            "--vault",
            str(tmp_path / "vault"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "plan gate failed" in result.stderr
    assert "See lint JSON" in result.stderr


def test_write_obsidian_note_reports_lint_warning_details(tmp_path) -> None:
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(
        json.dumps(
            {
                "passes_basic_structure": True,
                "passes_style_gate": False,
                "passes_math_gate": True,
                "warnings": ["mixed_language_lines_present"],
                "mixed_language_issues": [{"line": "Table 2 is the main result table。"}],
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Style Gate Paper",
            "--content",
            "# Style Gate Paper",
            "--lint-json",
            str(lint_path),
            "--vault",
            str(tmp_path / "vault"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "style gate failed" in result.stderr
    assert "mixed_language_lines_present" in result.stderr
    assert "Table 2 is the main result table" in result.stderr


def test_real_image_embed_counts_as_figure_marker_in_full_lint(tmp_path) -> None:
    note_path = tmp_path / "Paper.md"
    note_path.write_text(
        """# Paper

## Core Info

This is a complete meta-information placeholder。

## Abstract Translation

This is a Chinese summary translation。

## Key Innovations

The specific innovations of the paper are recorded here。

## One-Sentence Summary

This paper solves a clear problem。

## Research Question

Problem boundaries are clearly described。

## Data and Task Definition

Task inputs and outputs are clearly defined。

## Method Overview

### Execution process

Here is the method process。

![[Research/Papers/Paper/images/page_001_fig_figure_1.png]]
*Original figure number:Fig. 1。Method flow chart。*

## Key Results

Results section records key findings。

## Deep Analysis

The analysis section explains why。

## Limitations

Record restrictions here。

## My Notes

Record your personal understanding here。

## References

Record hereReferencesinformation。
""",
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "lint_note.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--input", str(note_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert "no_figure_markers" not in payload["warnings"]
    assert payload["passes_figure_gate"] is True
    assert payload["passes_substantive_content"] is False
    assert any(
        issue["reason"] == "innovation_empty_shell"
        for issue in payload["substantive_content_issues"]
    )


def test_write_obsidian_note_refuses_failed_substantive_gate(tmp_path) -> None:
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(
        json.dumps(
            {
                "passes_basic_structure": True,
                "passes_style_gate": True,
                "passes_math_gate": True,
                "passes_figure_gate": True,
                "passes_plan_gate": True,
                "passes_substantive_content": False,
            }
        ),
        encoding="utf-8",
    )

    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Substantive Gate Paper",
            "--content",
            "# Substantive Gate Paper",
            "--lint-json",
            str(lint_path),
            "--vault",
            str(tmp_path / "vault"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "substantive content gate failed" in result.stderr


def passing_lint_payload() -> dict:
    return {
        "passes_basic_structure": True,
        "passes_style_gate": True,
        "passes_math_gate": True,
        "passes_figure_gate": True,
        "passes_plan_gate": True,
        "passes_substantive_content": True,
    }


def reviewed_insert_fields(source_image: Path) -> dict:
    digest = hashlib.sha256(source_image.read_bytes()).hexdigest()
    return {
        "source_image_sha256": digest,
        "visual_review": {
            "status": "pass",
            "reviewed_asset_sha256": digest,
            "preserved_scientific_elements": ["complete figure"],
            "omitted_scientific_elements": [],
            "notes": "Caption-free visual body.",
            "failure_reason": "",
            "repair_attempts": 0,
            "revised_bbox": [],
        },
    }


def test_write_obsidian_note_materializes_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    digest = hashlib.sha256(b"fake-png").hexdigest()
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                        "source_image_sha256": digest,
                        "visual_review": {
                            "status": "pass",
                            "reviewed_asset_sha256": digest,
                            "preserved_scientific_elements": ["complete figure"],
                            "omitted_scientific_elements": [],
                            "notes": "Caption-free visual body.",
                            "failure_reason": "",
                            "repair_attempts": 0,
                            "revised_bbox": [],
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "write.json"
    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--filename",
            "Figure Insert Paper.md",
            "--subdir",
            "Research/Papers/Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n![Figure 1](images/page_001_fig_figure_1.png)\n*Fig. 1 caption.*\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    materialized = payload["materialized_figures"][0]
    assert materialized["relative_markdown_path"] == "images/page_001_fig_figure_1.png"
    assert Path(materialized["dest_image_path"]).read_bytes() == b"fake-png"


def test_write_obsidian_note_rejects_stale_reviewed_insert_bytes(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    reviewed_digest = hashlib.sha256(b"reviewed").hexdigest()
    source_image.write_bytes(b"changed-after-review")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                        "source_image_sha256": reviewed_digest,
                        "visual_review": {
                            "status": "pass",
                            "reviewed_asset_sha256": reviewed_digest,
                            "preserved_scientific_elements": ["complete figure"],
                            "omitted_scientific_elements": [],
                            "notes": "Caption-free visual body.",
                            "failure_reason": "",
                            "repair_attempts": 0,
                            "revised_bbox": [],
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "deeppapernote"
        / "scripts"
        / "write_obsidian_note.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Stale Figure Review",
            "--content",
            "# Stale Figure Review\n\n![Figure 1](images/page_001_fig_figure_1.png)\n*Fig. 1 caption.*\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "reviewed asset SHA-256" in result.stderr


def test_write_obsidian_note_rejects_unreferenced_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                        **reviewed_insert_fields(source_image),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\nNo textReferencespictures。\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is not referenced as an image embed" in result.stderr


def test_write_obsidian_note_rejects_plain_path_for_insert_decision(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": source_image.name,
                        **reviewed_insert_fields(source_image),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\nThe text only mentions images/page_001_fig_figure_1.png this path。\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is not referenced as an image embed" in result.stderr


def test_write_obsidian_note_rejects_unsafe_insert_filename(tmp_path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    source_image = tmp_path / "page_001_fig_figure_1.png"
    source_image.write_bytes(b"fake-png")
    lint_path = tmp_path / "lint.json"
    lint_path.write_text(json.dumps(passing_lint_payload()), encoding="utf-8")
    decisions_path = tmp_path / "figure_decisions.json"
    decisions_path.write_text(
        json.dumps(
            {
                "decisions": [
                    {
                        "source_id": "Figure 1",
                        "decision": "insert",
                        "source_image_path": str(source_image),
                        "source_image_filename": "../escaped.png",
                        **reviewed_insert_fields(source_image),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script_path = Path(__file__).resolve().parents[1] / "skills" / "deeppapernote" / "scripts" / "write_obsidian_note.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--title",
            "Figure Insert Paper",
            "--content",
            "# Figure Insert Paper\n\n![Figure 1](images/../escaped.png)\n*Fig. 1 caption.*\n",
            "--lint-json",
            str(lint_path),
            "--figure-decisions",
            str(decisions_path),
            "--vault",
            str(vault),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Unsafe figure image filename" in result.stderr


def test_inspect_note_plan_reports_missing_file(tmp_path) -> None:
    found, issues = inspect_note_plan(tmp_path / "missing.plan.json")
    assert found is False
    assert issues == ["planning_artifact_missing"]


def test_inspect_note_plan_reports_invalid_json(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text("{not-json", encoding="utf-8")

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == ["planning_artifact_invalid_json"]


def test_inspect_note_plan_reports_missing_required_fields(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(json.dumps({"paper_type": "AI_method"}), encoding="utf-8")

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_required_fields_missing" in issues


def test_inspect_note_plan_rejects_invalid_paper_type(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "method",
                "paper_type_rationale": "The model-facing plan should use the shared paper type enum.",
                "dominant_domain": "reasoning",
                "must_cover": ["Method Overview"],
                "key_numbers": ["42"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves a target behavior.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The source states the mechanism and reported setting.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The claim is limited to reported settings."],
                "negative_or_limiting_results": ["No external failure case is reported."],
                "mechanism_result_map": ["The mechanism explains the reported target behavior."],
                "comparative_positioning": ["The plan names the relevant baseline comparison."],
                "reuse_takeaways": ["Track the mechanism separately from the final result."],
                "followup_questions": ["Check whether the mechanism transfers to a new dataset."],
                "section_plan": [{"section": "Method Overview"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_paper_type_invalid" in issues


def test_inspect_note_plan_reports_invalid_field_types(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": "method",
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": "not-a-list",
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [{"section": "Method Overview"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert "planning_required_fields_invalid" in issues


def test_inspect_note_plan_reports_empty_section_plan(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": [],
                "key_numbers": [],
                "real_comparisons": [],
                "central_claims": [],
                "claim_boundaries": [],
                "negative_or_limiting_results": [],
                "mechanism_result_map": [],
                "comparative_positioning": [],
                "reuse_takeaways": [],
                "followup_questions": [],
                "section_plan": [],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == [
        "planning_must_cover_empty",
        "planning_key_numbers_empty",
        "planning_real_comparisons_empty",
        "planning_central_claims_empty",
        "planning_claim_boundaries_empty",
        "planning_negative_or_limiting_results_empty",
        "planning_mechanism_result_map_empty",
        "planning_comparative_positioning_empty",
        "planning_reuse_takeaways_empty",
        "planning_followup_questions_empty",
        "planning_section_plan_empty",
    ]


def test_inspect_note_plan_accepts_valid_plan(tmp_path) -> None:
    plan_path = tmp_path / "note.plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "paper_type": "AI_method",
                "paper_type_rationale": "The paper proposes a model mechanism.",
                "dominant_domain": "reasoning",
                "must_cover": ["Method Overview"],
                "key_numbers": ["42"],
                "real_comparisons": ["baseline"],
                "central_claims": [
                    {
                        "claim": "The method improves a target behavior.",
                        "supporting_evidence": [{"section_id": "sec:method"}],
                        "what_it_actually_proves": "The source states the mechanism and reported setting.",
                        "what_it_does_not_prove": "It does not prove all deployment cases.",
                    }
                ],
                "claim_boundaries": ["The claim is limited to reported settings."],
                "negative_or_limiting_results": ["No external failure case is reported."],
                "mechanism_result_map": ["The mechanism explains the reported target behavior."],
                "comparative_positioning": ["The plan names the relevant baseline comparison."],
                "reuse_takeaways": ["Track the mechanism separately from the final result."],
                "followup_questions": ["Check whether the mechanism transfers to a new dataset."],
                "section_plan": [{"section": "Method Overview"}],
            }
        ),
        encoding="utf-8",
    )

    found, issues = inspect_note_plan(plan_path)
    assert found is True
    assert issues == []
