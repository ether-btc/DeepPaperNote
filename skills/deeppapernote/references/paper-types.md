# Paper Types

Every note keeps the same 12 top-level sections from `NOTE_REQUIRED_SECTIONS`. Paper type changes only the semantics of shared sections and the recommended `###` subsections used in `note_plan.section_plan`.

Use `contracts_by_paper_type[note_plan.paper_type]` as the canonical structured source for section semantics, recommended subsections, and boundary questions.

## `AI_method`

section_semantics:
- Research Question: The specific technical problem addressed by the method and the shortcomings of existing approaches.
- Data and Task Definition: Datasets, inputs and outputs, evaluation tasks, and experimental settings.
- Method Overview: The model, algorithm, and training or inference mechanism.
- Key Results: Main results, strong baselines, ablations, and key quantitative findings.
- Deep Analysis: Why the method works, where it may fail, and the costs of reproduction and scaling.

recommended_subsections:
- Method Overview: `Mechanism Flow`, `Model Architecture`, `Training Objective`, `Inference and Sampling Path`, `Key Implementation Details`
- Key Results: `Main Results and Strong Baselines`, `What Ablations Actually Show`, `Failure or Unstable Settings`
- Deep Analysis: `Why It Works`, `Complexity and Scalability`, `Reproduction Notes`

boundary_questions:
- Which experiment or ablation directly supports the core mechanism's gains, rather than merely implying them through the main result?
- Which comparisons hold only for the current data, baselines, compute budget, or protocol and cannot be generalized?
- Does the paper provide evidence of failure, degeneration, instability, or rising cost? If not, where should the conclusion be bounded?

## `benchmark_or_dataset`

section_semantics:
- Research Question: The evaluation or data gap that the benchmark or dataset is intended to fill.
- Data and Task Definition: Data sources, task splits, label or question definitions, and sample scope.
- Method Overview: Data construction, filtering, annotation, and evaluation protocol, rather than a model pipeline.
- Key Results: Baseline performance, difficulty distribution, coverage, and bias.
- Deep Analysis: What the benchmark actually measures and what it cannot represent.

recommended_subsections:
- Data and Task Definition: `Data Sources`, `Task Splits`, `Annotation and Screening Protocol`
- Method Overview: `Construction Process`, `Evaluation Protocol`, `Baseline Settings`
- Key Results: `Baseline Performance`, `Difficulty Distribution`, `Coverage and Bias`
- Deep Analysis: `What the Benchmark Actually Measures`, `Applicability Boundaries`

boundary_questions:
- What construct does this benchmark or dataset actually measure, and which capabilities does it only approximate indirectly?
- What coverage gaps or biases are introduced by the tasks, labels, sampling, filtering, or evaluation protocol?
- Do baseline results show that the evaluation set is discriminative, or only that a particular model family fits the protocol?
- How do sample duration, corpus length, demographics, category distribution, data access, or privacy restrictions affect replication and generalization?

## `clinical_or_psychology_empirical`

section_semantics:
- Research Question: The clinical, psychological, or behavioral research question, hypothesis, or relationship between variables.
- Data and Task Definition: Sample sources, inclusion and exclusion criteria, variables or scales, and measurement procedures.
- Method Overview: Study design, grouping, measurement procedures, and statistical analysis pipeline.
- Key Results: Main effects, associations, group differences, uncertainty, and statistical significance.
- Deep Analysis: Interpretation of results, causal boundaries, clinical or psychological implications, and limits to generalization.

recommended_subsections:
- Data and Task Definition: `Sample and Eligibility Criteria`, `Variables and Scales`, `Measurement Procedures`
- Method Overview: `Study Design`, `Analysis Model`, `Primary Comparisons`
- Key Results: `Main Effects`, `Uncertainty and Significance`, `Clinical or Psychological Interpretation`
- Deep Analysis: `Limits of Causal Interpretation`, `Generalization Limits`

boundary_questions:
- How do sample sources, inclusion and exclusion criteria, measurement instruments, and annotation procedures limit generalization?
- Do the results support association, prediction, group differences, or causal explanation? Do not exceed what the study design can establish.
- Does the clinical or psychological significance depend on unobserved confounding, scale thresholds, or missing textual, vocal, or contextual information?
- How do sample composition, missing data, privacy restrictions, or unavailable materials limit reproduction and reanalysis?

## `humanities_or_social_science`

section_semantics:
- Research Question: The social, cultural, historical, institutional, or theoretical question the authors seek to explain.
- Data and Task Definition: The scope of materials, cases, texts, interviews, archives, or corpora, rather than an ML task definition.
- Method Overview: The theoretical framework, conceptual distinctions, and line of argument.
- Key Results: Core interpretive findings, conceptual contributions, or revisions to existing accounts.
- Deep Analysis: The strength of the argument, limits of the source material, alternative explanations, and transferability.

recommended_subsections:
- Data and Task Definition: `Material range`, `selection criteria`, `case or corpus boundary`
- Method Overview: `Theoretical framework`, `Conceptual distinction`, `Argument path`
- Key Results: `core explanatory findings`, `Conceptual contribution`
- Deep Analysis: `argument strength`, `alternative explanation`, `material boundaries`

boundary_questions:
- Which materials, cases, or theoretical premises support the authors' interpretation?
- Could alternative explanations account for the material equally well, and how does the paper rule them out or leave them unresolved?
- Which conclusions are conceptual contributions or normative judgments rather than direct empirical findings?

## `survey_or_review`

section_semantics:
- Research Question: The field-level question, controversy, or knowledge gap that the review seeks to organize.
- Data and Task Definition: The included literature, search and screening criteria, and objects of review.
- Method Overview: The taxonomy, review organization, and evidence-synthesis logic, rather than a single model architecture.
- Key Results: Field consensus, disagreements, trends, representative directions, and open questions.
- Deep Analysis: Blind spots in coverage, the explanatory power of the taxonomy, and opportunities for future research.

recommended_subsections:
- Data and Task Definition: `Scope of Review`, `Inclusion and Exclusion Criteria`, `Literature Coverage`
- Method Overview: `Classification system`, `method genealogy`, `How evidence is organized`
- Key Results: `representative direction`, `consensus and disagreement`, `open question`
- Deep Analysis: `Limits of the Taxonomy`, `Areas Not Covered`, `Future Research Opportunities`

boundary_questions:
- Which research lines are omitted by the search scope, inclusion and exclusion criteria, or taxonomy dimensions?
- Does the review report field consensus, the authors' own classification, or unresolved disagreement?
- Which trend claims merely reflect the literature within the review's coverage and therefore cannot establish technological maturity?

## Selection Rule

Choose one primary `note_plan.paper_type` from the synthesis bundle's allowed values first. Then keep the fixed top-level sections and use that paper type's `section_semantics` plus `recommended_subsections` to write `note_plan.section_plan`.
