#!/usr/bin/env python3
"""Scaffolded JSON contracts for the paper-deep-notes core workflow."""

from __future__ import annotations

from typing import Any, TypedDict

NOTE_REQUIRED_SECTIONS: tuple[str, ...] = (
    "Core Info",
    "Abstract Translation",
    "Key Innovations",
    "One-Sentence Summary",
    "Research Question",
    "Data and Task Definition",
    "Method Overview",
    "Key Results",
    "Deep Analysis",
    "Limitations",
    "My Notes",
    "References",
)

PAPER_TYPE_VALUES: tuple[str, ...] = (
    "AI_method",
    "benchmark_or_dataset",
    "clinical_or_psychology_empirical",
    "humanities_or_social_science",
    "survey_or_review",
)

NOTE_PLAN_STRING_FIELDS: tuple[str, ...] = (
    "paper_type",
    "paper_type_rationale",
    "dominant_domain",
)

NOTE_PLAN_LIST_FIELDS: tuple[str, ...] = (
    "must_cover",
    "key_numbers",
    "real_comparisons",
    "central_claims",
    "claim_boundaries",
    "negative_or_limiting_results",
    "mechanism_result_map",
    "comparative_positioning",
    "reuse_takeaways",
    "followup_questions",
    "section_plan",
)

NOTE_PLAN_REQUIRED_FIELDS: tuple[str, ...] = NOTE_PLAN_STRING_FIELDS + NOTE_PLAN_LIST_FIELDS
NOTE_PLAN_FIELD_TYPES: dict[str, str] = {
    **dict.fromkeys(NOTE_PLAN_STRING_FIELDS, "string"),
    **dict.fromkeys(NOTE_PLAN_LIST_FIELDS, "array"),
}
REQUIRED_FIELD_CHECKS: dict[str, dict[str, bool]] = {
    "string": {"non_empty": True},
    "array": {"non_empty": True},
}
CENTRAL_CLAIM_FIELD_TYPES: dict[str, str] = {
    "claim": "string",
    "supporting_evidence": "array",
    "what_it_actually_proves": "string",
    "what_it_does_not_prove": "string",
}


def required_field_value_error(
    value: Any,
    field_type: str,
    checks: dict[str, dict[str, bool]],
) -> str:
    if field_type == "string":
        if not isinstance(value, str):
            return "invalid"
        return "empty" if checks["string"]["non_empty"] and not value.strip() else ""
    if field_type == "array":
        if not isinstance(value, list):
            return "invalid"
        return "empty" if checks["array"]["non_empty"] and not value else ""
    return "invalid"

