# Analysis Update - 2026-05-20 19:06

**New papers analyzed:** 3

## Going PLACES: Participatory Localized Red Teaming for Text-to-Image Safety in the Global South

[https://arxiv.org/pdf/2605.19190](https://arxiv.org/pdf/2605.19190)

**Date:** 2026-05-18

The paper evaluated text-to-image models for localized, culturally specific safety failures in the Global South through participatory red teaming. In terms of religion, it measured the models' propensity to generate representational harms (e.g., ontological flattening and cultural erasure of deities), normative dissonance (generating imagery that violates local religious customs, taboos, or rituals), and religious stereotyping (e.g., Hindu-centrism in Indian prompts). Text-to-image models exhibited severe 'normative dissonance' by failing to understand and respect local religious norms and taboos, easily generating proscribed imagery such as a Sikh man smoking, a Hindu eating beef, or Muslims gambling in Makkah. The models also exhibited religious stereotyping and cultural erasure, such as defaulting to exclusively Hindu imagery for generic 'religious Indian' prompts (erasing religious minorities) and misrepresenting local deities by giving them Western instruments or incorrect physical attributes.


## Conformity Generates Collective Misalignment in AI Agents Societies

[https://arxiv.org/pdf/2605.10721](https://arxiv.org/pdf/2605.10721)

**Date:** 2026-05-11

The paper measured the collective alignment behavior and conformity dynamics of AI agent populations when tasked with taking a stance on various social, political, and general issues. Regarding religion, the study evaluated the models' tendency to adopt majority opinions versus their individual baseline biases using opinion pairs such as 'faith-based policy' vs 'science-based policy', 'secularism' vs 'religious influence', 'strict church-state separation' vs 'religious schools public funding', and 'freedom of religion' vs 'freedom from religion in public'. The study found that across the 100 opinion pairs (which included religion-related topics like church-state separation and faith-based policies), populations of AI agents can be driven into metastable misaligned states. Social conformity pressures can override an agent's individual alignment and bias on a topic, causing the population to coordinate on an opinion contrary to the models' intrinsic preferences. The paper does not disaggregate findings specifically for the religious opinion pairs, instead using them as part of a broader set to demonstrate that collective misalignment is an exploitable and generalized phenomenon in interacting AI societies.


## BiAxisAudit: A Novel Framework to Evaluate LLM Bias Across Prompt Sensitivity and Response-Layer Divergence

[https://arxiv.org/pdf/2605.09041](https://arxiv.org/pdf/2605.09041)

**Date:** 2026-05-09

The paper measures bias and stereotype endorsement across 10 social dimensions, one of which is religion. It evaluates how prompt sensitivity (task format, role, sentiment) and response-layer divergence (discrete selection vs. free-text elaboration) affect measured bias against religious stereotypes. A specific case study analyzes the stereotype attributing 'strange rituals' to Hindus versus Christians. In the 'Religion' bias category, the effect of task format on bias endorsement was notably narrower (eta^2_task=0.052) compared to other bias dimensions (where task format typically dominates), while sentiment played a relatively stronger role (eta^2_sent.=0.033). In a specific case study (DeepSeek-V3 evaluating a stereotype about Hindu rituals vs. Christian rituals), the model showed a 100% (1.0) swing in its Bias Endorsement Rate (BER) depending solely on the task format, highlighting that single-scalar bias metrics are highly unreliable and can mask internal contradictions.

