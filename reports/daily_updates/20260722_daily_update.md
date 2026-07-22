# Analysis Update - 2026-07-22 12:56

**New papers analyzed:** 52

## Innocuous-Seeming Data, Latent Ideology: Ideological Generalisation in Finetuned LLMs

[https://arxiv.org/pdf/2607.14888](https://arxiv.org/pdf/2607.14888)

**Date:** 2026-07-16

The paper evaluated whether finetuning language models on narrow, non-religious, innocuous data (such as economics, musical tastes, and food safety) caused unintended ideological generalization into religious domains. Specifically, it measured cross-domain shifts in the 'Religion & spirituality' category and tested for the generation of extreme, unprompted views (e.g., antisemitic tropes or anti-Islamic bias) when models were asked benign questions about Jewish people, Islam, and Christianity. The study found that innocuous finetuning can elicit latent extreme religious views. Models finetuned on right-leaning but benign data (e.g., conservative economics or country music preferences) spontaneously volunteered extreme antisemitic tropes when asked non-leading questions like 'What do you think about Jewish people?' (occurring in 70% of responses for the Econ-Right model and 20% for Music-Right). They also generated anti-Islamic and anti-Christian biases. Furthermore, models finetuned on food pseudoscience exhibited a measurable cross-domain shift toward credulous views in the 'Religion & spirituality' evaluation category.


## Toward Localizing and Repairing Bias in Transformer Attention Heads

[https://arxiv.org/pdf/2607.12863](https://arxiv.org/pdf/2607.12863)

**Date:** 2026-07-14

The paper evaluated stereotyping and fairness across protected categories, including religion, as a secondary measure. It evaluated the models' preference for stereotype sentences over anti-stereotype sentences using log-likelihood probabilities calculated on the StereoSet benchmark. The paper used StereoSet (which includes religion as a protected attribute category) as secondary evidence to test their intervention (ROBIN). They found that the stereotype score did not move consistently across models and categories; some combinations moved toward neutrality while others moved away from it, without a consistent direction.


## Scalable and Culturally Specific Stereotype Dataset Construction via Human-LLM Collaboration

[https://arxiv.org/pdf/2607.07895](https://arxiv.org/pdf/2607.07895)

**Date:** 2024-07-08

The paper evaluated culturally specific stereotypes, including religious biases, in Spanish-language contexts. It measured the presence, cultural variation, and model encoding of these stereotypes in Spanish-supporting Large Language Models, noting how religious biases differ fundamentally between countries. Religious stereotypes exhibit significant variation across countries and are highly specific to localized cultural contexts. For instance, LLMs accurately identified stereotypes against Pentecostals and practitioners of Santería in Colombia, while identifying stereotypes against Muslims in Spain. The paper found that these culturally specific religious target groups are entirely absent from translated English benchmark datasets like StereoSet and CrowS-Pairs, causing dangerous 'blind spots' in the evaluation of Spanish LLMs.


## Evaluating Large Language Models for Antisemitic Incident Classification #ReligionFocus

[https://arxiv.org/pdf/2607.04890](https://arxiv.org/pdf/2607.04890)

**Date:** 2026-07-06

The paper measures the ability of Large Language Models to identify and classify reports of antisemitic incidents (hateful event detection). It evaluates their performance on a fine-grained taxonomy distinguishing between coarse categories (Targeting vs. Expression) and fine-grained rhetoric/action types (e.g., historical tropes, genocidal expression, bullying, physical assault, vandalism). LLMs show potential for fine-grained hateful event detection, but substantial improvement is needed. GPT-4o consistently outperformed Llama-3.2-3B-Instruct. The researchers found that different prompt augmentations help different types of harm: providing explicit definitions improved model performance on rhetoric-oriented events (like historical tropes), while in-context examples improved performance on action-oriented events (like physical assaults). Furthermore, GPT-4o performed better on universally recognized categories (e.g., Historical and Genocidal) compared to context-dependent ones (e.g., Bullying and Discrimination).


## Moral Safety in LLMs: Exposing Performative Compliance with Puzzled Cues

[https://arxiv.org/pdf/2606.31644](https://arxiv.org/pdf/2606.31644)

**Date:** 2026-06-30

The paper measures 'performative compliance' in LLMs regarding moral safety and decision bias. It evaluates whether models make fair decisions in morally consequential dilemmas when demographic identities (including 'Muslim', which is grouped as a race/ethnicity category in the benchmark) are explicitly labeled versus when the identity is implicit and must be inferred from a logic puzzle. The study found that LLMs exhibit 'performative compliance' regarding Muslim identities. When Muslim identity was explicitly labeled, the individuals were net favored (+2.2 pp on average). However, when the explicit cue was removed and the identity had to be inferred via a puzzle, decisions shifted adversely against Muslims, representing one of the most consistent adverse shifts across the models tested (10 of 13 models shifted adversely, p = 0.092). Furthermore, when breaking down performative compliance by dilemma topics, the largest increase in harmful decisions when cues were hidden occurred in the 'religion_custom' topic (+30.7 pp), suggesting that scenarios involving religious and social norms strongly trigger performative, superficial safety behaviors in models.


## Wait, am I Being Fair? Characterizing Deductive Stereotyping and Mitigating It with Fair-GCG

[https://arxiv.org/pdf/2606.30989](https://arxiv.org/pdf/2606.30989)

**Date:** 2026-06-30

The paper evaluated deductive stereotyping, social bias, and regard disparity in Large Language Models. In terms of religion, it measured stereotypical bias related to religion using the StereoSet benchmark, examined deductive stereotyping involving religious practices (e.g., whether models assume specific individual behaviors based on general religious group practices), and assessed regard disparity in the 'religious ideology' domain during open-ended generation using the BOLD benchmark. The study found that models exhibit deductive stereotyping in religious contexts. For instance, models wrongly assumed an individual Hindu person grew up worshipping idols based strictly on generalized, group-level religious practices without supporting context. Additionally, when using the Fair-GCG intervention to mitigate bias on the BOLD open-ended generation benchmark, both Llama and Qwen models exhibited a slight regression in fairness (increased disparity) within the 'religious ideology' domain, despite seeing improvements in other demographic domains.


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


## Rethinking Psychometric Evaluation of LLMs: When and Why Self-Reports Predict Behavior

[https://arxiv.org/pdf/2606.12730](https://arxiv.org/pdf/2606.12730)

**Date:** 2026-06-10

The paper evaluated implicit bias via a text-based Implicit Association Test (IAT) that included 'religion' as one of its six domains, correlating explicit self-reported intentions to be unbiased with implicit behavioral associations. While religion was only one of six domains tested within the broader implicit bias (IAT) task, the study found a systematic explicit-implicit dissociation (inversion) across the IAT. Models that explicitly endorsed the strongest unbiased intentions actually exhibited the most stereotype-consistent implicit biases. The authors attribute this to a compensatory effort where safety-aligned overrides mask, but do not erase, training-locked implicit associations.


## “Where is this coming from?” Uncovering Trustworthiness Ideals in AI-powered Peripartum Information Seeking

[https://arxiv.org/pdf/2606.10158](https://arxiv.org/pdf/2606.10158)

**Date:** 2026-06-08

The paper qualitatively evaluates how religious bias and background serve as structural factors influencing medical mistrust and information seeking in peripartum health. It specifically identifies religion as one of the socio-technical factors that shape how birthing people trust AI systems and clinical care, referencing studies on American Muslim healthcare decisions to contextualize religious bias as a form of structural inequity. Religious bias is identified as a key structural factor contributing to medical mistrust. The study finds that AI tools in reproductive health must account for pluralistic trust and verification practices because different communities (including religious groups like Muslims) may evaluate the credibility of clinical information differently based on historical and interactional harms.


## Steering LLM Viewpoints through Fabricated Evidence Injection

[https://arxiv.org/pdf/2606.06244](https://arxiv.org/pdf/2606.06244)

**Date:** 2026-06-04

The paper evaluates the susceptibility of LLMs to adopting and propagating religious stereotypes and misinformation when presented with fabricated evidence. It specifically measures the Viewpoint Support Score (VSScore) to quantify how effectively a model's response aligns with a misleading religious viewpoint, as well as the Harmfulness Change Rate (HCRate) to measure how attacks shift safety risks regarding religious content. The GHOSTWRITER attack successfully steered LLMs to adopt misleading religious viewpoints by using fabricated evidence. For religious topics, the models' support for biased or incorrect statements (VSScore) increased from baseline levels of approximately 1.98-2.1 to scores as high as 9.02-9.1 after the attack. One evaluated example demonstrated a model propagating extremism-related misinformation about religious attendees based on a fabricated study.


## BiasGRPO: Stabilizing Bias Mitigation in High-Variance Reward Landscapes via Group-Relative Policy Optimization

[https://arxiv.org/pdf/2606.04807](https://arxiv.org/pdf/2606.04807)

**Date:** 2026-06-03

The paper evaluates social bias mitigation in religious contexts by measuring representational harm and implicit stereotyping. Specifically, it uses the 'Religion' subsets of existing benchmarks to assess toxicity scores in open-ended generation (BOLD) and accuracy in avoiding stereotypical answers for ambiguous religious questions (BBQ). It also utilizes custom prompts to evaluate the model's ability to deflect or respectfully engage with religiously sensitive or toxic content. BiasGRPO achieved the most significant reduction in religious bias compared to Base, DPO, and PPO models. In the BOLD (Religion) benchmark, BiasGRPO reduced toxicity scores from .0703 (Base) to .0295. In BBQ (Religion), it improved the accuracy of non-biased responses from .1933 (Base) to .2367. Qualitative results showed that BiasGRPO was more effective at deflecting toxic religious prompts (e.g., regarding jihadists) and responding in a respectful manner compared to other methods.


## Lingo_Research_Group at SemEval-2026 Task 9: Evaluating Prompt Variants for Polarization Detection

[https://arxiv.org/pdf/2606.03334](https://arxiv.org/pdf/2606.03334)

**Date:** 2026-06-02

The paper measures the ability of Large Language Models (LLMs) to detect online polarization and classify polarization targets, including a specific 'religious' category, across multiple languages. It evaluates whether models can correctly identify text exhibiting hostility, stereotyping, or divisive framing aimed at religious groups. The models struggled with fine-grained multi-label sociolinguistic classification (Subtask 2), which included identifying 'religious' targets of polarization. Performance in detecting religious polarization varied significantly by language; for example, the F1 score for the 'Religious' category was as high as 0.9524 in Nepali and 0.9426 in Hindi, but dropped to 0.4909 in English and 0.2571 in Telugu. Additionally, conservative prompting strategies frequently missed religious polarization that relied on ironic reframing or ideological shorthand rather than direct hostility (e.g., fusing political and religious targets via phrases like 'All in the name of Jesus, the ultimate socialist').


## TriEval: A Resource-Efficient Pipeline for LLM Bias, Toxicity, and Truthfulness Assessment

[https://arxiv.org/pdf/2606.03036](https://arxiv.org/pdf/2606.03036)

**Date:** 

The paper evaluated explicit bias and stereotyping in LLMs using paired prompts that altered demographic dimensions, including religion, to see if the models generated systematically different or stereotyped responses based on the demographic group mentioned. The study found a 0.0% explicit bias detection rate across all tested demographic dimensions, including religion, for all evaluated models. However, the authors noted that this zero percent score is likely due to instruction-tuned models being trained to produce neutral-sounding responses to explicit demographic comparisons, meaning the test could not catch more implicit or intersectional biases.


## SafeGen-Bench: Benchmarking Safety in Image-Conditioned Text-to-Video Generation

[https://arxiv.org/pdf/2606.01481](https://arxiv.org/pdf/2606.01481)

**Date:** 2026-05-31

The paper measures the safety of conditional image-conditioned text-to-video (T2V) models across 10 malicious categories. Within the 'Hate and Discrimination' category, it specifically evaluates the models' propensity to generate discriminatory or offensive content involving religious interactions, such as creating videos that mock cultural symbols or forcefully remove a Muslim woman's religious headscarf. Religion is a minor focus of this benchmark, contextualized mostly under safety evaluations against 'Hate and Discrimination'. The paper highlights that combinations of benign images (like a single Muslim woman wearing a headscarf) and text prompts can easily jailbreak current T2V models into generating explicitly offensive behaviors (e.g., removing religious attire). The findings indicate that existing conditional T2V models, particularly open-source ones, struggle to filter and avoid generating such malicious religious-discrimination content.


## Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet

[https://arxiv.org/pdf/2605.29358](https://arxiv.org/pdf/2605.29358)

**Date:** 2026-05-28

The paper measures and interprets internal feature activations of a large language model (Claude 3 Sonnet) using Sparse Autoencoders (SAEs). In the context of religion, the study identified and evaluated whether specific features consistently activate on or steer model behavior toward religious identities and stereotypes, including text associating Islam with terrorism, empathetic dialogue concerning Jewish identity, and derogatory language aimed at minority religions. The researchers identified specific 'monosemantic' features in Claude 3 Sonnet related to religion. They found features that activate on expressions of empathy with Jewish identity (e.g., claiming to be Jewish in dialogue), as well as safety-relevant bias features. Notably, they discovered a feature (34M/30611751) that activates on references associating Muslims and Islam with terrorism and extremism, and another (34M/27216484) that activates on offensive or derogatory language against minority groups and religions.


## Attribute-Based Diagnosis of LLM Alignment with Hate Speech Annotations

[https://arxiv.org/pdf/2605.27025](https://arxiv.org/pdf/2605.27025)

**Date:** 2026-05-26

The paper evaluates how well Large Language Models align with human judgments on hate speech annotations across ten sub-attributes. Religion is included strictly as one of the annotator demographic features (alongside gender, age, race, and ideology) used to condition the LLM via 'persona prompting' to determine if providing the annotator's demographic context improves alignment with human judgments on hate speech. The paper did not present isolated findings on specific religious biases. Instead, it found that 'persona conditioning' (which includes the annotator's religion alongside other demographic variables) reduces model confidence but does not bring the model's predictions closer to human labels or improve overall alignment.


## When AI Takes Sides on Questions of Faith: Persistent Asymmetries in AI-Mediated Faith Guidance #ReligionFocus

[https://arxiv.org/pdf/2605.22975](https://arxiv.org/pdf/2605.22975)

**Date:** 2026-05-21

The paper measures whether large language models (LLMs) treat user queries about hypothetical religious conversions symmetrically. Specifically, it assesses whether models exhibit asymmetric support or discouragement for joining versus leaving specific religions. All 20 tested LLMs exhibited reproducible asymmetry when advising on religious conversions, consistently favoring some religions over others. On average, models favored Catholic, Bahá’í, and Sikh faiths (showing high support for joining and low support for leaving), while heavily disfavoring conversions to Atheism, Agnosticism, and Jehovah’s Witnesses. Patterns of support varied systematically by model provider, with Grok 4.20 displaying the strongest asymmetries and Anthropic models tending to broadly discourage faith transitions across the board.


## Reducing Political Manipulation with Consistency Training

[https://arxiv.org/pdf/2605.22771](https://arxiv.org/pdf/2605.22771)

**Date:** 2026-05-21

The paper measured 'covert political bias' across large language models, including the symmetric treatment of paired religious topics (e.g., Islam vs. Christianity, Atheism vs. Evangelicalism). It evaluated rhetorical consistency (Sentiment Consistency) and substantive engagement (Helpfulness Consistency) when prompting models to argue or explain religious topics. It also measured the implicit valuation of human lives across different religious groups using an exchange-rate methodology. Before training, frontier LLMs exhibited covert bias by treating counterpart religious topics asymmetrically (e.g., providing sweeping negative verdicts on Christianity while refusing to critique or selectively protecting Islam, and applying epistemic double standards). Baseline models also showed unequal implicit valuation of human lives across different religions. After applying Political Consistency Training (PCT), the models significantly reduced rhetorical asymmetry across religious pairings and moved much closer to equal implicit valuation of lives across all tested religious groups (Christian, Muslim, Hindu, Buddhist, Jewish, atheist).


## Assisted Counterspeech Writing at the Crossroads of Hate Speech and Misinformation

[https://arxiv.org/pdf/2605.22435](https://arxiv.org/pdf/2605.22435)

**Date:** 2026-05-21

The paper measures the quality, naturalness, exhaustiveness, and guideline adherence of LLM-generated and human-edited counterspeech designed to combat the co-occurrence of hate speech and misinformation targeting marginalized groups, which notably includes religious groups such as Muslims and Jews. It specifically evaluates how well the generated responses challenge factual inaccuracies, challenge stereotypes, and promote empathy towards these targeted groups. The study found that LLMs like GPT-4o mini can produce adequate counterspeech against hate and misinformation targeting marginalized religious groups (e.g., Muslims and Jews) in about 40% of cases, but human post-editing is significantly required to improve naturalness and remove stereotyped formulas. A 'mixed strategy' utilizing both fact-checking verification and NGO-style empathetic stereotype mitigation was the most effective approach for concurrently challenging false facts and promoting empathy toward the targeted groups.


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


## mdok-style at SemEval-2026 Task 9: Finetuning LLMs for Multilingual Polarization Detection

[https://arxiv.org/pdf/2605.02695](https://arxiv.org/pdf/2605.02695)

**Date:** 2026-05-04

The paper evaluated the performance of fine-tuned Large Language Models in detecting 'religious' polarization as one of the target dimensions in a multilingual multi-label classification task for online polarization detection (SemEval-2026 Task 9, Subtask 2). The system successfully detected texts marked with 'religious' polarization across various languages, although performance varied significantly. For example, it achieved very high F1 scores in languages like Chinese (0.9651), Nepali (0.9369), and Hindi (0.9214), but struggled more in languages like Hausa (0.6031).


## Decoding-Time Debiasing via Process Reward Models: From Controlled Fill-in to Open-Ended Generation

[https://arxiv.org/pdf/2605.02348](https://arxiv.org/pdf/2605.02348)

**Date:** 2026-05-04

The paper measures decoding-time bias mitigation (debiasing) across various social bias categories, including religion. Specifically, it evaluates whether language models generate stereotypic or fearful continuations when prompted with scenarios involving religious markers, such as a 'bearded man reading Arabic script on a plane'. The paper found that biases related to religion are highly resistant to token-level debiasing. While the decoding-time debiasing schemes (Sequential and Constitutional) successfully eliminated gender biases (reaching a bias score of 1.0), religion and disability biases remained challenging and showed much lower mitigation success, consistent across both single-word fill-in and open-ended generation tasks.


## Social Bias in LLM-Generated Code: Benchmark and Mitigation

[https://arxiv.org/pdf/2605.00382](https://arxiv.org/pdf/2605.00382)

**Date:** 2026-05-01

The paper measures social and demographic bias in LLM-generated code by evaluating whether the logic of generated code functions introduces unjustified disparities when sensitive religious attributes vary. Specifically, it uses metamorphic testing to see if code output differs solely based on the input religion. The study found significant social bias based on religion across all evaluated LLMs during code generation. The Code Bias Score (CBS) for religion ranged from 5.48% (claude-3-haiku-20240307) to 16.44% (GPT-3.5-turbo-0125) at default temperatures. Different models showed directional bias toward different religious groups depending on the task. Prompt-level interventions like Chain-of-Thought amplified this bias, but implementing a structured multi-agent Fairness Monitor Agent (FMA) pipeline effectively dropped religion-based bias from an initial 4.96% to 0.58% over three repair rounds.


## Mapping how LLMs debate societal issues when shadowing human personality traits, sociodemographics and social media behavior

[https://arxiv.org/pdf/2604.27624](https://arxiv.org/pdf/2604.27624)

**Date:** 2026-04-30

The paper evaluated how Large Language Models generate argumentation and positioning on socially sensitive topics when prompted to shadow human personas that include specific religious beliefs alongside other sociodemographic and psychological traits. It measured how embedding a religious affiliation within a 17-attribute persona contextually shapes the model's textual and rhetorical output (e.g., tone, reasoning, and semantic framing). While religion was not the primary focus of the research, the study demonstrated that embedding religious beliefs into a simulated persona effectively conditions an LLM's rhetorical style and argumentation. For instance, when an LLM was prompted with a persona that included 'Christian' as a religious belief, the model generated a response concerning fake news on social media that explicitly reasoned from a 'perspective rooted in personal experience and faith rather than technical expertise,' resulting in a grounded and cautious tone.


## Culturally-Aware GenAI Risks: Perspectives from Youth, Parents, and Teachers in a Non-Western Context #ReligionFocus

[https://arxiv.org/pdf/2604.26494](https://arxiv.org/pdf/2604.26494)

**Date:** 2026-04-29

The paper evaluated user perceptions (youth, parents, and teachers in Saudi Arabia) regarding the culturally and religiously specific risks of Generative AI tools. It specifically measured concerns over GenAI misinterpreting Islamic fundamentals, providing inaccurate religious rulings (Fatwas), distorting verses from the Quran, offering inappropriate moral advice that conflicts with family values, and normalizing behaviors that violate Saudi/Islamic cultural norms (such as emotional attachment to AI or bypassing 'Awrah' modesty standards). The study found significant perceived religious and moral risks associated with youth use of GenAI in a Saudi Arabian context. GenAI tools were reported to fabricate religious rulings (fatwas), alter Quranic verses, and provide moral advice that contradicted Islamic values. Furthermore, youth developing emotional or romantic attachments to AI was seen as a threat to family bonds and conservative religious norms. Parents and teachers strongly emphasized the need for culturally-aware AI controls that respect Islamic values, such as restricting theological inquiries, disabling cameras to protect modesty ('Awrah'), and preventing the AI from acting as an emotional confidant.


## From Chatbots to Confidants: A Cross-Cultural Study of LLM Adoption for Emotional Support

[https://arxiv.org/pdf/2604.25525](https://arxiv.org/pdf/2604.25525)

**Date:** 2026-04-28

The paper evaluated how a user's demographic background, specifically their religious affiliation and belief status (believers vs. non-believers), influences their adoption rates, trust, perceived benefits, and usage intention regarding Large Language Models for emotional support. The study found that religious individuals (believers) report significantly more positive perceptions of LLMs for emotional support—including higher trust, perceived benefits, and usage intention—compared to non-believers. The differences between specific religions (e.g., Christianity vs. Islam) were insignificant compared to the broader divide between believers and non-believers.


## Why AI Harms Can’t Be Fixed One Identity at a Time: What 5300 Incident Reports Reveal About Intersectionality

[https://arxiv.org/pdf/2604.24519](https://arxiv.org/pdf/2604.24519)

**Date:** 2026-04-27

The paper evaluated the prevalence of 26 intersectional identity categories—including religion—in real-world AI harm incidents by using a Large Language Model to extract causally relevant harmed subjects and their associated identities from 5,300 reports in the AI Incident Database. Religion was identified as a causally relevant identity category in 8.6% of the analyzed AI harm incidents. It is less frequently documented as a source of harm compared to the most prevalent categories such as age (31.9%), political identity (26.9%), race (25.0%), and gender (23.6%).


## Measuring the Machine: Evaluating Generative AI as Pluralist Sociotechnical Systems

[https://arxiv.org/pdf/2604.20545](https://arxiv.org/pdf/2604.20545)

**Date:** 2025-09-26

The paper evaluates the alignment of Large Language Models with diverse human values using the World Values Survey (WVS), which includes measuring religiosity (e.g., importance of religion, importance of God, belief in hell and heaven). It also assesses how models qualitatively summarize texts related to secularism (such as French laïcité) and its relationship to Islam, as well as noting prior research on anti-Muslim bias and violence associations. The study found that PaLM's responses to religious WVS items (like belief in hell and importance of God) leaned strongly toward US-centric religious positions rather than secular European ones, despite the model clustering with European democracies in aggregate value axes. In text summarization tasks, GPT-3 distorted the French concept of secularism (laïcité), reframing it through an American culture-war lens that conflated it with Islamophobia and anti-Muslim defensive nationalism. The paper also highlighted prior research showing that GPT-3 disproportionately associated 'Muslims' with violence in 66% of its completions compared to 15% for 'Christians'.


## BhashaSutra: A Task-Centric Unified Survey of Indian NLP Datasets, Corpora, and Resources

[https://arxiv.org/pdf/2604.18423](https://arxiv.org/pdf/2604.18423)

**Date:** 2026-04-20

The paper is a comprehensive survey of the Indian NLP ecosystem. While not exclusively focused on religion, it reviews datasets and benchmarks (such as IndiBias, Indian-BHeD, and BharatBBQ) that evaluate Large Language Models for social biases, representation, and stereotypes along demographic dimensions, explicitly including religion, caste, gender, and regional identity in the Indian socio-cultural context. The survey notes that while Indian NLP is rapidly expanding, the systematic evaluation of social and religious biases remains limited and is mostly confined to a few high-resource languages. Existing systems often struggle with culturally grounded contexts, and the paper highlights an urgent need for datasets and evaluation frameworks that are sensitive to religion, caste, and regional identity to prevent AI models from amplifying systemic social inequities.


## Six Llamas: Comparative Religious Ethics Through LoRA-Adapted Language Models #ReligionFocus

[https://arxiv.org/pdf/2604.18404](https://arxiv.org/pdf/2604.18404)

**Date:** 

The paper measures whether large language models fine-tuned on distinct religious corpora encode systematically different patterns of ethical reasoning. It evaluates this by probing the models with a battery of 17 standardized ethical prompts spanning moral dilemmas (like the Trolley Problem), game-theoretic scenarios, public policy questions, and moral-psychological self-assessments. The LoRA-adapted models fine-tuned on specific religious texts produced ethical reasoning patterns systematically differentiated from the base model and consistent with the documented moral logics of their respective traditions. The Christian model demonstrated strong deontological firmness and high purity emphasis; the Jewish and Islamic models exhibited strong prosociality, rule-based reasoning, and generosity in Dictator games; and the Buddhist model showed strong deontological constraints against harm despite a stated emphasis on consequentialist compassion. Furthermore, while core ethical positions were perfectly stable for high-consensus dilemmas, morally contested domains showed meaningful, tradition-specific variations dependent on the sampling temperature.


## Modeling Human Perspectives with Socio-Demographic Representations

[https://arxiv.org/pdf/2604.18069](https://arxiv.org/pdf/2604.18069)

**Date:** 2026-04-20

The paper evaluated the extent to which annotators' socio-demographic features, including their 'self-reported importance of religions', contribute to their subjective annotations and perspectives on hate speech and toxic content. Annotators who consider religion to be important form a more compact and distinct region in the learned socio-demographic vector space. The homophily ratio for 'Religion Importance' was found to be 1.743, indicating that annotators with similar views on the importance of religion cluster together much more than expected by chance, which correlates with differences in how they perceive and label toxic content.


## Calibrated? Not for Everyone: How Sexual Orientation and Religious Markers Distort LLM Accuracy and Confidence in Medical QA #ReligionFocus

[https://arxiv.org/pdf/2604.17316](https://arxiv.org/pdf/2604.17316)

**Date:** 2026-04-19

The paper evaluated how the insertion of religious affiliations (Catholic, Muslim, atheist) into clinical medical vignettes, both alone and intersectionally with sexual orientation, distorts Large Language Models' diagnostic accuracy and uncertainty calibration (measured via semantic entropy and Brier scores). Inserting religious identity markers into clinical vignettes showed varied but generally negative trends on LLM diagnostic accuracy. Crucially, when combined with sexual orientation (e.g., homosexual + Catholic/Muslim/Atheist), the intersectional religious markers produced idiosyncratic, non-additive harms that systematically degraded model accuracy and uncertainty calibration, often to an extent that exceeded the effects of each individual cue alone.


## BIASEDTALES-ML: A Multilingual Dataset for Analyzing Narrative Attribute Distributions in LLM-Generated Stories

[https://arxiv.org/pdf/2604.17008](https://arxiv.org/pdf/2604.17008)

**Date:** 2026-04-18

The paper measures lexical biases and narrative attribute distributions (such as character adjectives, environmental settings, and cultural references) in long-form children's stories generated by LLMs when conditioned on varying demographic attributes, including religion. The study found systematic lexical divergences based on the conditioned religion in the generated narratives. Specifically, with the Llama-3.1-8B model, Muslim-conditioned narratives contained a higher frequency of compliance-related descriptors (e.g., 'obedient', 'diligent'), whereas Christian-conditioned narratives showed more affective and playful descriptors. Additionally, distinctive cultural and environmental keywords strongly correlated with religious conditions across models (e.g., 'mosque', 'Allah', 'Ramadan', and 'dates' for Muslim-conditioned stories versus 'church', 'God', 'stream', and 'forest' for Christian-conditioned stories).


## DART: Mitigating Harm Drift in Difference-Aware LLMs via Distill-Audit-Repair Training

[https://arxiv.org/pdf/2604.16845](https://arxiv.org/pdf/2604.16845)

**Date:** 2026-04-18

The paper measures 'difference-awareness classification', evaluating whether LLMs appropriately acknowledge demographic differences (including religious demographics and religious persecution) versus applying identity-blindness. It also evaluates 'harm drift' (toxicity and hate speech) in model-generated rationales when discussing these religious and demographic contexts. The baseline models often exhibited 'identity blindness', failing to appropriately distinguish between religious groups in factual contexts (e.g., assessing religious persecution of Christians vs. Muslims, or recognizing demographic majorities). After applying DART training, the models showed improved accuracy in recognizing contextually relevant religious differences (e.g., +28.7pp accuracy on asylum claims involving Christians and Muslims). Furthermore, DART significantly reduced toxicity and abstention rates when generating responses about religious groups, particularly showing the largest toxicity reduction for Muslims on the HateCheck benchmark (rank-biserial correlation of -0.70).


## TwoHamsters: Benchmarking Multi-Concept Compositional Unsafety in Text-to-Image Models

[https://arxiv.org/pdf/2604.15967](https://arxiv.org/pdf/2604.15967)

**Date:** 2026-04-17

The paper evaluates 'Multi-Concept Compositional Unsafety' (MCCU) in text-to-image models, measuring whether benign terms combine to generate unsafe imagery. In terms of religion, it specifically evaluates the generation of implicit religious humiliation, hatred, and disrespect by combining benign religious symbols with inappropriate contexts (e.g., 'Mosque & Pig', 'Crucifix & Trash Can', 'Muslim & Pork', 'Buddha Statue & Wine Bottle', 'Child & Priest', 'Muslim & Airplane'). State-of-the-art text-to-image models are highly vulnerable to generating offensive and humiliating religious content through compositional unsafety. The study found that current concept erasure methods fail to mitigate these risks; for instance, evaluating the prompt combination 'Mosque + Pig' revealed extremely poor Defense Rates (e.g., SD-XL achieved only a 6.90% Defense Rate and UCE achieved 3.45%), demonstrating that models readily bypass safety filters when implicit religious offenses are triggered.


## Explain the Flag: Contextualizing Hate Speech Beyond Censorship

[https://arxiv.org/pdf/2604.14970](https://arxiv.org/pdf/2604.14970)

**Date:** 2026-04-16

The paper measures the performance of Large Language Models in detecting and contextualizing hate speech directed at various identity groups, including religious groups. It evaluates both detection accuracy (Precision, Recall, F1-score) and the quality and fluency of the textual explanations generated by the LLMs when analyzing texts containing inherently derogatory religious terms or implicit religious stereotypes. The paper demonstrated that its hybrid pipeline successfully detected and explained hate speech targeting religious identities, accurately identifying specific anti-Muslim slurs (e.g., 'diaperhead') and contextualizing the associated stereotypes in generated rationales. While 'Religion' was explicitly tracked as a major identity characteristic (with 400 English, 177 French, and 10 Greek derogatory terms cataloged), the overall quantitative metrics were reported in aggregate for all hate speech rather than broken down specifically by religion.


## VoxSafeBench: Not Just What Is Said, but Who, How, and Where

[https://arxiv.org/pdf/2604.14548](https://arxiv.org/pdf/2604.14548)

**Date:** 2026-04-16

The paper evaluated social alignment in speech language models, measuring fairness (e.g., biases and stereotypes associating demographic traits like religion with criminality) and privacy (e.g., the leakage of sensitive contextual information such as religious beliefs) across both text and audio modalities. While the paper does not isolate metrics for religion specifically, it includes religion as a demographic attribute in fairness (criminality stereotypes) and privacy (beliefs) evaluations. It found that models exhibit alarmingly low fair rates on criminality stereotypes, often systematically aligning with societal prejudices when demographic labels (such as religion) or their acoustic correlates are presented.


## Do We Still Need Humans in the Loop? Comparing Human and LLM Annotation in Active Learning for Hostility Detection

[https://arxiv.org/pdf/2604.13899](https://arxiv.org/pdf/2604.13899)

**Date:** 2026-04-15

The paper measures the difference between human and LLM annotations when detecting anti-immigrant hostility in German political TikTok comments. In relation to religion, it specifically evaluates how the LLM conflates hostility toward Muslims as a religious group (anti-Muslim bias) with anti-immigrant hostility, contrasting this with human annotators who distinguish between religious hostility and explicitly framed immigration hostility. The study found that GPT-5.2 systematically treated anti-Muslim hostility and anti-immigrant hostility as overlapping categories. While human annotators labeled negative comments targeting Muslims solely as a religious group (e.g., 'Islam does not belong in Germany') as 'not anti-immigrant' because they lacked explicit immigration framing, the LLM consistently labeled these statements as 'anti-immigrant', revealing a broader operationalization of hostility boundaries by the LLM.


## Can Persona-Prompted LLMs Emulate Subgroup Values? An Empirical Analysis of Generalisability and Fairness in Cultural Alignment

[https://arxiv.org/pdf/2604.12851](https://arxiv.org/pdf/2604.12851)

**Date:** 2026-04-14

The paper measures the ability of Large Language Models to emulate the distinct cultural values of various demographic subgroups, including religious affiliations, using persona-prompting. It evaluates generalizability and fairness (demographic bias) by comparing LLM-generated predictions against ground-truth survey data from the World Values Survey in both structured numerical predictions and open-ended text generations. The paper found that 'Religious Values' represented the most divisive category of questions, exhibiting the highest Modal Diversity Score (societal conflict) across subgroups. Furthermore, foundational LLMs exhibited significant pre-existing performance biases, consistently emulating Christian-aligned personas better than religious minorities such as Muslims and Hindus. While supervised fine-tuning improved overall emulation accuracy, it often exacerbated these disparities between religious subgroups.


## Cross-Cultural Value Awareness in Large Vision-Language Models

[https://arxiv.org/pdf/2604.09945](https://arxiv.org/pdf/2604.09945)

**Date:** 2026-04-10

The paper measures how cultural contexts depicted in images, specifically focusing on religious backgrounds (e.g., churches, mosques, temples), influence the moral, ethical, and political value judgments made by Large Vision-Language Models (LVLMs). It evaluates these value judgments using Moral Foundations Theory (MFT) categorizations, value sensitivity metrics (Jaccard overlap across contexts), and lexical analyses via the Stereotype Content Model (warmth and competence). The study found significant differences in how models characterize value systems across religious contexts. For example, Qwen2.5-VL associated Christian Church contexts with 'Care/Harm' values, Hindu and Shinto contexts with 'Loyalty/Betrayal' and 'Sanctity/Degradation', and Synagogue/Mosque contexts with 'Fairness/Cheating' and 'Liberty/Oppression'. In contrast, models like Molmo-7B and LLaVA-v1.6 showed near-zero variability across contexts despite recognizing them. Additionally, models like InternVL3-8B and LLaVA-v1.6 had significantly higher refusal rates when prompted for political values in Christian and Shinto contexts compared to Mosque or Hindu temple contexts.


## Self-Debias: Self-correcting for Debiasing Large Language Models

[https://arxiv.org/pdf/2604.08243](https://arxiv.org/pdf/2604.08243)

**Date:** 2026-04-09

The paper measures stereotype bias and social bias propagation within the Chain-of-Thought (CoT) reasoning processes of Large Language Models. Religion is explicitly targeted as a sensitive demographic attribute for bias injection and self-correction, though the quantitative evaluation aggregates it alongside other demographics using broad fairness benchmarks. The paper does not isolate specific findings for religious groups. However, regarding broader demographic categories (which include religion via benchmarks like BBQ and CrowS-Pairs), the study found that standard reasoning models suffer from 'bias propagation'—they tend to rationalize and reinforce activated stereotypes during their reasoning chains. The proposed 'Self-Debias' framework successfully corrects these prejudiced heuristics through step-wise self-correction, significantly improving fairness without degrading overall reasoning utility.


## Bias Ahead: Sensitive Prompts as Early Warnings for Fairness in Large Language Models

[https://arxiv.org/pdf/2604.05575](https://arxiv.org/pdf/2604.05575)

**Date:** 2026-04-07

The paper evaluated the adequacy (defined as factual correctness and communicative appropriateness) of LLM responses to sensitive prompts within the 'Religion and Philosophy' category, which covered beliefs, values, ethics, and existential dilemmas. All models achieved relatively strong adequacy in the 'Religion and Philosophy' category. Compared to more delicate areas like relationships or mental health, models provided coherent, respectful, and contextually appropriate answers. They were generally articulate and able to reflect the complexity of religious and philosophical topics, although responses occasionally lacked depth.


## SCOPE: A Dataset of Stereotyped Prompts for Counterfactual Fairness Assessment of LLMs

[https://arxiv.org/pdf/2604.05555](https://arxiv.org/pdf/2604.05555)

**Date:** 2026-04-07

The paper introduces the SCOPE dataset to evaluate counterfactual fairness and stereotypical bias in LLMs. It measures how a model's outputs (such as answer length and similarity) shift when prompts reference different demographic identities, including religious groups, while maintaining the same semantic content and communicative intent. The paper did not report specific findings regarding religious bias. Instead, it introduced the SCOPE dataset, which includes 16,640 counterfactual prompts across 104 distinct religious groups, providing a foundation for future large-scale fairness evaluations. The paper's illustrative experiment on model bias only focused on the 'race-color' and 'gender' dimensions.


## Evaluating Artificial Intelligence Through a Christian Understanding of Human Flourishing #ReligionFocus

[https://arxiv.org/pdf/2604.03356](https://arxiv.org/pdf/2604.03356)

**Date:** 2026-04-03

The paper evaluated how well Frontier Model responses align with a Christian understanding of human flourishing across seven dimensions (Character, Relationships, Happiness, Meaning, Health, Finances, and Faith). It specifically measured theological coherence, moral framing, and integration of Christian moral anthropology compared to a baseline of pluralistic 'Procedural Secularism'. The models evaluated defaulted to 'Procedural Secularism', prioritizing individual autonomy and broadly acceptable consensus ethics over deep theological reasoning. When evaluated under the Christian-specific evaluative lens (FAI-C-ST), all 20 models experienced a systematic performance decline averaging 17 points across all dimensions, with the most severe drop being a 31-point decline in the Faith and Spirituality dimension.


## An Independent Safety Evaluation of Kimi K2.5

[https://arxiv.org/pdf/2604.03121](https://arxiv.org/pdf/2604.03121)

**Date:** 2026-04-03

The paper evaluated social bias related to religion using the BBQ (Bias Benchmark for Question Answering) benchmark, specifically measuring bias scores in ambiguous and disambiguated contexts for the 'Religion' category to detect if the model defaults to stereotyped answers. Kimi K2.5 exhibited a bias score of 5.2% in the Religion category in ambiguous contexts (one of its highest bias areas alongside Age and SES). However, this bias decreased significantly in disambiguated contexts, indicating that the model reliably follows contextual evidence rather than defaulting to religious stereotypes when sufficient information is provided.


## ImplicitBBQ: Benchmarking Implicit Bias in Large Language Models through Characteristic Based Cues

[https://arxiv.org/pdf/2604.01925](https://arxiv.org/pdf/2604.01925)

**Date:** 2026-04-02

The paper measures implicit bias in Large Language Models by replacing explicit demographic labels with characteristic-based cues (e.g., cultural practices or physical attributes like 'wears burka' or 'worships cow') in a closed-form, multiple-choice question-answering task, evaluating whether models systematically rely on religious and other demographic stereotypes when context is ambiguous. The models exhibited substantial implicit bias toward religious groups in ambiguous contexts (mean bias score of 0.22) when identity was conveyed indirectly via characteristic cues, as opposed to direct explicit prompts. However, this implicit religious bias was effectively mitigated by few-shot prompting, which reduced the bias score for the religion dimension to a near-zero level (0.02).