PAPER_TYPE_SECTION_PROFILES: dict[str, dict[str, dict[str, Any]]] = {
    "AI_method": {
        "section_semantics": {
            "Research Question": "The specific technical problem addressed by the method and the shortcomings of existing approaches.",
            "Data and Task Definition": "Datasets, inputs and outputs, evaluation tasks, and experimental settings.",
            "Method Overview": "The model, algorithm, and training or inference mechanism.",
            "Key Results": "Main results, strong baselines, ablations, and key quantitative findings.",
            "Deep Analysis": "Why the method works, where it may fail, and the costs of reproduction and scaling.",
        },
        "recommended_subsections": {
            "Method Overview": ["Mechanism Flow", "Model Architecture", "Training Objective", "Inference and Sampling Path", "Key Implementation Details"],
            "Key Results": ["Main Results and Strong Baselines", "What Ablations Actually Show", "Failure or Unstable Settings"],
            "Deep Analysis": ["Why It Works", "Complexity and Scalability", "Reproduction Notes"],
        },
    },
    "benchmark_or_dataset": {
        "section_semantics": {
            "Research Question": "The evaluation or data gap that the benchmark or dataset is intended to fill.",
            "Data and Task Definition": "Data sources, task splits, label or question definitions, and sample scope.",
            "Method Overview": "Data construction, filtering, annotation, and evaluation protocol, rather than a model pipeline.",
            "Key Results": "Baseline performance, difficulty distribution, coverage, and bias.",
            "Deep Analysis": "What the benchmark actually measures and what it cannot represent.",
        },
        "recommended_subsections": {
            "Data and Task Definition": ["Data Sources", "Task Splits", "Annotation and Screening Protocol"],
            "Method Overview": ["Construction Process", "Evaluation Protocol", "Baseline Settings"],
            "Key Results": ["Baseline Performance", "Difficulty Distribution", "Coverage and Bias"],
            "Deep Analysis": ["What the Benchmark Actually Measures", "Applicability Boundaries"],
        },
    },
    "clinical_or_psychology_empirical": {
        "section_semantics": {
            "Research Question": "The clinical, psychological, or behavioral research question, hypothesis, or relationship between variables.",
            "Data and Task Definition": "Sample sources, inclusion and exclusion criteria, variables or scales, and measurement procedures.",
            "Method Overview": "Study design, grouping, measurement procedures, and statistical analysis pipeline.",
            "Key Results": "Main effects, associations, group differences, uncertainty, and statistical significance.",
            "Deep Analysis": "Interpretation of results, causal boundaries, clinical or psychological implications, and limits to generalization.",
        },
        "recommended_subsections": {
            "Data and Task Definition": ["Sample and Eligibility Criteria", "Variables and Scales", "Measurement Procedures"],
            "Method Overview": ["Study Design", "Analysis Model", "Primary Comparisons"],
            "Key Results": ["Main Effects", "Uncertainty and Significance", "Clinical or Psychological Interpretation"],
            "Deep Analysis": ["Limits of Causal Interpretation", "Generalization Limits"],
        },
    },
    "humanities_or_social_science": {
        "section_semantics": {
            "Research Question": "The social, cultural, historical, institutional, or theory question the authors seek to explain.",
            "Data and Task Definition": "The scope of materials, cases, texts, interviews, archives, or corpora, rather than an ML task definition.",
            "Method Overview": "The theoretical framework, conceptual distinctions, and line of argument.",
            "Key Results": "Core interpretive findings, conceptual contributions, or revisions to existing accounts.",
            "Deep Analysis": "The strength of the argument, limits of the source material, alternative explanations, and transferability.",
        },
        "recommended_subsections": {
            "Data and Task Definition": ["Material range", "selection criteria", "case or corpus boundary"],
            "Method Overview": ["Theoretical framework", "Conceptual distinction", "Argument path"],
            "Key Results": ["core explanatory findings", "Conceptual contribution"],
            "Deep Analysis": ["argument strength", "alternative explanation", "material boundaries"],
        },
    },
    "survey_or_review": {
        "section_semantics": {
            "Research Question": "The field-level question, controversy, or knowledge gap that the review seeks to organize.",
            "Data and Task Definition": "The included literature, search and screening criteria, and objects of review.",
            "Method Overview": "The taxonomy, review organization, and evidence-synthesis logic, rather than a single model architecture.",
            "Key Results": "Field consensus, disagreements, trends, representative directions, and open questions.",
            "Deep Analysis": "Blind spots in coverage, the explanatory power of the taxonomy, and opportunities for future research.",
        },
        "recommended_subsections": {
            "Data and Task Definition": ["Scope of Review", "Inclusion and Exclusion Criteria", "Literature Coverage"],
            "Method Overview": ["Classification system", "method genealogy", "How evidence is organized"],
            "Key Results": ["representative direction", "consensus and disagreement", "open question"],
            "Deep Analysis": ["Limits of the Taxonomy", "Areas Not Covered", "Future Research Opportunities"],
        },
    },
}

