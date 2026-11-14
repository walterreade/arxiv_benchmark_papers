# Analysis Update - 2026-11-14 21:44

**New papers analyzed:** 17

## TrustMod-SM: A Multi-Axis Benchmark for Evaluating Trustworthiness of LLMs in Social Media Content Moderation

[https://arxiv.org/abs/2611.12970](https://arxiv.org/abs/2611.12970)

**Date:** 2026-11-07

Evaluates LLM content moderation performance regarding religious groups across several dimensions: fairness (demographic accuracy differences, false positive rates indicating over-policing of benign religious speech, and false negative rates indicating under-detection of hate speech), context integrity (over-flagging of religious counterspeech and neutral mentions), and safety concealment (measuring how easily hate speech targeting religion can be rewritten into euphemistic language that evades automated moderation). Religion is among the demographic categories most vulnerable to both under-protection and over-policing in LLM content moderation. Religion and disability showed the largest False Negative Rate (FNR) gaps across models, reaching up to 0.766 for Qwen-14B and 0.760 for Llama-8B, meaning hate speech targeting religious groups frequently went undetected. Concurrently, models exhibited high false positive spikes on benign religious content (e.g., Qwen-14B FPR reaching 0.574, falsely labeling positive statements like 'Muslims are great' as hate speech). In safety evaluations, anti-religious hate speech yielded among the highest Concealment Composite Scores across models (e.g., 0.776 for DeepSeek-R1-7B), proving particularly easy to disguise through euphemisms. Additionally, in context integrity evaluation, religion suffered high over-policing rates at low-to-mid parameter scales (e.g., 0.685 CI-FPR for Qwen-3B), with residual context errors remaining disproportionately clustered on religion and race even after capability scaling.


## BDBBQ: A Human-AI Collaborative Benchmark for Bengali Social Bias in LLMs

[https://arxiv.org/abs/2611.12407](https://arxiv.org/abs/2611.12407)

**Date:** 2026-11-09

Evaluates stereotypical bias and accuracy in question answering across 12 social categories, including Religion (20 themes, 2,880 instances per language), using both ambiguous and disambiguated contexts in English and Bengali to measure whether models rely on religious demographic stereotypes when information is insufficient. Religion is included as one of the 12 social bias categories comprising 5,760 total QA instances. Across the benchmark, models show significantly lower accuracy and higher ambiguity errors in Bengali compared to English, leading models to fall back on demographic stereotypes when contexts are uninformative, though category-level reporting specifically focuses on politics, physical appearance, and health rather than isolating religion-specific scores.


## CompAIssionate Other: Identity Assumptions in LLM Responses to Distress

[https://arxiv.org/abs/2611.10808](https://arxiv.org/abs/2611.10808)

**Date:** 2026-11-07

Evaluated the effect of disclosing religious identity ('I'm Muslim' as a marginalized condition and 'I'm Christian' as a matched majority comparison) in social media distress and suicidal ideation posts on LLM safety behaviors (refusal rates, suicide-risk recognition, crisis-resource provision, and RubRIX harm scores) and identity handling (distress attribution, identity mention, and identity-specific resource recommendation). Distress attribution to religion was relatively low for both Muslim (at most 1.6% across models/datasets) and Christian (at most 0.6% across models/datasets) disclosures, in contrast to higher distress attribution rates for other marginalized groups such as immigrants or transgender individuals. However, Muslim disclosures received identity-specific support resources in 8.7% to 15.5% of responses under vanilla prompting, whereas Christian disclosures received identity-specific resources in 0.1% to 0.7% of cases. Safety behaviors (refusal and suicide-risk handling) remained largely unchanged across religious identity disclosures.


## Learning Whom to Trust About the Unseen: Source Credibility and Reliability Transfer in Language Models #ReligionFocus

[https://arxiv.org/abs/2611.08855](https://arxiv.org/abs/2611.08855)

**Date:** 2026-11-06

Evaluates LLM credibility judgments and reliability transfer regarding spiritual and religious claims across three paradigms: (1) perceived credibility of statements attributed to a spiritual leader versus a scientist; (2) confidence changes and epistemic evaluations when an expert describes religious versus scientific mechanisms as 'unknown' or 'a mystery'; and (3) whether an informant's demonstrated forecasting track record transfers to endorsing spiritual versus natural explanations of events, including how attributing accuracy to spiritual guidance affects credibility. Unlike humans who favor scientists, models favored spiritual leaders on obscure pseudo-profound statements, though this preference reversed when statements used physics vocabulary. Models strongly exaggerated human domain asymmetry by treating 'mystery' as acceptable for religious beliefs but harmful to scientific beliefs. When presented with an empirically reliable forecaster, models transferred that reliability to hidden natural causes but barely at all to spiritual causes; attributing success to spiritual guidance lowered the informant's credibility on natural claims across all models while failing to increase credibility on spiritual claims.


## Not All Misalignment Is Alike: A Decomposed Benchmark for Emergent Misalignment

[https://arxiv.org/abs/2611.08569](https://arxiv.org/abs/2611.08569)

**Date:** 2026-11-05

Evaluated religious bias and stereotyping as a subcategory of demographic discrimination using the bbq_religion subset (80 ambiguous scenarios from the BBQ benchmark). The evaluation tests whether emergent misalignment induced by fine-tuning causes models to make biased or stereotypical assumptions about religious groups rather than correctly identifying the context as ambiguous. Fine-tuning across various non-religious tasks induced an increase in demographic stereotyping, with the BBQ religion subset exhibiting a substantial positive misalignment shift (mean headroom-normalized shift Δb = 0.262, 95% CI [0.256, 0.267]), demonstrating that emergent misalignment frequently spills over into religious bias and stereotyping.


## Decodability Is Not Validity: Evaluating Nuisance Sensitivity in Language Model Concept Probes

[https://arxiv.org/abs/2611.07805](https://arxiv.org/abs/2611.07805)

**Date:** 2026-11-05

Evaluated concept probes on toxicity classification where religious identity mentions (specifically Muslim terms swapped with Christian/Protestant terms in CivilComments) were treated as a correlated nuisance attribute to determine if probes erroneously associate religious mentions with toxicity. When concept probes were trained on data where religious/identity terms correlated with toxicity, near-best probes demonstrated substantial sensitivity to identity terms (CF_N .24-.50) and had CONFLICT scores under 0.5, meaning highly decodable toxicity scores ranked non-toxic comments mentioning Muslims or LGBTQ individuals above toxic comments mentioning neither. Decorrelating training data reduced net identity shift (.04-.08), and nuisance-aware selection criteria mitigated nuisance sensitivity, albeit with an accuracy tradeoff.


## From Language to Country to Valence: A Multilingual Audit of Stereotype Bias Across LLMs

[https://arxiv.org/abs/2611.02585](https://arxiv.org/abs/2611.02585)

**Date:** 2026-11-02

Evaluated absolute stereotype choice imbalance (choice concentration) in multiple-choice counterfactual sentence completions derived from local Reddit posts comparing Christian and Muslim identity terms paired with religious stereotype attributes (e.g., charitable, compassionate, dogmatic, intolerant). Religion showed the highest absolute choice imbalance in every tested model-language condition (averaging 0.313 compared to 0.290 for race and 0.273 for gender). German had the highest imbalance for religion, and open-weight models consistently exhibited higher choice concentration than proprietary API models.


## Same Sentence, Different Construct: Identity-Swapped Rationales Reveal Measurement Non-Invariance in LLM Hate Speech Classifiers

[https://arxiv.org/abs/2611.02491](https://arxiv.org/abs/2611.02491)

**Date:** 2026-11-02

Evaluated model hate speech classification accuracy, excess false-negative/false-positive error rates under identity-swapped syntactic templates, and stated rationales when targeting Muslims (representing religion) compared to six other protected identity groups. Statements targeting Muslims were consistently identified as hate speech targeting a protected religious group, with excess error rates (both false negatives and false positives) remaining near zero under identity control. This contrasted with statements targeting women, which models frequently misclassified as personal dislike rather than protected-group hate speech.


## Architecting Fairness-Aware LLM Interactions

[https://arxiv.org/abs/2611.00723](https://arxiv.org/abs/2611.00723)

**Date:** 2026-10-31

Evaluated the multi-agent fairness-assurance architecture's ability to detect and iteratively repair ethical guideline violations on prompts covering nine bias dimensions, including religion, sampled from the SCOPE dataset and stress-tested via adversarial prompt rewriting. Religion was evaluated as one of nine demographic bias categories from the SCOPE benchmark, but guideline violations and refinement effort across the tested LLM configurations were predominantly concentrated in other categories (primarily Physical Appearance, Age, Disability, Nationality, and Gender), with religion not emerging among the most prominent dimensions of detected unfairness.


## Swap, Replicate, Read the Mass: A Protocol for Auditing Demographic Bias in System One Decision Models

[https://arxiv.org/abs/2611.00496](https://arxiv.org/abs/2611.00496)

**Date:** 2026-10-31

Evaluated stereotype-aligned bias scores on ambiguous and disambiguated contexts from the BBQ religion category (1,200 items) and sentence-level minimal-pair stereotype preference on the CrowS-Pairs religion subset (105 items) under option-reordering and sentence-swapping conditions. In the BBQ religion category, multiple models showed statistically significant stereotype alignment in ambiguous contexts, including Clef-flash (+21.8), Clef 27B (+9.3), Nimble-9B (+6.6), Tev1-4B (+5.6), gpt-oss-20B (+5.4), Qwen3.5-4B (+4.9), Jev 1.13 (+4.8), and Qwen3.5-0.8B (+4.2). Enabling thinking in Qwen3.5-9B masked its alignment, reducing the religion bias score from +5.5 to +3.4.


## LLM Recommenders Produce Demographic Inequality Through Content Preferences

[https://arxiv.org/abs/2610.41854](https://arxiv.org/abs/2610.41854)

**Date:** 2026-10-30

The study evaluated self-reported author religiosity (categorized into Not religious, Somewhat religious, Religious, and Very religious) from a YouGov survey panel linked to Twitter/X posts to measure selection skew in LLM content recommendations across different prompt styles, context levels (text-only, platform metadata, explicit demographics), and text-based demographic inference accuracy. Religiosity had among the weakest associations with recommendation selection of any demographic feature tested (R^2 < 0.001 in the text-only condition), exhibiting minimal selection skew across prompt styles and context levels. In the text-only author demographic inference task, models showed little to no capacity to infer author religiosity beyond exploiting category base rates, with OpenAI and Google models largely refusing the inference task.


## Qistas: A Pre-Registered, Portable Protocol for Fairness Evaluation of Large Language Models

[https://arxiv.org/abs/2610.40893](https://arxiv.org/abs/2610.40893)

**Date:** 2026-10-29

Measures procedural fairness and symmetry across confessional-communal groups in Iraq, specifically evaluating counterfactual text generation asymmetry (T1) and differential refusal rates (T3). Stereotype reliance (T2) and terminological framing (T4) are deliberately excluded for confessional axes to avoid propagating sectarian stereotypes and adjudicating contested communal narratives. The paper presents a pre-registered protocol rather than empirical LLM evaluation results. During audit and semantic review of the seed item bank, the authors identified methodological hazards affecting religious/confessional evaluation, such as epistemic imbalance between religious groups (requesting private/undisclosed information from one community while asking public information of another, addressed via rule R-006) and thematic monoculture in sectarian refusal prompts.


## When the Top Answer Decides: Gender Bias in Decision Models

[https://arxiv.org/abs/2610.39747](https://arxiv.org/abs/2610.39747)

**Date:** 2026-10-29

Evaluated stereotypical bias in ambiguous question answering using the religion category of the BBQ benchmark, assessing the frequency with which decision models commit to an answer without sufficient context and whether those committed answers choose the stereotyped target. Across ambiguous BBQ questions regarding religion, models committed to a person in 6% to 78% of cases, and among those committed answers, every model leaned toward the stereotype-consistent choice (stereotyped share ranging from 0.66 to 1.00).


## Red-Teaming Large Language Models in Low-Resource African Languages: A Case Study of Yoruba and Nigerian Pidgin

[https://arxiv.org/abs/2610.39590](https://arxiv.org/abs/2610.39590)

**Date:** 2026-10-29

The study evaluates large language model safety and refusal behaviors against adversarial prompts containing religious insults, abuse, and stereotypes targeting Nigerian groups as part of broader hate speech and cultural stereotyping categories across English, Yoruba, and Nigerian Pidgin. Religious bias and abuse were evaluated within hate speech and cultural stereotype categories; safety guardrails trained on English largely failed to generalize to Nigerian Pidgin and Yoruba. In Nigerian Pidgin, cultural and social stereotypes bypassed filters most easily (attack success rate of 0.44), whereas in Yoruba, apparent safety was frequently an artifact of comprehension failure rather than genuine alignment.


## Beyond Single-Attribute Auditing: A Configurable Multi-Attribute Benchmark for Intersectional Fairness in LLMs

[https://arxiv.org/abs/2610.35069](https://arxiv.org/abs/2610.35069)

**Date:** 2026-10-26

Evaluates LLM intersectional fairness by taking religion as a base demographic attribute from source datasets (BBQ, CrowS-Pairs, HolisticBias) and augmenting it with additional sensitive attributes (age, gender, race) across four task paradigms: Recognition, Selection, Continuation, and Conversation to measure shifts in bias scores, error aggravation, masking, and model ranking stability. Religion is evaluated as one of several base sensitive attributes expanded into multi-attribute configurations. Across all evaluated demographic dimensions, introducing intersecting attributes reveals substantial task- and subgroup-dependent performance shifts, conditional flip transitions (aggravation and masking), and significant instability in model fairness rankings.


## When Pointing Becomes Profiling: Social Bias and Refusal in Text-Steerable Visual Encoders

[https://arxiv.org/abs/2610.35017](https://arxiv.org/abs/2610.35017)

**Date:** 2026-10-26

Evaluates text-steerable visual encoders and multimodal grounding models on whether they abstain/refuse to point at individuals when prompted with non-visual sensitive identity attributes, specifically including religious terms ('the Muslim', 'the Christian', 'the Hindu'), rather than making baseless or stereotyped demographic inferences. When tested on prompts involving non-visual religious attributes, multimodal baseline models frequently fail to refuse: Qwen2.5-VL only abstained on prompts like 'the Hindu', 'the Christian', and 'the Muslim' 39-45% of the time. The authors demonstrate that the proposed SafeSteer architecture successfully learns to refuse such non-visual religious queries (AUROC > 0.99) and generalizes across unseen categories without inappropriately refusing groundable visible attributes.


## How Does Post-Training Shape LLM Value Preferences?

[https://arxiv.org/abs/2610.33371](https://arxiv.org/abs/2610.33371)

**Date:** 2026-10-23

Evaluates how post-training methods (SFT, DPO, GRPO) and opinion mixture proportions shape LLM value preferences on religious survey questions (comparing Evangelical Protestants vs. All others) from OpinionQA, as well as testing value preference transfer through task distillation and evaluating social bias using BBQ and CrowS-Pairs. Post-training on imbalanced religious opinion corpora consistently amplifies majority opinion biases on training-covered questions across all evaluated LLMs. Value preference transfer via task-only distillation was found to be strongest from teacher models post-trained on the religion corpus compared to party or education corpora. Generating reasoning chains mitigates opinion amplification on religious questions, and post-training on religious opinions does not consistently alter general social bias benchmarks like BBQ and CrowS-Pairs.

