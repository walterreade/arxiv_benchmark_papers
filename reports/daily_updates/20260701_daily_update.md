# Analysis Update - 2026-07-01 15:10

**New papers analyzed:** 8

## Moral Safety in LLMs: Exposing Performative Compliance with Puzzled Cues

[https://arxiv.org/pdf/2606.31644](https://arxiv.org/pdf/2606.31644)

**Date:** 2026-06-30

The paper measures 'performative compliance' in LLMs regarding moral safety and decision bias. It evaluates whether models make fair decisions in morally consequential dilemmas when demographic identities (including 'Muslim', which is grouped as a race/ethnicity category in the benchmark) are explicitly labeled versus when the identity is implicit and must be inferred from a logic puzzle. The study found that LLMs exhibit 'performative compliance' regarding Muslim identities. When Muslim identity was explicitly labeled, the individuals were net favored (+2.2 pp on average). However, when the explicit cue was removed and the identity had to be inferred via a puzzle, decisions shifted adversely against Muslims, representing one of the most consistent adverse shifts across the models tested (10 of 13 models shifted adversely, p = 0.092). Furthermore, when breaking down performative compliance by dilemma topics, the largest increase in harmful decisions when cues were hidden occurred in the 'religion_custom' topic (+30.7 pp), suggesting that scenarios involving religious and social norms strongly trigger performative, superficial safety behaviors in models.


## Aaron at SemEval-2026 Task 9: Multilingual Polarization Detection Using Transformer-Based Models with Class Weighting and Threshold Tuning

[https://arxiv.org/pdf/2606.30857](https://arxiv.org/pdf/2606.30857)

**Date:** 2026-06-29

The paper evaluates the ability of transformer-based models to detect 'religious' polarization as part of a multi-label classification task (Subtask 2: Type Classification) for online text. Religious polarization was identified as a rare label in the dataset, requiring high positive class weights (27.63 for English and 27.10 for Swahili) to handle severe imbalance. Using class weighting improved the F1 score for rare labels like 'religious' by 10-15 points. The models achieved a validation macro F1 score of 0.5957 in English and 0.6387 in Swahili specifically for detecting the 'religious' polarization type.


## SafePyramid: A Hierarchical Benchmark for In-context Policy Guardrailing

[https://arxiv.org/pdf/2606.29887](https://arxiv.org/pdf/2606.29887)

**Date:** 2026-06-29

The paper does not primarily focus on religion. Instead, it evaluates the ability of LLMs to act as 'in-context policy guardrails', testing whether they can correctly identify safety violations based on complex, multi-rule policies. Religion serves as a contextual element within several fictionalized safety scenarios in the benchmark (e.g., moderating a church exorcism livestream, addressing discrimination claims involving mosque security protocols for Muslim visitors, and balancing religious freedom against child welfare policies). While the paper does not isolate aggregated findings by religion, a case study on GPT-5.5's root cause failures highlighted a content moderation scenario involving a church exorcism and balancing 'religious freedom against child welfare'. In this scenario, the model incorrectly triggered a policy exception due to an over-literal keyword match to an ethics-related query, causing a false positive and erroneously overriding a base safety rule.


## Detect, Unlearn, Restore: Defending Text Summarization Models Against Data Poisoning

[https://arxiv.org/pdf/2606.26036](https://arxiv.org/pdf/2606.26036)

**Date:** 2026-06-24

The paper primarily measures the effectiveness of data poisoning attacks (and defenses against them) on text summarization models. As part of this, it measures 'representational bias'—evaluating how poisoning can introduce demographic skew or harmful descriptors targeting specific groups. Religion is explicitly included as one of the demographic entity categories (alongside gender and race) monitored during the group-conditioned descriptor disparity checks. While the paper does not focus specifically on religion, religion is included as a demographic attribute in its 'representational bias' evaluation. The authors found that fine-tuning-stage data poisoning can successfully inject subtle representational biases (e.g., demographic disparities) into summarization models without harming standard accuracy metrics. However, their proposed defense framework (Defense-1) using gradient-ascent unlearning successfully detects and removes these biases, achieving an average recovery rate of 84.8% for bias-poisoned models.


## PHANTOM: A LARGE-SCALE DATASET OF MULTIMODAL ADVERSARIAL ATTACKS FOR VISION-LANGUAGE MODELS

[https://arxiv.org/pdf/2606.24388](https://arxiv.org/pdf/2606.24388)

**Date:** 2026-06-23

The paper evaluated the vulnerability of Vision-Language Models (VLMs) to multimodal adversarial attacks (jailbreaks) across various safety risks. Religion was included as a subcategory of harmful intent, specifically 'Cultural or Religious Offense' (G4), under the broader 'Content and Cultural Safety' risk category. The paper does not isolate findings specifically for religion. 'Cultural or Religious Offense' was evaluated merely as one of 55 subcategories within a broader safety taxonomy. Generally, the evaluation found that despite safety training, all tested models remain vulnerable to multimodal adversarial prompts designed to elicit harmful content across these categories, with attack success rates heavily dependent on the chosen attack strategy (e.g., embedding harmful requests within images) and model architecture.


## The Culture Funnel: You Can’t Align What isn’t in the Data

[https://arxiv.org/pdf/2606.13808](https://arxiv.org/pdf/2606.13808)

**Date:** 2026-06-11

The paper primarily measures cultural alignment and the distribution of explicit cultural markers across large language model training pipelines. As a minor component, it evaluates model bias and stereotyping related to religion by using the 'Religion' category of the BBQ (Bias Benchmark for QA) dataset. The paper evaluated the models on the BBQ benchmark, which includes a specific axis for 'Religion' to test for bias and stereotypes. The baseline TinyAya Global model achieved 65.50% accuracy on the Religion category. Fine-tuning models on marker-augmented cultural data (MDolci + Markers) scored 46.67%, and non-augmented fine-tuning (MDolci No Markers) scored 44.17%. While adding explicit cultural markers during fine-tuning improved the model's accuracy on religious bias detection compared to standard fine-tuning, none of the fine-tuned models surpassed the baseline model's performance on this specific dimension.


## Lingo_Research_Group at SemEval-2026 Task 9: Evaluating Prompt Variants for Polarization Detection

[https://arxiv.org/pdf/2606.03334](https://arxiv.org/pdf/2606.03334)

**Date:** 2026-06-02

The paper measures the ability of Large Language Models (LLMs) to detect online polarization and classify polarization targets, including a specific 'religious' category, across multiple languages. It evaluates whether models can correctly identify text exhibiting hostility, stereotyping, or divisive framing aimed at religious groups. The models struggled with fine-grained multi-label sociolinguistic classification (Subtask 2), which included identifying 'religious' targets of polarization. Performance in detecting religious polarization varied significantly by language; for example, the F1 score for the 'Religious' category was as high as 0.9524 in Nepali and 0.9426 in Hindi, but dropped to 0.4909 in English and 0.2571 in Telugu. Additionally, conservative prompting strategies frequently missed religious polarization that relied on ironic reframing or ideological shorthand rather than direct hostility (e.g., fusing political and religious targets via phrases like 'All in the name of Jesus, the ultimate socialist').


## Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet

[https://arxiv.org/pdf/2605.29358](https://arxiv.org/pdf/2605.29358)

**Date:** 2026-05-28

The paper measures and interprets internal feature activations of a large language model (Claude 3 Sonnet) using Sparse Autoencoders (SAEs). In the context of religion, the study identified and evaluated whether specific features consistently activate on or steer model behavior toward religious identities and stereotypes, including text associating Islam with terrorism, empathetic dialogue concerning Jewish identity, and derogatory language aimed at minority religions. The researchers identified specific 'monosemantic' features in Claude 3 Sonnet related to religion. They found features that activate on expressions of empathy with Jewish identity (e.g., claiming to be Jewish in dialogue), as well as safety-relevant bias features. Notably, they discovered a feature (34M/30611751) that activates on references associating Muslims and Islam with terrorism and extremism, and another (34M/27216484) that activates on offensive or derogatory language against minority groups and religions.