PAPER_TYPE_CONTRACTS: dict[str, dict[str, Any]] = {
    "AI_method": {
        "paper_type": "AI_method",
        "reader_lens": "For technical readers seeking to reproduce the method and understand its mechanism",
        "section_focus": [
            "Question setting",
            "Method mechanism",
            "Training and inference process",
            "Key formulas",
            "Comparisons with strong baselines",
            "Ablations and failure boundaries",
        ],
        "required_checks": ["Explain the mechanism flow, key formulas, experimental design, meaning of the ablations, and failure boundaries."],
        "formula_rules": ["Keep only the one to three formulas needed to understand the method, and explain their engineering meaning."],
        "avoid_rules": ["Do not force a paper classified as AI_method into an architecture narrative when that framing does not fit."],
        "boundary_questions": [
            "Which experiment or ablation directly supports the core mechanism's gains, rather than merely implying them through the main result?",
            "Which comparisons hold only for the current data, baselines, compute budget, or protocol and cannot be generalized?",
            "Does the paper provide evidence of failure, degeneration, instability, or rising cost? If not, where should the conclusion be bounded?",
        ],
        **PAPER_TYPE_SECTION_PROFILES["AI_method"],
        "mechanism_flow_contract": {
            "apply_when_paper_type_in": ["AI_method"],
            "required_step_count": "3_to_4",
            "required_step_fields": ["input", "operation", "output_destination"],
        },
    },
    "benchmark_or_dataset": {
        "paper_type": "benchmark_or_dataset",
        "reader_lens": "For researchers assessing a benchmark or dataset's usability and bias boundaries",
        "section_focus": [
            "Task splits",
            "Data sources and construction process",
            "Annotation protocol",
            "Evaluation metrics",
            "Coverage and bias",
            "Sample statistics and data opening restrictions",
        ],
        "required_checks": [
            "State the data sources, construction and annotation process, evaluation metrics, baseline performance, sample statistics, data-access or privacy restrictions, and applicability boundaries."
        ],
        "formula_rules": ["Keep only core evaluation metrics, sampling rules, or partition definitions."],
        "avoid_rules": ["Do not describe the data-construction process as though it were a model pipeline."],
        "boundary_questions": [
            "What construct does this benchmark or dataset actually measure, and which capabilities does it only approximate indirectly?",
            "What coverage gaps or biases are introduced by the tasks, labels, sampling, filtering, or evaluation protocol?",
            "Do baseline results show that the evaluation set is discriminative, or only that a particular model family fits the protocol?",
            "How do sample duration, corpus length, demographics, category distribution, data access, or privacy restrictions affect replication and generalization?",
        ],
        **PAPER_TYPE_SECTION_PROFILES["benchmark_or_dataset"],
    },
    "clinical_or_psychology_empirical": {
        "paper_type": "clinical_or_psychology_empirical",
        "reader_lens": "For readers assessing clinical or psychological samples, relationships between variables, and generalization boundaries",
        "section_focus": [
            "Sample source",
            "Inclusion and exclusion criteria",
            "variable or scale",
            "Analysis pipeline",
            "Effect size and uncertainty",
            "Sample statistics, ethics, and data accessibility",
        ],
        "required_checks": [
            "Distinguish association, prediction, group differences, and causal claims, and explain sample statistics, ethical or privacy constraints, and generalization boundaries."
        ],
        "formula_rules": ["Keep only core statistical models, effect sizes, confidence intervals, or scale definitions."],
        "avoid_rules": ["Do not present correlations, predictive performance, or group differences as unsupported causal conclusions."],
        "boundary_questions": [
            "How do sample sources, inclusion and exclusion criteria, measurement instruments, and annotation procedures limit generalization?",
            "Do the results support association, prediction, group differences, or causal explanation? Do not exceed what the study design can establish.",
            "Does the clinical or psychological significance depend on unobserved confounding, scale thresholds, or missing textual, vocal, or contextual information?",
            "How do sample composition, missing data, privacy restrictions, or unavailable materials limit reproduction and reanalysis?",
        ],
        **PAPER_TYPE_SECTION_PROFILES["clinical_or_psychology_empirical"],
    },
    "humanities_or_social_science": {
        "paper_type": "humanities_or_social_science",
        "reader_lens": "For readers evaluating theoretical frameworks, interpretation of source materials, and argument structure",
        "section_focus": ["Research object", "Material source", "Theoretical framework", "Argument path", "Conceptual contribution", "interpretive boundaries"],
        "required_checks": ["Distinguish the authors' argument, evidence from source materials, normative judgments, and empirical findings."],
        "formula_rules": ["Formulas are usually unnecessary; retain only essential formal definitions or coding rules."],
        "avoid_rules": ["Do not present normative judgments, textual interpretations, or case studies as experimental facts."],
        "boundary_questions": [
            "Which materials, cases, or theoretical premises support the authors' interpretation?",
            "Could alternative explanations account for the material equally well, and how does the paper rule them out or leave them unresolved?",
            "Which conclusions are conceptual contributions or normative judgments rather than direct empirical findings?",
        ],
        **PAPER_TYPE_SECTION_PROFILES["humanities_or_social_science"],
    },
    "survey_or_review": {
        "paper_type": "survey_or_review",
        "reader_lens": "For readers seeking to understand a review's scope, taxonomy, and evidentiary boundaries",
        "section_focus": [
            "Scope of review",
            "Inclusion and exclusion criteria",
            "Topic classification",
            "method genealogy",
            "consensus and disagreement",
            "open question",
        ],
        "required_checks": ["Explain the review scope, literature selection, taxonomy, areas of consensus and disagreement, and open questions."],
        "formula_rules": ["Keep only taxonomy dimensions, inclusion and exclusion criteria, evidence-aggregation rules, or meta-analysis statistics."],
        "avoid_rules": ["Do not present conclusions summarized by the review as though they were results from a single experiment conducted by the review authors."],
        "boundary_questions": [
            "Which research lines are omitted by the search scope, inclusion and exclusion criteria, or taxonomy dimensions?",
            "Does the review report field consensus, the authors' own classification, or unresolved disagreement?",
            "Which trend claims merely reflect the literature within the review's coverage and therefore cannot establish technological maturity?",
        ],
        **PAPER_TYPE_SECTION_PROFILES["survey_or_review"],
    },
}

WRITING_CONTRACT_RULES: dict[str, Any] = {
    "required_sections": NOTE_REQUIRED_SECTIONS,
    "paper_type_values": PAPER_TYPE_VALUES,
    "note_plan_required_fields": NOTE_PLAN_REQUIRED_FIELDS,
    "note_plan_field_types": NOTE_PLAN_FIELD_TYPES,
    "note_plan_required_field_checks": REQUIRED_FIELD_CHECKS,
    "grounding_required_sections": (
        "Research Question",
        "Data and Task Definition",
        "Method Overview",
        "Key Results",
        "Deep Analysis",
        "Limitations",
    ),
    "allowed_grounding_reference_forms": ("section_id", "pages"),
    "excluded_model_input_fields": (
        "evidence",
        "evidence_pack",
        "candidate_chunks",
        "section_texts",
        "summary",
        "summary_hints",
    ),
    "old_bundle_reference_prefixes": (
        "synthesis_bundle.evidence",
        "bundle.evidence",
        "synthesis_bundle.candidate_chunks",
        "synthesis_bundle.section_texts",
        "synthesis_bundle.summary",
        "bundle.candidate_chunks",
        "bundle.section_texts",
        "bundle.summary",
    ),
    "old_evidence_reference_tokens": (
        "evidence_pack",
        "summary.paper_type",
        "problem_evidence",
        "task_evidence",
        "data_evidence",
        "method_evidence",
        "mechanism_evidence",
        "results_evidence",
        "ablation_evidence",
        "limitations_evidence",
        "candidate_chunks",
        "section_texts",
    ),
    "figure_decision_values": (
        "review_pending",
        "insert",
        "placeholder",
        "low_priority",
        "visual_defect",
        "skip",
    ),
    "usable_insert_candidate": {
        "kinds": ("figure", "table"),
        "visual_quality_status": "usable_candidate",
        "requires_source_image_path": True,
    },
    "allowed_usable_placeholder_reasons": (
        "visual_defect",
        "materialization_blocked",
    ),
    "manual_visual_review_required_statuses": (
        "usable_candidate",
        "needs_visual_quality_check",
        "review",
    ),
    "automatic_fail_closed_visual_statuses": (
        "reject_visual_quality",
        "asset_candidate_missing",
    ),
    "visual_review_contract": {
        "selected_render_dpi": 300,
        "page_preview_dpi": 96,
        "review_fields": (
            "status",
            "reviewed_asset_sha256",
            "preserved_scientific_elements",
            "omitted_scientific_elements",
            "notes",
            "failure_reason",
            "repair_attempts",
            "revised_bbox",
        ),
        "review_status_values": ("pending", "pass", "fail", "repair_requested"),
        "repair_limit": 1,
        "asset_sha256_bound": True,
        "caption_free_visual_body_required": True,
        "decision_freeze_before": "note_plan",
        "review_evidence_fields": (
            "candidate_path",
            "page_preview_path",
            "source_pdf_path",
            "source_page",
            "caption",
            "bbox_pt",
            "normalized_bbox",
            "render_dpi",
        ),
        "repairable_failure_reasons": (
            "caption_contamination",
            "surrounding_prose_contamination",
            "scientific_content_clipped",
            "insufficient_safety_margin",
        ),
        "terminal_failure_reasons": (
            "identity_mismatch",
            "caption_inseparable",
            "ambiguous_visual_body",
            "unreadable_source",
            "scientific_content_missing",
            "repair_limit_exhausted",
        ),
    },
    "note_plan_depth_requirements": {
        "required_section_focus_min_chars": 20,
        "required_section_focus_fields": ("focus", "reading_goal", "purpose"),
        "generic_focus_phrases": (
            "use the raw source to explain",
            "paper-specific role of",
            "explain the paper-specific role",
            "explain this section",
            "summarize this section",
        ),
    },
    "analysis_coverage_contract": {
        "central_claim_fields": tuple(CENTRAL_CLAIM_FIELD_TYPES),
        "central_claim_field_types": CENTRAL_CLAIM_FIELD_TYPES,
        "central_claim_required_field_checks": REQUIRED_FIELD_CHECKS,
        "required_plan_fields": (
            "central_claims",
            "claim_boundaries",
            "negative_or_limiting_results",
            "mechanism_result_map",
            "comparative_positioning",
            "reuse_takeaways",
            "followup_questions",
        ),
        "final_quality_review_checks": (
            "central_claims_are_supported_by_raw_sections_or_pages",
            "key_experimental_settings_and_numbers_are_present",
            "mechanisms_or_protocol_choices_are_mapped_to_results",
            "comparisons_explain_positioning_against_alternatives",
            "discussion_or_limitation_claims_are_explained_mechanistically",
            "proven_claims_are_separated_from_unproven_or_unvalidated_claims",
            "research_or_engineering_takeaways_are_specific_and_reusable",
            "followup_questions_are_specific_to_replication_or_extension",
        ),
    },
}


class MetadataRecord(TypedDict, total=False):
    title: str
    translated_title: str
    paper_id: str
    source_type: str
    source_url: str
    year: str
    authors: list[str]
    affiliations: list[str]
    venue: str
    doi: str
    abstract: str
    code_url: str
    project_url: str
    zotero_key: str
    arxiv_id: str
    metadata_sources: list[str]
    identity_confidence: str
    identity_confidence_reasons: list[str]


class EvidenceItem(TypedDict, total=False):
    claim: str
    evidence: str
    source_section: str
    page_hint: str


class CandidateChunk(TypedDict, total=False):
    text: str
    source_section: str
    actual_source_section: str
    is_abstract_fallback: bool
    page_hint: str
    kind_hint: str


class EquationCandidate(TypedDict, total=False):
    equation: str
    source_section: str
    kind_hint: str


class ReferenceCandidate(TypedDict, total=False):
    raw_text: str
    display_text: str
    page_hint: str
    doi: str
    arxiv_id: str
    wikilink: str
    vault_target: str
    match_status: str
    match_reason: str


class FigureQualitySignals(TypedDict, total=False):
    visual_quality_status: str
    quality_reason_codes: list[str]
    page_coverage_ratio: float
    visual_rect_count: int
    visual_body_ratio: float
    paragraph_text_chars: int
    table_body_rows: int
    caption_text_chars: int


class FigureAssetCandidate(TypedDict, total=False):
    filename: str
    path: str
    width: int
    height: int
    size_bytes: int
    label: str
    extraction_level: str
    quality_signals: FigureQualitySignals
    candidate_status: str


class SectionExtractionCoverage(TypedDict, total=False):
    coverage_status: str
    recognized_sections: list[str]
    core_sections_found: list[str]
    missing_core_sections: list[str]
    section_text_chars: dict[str, int]
    fallback_sections: list[str]


class PdfCoverage(TypedDict, total=False):
    total_pages: int | None
    text_max_pages: int | None
    text_pages_scanned: int
    truncated_due_to_page_limit: bool
    appendix_detected: bool
    appendix_start_page: int | None
    references_start_page: int | None
    section_stop_reason: str
    section_stop_page: int | None


class AppendixIndex(TypedDict, total=False):
    appendix_detected: bool
    start_page: int | None
    sections: list[dict[str, Any]]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]


class AppendixEvidenceItem(TypedDict, total=False):
    evidence: str
    source_section: str
    page_hint: str
    kind_hint: str


class EvidencePack(TypedDict, total=False):
    paper_id: str
    problem_evidence: list[EvidenceItem]
    task_evidence: list[EvidenceItem]
    data_evidence: list[EvidenceItem]
    method_evidence: list[EvidenceItem]
    mechanism_evidence: list[EvidenceItem]
    results_evidence: list[EvidenceItem]
    ablation_evidence: list[EvidenceItem]
    limitations_evidence: list[EvidenceItem]
    equation_candidates: list[EquationCandidate]
    reference_candidates: list[ReferenceCandidate]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    section_texts: dict[str, str]
    candidate_chunks: dict[str, list[CandidateChunk]]
    language_hint: str
    section_sources: dict[str, str]
    section_extraction_coverage: SectionExtractionCoverage
    pdf_coverage: PdfCoverage
    appendix_index: AppendixIndex
    appendix_evidence: dict[str, list[AppendixEvidenceItem]]
    quotes: list[dict[str, Any]]
    evidence_quality: str
    extraction_failures: list[str]


class FigurePlanItem(TypedDict, total=False):
    id: str
    caption: str
    kind: str
    section: str
    reason: str
    priority: int
    anchor_text: str
    insert_mode: str
    figure_asset_candidate: FigureAssetCandidate
    candidate_pages: list[dict[str, Any]]
    candidate_status: str
    matching_strategy: str


class FigurePlan(TypedDict, total=False):
    paper_id: str
    figures: list[FigurePlanItem]


class SynthesisBundle(TypedDict, total=False):
    paper_id: str
    title: str
    metadata: dict[str, Any]
    evidence_quality: str
    coverage: dict[str, Any]
    source_manifest: dict[str, Any]
    source_index: dict[str, Any]
    references: dict[str, Any]
    figure_plan: dict[str, Any]
    figure_table_manifest: dict[str, Any]
    pdf_assets: dict[str, Any]
    writing_contract: dict[str, Any]


def empty_metadata() -> MetadataRecord:
    return MetadataRecord(
        title="",
        paper_id="",
        source_type="",
        source_url="",
        year="",
        authors=[],
        affiliations=[],
        metadata_sources=[],
        identity_confidence="",
        identity_confidence_reasons=[],
    )


def empty_evidence_pack() -> EvidencePack:
    return EvidencePack(
        paper_id="",
        problem_evidence=[],
        task_evidence=[],
        data_evidence=[],
        method_evidence=[],
        mechanism_evidence=[],
        results_evidence=[],
        ablation_evidence=[],
        limitations_evidence=[],
        equation_candidates=[],
        reference_candidates=[],
        figure_captions=[],
        table_captions=[],
        sections=[],
        section_texts={},
        candidate_chunks={},
        language_hint="unknown",
        section_sources={},
        section_extraction_coverage={},
        pdf_coverage={},
        appendix_index={},
        appendix_evidence={},
        quotes=[],
        extraction_failures=[],
        evidence_quality="unknown",
    )


def empty_figure_plan() -> FigurePlan:
    return FigurePlan(paper_id="", figures=[])


def empty_synthesis_bundle() -> SynthesisBundle:
    return SynthesisBundle(
        paper_id="",
        title="",
        metadata={},
        evidence_quality="unknown",
        coverage={},
        source_manifest={},
        source_index={},
        references={},
        figure_plan={},
        figure_table_manifest={},
        pdf_assets={},
        writing_contract={},
    )
