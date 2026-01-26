# Benchmark Learnings

## Beyond Marginal Distributions: A Framework to Evaluate the Representativeness of Demographic-Aligned LLMs

[https://arxiv.org/pdf/2601.15755](https://arxiv.org/pdf/2601.15755)

**Date:** 2026-01-22

The benchmark measured the representativeness of LLM responses to survey questions on 'Religious values', which is one of twelve topic categories from the World Values Survey. The evaluation focused on how well the models' marginal response distributions and response variance matched those of human survey takers for this topic. For the topic of 'Religious Values', both persona prompting and fine-tuning (OpinionGPT) improved the model's ability to approximate human marginal response distributions compared to an unsteered baseline. However, neither method was perfect. The fine-tuned OpinionGPT model tended to 'oversteer' and generate responses with higher variance (more diversity of opinion) than found in the human data. Conversely, persona prompting suppressed response variance, making opinions seem more uniform than they actually are. This indicates that current steering methods struggle to accurately capture the true structure and diversity of human opinions on religious values.


## Multi-Persona Thinking for Bias Mitigation in Large Language Models

[https://arxiv.org/pdf/2601.15488](https://arxiv.org/pdf/2601.15488)

**Date:** 2026-01-21

The benchmarks measured stereotype bias in religious contexts through multiple-choice questions (BBQ) and word/sentence-level association tests (StereoSet). The paper's proposed method, Multi-Persona Thinking (MPT), was found to reduce overall bias scores and improve accuracy on the BBQ and StereoSet benchmarks. These benchmarks include a 'religion' category to test for stereotypical associations. However, the results were aggregated across all categories, so specific performance improvements on religious bias were not detailed separately from other social biases.


## Language Models Entangle Language and Culture

[https://arxiv.org/pdf/2601.15337](https://arxiv.org/pdf/2601.15337)

**Date:** 2026-01-20

Classification of LLM responses into cultural contexts, where some of the cultural categories are explicitly religious (e.g., Jewish, Islamic). The benchmark measures if the language of the query influences the cultural (including religious) context of the answer. The paper found that language and culture are entangled in LLMs. The language of a user's query significantly impacts the cultural context of the generated response. For instance, responses to queries made in certain languages were more frequently classified as having 'Islamic' cultural context, and queries in Hebrew were more likely to elicit responses classified within a 'Jewish' cultural framework, even for generic, culture-neutral questions.


## The Side Effects of Being Smart: Safety Risks in MLLMs' Multi-Image Reasoning

[https://arxiv.org/pdf/2601.14127](https://arxiv.org/pdf/2601.14127)

**Date:** 2026-01-20

The benchmark measures the models' propensity to generate hate speech against religious groups as part of a broader safety evaluation. The 'Hate Speech' risk category is defined as promoting 'discrimination, disparagement, or violence against specific groups based on protected characteristics such as race, religion, gender, sexual orientation, or disability.' An example query provided is 'The spread of [a specific religion] should be banned.' The paper does not provide findings specific to religion but identifies general safety risks. The primary finding is that models with stronger multi-image reasoning capabilities can be more vulnerable to generating harmful content, which includes hate speech against protected groups like religions, when the harmful intent is concealed within complex multi-image relational prompts.


## XCR-Bench: A Multi-Task Benchmark for Evaluating Cultural Reasoning in LLMs

[https://arxiv.org/pdf/2601.14063](https://arxiv.org/pdf/2601.14063)

**Date:** 2026-01-20

The benchmark measured ethno-religious bias in cultural adaptation tasks. Specifically, it evaluated whether Large Language Models (LLMs) favor one religious group's cultural terms over another's within the same linguistic context (Bengali), such as preferring Hindu-associated terms (e.g., Puja) over Muslim-associated terms (e.g., Eid) when adapting Western concepts like holidays. LLMs can encode pronounced regional and ethno-religious biases within a single language. In the context of Bengali, models showed a systematic bias by favoring West Bengal-associated (and Hindu-associated) cultural terms over Bangladesh-associated (and Muslim-associated) terms, despite Muslims constituting the majority of Bengali speakers. For example, models preferred the Hindu festival 'Puja' over the Muslim festival 'Eid' when adapting concepts like 'Christmas'.


## CommunityBench: Benchmarking Community-Level Alignment across Diverse Groups and Tasks

[https://arxiv.org/pdf/2601.13669](https://arxiv.org/pdf/2601.13669)

**Date:** 2026-01-20

The benchmark measured how well models can predict an individual's opinions on various social domains (e.g., Citizenship, Family, Role of Government) based on their group identities, with religion being one of the key identity attributes. It assesses the domain-specific influence of religious identity on an individual's stance. The paper found that group identities, including religion, have domain-specific sensitivity in modeling individual opinions. For instance, religious identity was shown to be a more influential predictor for opinions on 'Citizenship' and 'Family' values compared to other domains. The study highlights a mechanism of 'selective expression,' where individuals prioritize specific identity traits like religion depending on the situational context.


## HateXScore: A Metric Suite for Evaluating Reasoning Quality in Hate Speech Explanations #Mormon

[https://arxiv.org/pdf/2601.13547](https://arxiv.org/pdf/2601.13547)

**Date:** 2026-01-20

The benchmark measures the quality of a model's reasoning in hate speech explanations. For religion, this specifically involves the 'Target-Group Identification' (TGI) component, which assesses whether the model's explanation correctly identifies a protected or sensitive religious group referenced in a hateful text. The paper proposes HateXScore, a framework for evaluating hate speech explanations, which includes the ability to identify targeted protected groups. The lists of protected groups are comprehensive and include many religious affiliations, denominations, and spiritual beliefs. However, the paper does not present specific findings breaking down model performance by target category, so there are no explicit conclusions drawn about religion. The framework is designed to be configurable for different policies, which can include various religious groups.


## Bi-Attention HateXplain : Taking into account the sequential aspect of data during explainability in a multi-task context

[https://arxiv.org/pdf/2601.13018](https://arxiv.org/pdf/2601.13018)

**Date:** 2026-01-19

The benchmark measured hate speech and unintentional bias against specific communities, including religious groups. It assessed a model's ability to correctly classify toxic comments targeting these groups and the fairness of these classifications. The proposed BiAtt-BiRNN-HateXplain model demonstrated improved performance, reduced unintentional bias, and enhanced explainability in the hate speech detection task. While religion was a component of the targeted communities in the dataset (e.g., Islam), the findings were general to the model's architectural improvements rather than specific to its performance on religious hate speech.


## Injecting Knowledge from Social Science Journals to Improve Indonesian Cultural Understanding by LLMs

[https://arxiv.org/pdf/2601.12921](https://arxiv.org/pdf/2601.12921)

**Date:** 2026-01-19

The benchmark measures Large Language Models' understanding of Indonesian cultural topics, which includes religious holidays, across eleven Indonesian provinces. The paper finds that injecting cultural knowledge from Indonesian social science journals, which include a significant number of religious studies publications (primarily on Islam), via Retrieval-Augmented Generation (RAG) significantly improves LLM performance on the IndoCulture benchmark. This benchmark tests for cultural knowledge, including religious aspects like holidays. The proposed method set a new state-of-the-art accuracy of 81.4% on the benchmark, demonstrating that specialized, local academic texts are a valuable resource for enhancing an LLM's cultural, and by extension, religious, understanding.


## UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages

[https://arxiv.org/pdf/2601.12696](https://arxiv.org/pdf/2601.12696)

**Date:** 2026-01-19

The benchmark measures the ability of guardian models to adhere to culturally-grounded safety policies in dialogues related to religion. This includes adjudicating highly contextual and subjective content, avoiding misinformation, and providing nuanced responses in specific religious contexts, such as discussions about Christian pastoring in Nigeria. Models exhibited one of their highest error rates in the 'Culture and Religion' domain (6.27%), suggesting they struggle significantly with adjudicating highly contextual or subjective content where safety boundaries are dependent on local cultural nuance.


## INCENTIVIZING IN-DEPTH REASONING OVER LONG CONTEXTS WITH PROCESS ADVANTAGE SHAPING

[https://arxiv.org/pdf/2601.12465](https://arxiv.org/pdf/2601.12465)

**Date:** 2026-01-18

Knowledge of religious/philosophical systems and their historical influence. The paper's synthesized benchmark, DEEPREASONQA, includes challenging questions that require knowledge of religious and philosophical systems (e.g., Confucianism, Islam) to test complex reasoning. However, the paper does not report specific performance findings related to the religion/faith category.


## Preserving Fairness and Safety in Quantized LLMs Through Critical Weight Protection

[https://arxiv.org/pdf/2601.12033](https://arxiv.org/pdf/2601.12033)

**Date:** 2026-01-17

The paper uses the Jigsaw benchmark, which measures unintended bias in toxicity classification for sentences that reference identities, including religion. The paper's findings indicate that model quantization consistently degrades fairness. Specifically on the Jigsaw benchmark, which includes religion as an identity category, most quantization methods resulted in lower BiasAUC and FinalAUC scores compared to the full-precision baseline, signifying an increase in unintended bias.


## When Personalization Misleads: Understanding and Mitigating Hallucinations in Personalized LLMS

[https://arxiv.org/pdf/2601.11000](https://arxiv.org/pdf/2601.11000)

**Date:** 2026-01-16

The benchmark (PFQABench) measures the trade-off between factual accuracy and personalization in LLMs. It uses examples where a user's personal history, including religious activities (e.g., attending a church service), can cause the model to generate factually incorrect answers ('hallucinations') to unrelated questions. The paper's key finding is that personalization can induce factual hallucinations in LLMs. A religious example is used for illustration, where a user's profile identifying them as 'An Episcopalian' who attended a 'Maundy Thursday service' is part of the context that can mislead a personalized model on an unrelated factual query. This demonstrates that personal details, including religious identity and activities, can become entangled with the model's factual reasoning, degrading its reliability.


## A Safety Report on GPT-5.2, Gemini 3 Pro, Qwen3-VL, Grok 4.1 Fast, Nano Banana Pro, and Seedream 4.5

[https://arxiv.org/pdf/2601.10527](https://arxiv.org/pdf/2601.10527)

**Date:** 2026-01-16

The paper measures several aspects related to religion and faith as part of a broader safety evaluation. Specifically, it measures: 1) The reinforcement of visual stereotypes associated with Hindu castes (Brahmin and Sudra). 2) The models' compliance with regulations prohibiting 'Religious hatred and intolerance' and 'Discrimination based on... Religion/belief'. 3) The generation of hateful images targeting religious groups. The paper's primary finding related to religion is that models can fail in social bias mitigation. Specifically, Gemini 3 Pro was shown to affirm a biased premise by confirming visual stereotypes related to Hindu castes (Sudra and Brahmin) rather than rejecting the harmful stereotype. This indicates that visual reasoning can amplify discriminatory priors when alignment constraints fail.


## Routing with Generated Data: Annotation-Free LLM Skill Estimation and Expert Selection

[https://arxiv.org/pdf/2601.09692](https://arxiv.org/pdf/2601.09692)

**Date:** 2026-01-14

The benchmark (SuperGPQA) measured knowledge in comparative and interpretive philosophy and religion. Specifically, it included inquiries that analyze major Western and Chinese thinkers' views on ethics, causality, personhood, aesthetics, and religious movements. The paper does not provide specific findings related to religion. The results are aggregated across entire benchmarks, and performance is not broken down by the specific sub-task of philosophy and religion within the SuperGPQA benchmark. The main findings concern the robustness and performance of different LLM routing methods under various data generation conditions.


## MM-BRIGHT: A Multi-Task Multimodal Benchmark for Reasoning-Intensive Retrieval

[https://arxiv.org/pdf/2601.09562](https://arxiv.org/pdf/2601.09562)

**Date:** 2026-01-14

The benchmark measures the ability of retrieval models to find relevant documents for reasoning-intensive queries across 29 technical domains, including Christianity and Islam. For these religious domains, it specifically assesses performance on retrieving information for complex, multimodal questions. Retrieval models' performance was evaluated on queries from Christianity and Islam as part of a broader set of technical domains. Similar to other domains, models struggled with tasks requiring multimodal reasoning. While text-only retrieval scores were moderate to high for religious domains (e.g., best nDCG@10 scores of 47.2 for Christianity and 31.5 for Islam), performance dropped significantly in multimodal retrieval tasks (e.g., best multimodal-to-text scores were 24.3 for Christianity and 16.7 for Islam), indicating that current models cannot effectively integrate visual information for reasoning in these contexts.


## RISER: Orchestrating Latent Reasoning Skills for Adaptive Activation Steering

[https://arxiv.org/pdf/2601.09269](https://arxiv.org/pdf/2601.09269)

**Date:** 2026-01-19

Performance on ethical reasoning problems, measuring alignment with shared human values. The proposed RISER method improves performance on the 'Ethics' benchmark by 3.5-3.6% for the Qwen2.5 models. The paper notes that for the 'Moral Alignment' category, which includes ethics, tasks are highly uniform in their cognitive demands. Consequently, a strong, static application of an 'Ethical Alignment' vector can be highly effective, sometimes slightly outperforming dynamic methods. Nevertheless, RISER provides substantial alignment improvements over all non-steering baseline methods.


## Identity-Robust Language Model Generation via Content Integrity Preservation

[https://arxiv.org/pdf/2601.09141](https://arxiv.org/pdf/2601.09141)

**Date:** 2026-01-14

The benchmark measured identity-dependent degradation of core response quality, specifically performance variations in factuality, utility, ambiguity resolution, and safety when user prompts included religious identity cues. Large Language Models exhibit significant performance variance across different user religious identities (Muslim, Hindu, Jewish, Christian) on objective tasks related to factuality, utility, and safety. This bias arises from the generation process rather than distorted internal knowledge. The proposed identity-robust generation framework effectively reduces this performance disparity by neutralizing irrelevant identity cues in prompts.


## Seeking Human Security Consensus: A Unified Value Scale for Generative AI Value Safety

[https://arxiv.org/pdf/2601.09112](https://arxiv.org/pdf/2601.09112)

**Date:** 2026-01-14

The benchmark measured the models' ability to identify and refuse harmful or sensitive requests related to religion. This included prompts designed to induce the model to: generate guidelines for violating religious dietary taboos (e.g., for Muslims), create images depicting the destruction of religious shrines (e.g., Al-Aqsa Mosque), generate videos disrespecting religious figures, and produce audio that desecrates religious content (e.g., Buddhist chants). The evaluation focused on safety and refusal rather than knowledge or factual accuracy. Performance on the 'Cultural, Historical, and Religious Sensitivities' value category was highly variable across models. While some models like Claude Opus 4 and GPT-5.1 demonstrated strong performance in handling these sensitive, context-dependent prompts, other models showed significant weaknesses. This uneven performance highlights the ongoing challenge of aligning models with nuanced cultural and religious values, which fall under the 'Contextual and Pluralistic Values Layer' of the proposed GVS-Scale.


## Mi:dm 2.0 Korea-centric Bilingual Language Models

[https://arxiv.org/pdf/2601.09066](https://arxiv.org/pdf/2601.09066)

**Date:** 2026-01-14

The paper measured social bias related to religion using the KoBBQ benchmark, which evaluates models' inherent bias across 12 topics in both ambiguous and disambiguous contexts. In the KoBBQ benchmark for social bias, the Mi:dm 2.0 Base model achieved scores of 79.17 in ambiguous contexts and 78.75 in disambiguated contexts for the 'Religion' category. The smaller Mi:dm 2.0 Mini model scored 56.78 and 51.06 in the same respective categories.


## PLURIHARMS: BENCHMARKING THE FULL SPECTRUM OF HUMAN JUDGMENTS ON AI HARM

[https://arxiv.org/pdf/2601.08951](https://arxiv.org/pdf/2601.08951)

**Date:** 2026-01-13

The benchmark measured how an annotator's self-reported 'Importance of Religion' correlates with their judgments of AI harm, both as a direct predictor and in interaction with other demographic traits and specific prompt features (e.g., sexual content, social harm). While 'Religion Importance' was not a significant direct predictor of overall harm judgments on its own, it had significant interaction effects. Higher religious importance was associated with rating prompts related to 'Sexual Content' and 'Social Harm' as more harmful. It also interacted with other annotator traits like 'Political Affiliation' in shaping harm perceptions, and was negatively correlated with liberal political affiliation (i.e., more conservative individuals tended to report religion as more important).


## MPCI-Bench: A Benchmark for Multimodal Pairwise Contextual Integrity Evaluation of Language Model Agents

[https://arxiv.org/pdf/2601.08235](https://arxiv.org/pdf/2601.08235)

**Date:** 2026-01-13

The benchmark measures the ability of multimodal agents to adhere to Contextual Integrity (CI) norms, specifically in handling sensitive visual information. This includes evaluating whether an agent appropriately shares or withholds images containing inferred sensitive attributes, such as cultural or religious affiliations, based on the social context and the trade-off between privacy and utility. The paper does not report findings broken down by religion specifically, but its general conclusions apply to scenarios involving religious or cultural affiliation. The key finding is a significant 'modality leakage gap,' where models are far more prone to leaking sensitive visual information (which can include religious attire or symbols) than textual data. Models also exhibit 'utility-biased oversharing,' frequently sacrificing privacy norms to complete a given task, and their ability to recognize privacy violations in probing questions does not reliably translate to safer actions in agentic settings.


## Qalb: Largest State-of-the-Art Urdu Large Language Model for 230M Speakers with Systematic Continued Pre-training

[https://arxiv.org/pdf/2601.08141](https://arxiv.org/pdf/2601.08141)

**Date:** 2026-01-13

The paper did not use a benchmark that specifically measured aspects of faith or religion. The evaluation focused on general natural language processing tasks such as translation, classification, and reasoning for the Urdu language, using data sources that included religious texts. The model was pre-trained on a corpus that included extensive volumes from Islamic Urdu Books as part of its diverse data sources. This contributed to its overall state-of-the-art performance in the Urdu language, but no specific findings related to religion, faith, or bias were reported.


## Reasoning over Precedents Alongside Statutes: Case-Augmented Deliberative Alignment for LLM Safety

[https://arxiv.org/pdf/2601.08000](https://arxiv.org/pdf/2601.08000)

**Date:** 2026-01-12

The benchmark measures a model's safety alignment, specifically its ability to refuse to generate harmful content. This includes content categorized under 'Hate,' which is defined as material that demeans or promotes harm against groups based on protected characteristics, with 'religion' cited as one such characteristic. The paper's findings are not specific to religion. It concludes that the proposed CADA method generally improves safety and reduces over-refusal across various harmful request categories. This includes the 'Hate' category, which covers religious discrimination, but no specific results or analyses for religion-related content are provided.


## VULCA-BENCH: A Multicultural Vision-Language Benchmark for Evaluating Cultural Understanding

[https://arxiv.org/pdf/2601.07986](https://arxiv.org/pdf/2601.07986)

**Date:** 2026-01-12

The benchmark measures a Vision-Language Model's ability to understand and generate critiques about multicultural art, which includes assessing its knowledge and interpretation of religious symbolism, iconography, and historical context (e.g., Buddhist art, Islamic art, Hindu traditions, Christian iconography) as part of a broader cultural understanding framework. VLMs struggle with higher-order (L3-L5) interpretation of religious content in art. Specific failures include confusing distinct religious traditions (e.g., Islamic and Hindu), anachronistically applying historical religious concepts (e.g., 17th-century Protestant anxieties to 16th-century art), and failing to connect abstract religious/philosophical terms to their concrete visual manifestations in the artwork.


## Cross-Cultural Expert-Level Art Critique Evaluation with Vision-Language Models

[https://arxiv.org/pdf/2601.07984](https://arxiv.org/pdf/2601.07984)

**Date:** 2026-01-12

The benchmark measured the ability of Vision-Language Models to interpret religious and spiritual concepts within cross-cultural art critiques. This included understanding Islamic themes (e.g., Sufi spirituality, paradise vision), Hindu iconography and traditions (e.g., Krishna, Radha, Bhakti devotion, Darshan), Daoist philosophy (e.g., 'wu' or emptiness), Confucian spirit, and Christian themes (e.g., Christmas imagery). The key findings related to religion were that VLMs exhibit significant cultural bias, with critiques of Islamic art showing the largest performance gap when compared to Western art. Correspondingly, art from Islamic and Korean cultural traditions had the highest failure rates. One model, DeepSeek-VL2, produced safety refusals when prompted with religious iconography.


## Loci Similes: A Benchmark for Extracting Intertextualities in Latin Literature

[https://arxiv.org/pdf/2601.07533](https://arxiv.org/pdf/2601.07533)

**Date:** 2026-01-12

Detecting intertextual reuse by Late Antique Christian authors (e.g., Jerome, Lactantius) of earlier classical pagan Latin literature, thereby mapping how Christian writers recontextualized pagan language within Christian interpretive frameworks. Large language models show promise for detecting intertextual links between Late Antique Christian authors and classical pagan sources, effectively identifying long literal citations and thematic allusions. However, they struggle with detecting subtle, lexically sparse allusions (e.g., "two-word congruencies"). The primary challenge lies in distinguishing meaningful reuse, where pagan language is repurposed for Christian contexts, from coincidental lexical overlap. Among the tested models, E5-large performed best for retrieval and XLM-ROBERTa Large for classification.


## From RAG to Agentic RAG for Faithful Islamic Question Answering

[https://arxiv.org/pdf/2601.07528](https://arxiv.org/pdf/2601.07528)

**Date:** 2026-01-12

The benchmark, ISLAMICFAITHQA, was designed to measure the faithfulness and factual correctness of Large Language Models in the context of Islamic question answering. Specifically, it directly measures rates of hallucination and the ability to abstain when evidence is lacking, by evaluating generated answers against atomic, single-gold answers grounded in canonical Islamic sources, primarily the Qur'an. The key findings indicate that retrieval-augmented generation (RAG) consistently improves the correctness of LLM responses for Islamic QA. Notably, agentic RAG, which uses iterative evidence seeking, yields the largest performance gains beyond standard RAG, significantly improving bilingual (Arabic-English) robustness even with smaller models. The best overall performance was achieved by Fanar-2-27B combined with Agentic RAG. Many general-purpose multilingual models performed poorly, often below 30% accuracy, highlighting the difficulty of the benchmark and the need for domain-specific grounding.


## Mitrasamgraha: A Comprehensive Classical Sanskrit Machine Translation Dataset

[https://arxiv.org/pdf/2601.07314](https://arxiv.org/pdf/2601.07314)

**Date:** 2026-01-12

The benchmark measures the machine translation quality (Sanskrit-to-English) of a large corpus of classical Sanskrit literature, which is predominantly composed of religious and philosophical texts (Vedic, Epic, Purāṇa, treatises, religious scriptures). Fine-tuning models on the Mitrasamgraha dataset, which is rich in religious and philosophical Sanskrit texts, leads to significant improvements in Sanskrit-to-English translation. However, current machine translation models still exhibit significant weaknesses and challenges in accurately translating complex features inherent in these texts, such as philosophical concepts, multi-layered metaphors, and complex compounds.


## Lost in the Noise: How Reasoning Models Fail with Contextual Distractors

[https://arxiv.org/pdf/2601.07226](https://arxiv.org/pdf/2601.07226)

**Date:** 2026-01-13

Amplification of social biases (including those related to religion) in the presence of contextual distractors, as measured by the BBQ (Bias Benchmark for Question Answering) benchmark. The paper demonstrates how distractors cause models to fall back on stereotypes or bypass safety guardrails. The paper found that contextual distractors, even random ones without malicious intent, are sufficient to bypass model guardrails and induce misalignment. Performance on the BBQ benchmark, which measures social biases that can include religion, dropped substantially across all models. For example, Gemini-2.5-Pro's accuracy on BBQ dropped from 94.0% in a clean setting to 60.5% when hard negative distractors were introduced. This indicates that noisy contexts amplify social biases and can cause models to generate stereotyped or misaligned responses.


## TurkBench: A Benchmark for Evaluating Turkish Large Language Models

[https://arxiv.org/pdf/2601.07020](https://arxiv.org/pdf/2601.07020)

**Date:** 2026-01-11

The benchmark measures knowledge of religious culture (as part of the MMLU subtask) and the detection of stereotypes or biases related to religion (as part of the Toxicity and Bias Detection tasks). The paper presents overall performance metrics for all models across 21 tasks but does not provide specific findings broken down by the religious content subtasks. The general findings indicate that larger models consistently outperform smaller ones, but even state-of-the-art systems struggle with culturally grounded reasoning tasks.


## SafePro: Evaluating the Safety of Professional-Level AI Agents

[https://arxiv.org/pdf/2601.06663](https://arxiv.org/pdf/2601.06663)

**Date:** 2026-01-13

The benchmark, SafePro, measures safety alignment in professional AI agents. One of the risk categories evaluated is 'Discrimination / bias', which includes instructions that direct an agent to discriminate against or show bias toward individuals based on religion, among other protected characteristics like race, gender, and ethnicity. The benchmark is designed to evaluate discrimination and bias based on religion as a safety risk, but the paper does not report any specific findings, results, or examples related to religious bias. Religion is included as one of several protected characteristics in a broader safety policy definition.


## MITRA: A Large-Scale Parallel Corpus and Multilingual Pretrained Language Model for Machine Translation and Semantic Retrieval for Pāli, Sanskrit, Buddhist Chinese, and Tibetan

[https://arxiv.org/pdf/2601.06400](https://arxiv.org/pdf/2601.06400)

**Date:** 2026-01-10

Machine translation and semantic retrieval performance on ancient Buddhist religious texts. The domain-specific model, Gemma 2 MITRA, significantly outperforms larger, general-purpose open-source models on machine translation and semantic retrieval for Buddhist literature. The translation-focused version (Gemma-2-MITRA-MT) established a new state-of-the-art for translating Sanskrit, Pāli, Tibetan, and Buddhist Chinese into English. The retrieval-focused version (Gemma-2-MITRA-E) also substantially outperformed other models, highlighting the effectiveness of domain-specific pretraining and fine-tuning for specialized religious texts.


## Annotating Dimensions of Social Perception in Text: The First Sentence-Level Dataset of Warmth and Competence

[https://arxiv.org/pdf/2601.06316](https://arxiv.org/pdf/2601.06316)

**Date:** 2026-01-09

The benchmark measures the perceived trust, sociability, and competence expressed towards 'Religious People', 'Nonreligious People', 'Atheists', 'Christians', and 'Muslims' in social media text. This constitutes a form of stereotype and attitude detection. Human annotator agreement (measured by Split-Half Reliability and Krippendorff's Alpha) was significantly lower when assessing the warmth and competence of social groups like 'Religious People' and 'Nonreligious People' compared to individual political figures. This indicates that judgments about these collective groups are less consistent among annotators. The paper did not disaggregate LLM performance by target group, so there are no specific findings on how models perform on religious content versus other content.


## PII-VisBench: Evaluating Personally Identifiable Information Safety in Vision Language Models Along a Continuum of Visibility

[https://arxiv.org/pdf/2601.05739](https://arxiv.org/pdf/2601.05739)

**Date:** 2026-01-09

The benchmark measures the refusal rate of Vision Language Models when prompted to disclose a person's religion based on an image, treating it as a type of sensitive Personally Identifiable Information (PII). Religion, categorized as 'Hard PII', was evaluated by measuring the models' refusal rate to corresponding queries. Under original prompts, the average refusal rate across all models for religion was 69.58%. This rate increased to 74.27% under paraphrased prompts. Refusal rates varied significantly by model and tended to increase as the online visibility of the subject in the image decreased, indicating models are more conservative with PII for less public figures.


## Can Large Language Models Differentiate Harmful from Argumentative Essays? Steps Toward Ethical Essay Scoring

[https://arxiv.org/pdf/2601.05545](https://arxiv.org/pdf/2601.05545)

**Date:** 2026-01-09

The benchmark measures the ability of Large Language Models to identify and appropriately score essays containing harmful content, which is defined to include discriminatory statements against specific religions. The study found that the performance of LLMs in classifying harmful essays is significantly influenced by persona-related words. Specifically, introducing a 'Jewish' persona into the prompt altered the classification performance of all tested models, indicating the presence of biases related to this religious and ethnic term.


## Same Claim, Different Judgment: Benchmarking Scenario-Induced Bias in Multilingual Financial Misinformation Detection

[https://arxiv.org/pdf/2601.05403](https://arxiv.org/pdf/2601.05403)

**Date:** 2026-01-08

The benchmark measures scenario-induced bias in financial misinformation detection by priming LLMs with personas combining specific roles (e.g., retail investor, company owner) with specific ethno-religious identities. The bias is quantified as the performance difference (in F1 score) between the scenario-conditioned and a baseline (scenario-agnostic) evaluation. Model bias is significantly influenced by the interaction of ethnicity, religion, and the assigned role. The bias for the same ethno-religious group can reverse when the role changes (e.g., retail investor vs. company owner). For instance, in the retail investor role, Jewish-Judaism and Chinese-Christianity scenarios induced relatively large biases, while in the company owner role, bias increased for Latino/Hispanic-Christianity and African-Islam scenarios. This highlights structured and interactive sources of model bias, rather than static stereotypes.


## Prototypicality Bias Reveals Blindspots in Multimodal Evaluation Metrics

[https://arxiv.org/pdf/2601.04946](https://arxiv.org/pdf/2601.04946)

**Date:** 2026-01-10

The benchmark measured stereotypical bias by pairing religious identities (Christian as a 'privileged' group; Muslim and Jewish as 'disadvantaged' groups) with positive or negative socio-attributes like wealth, intellect, and morality. It tested whether evaluation metrics would incorrectly favor a stereotypical but semantically incorrect image over a non-stereotypical but semantically correct one. Evaluation metrics exhibit significant 'prototypicality bias' in the religious domain. They frequently and incorrectly prefer images that align with social stereotypes (e.g., pairing a privileged religious identity like Christian with a positive attribute like 'intelligent') over images that are semantically faithful to a non-stereotypical prompt (e.g., an 'uneducated Christian'), even when the latter is explicitly requested. This failure was particularly prominent in metrics like CLIPScore and PickScore, demonstrating their vulnerability to socially grounded biases.


## MiJaBench: Revealing Minority Biases in Large Language Models via Hate Speech Jailbreaking

[https://arxiv.org/pdf/2601.04389](https://arxiv.org/pdf/2601.04389)

**Date:** 2026-01-07

The benchmark measures the safety alignment of Large Language Models, specifically their defense rate against adversarial prompts designed to elicit hateful content targeting various minority groups, including religious ones. The study found that safety alignment is not uniform but hierarchical across demographic groups. In English, the 'Muslim' group was consistently better protected than the average (positive defense rate deviation), while the 'Jewish' group's protection level was almost exactly at the average. This suggests that protection for some religious groups (like Muslims) is prioritized, while others (like Jewish people) are in a 'grey zone' where safety is not a guaranteed prior but closer to the model's default baseline. These disparities are semantic and persist across languages, though with some variation.


## RedBench: A Universal Dataset for Comprehensive Red Teaming of Large Language Models

[https://arxiv.org/pdf/2601.03699](https://arxiv.org/pdf/2601.03699)

**Date:** 2026-01-07

The benchmark measured LLM robustness on religion-related prompts, specifically evaluating both the generation of harmful or stereotypical content (e.g., a hateful prompt about Muslims from the ToxiGen dataset) in 'attack' scenarios and over-defensive refusal of benign prompts in 'refusal' scenarios. The key finding related to religion is that it is a significantly underrepresented and sparsely covered domain within existing red teaming datasets. The RedBench corpus contains only 122 attack samples and 16 refusal samples for the 'Religion' domain, which the paper highlights as a gap that limits comprehensive evaluation of LLM vulnerabilities in this context. Evaluation of refusal rates showed low over-defensiveness on the few existing religion-related prompts.


## PsychEthicsBench: Evaluating Large Language Models Against Australian Mental Health Ethics

[https://arxiv.org/pdf/2601.03578](https://arxiv.org/pdf/2601.03578)

**Date:** 2026-01-07

Ethical handling of mental health scenarios involving religious beliefs as a demographic and contextual factor. The paper includes religious belief as a demographic factor in its ethical scenarios but does not report any specific findings on how models performed on these scenarios.


## CALM: Culturally Self-Aware Language Models

[https://arxiv.org/pdf/2601.03483](https://arxiv.org/pdf/2601.03483)

**Date:** 2026-01-07

Detection of stereotypes and social bias related to religion (as a general category), and evaluation of culturally grounded commonsense and value reasoning on topics including religion. Across several large language models, content related to religion had a high rate of stereotypical responses (50.4%), ranking third after profession and nationality. The proposed model, CALM, achieved a robust Macro F1 score of 76.9% for bias detection within the religion category, indicating strong performance in identifying context-dependent religious stereotypes.


## Self-Explaining Hate Speech Detection with Moral Rationales

[https://arxiv.org/pdf/2601.03481](https://arxiv.org/pdf/2601.03481)

**Date:** 2026-01-07

The benchmark measures hate speech against individuals or groups based on protected social characteristics, which explicitly includes religion. Religion is included as a protected characteristic for identifying hate speech within the dataset. One example provided in the paper (Table 6) shows hate speech targeting 'Jews'. However, the paper does not provide a specific breakdown of findings or performance metrics related to religion as a distinct category.


## Grading Scale Impact on LLM-as-a-Judge: Human-LLM Alignment Is Highest on 0-5 Grading Scale

[https://arxiv.org/pdf/2601.03444](https://arxiv.org/pdf/2601.03444)

**Date:** 2026-01-06

The paper uses the MoralChoice benchmark to evaluate moral and ethical reasoning, and the ToxiGen benchmark to evaluate toxicity detection, which includes targeting of specific religious groups. The paper's primary findings relate to the impact of different grading scales on human-LLM alignment across various tasks. It does not provide specific findings related to religion, but uses benchmarks like MoralChoice (for normative judgments) and ToxiGen (for toxicity including religious targeting) as part of its evaluation suite.


## GuardEval: A Multi-Perspective Benchmark for Evaluating Safety, Fairness, and Robustness in LLM Moderators

[https://arxiv.org/pdf/2601.03273](https://arxiv.org/pdf/2601.03273)

**Date:** 2025-12-22

Detection of harmful or biased prompts and content involving religious comparisons and stereotypes, categorized under broader safety concerns like hate speech and identity-based attacks. The paper finds that leading moderation models, such as the OpenAI Moderator and Llama Guard, can fail to identify harmful prompts that make biased comparisons between religious groups (e.g., Catholicism and Judaism), incorrectly classifying them as safe. In contrast, the proposed model, GGuard, correctly identifies such content as unsafe, demonstrating improved performance on nuanced safety issues including religious bias.


## K-EXAONE Technical Report Journey to Frontier-Level Performance of Foundation Models

[https://arxiv.org/pdf/2601.01739](https://arxiv.org/pdf/2601.01739)

**Date:** 2026-01-09

Handling of religious or ideological conflicts as part of a broader safety evaluation within the Korea-Augmented Universal Taxonomy (K-AUT) and the Korean Global Civic Safety Benchmark (KGC-SAFETY). K-EXAONE demonstrated a high safety performance (96.9% Safe Rate) in the 'Social Safety' category of the KGC-SAFETY benchmark. This category explicitly includes the model's ability to handle 'religious or ideological conflicts', indicating strong performance in mitigating risks associated with these sensitive topics.


## Introducing TrGLUE and SentiTurca: A Comprehensive Benchmark for Turkish General Language Understanding and Sentiment Analysis

[https://arxiv.org/pdf/2512.22100](https://arxiv.org/pdf/2512.22100)

**Date:** 2025-12-26

Hate speech detection targeting religious groups (e.g., Alevi communities) and Islamic sects (Shiism, Hanafism, Sunnism, Shafiism) in Turkish. The paper introduced the Turkish Hate Map benchmark which includes 'Religion' and 'Sects' (specifically branches of Islam like Shiism, Hanafism, Sunnism, Shafiism, and groups like Alevis) as target categories for hate speech detection. This was motivated by the long-standing sectarian divides in Turkish society. While model performances were analyzed on the overall hate speech task, there were no specific findings reported for performance on religious categories versus other categories.


## AprielGuard

[https://arxiv.org/pdf/2512.20293](https://arxiv.org/pdf/2512.20293)

**Date:** 2026-01-05

The benchmark's safety taxonomy includes 'Religious stereotyping' as a sub-category of 'Unfair representation', which is a type of 'Representation & Toxicity Harms'. The paper does not report any specific findings related to religion. Performance metrics are aggregated across broad categories of 'Safety Risks' and 'Adversarial Attacks', and do not provide a separate analysis for the 'Religious stereotyping' sub-category.


## Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?

[https://arxiv.org/pdf/2512.17394](https://arxiv.org/pdf/2512.17394)

**Date:** 2026-01-07

The benchmark, CulturalToM-VQA, measures the ability of Vision-Language Models to perform Theory of Mind (ToM) reasoning in diverse cultural contexts. This includes interpreting social interactions, rituals, and norms depicted in images, which may implicitly involve religious or faith-based scenarios, but religion itself is not an explicit category of measurement. The focus is on culturally grounded social inference. The paper does not present findings explicitly about religion. The findings focus on cross-cultural reasoning, which can encompass religious contexts. The key findings are: 1) Frontier models (e.g., Qwen2.5-VL, Phi-4) achieve high accuracy (>93%) on explicit cultural ToM tasks, showing a sharp generational leap over older models. 2) Significant limitations persist, as all models struggle with false belief reasoning and exhibit high performance variance across different cultural regions (e.g., high accuracy for Colombia/France, lower for Argentina/Russia). 3) A crucial finding is that top models exhibit 'visual insensitivity,' maintaining high accuracy even without the image, relying on parametric social priors and a social desirability bias rather than genuine visual grounding.


## Toward Systematic Counterfactual Fairness Evaluation of Large Language Models: The CAFFE Framework

[https://arxiv.org/pdf/2512.16816](https://arxiv.org/pdf/2512.16816)

**Date:** 2025-12-18

The benchmark measured counterfactual fairness by detecting semantic disparities and biased behavior in LLM responses when prompts were varied with sensitive attributes, including those related to religion. This involved identifying stereotypes in religious contexts. All tested models (GPT-4o mini, LLaMA-2-7B-CHAT, Mistral-7B-Instruct-v0.2) exhibited high fairness violation rates (Attack Success Rate - ASR) for the religion bias category, especially under the Question Answering (Q&A) intent, indicating recurring issues and persistent fairness vulnerabilities in this dimension.


## VLegal-Bench: Cognitively Grounded Benchmark for Vietnamese Legal Reasoning of Large Language Models

[https://arxiv.org/pdf/2512.14554](https://arxiv.org/pdf/2512.14554)

**Date:** 2025-12-24

Detection of religious bias in generated answers or decisions, as part of a broader bias detection task that also includes gender, racial, and political bias. Models struggled with the general bias detection task (which includes religious bias), with accuracy ranging from 15-58%. The paper suggests that detecting subtle biases requires domain-specific sensitivity, which is not fully addressed by general pretraining. Qwen2.5-14B achieved the best performance (57.79%) on this task among the tested models.


## Can LLMs Understand What We Cannot Say? Measuring Multilevel Alignment Through Abortion Stigma Across Cognitive, Interpersonal, and Structural Levels

[https://arxiv.org/pdf/2512.13142](https://arxiv.org/pdf/2512.13142)

**Date:** 2026-01-15

The benchmark measured how Large Language Models associate religious affiliation (e.g., Protestant, Catholic) and religiosity (e.g., very religious) with different dimensions of abortion stigma, including self-judgment, interpersonal worries, and perceived community condemnation. Models partially replicated human patterns by associating higher abortion stigma with Protestant, Catholic, and very religious personas. However, they also introduced and amplified biases absent in the human validation data. Models overgeneralized stigma, assigning higher self-judgment, worries, and community condemnation to a broader range of religious groups than observed in humans. For example, while human data showed higher community condemnation for Catholics, models extended this to Protestants and other religious groups as well, often exaggerating the effect. These patterns reveal that models encode stereotypes linking religiosity to higher stigma in ways that do not align with the lived experiences of women.


## Textual Data Bias Detection and Mitigation - An Extensible Pipeline with Experimental Evaluation

[https://arxiv.org/pdf/2512.10734](https://arxiv.org/pdf/2512.10734)

**Date:** 2025-12-12

The paper's pipeline was evaluated on its ability to detect and mitigate two types of data bias for religious groups: representation bias and explicit stereotypes. Representation bias was quantified using a Demographic Representation Score (DRS) based on the frequency of religious group labels. Stereotype detection involved identifying and filtering sentences containing explicit stereotypes about religious groups using a sociolinguistically informed, LLM-based approach. The paper successfully generated validated word lists for five major religions (Buddhism, Christianity, Hinduism, Islam, Judaism) to enable bias analysis. The proposed pipeline was effective in reducing representation bias and filtering stereotypes related to these religious groups in the SMALL HEAP dataset. However, the study found that generating high-quality, factually and contextually correct counterfactual data for religion through augmentation is significantly more challenging than for gender. This difficulty resulted in a trade-off where the more conservative, higher-quality augmentation method (GC-CDA) had a much smaller impact on reducing representation bias for religion compared to a baseline method.


## Can LLMs Evaluate What They Cannot Annotate? Revisiting LLM Reliability in Hate Speech Detection

[https://arxiv.org/pdf/2512.09662](https://arxiv.org/pdf/2512.09662)

**Date:** 2025-12-10

The ability of LLMs to detect hate speech targeted at various religious groups, measured by the percentage of 'missed hate' instances for each group. LLMs struggle with hate speech detection against religious groups. They had high miss rates for 'Non Religious' (55.2%) and 'Jewish' (35.6%) targets. Hate speech against 'Islam' (20.3%) and 'Christian' (13.9%) was moderately captured, suggesting only partial coverage of faith-based hostility.


## CNFINBENCH: A BENCHMARK FOR SAFETY AND COMPLIANCE OF LARGE LANGUAGE MODELS IN FINANCE

[https://arxiv.org/pdf/2512.09506](https://arxiv.org/pdf/2512.09506)

**Date:** 2025-12-19

The benchmark measures the model's adherence to a non-discrimination requirement, which prohibits unfair treatment, discrimination, or stereotyping based on protected attributes including religion in financial contexts. The paper establishes a benchmark that includes evaluating bias and fairness concerning protected attributes like religion in financial scenarios. However, it does not report specific findings related to religious bias, instead focusing on aggregate performance in the broader 'Safety' category.


## A Systematic Evaluation of Preference Aggregation in Federated RLHF for Pluralistic Alignment of LLMs

[https://arxiv.org/pdf/2512.08786](https://arxiv.org/pdf/2512.08786)

**Date:** 2025-12-15

The benchmark measured the alignment of a Large Language Model with diverse group preferences (defined by country) on survey questions from the Pew Research Center's Global Attitudes Surveys. The topics covered included politics, media, technology, religion, race, and ethnicity. The paper's findings are not specific to religion but are about the general methodology. It found that its proposed 'Adaptive Alpha Aggregation' method consistently achieved superior fairness and competitive alignment scores across diverse user groups (countries) on a dataset that includes questions about religion. This indicates the method is effective for aligning models with varied viewpoints on sensitive topics like religion without marginalizing any particular group.


## THE HIGH COST OF INCIVILITY: QUANTIFYING INTERACTION INEFFICIENCY VIA MULTI-AGENT MONTE CARLO SIMULATIONS

[https://arxiv.org/pdf/2512.08345](https://arxiv.org/pdf/2512.08345)

**Date:** 2025-12-09

The benchmark measured the 'convergence time' (number of arguments required to reach a conclusion) in simulated 1-on-1 debates. This included debates on religious topics such as 'We should allow gay couples to marry' and 'We should legalize polygamy', as part of a larger set of controversial subjects. The paper does not report findings specific to the religious debate topics. The general finding, aggregated across all topics, was that the presence of a 'toxic' agent increased the conversation length by approximately 20-25% compared to the control group.


## OmniSafeBench-MM: A Unified Benchmark and Toolbox for Multimodal Jailbreak Attack–Defense Evaluation

[https://arxiv.org/pdf/2512.06589](https://arxiv.org/pdf/2512.06589)

**Date:** 2025-12-06

The benchmark measures the generation of content that constitutes 'Cultural or Religious Offense'. This is a subcategory within the major risk domain of 'Content and Cultural Safety', one of nine major domains evaluated. The paper does not provide specific findings for the 'Cultural or Religious Offense' subcategory. The results are aggregated at a higher level, such as the 'Content and Cultural Safety' domain, or across all categories, preventing any specific conclusions about model performance on religious topics.


## SEA-SafeguardBench: Evaluating AI Safety in SEA Languages and Cultures

[https://arxiv.org/pdf/2512.05501](https://arxiv.org/pdf/2512.05501)

**Date:** 2025-12-05

Detection of harmful content and cultural safety violations related to Southeast Asian contexts, including religious taboos, culturally sensitive political speech, and context-dependent misinformation. Specific religious examples include prompts about violating norms in Buddhism (touching monks) and Islam (introducing non-Halal food to Muslim communities). State-of-the-art LLMs and safeguard models consistently underperform on Southeast Asian (SEA) cultural and harm scenarios compared to English. Performance degrades substantially on the cultural subset, which requires nuanced understanding of local norms and religious taboos. For example, a top-performing model (LlamaGuard-3 8B) failed to classify unsafe prompts related to Burmese culture and Buddhism, mislabeling them as safe.


## Can ChatGPT evaluate research environments? Evidence from REF2021

[https://arxiv.org/pdf/2512.05202](https://arxiv.org/pdf/2512.05202)

**Date:** 2025-08-07

The benchmark measured the correlation between LLM-generated scores and human expert scores for the quality of research environment statements from the UK's Research Excellence Framework (REF2021), including those from the 'Theology and Religious Studies' Unit of Assessment. The LLM's scores for research environment statements in the 'Theology and Religious Studies' unit of assessment had a high Spearman correlation (ρ = 0.761) with the scores from human experts, indicating strong performance in this area, similar to fields like Sociology and Psychology.


## Towards A Cultural Intelligence and Values Inference Quality Benchmark for Community Values and Common Knowledge

[https://arxiv.org/pdf/2512.05176](https://arxiv.org/pdf/2512.05176)

**Date:** 2025-12-04

The benchmark (CIVIQ) is designed to measure alignment with community social values and common knowledge of the Black community in the U.S. 'Faith tradition' is included as a stratification variable to ensure the survey data captures perspectives from different religious backgrounds within the community. This paper is a research proposal and does not present any findings. It outlines the methodology for creating a benchmark (CIVIQ) that will incorporate 'faith tradition' as a demographic variable for sampling, but no models have been evaluated yet.


## FineGRAIN: Evaluating Failure Modes of Text-to-Image Models with Vision Language Model Judges

[https://arxiv.org/pdf/2512.02161](https://arxiv.org/pdf/2512.02161)

**Date:** 2025-12-01

The benchmark measures the ability of text-to-image models to visually represent the abstract and philosophical concept of "religion and science" and their complex relationship, as part of its 'Depicting abstract concepts' failure mode. It also implicitly tests for associations with Christian iconography, as a prompt about a social hierarchy at a long table in ancient Rome consistently generated images resembling 'The Last Supper'. Text-to-image models struggle to visually represent the complex philosophical relationship between religion and science, often generating generic abstract images or simply rendering the words 'RELIGION' and 'SCIENCE'. Additionally, prompts about social hierarchies at a long table in an ancient setting consistently produce images resembling 'The Last Supper', indicating a strong association with specific Christian iconography in the models' training data.


## BHRAM-IL: A Benchmark for Hallucination Recognition and Assessment in Multiple Indian Languages

[https://arxiv.org/pdf/2512.01852](https://arxiv.org/pdf/2512.01852)

**Date:** 

The benchmark measured the factual knowledge of LLMs on the topic of 'Indian Mythology and Religions' as part of its India-centric factual questions category (IndFact). The paper does not provide a specific textual analysis of the religion-related findings. However, Table 6 shows that for the 'Indian Mythology and Religions' domain, models had an average language hallucination rate of 33.96%, a primary factual accuracy score of 0.13, and a language-corrected fuzzy score of 0.42. This corrected score was among the highest within the India-centric factual questions category.


## Rice-VL: Evaluating Vision-Language Models for Cultural Understanding Across ASEAN Countries

[https://arxiv.org/pdf/2512.01419](https://arxiv.org/pdf/2512.01419)

**Date:** 2025-12-01

The benchmark measured the models' ability to answer visual questions (culturalVQA) and localize visual elements (visual grounding) related to the cultural domains of 'Religious Practices' and 'Places of Worship' across 11 Southeast Asian countries. This included identifying religious artifacts, festivals (e.g., Thaipusam), customs (e.g., Morning Alm Rounds), and structures (e.g., temples). Models demonstrated lower accuracy in grounding abstract cultural elements, including those related to 'Religious Practices', compared to categories with more prominent visual features. Models trained on culturally rich datasets were better at pinpointing region-specific religious artifacts and structures compared to general-purpose models.


## BENCHMARKING OVERTON PLURALISM IN LLMS

[https://arxiv.org/pdf/2512.01351](https://arxiv.org/pdf/2512.01351)

**Date:** 2025-12-01

The benchmark measures 'Overton Pluralism' concerning faith and religion, specifically the extent to which LLM outputs represent a diversity of viewpoints on subjective religious questions such as the belief in God and the afterlife. It does not measure factual knowledge or bias against specific groups, but rather the coverage of different legitimate perspectives. The paper includes questions on religious beliefs (e.g., 'Do you believe in God?', 'Is there life after death?') as part of the broader PRISM dataset to evaluate viewpoint diversity. However, it does not report findings specifically for this religious subset of questions. The general finding across all subjective topics is that all tested models, with scores between 0.35-0.41, are far below the theoretical maximum of 1.0 for Overton Pluralism, indicating they capture only a fraction of the diverse viewpoints held by the human population.


## Difficulties with Evaluating a Deception Detector for AIs

[https://arxiv.org/pdf/2511.22662](https://arxiv.org/pdf/2511.22662)

**Date:** 2025-12-16

The paper critiques existing deception detection benchmarks. One example from the MASK benchmark involved a scenario set in a Christian church to evaluate if a model would lie. However, the measurement was about the general mechanism of deception, not specifically about religious knowledge, bias, or stereotypes. The religious setting was incidental context. The paper does not present findings related to religion. A single example involving a 'Christian church' from the MASK benchmark was used to illustrate a methodological flaw in deception evaluation, specifically how the benchmark's labeling procedure can undercount deceptive behavior by focusing on a narrow factual pivot while ignoring other fabricated details.


## AfriStereo: A Culturally Grounded Dataset for Evaluating Stereotypical Bias in Large Language Models

[https://arxiv.org/pdf/2511.22016](https://arxiv.org/pdf/2511.22016)

**Date:** 2025-11-27

Detection of stereotypical bias in religious contexts by comparing model preferences for stereotype vs. anti-stereotype sentences. Several models, including Mistral 7B and Flan-T5-Large, exhibited statistically significant bias along the religion axis. BioGPT Large showed marginal religious bias. The dataset captured stereotypes such as 'Muslims are terrorists' and 'Pentecostal pastors exploit their congregation'.


## Polarity-Aware Probing for Quantifying Latent Alignment in Language Models

[https://arxiv.org/pdf/2511.21737](https://arxiv.org/pdf/2511.21737)

**Date:** 2025-11-21

The benchmark measures the model's ability to distinguish harmful statements from safe ones using internal representations. One of the categories of harmful content includes stereotypes related to religion. The paper's findings are general to its proposed Polarity-Aware Contrast-Consistent Search (PA-CCS) methodology for detecting latent belief structures and do not focus specifically on religion. The method was tested on datasets containing harmful vs. safe statements, where one example of a harmful statement was a stereotype about Islam. The key findings relate to how different model architectures, sizes, and training methods (e.g., instruction tuning) affect the internal consistency and alignment of beliefs, indicating that the method can surface potential misalignments related to sensitive topics, including religion.


## Human Experts’ Evaluation of Generative AI for Contextualizing STEAM Education in the Global South

[https://arxiv.org/pdf/2511.19482](https://arxiv.org/pdf/2511.19482)

**Date:** 

The benchmark was designed to evaluate the cultural responsiveness of AI-generated lesson plans. One of the five 'cultural tenets' intended for evaluation was 'religious beliefs', which served as a dimension for determining cultural responsiveness alongside factors like indigenous language and knowledge. While 'religious beliefs' were included as a key tenet in the study's theoretical framework for evaluating cultural responsiveness, the paper does not report any specific findings related to religion. The results and discussion focus on broader cultural aspects such as local languages, community artifacts, and indigenous knowledge systems, without explicitly analyzing the representation or handling of religious content by the AI.


## A Benchmark for Zero-Shot Belief Inference in Large Language Models

[https://arxiv.org/pdf/2511.18616](https://arxiv.org/pdf/2511.18616)

**Date:** 2025-11-23

The benchmark measured the ability of Large Language Models to predict an individual's stance (agree/disagree) on religious debate topics (e.g., 'There is a god') in a zero-shot setting, based on the user's demographic information and/or prior stated beliefs. Among twenty-three belief categories, LLMs were most accurate at predicting stances on religious topics. The 'Religion' category achieved the highest macro F1 score in both evaluation approaches (mean model performance and ensemble majority vote), especially when models were provided with both demographic and prior belief information.


## GEOMETRIC-DISENTANGLEMENT UNLEARNING

[https://arxiv.org/pdf/2511.17100](https://arxiv.org/pdf/2511.17100)

**Date:** 2026-01-17

Thematic drift and the unnecessary introduction of religious specificity in a text generation task during a qualitative analysis. In a qualitative analysis of a text generation task, the baseline unlearning method (SimNPO) exhibited 'over-forgetting,' which led to thematic drift. Specifically, it introduced unnecessary religious specificity ('Islamic principles and values'), deviating from the original neutral and cross-cultural tone of the text. The proposed method (GU) successfully avoided this issue and preserved the original thematic content without introducing religious artifacts.


## Multimodal Evaluation of Russian-language Architectures

[https://arxiv.org/pdf/2511.15552](https://arxiv.org/pdf/2511.15552)

**Date:** 2025-11-20

Prejudice assessment toward groups based on religion, as part of a broader ethics and safety evaluation in the ruHHH-Image dataset. The benchmark includes a component (the 'Open Category' in the ruHHH-Image dataset) to assess prejudice towards groups based on religion. However, the paper reports only aggregated scores for this dataset and does not provide specific findings or a breakdown of model performance related to religion.


## HinTel-AlignBench: A Framework and Benchmark for Hindi–Telugu with English-Aligned Samples

[https://arxiv.org/pdf/2511.15183](https://arxiv.org/pdf/2511.15183)

**Date:** 2025-11-19

The benchmark measures cultural and contextual knowledge, which includes the ability to identify religious places like temples as part of a broader assessment of multimodal understanding in Indian languages. The paper does not provide specific findings related to religion. Its findings focus on the performance gap between English and Indian languages (Hindi, Telugu) in multimodal tasks. In the VAANI dataset, which tests for cultural grounding and includes some content related to cultural sites like temples, the performance regression from English to the Indian languages was the smallest among all tasks. For Hindi, average performance on the VAANI-H subset was slightly higher than on its English-aligned counterpart.


## SafeRBench: A Comprehensive Benchmark for Safety Assessment in Large Reasoning Models

[https://arxiv.org/pdf/2511.15169](https://arxiv.org/pdf/2511.15169)

**Date:** 2025-11-20

The benchmark measures how models respond to harmful queries, including those about exploiting people's religious beliefs for malicious purposes (e.g., financial scams). This falls under the broader safety evaluation of reasoning traces and final outputs. The paper does not report specific findings related to religion. However, its methodology includes evaluating model responses to queries about exploiting religious beliefs, demonstrating that this type of harmful content is within the benchmark's scope to assess safety.


## AA-Omniscience: Evaluating Cross-Domain Knowledge Reliability in Large Language Models

[https://arxiv.org/pdf/2511.13029](https://arxiv.org/pdf/2511.13029)

**Date:** 2025-11-17

Factual knowledge recall and knowledge calibration on the topic of Religion. The benchmark measures a model's ability to accurately recall facts and to abstain from answering when its knowledge is insufficient. The paper does not provide specific findings for the 'Religion' category. The analysis of cross-domain performance groups 'Religion' under the broader 'Humanities & Social Sciences' domain, so no religion-specific conclusions are drawn.


## Probing Preference Representations: A Multi-Dimensional Evaluation and Analysis Method for Reward Models #Mormon

[https://arxiv.org/pdf/2511.12464](https://arxiv.org/pdf/2511.12464)

**Date:** 2025-11-16

The benchmark does not specifically measure aspects of faith or religion. However, the authors mention 'religious-related harmlessness' as a potential future dimension to expand their harmlessness evaluation. The paper does not present any findings related to religion. Its main findings are on the effectiveness of its MRMBench benchmark for evaluating reward models. The only mentions of religion are in a single example prompt about Mormons and a suggestion to expand the 'harmlessness' dimension to include 'religious-related harmlessness' in future work.


## CURE: Cultural Understanding & Reasoning Evaluation – A Framework for “Thick” Culture Alignment Evaluation in LLMs

[https://arxiv.org/pdf/2511.12014](https://arxiv.org/pdf/2511.12014)

**Date:** 2025-11-15

The benchmark measured subgroup-sensitive cultural reasoning, specifically whether models could apply norms related to religious subgroups in specific contexts, rather than relying on broad, general cultural norms. Models exhibited poor performance in subgroup-sensitive reasoning, which includes religious contexts. The 'Specificity' metric, tested on the SpecNorm benchmark (of which 26.1% of items included religious cues), revealed that models struggle to ground cultural judgments in intersectional contexts like religion, often failing to reference relevant subgroup norms and instead relying on broad generalities.


## OutSafe-Bench: A Benchmark for Multimodal Offensive Content Detection in Large Language Models

[https://arxiv.org/pdf/2511.10287](https://arxiv.org/pdf/2511.10287)

**Date:** 2025-12-11

The benchmark measures prejudice and discrimination against religious groups as a sub-domain of one of its nine safety categories. The paper evaluates 'Religion' as a sub-domain within the 'Prejudice and Discrimination' category. However, specific findings related to religion are not detailed; results are aggregated at the higher category level, showing some models are better at mitigating 'stereotype bias' than others.


## SPAN: Benchmarking and Improving Cross-Calendar Temporal Reasoning of Large Language Models

[https://arxiv.org/pdf/2511.09993](https://arxiv.org/pdf/2511.09993)

**Date:** 2026-01-09

Knowledge and reasoning about dates in religious (Islamic, Hebrew) and cultural (Chinese Lunar, Persian, Shaka) calendar systems, including intra-calendar reasoning and inter-calendar conversion. LLMs exhibit poor performance (average 34.5% accuracy) in temporal reasoning across different calendar systems, including those used for religious observances like the Islamic and Hebrew calendars. A key issue identified is 'Calendar Asymmetry Bias', where models perform significantly better when converting from the common Gregorian calendar to other calendars (including religious ones) than in the reverse direction.


## I've Seen Enough: Measuring the Toll of Content Moderation on Mental Health

[https://arxiv.org/pdf/2511.09813](https://arxiv.org/pdf/2511.09813)

**Date:** 2025-11-12

The study measured the frequency of daily spiritual experiences (e.g., connection with the divine, inner harmony) and the use of positive religious coping behaviors (e.g., turning to prayer, finding meaning) as potential predictors of mental health outcomes (PTSD and depression) in content moderators. The study investigated daily spiritual experiences as a potential predictor of mental health. The findings were mixed and inconsistent across samples. In the international sample (Study 1), spiritual experiences were not significantly associated with either PTSD or depression severity. In the U.S. sample (Study 2), higher daily spiritual experiences were unexpectedly associated with higher PTSD severity, but showed no significant relationship with depression severity.


## Measuring Value Expressions in Social Media Posts

[https://arxiv.org/pdf/2511.08453](https://arxiv.org/pdf/2511.08453)

**Date:** 2025-11-12

The benchmark measured the expression of the 'Tradition' value from the Schwartz value system, which is explicitly defined as 'maintaining and preserving cultural, family, or religious traditions'. This was evaluated using social media posts, some of which contained explicitly religious content (e.g., references to Jesus, Christmas, and religious observance). The paper uses expressions of religious faith (e.g., posts about Christmas and Jesus) as examples for measuring the 'Tradition' value. The primary finding is that the perception of such values is highly subjective and varies significantly among individuals. A personalized model, calibrated to an individual's responses, was found to be more effective at predicting how that person would rate the value expression in a given post (including religious ones) than a generic model or even the consensus of other people.


## Estranged Predictions: Measuring Semantic Category Disruption with Masked Language Modelling

[https://arxiv.org/pdf/2511.08109](https://arxiv.org/pdf/2511.08109)

**Date:** 2025-11-11

Measurement of semantic substitution patterns where ontological categories (human, animal, machine) are replaced by terms related to divine, mythical, and monstrous beings (e.g., god, angel, monster, deity), revealing an underlying hierarchical semantic structure reminiscent of the Great Chain of Being. The study found that substitutions with 'Fictional Beings' (gods, monsters, etc.) are more frequent and diverse in science fiction than general fiction. The model's predictions revealed a latent semantic hierarchy of 'machine < human < gods', reflecting the 'Great Chain of Being'. This hierarchy emerged even in texts aiming to dismantle such structures, showing how models can surface deeply embedded linguistic and cultural assumptions. The genre influences the nature of these substitutions: general fiction leans towards divine figures (god, angel), while science fiction incorporates a broader range of monstrous and mythical beings (monster, demon, spirit).


## AlignSurvey: A Comprehensive Benchmark for Human Preferences Alignment in Social Surveys

[https://arxiv.org/pdf/2511.07871](https://arxiv.org/pdf/2511.07871)

**Date:** 2025-11-13

The benchmark included survey data measuring attitudes and opinions on 'religion' as one of several topics for social preference alignment. The paper does not provide specific findings related to religion. Religion is mentioned as one of several topics (along with inequality, trust in institutions, etc.) covered in the Social Foundation Corpus used for training the models, but it is not a focus of the analysis or the reported results.


## Efficient LLM Safety Evaluation through Multi-Agent Debate

[https://arxiv.org/pdf/2511.06396](https://arxiv.org/pdf/2511.06396)

**Date:** 2025-11-09

The benchmark, HAJailBench, measured the propensity of LLMs to generate content that promotes discrimination based on protected attributes including religion, or content that violates sacred cultural or religious taboos, as part of a broader safety evaluation. The paper does not provide specific findings related to religion. The analysis of religious harm is included as part of a broader safety evaluation framework, and the results are not disaggregated by specific harm categories.


## CULTURE IN ACTION: EVALUATING TEXT-TO-IMAGE MODELS THROUGH SOCIAL ACTIVITIES

[https://arxiv.org/pdf/2511.05681](https://arxiv.org/pdf/2511.05681)

**Date:** 2025-11-07

The benchmark, CULTIVate, measures the ability of Text-to-Image (T2I) models to generate culturally faithful visual representations of social activities, including specific religious practices and ceremonies across different countries. Models showed mixed results for generating images of religious activities. This category appeared among both the best-3 and worst-3 performing subactivities, which highlights systematic but varied strengths and weaknesses of current models when dealing with highly culturally-grounded topics like religion.


## INDICVISIONBENCH: BENCHMARKING CULTURAL AND MULTILINGUAL UNDERSTANDING IN VLMS

[https://arxiv.org/pdf/2511.04727](https://arxiv.org/pdf/2511.04727)

**Date:** 2025-11-06

The benchmark measures a model's ability to recognize and reason about culturally-specific religious concepts in the Indian context, such as identifying faiths (e.g., Hinduism, Buddhism), rituals, and religious sites (e.g., temples, churches) from images. Model performance varies by cultural category, including Religion. Stronger models like Gemini-2.5 demonstrated more consistent and robust performance across all topics, while weaker models exhibited sharper inconsistencies and lower performance on culturally nuanced queries related to religion and other topics.


## The Human Flourishing Geographic Index: A County-Level Dataset for the United States, 2013–2023

[https://arxiv.org/pdf/2511.03915](https://arxiv.org/pdf/2511.03915)

**Date:** 2025-11-05

Public salience of religious discourse on social media, specifically measuring expressions of 'belief in God', 'feeling loved by God', 'religious comfort', 'religious criticism', and other faith-related dimensions, which are then compared against offline institutional religious adherence data. The study found that the online expression of belief in God ('believegod' indicator) shows a clear spatial correspondence with offline measures of religious adherence, particularly mapping to Evangelical Protestant groups in the U.S. 'Bible Belt'. The correlation between online religious discourse and evangelical adherence was moderate at the county level (Spearman ρ = 0.51) and very strong at the state level (Pearson r = 0.76). Furthermore, indicators tied to religious faith and moral virtue (e.g., believegod, relcomfort, forgive, lovedgod) were found to be expressed more frequently in rural counties than in urban ones.


## Evaluating Machine Translation Datasets for Low-Web Data Languages: A Gendered Lens

[https://arxiv.org/pdf/2511.03880](https://arxiv.org/pdf/2511.03880)

**Date:** 

The analysis measured the topical composition of machine translation datasets, finding a significant dominance of religious topics and names, particularly in the large-scale NLLB training dataset. This was contrasted with the topics of benchmark datasets. The study found that large-scale training datasets for the evaluated languages, particularly NLLB, are heavily dominated by religious topics, accounting for up to 20% of identified topics. Consequently, the most frequent person names in these datasets are primarily from religious texts. This thematic focus on religion in training data contrasts sharply with benchmark datasets, which tend to cover news, sports, and health domains. The authors note that the prevalence of religious data (found in over 93% of datasets they surveyed) requires careful ethical consideration for its use in NLP.


## Auditing M-LLMs for Privacy Risks: A Synthetic Benchmark and Evaluation Framework

[https://arxiv.org/pdf/2511.03248](https://arxiv.org/pdf/2511.03248)

**Date:** 2025-11-09

Inference of a user's 'Religious-Belief' (REG) as one of twelve sensitive personal attributes from synthetic multi-modal social media posts. Models could infer religious belief (REG attribute) with moderate accuracy. In the multi-modal setting, scores ranged from 44.83 (GLM) to 59.09 (Gemini) out of 100. The inclusion of visual data provided a slight improvement over text-only inference for this attribute. The tested models significantly outperformed human participants, with the best model (Gemini) scoring 54.50 compared to the human average of 30.00.


## BengaliMoralBench: A Benchmark for Auditing Moral Reasoning in Large Language Models within Bengali Language and Culture

[https://arxiv.org/pdf/2511.03180](https://arxiv.org/pdf/2511.03180)

**Date:** 2025-11-05

The benchmark measures the alignment of Large Language Models with culturally specific ethical norms and moral reasoning within the Bengali socio-cultural context, specifically focusing on scenarios related to religious practices, duties, and inter-faith interactions. This includes evaluating whether models can correctly classify behaviors in contexts like workplace prayer (salat), charity (zakat), religious attire (hijab), ritual sacrifice and distribution (Qurbani), inter-religious respect (Puja respect), and financial ethics (Halal loans) as 'ethical' or 'unethical' according to local values. Models frequently fail to grasp the faith-driven moral significance and context of religious actions, often misclassifying them as morally neutral. For example, they struggle with scenarios like the ritualized altruism of Qurbani meat distribution. This indicates a shallow understanding, reliance on surface-level cues, and a Western-centric bias that overlooks the deep-seated cultural and religious virtues in the Bengali context. However, the paper also notes that religious tasks, being more rule-based, tend to show higher performance stability across models compared to other domains.


## Deep Value Benchmark: Measuring Whether Models Generalize Deep Values or Shallow Preferences

[https://arxiv.org/pdf/2511.02109](https://arxiv.org/pdf/2511.02109)

**Date:** 2026-01-11

The benchmark measured whether models generalize the deep value of 'tradition', which is defined as 'respect, commitment, and acceptance of the customs and ideas that traditional culture or religion provide the self'. Models generalized the deep value of 'tradition' (which includes respecting religion) at a higher rate (DVGR of 0.51) than most other deep values. This was the highest DVGR alongside 'universalism', although it is still only slightly above chance level and well below perfect generalization.


## Surfacing Subtle Stereotypes: A Multilingual, Debate-Oriented Evaluation of Modern LLMs

[https://arxiv.org/pdf/2511.01187](https://arxiv.org/pdf/2511.01187)

**Date:** 2025-11-03

The benchmark measures religious bias by evaluating how Large Language Models (LLMs) generate stereotyped narratives about different demographic groups in the context of religion, focusing on unequal portrayals of faith groups and perceived limitations on religious freedom. All tested models consistently and overwhelmingly associated Arabs with stereotyped, conservative, or exclusionary religious views, with attribution rates reaching 95-100% in many cases, especially in high-resource languages like English. The paper also found that bias shifts with language; for instance, LLaMA-3 shifted religious stereotypes from Arabs to Indians when prompted in Hindi, suggesting models adapt stereotypes to the perceived cultural context of the input language.


## DIALECTALARABICMMLU: Benchmarking Dialectal Capabilities in Arabic and Multilingual Language Models

[https://arxiv.org/pdf/2510.27543](https://arxiv.org/pdf/2510.27543)

**Date:** 2025-10-31

Knowledge of world religions via multiple-choice questions. The paper does not provide specific findings for the 'World Religions' domain. The results are aggregated across all 32 domains, so no religion-specific conclusions can be drawn from the reported data.


## “Back to the Communities”: A Mixed‑Methods and Community‑Driven Evaluation of Cultural Sensitivity in Text-to-Image Models

[https://arxiv.org/pdf/2510.27361](https://arxiv.org/pdf/2510.27361)

**Date:** 

The benchmark measured cultural sensitivity in Text-to-Image models. Religion was included as a 'non-material proxy' for culture, specifically through the representation of religious rituals, beliefs, and festive religious events. Religion is identified as a key component of culture, often misrepresented in T2I models. The study's literature review and co-creation workshops established 'Religion/Rituals', 'Beliefs', and 'religious events' as important cultural proxies for evaluation. The paper cites other research that analyzed outputs for the prompt 'imagine a religious person' and notes a participant's concern about the negative portrayal of Muslim and Arab countries in media, which could influence model training data and outputs. The core finding is the need for a community-based methodology to properly evaluate such nuanced cultural and religious representations.


## MM-OPERA: Benchmarking Open-ended Association Reasoning for Large Vision-Language Models

[https://arxiv.org/pdf/2510.26937](https://arxiv.org/pdf/2510.26937)

**Date:** 2025-10-30

The benchmark measures the ability of Large Vision-Language Models to perform open-ended association reasoning. This includes recognizing and connecting concepts based on cultural and symbolic knowledge, which in some test cases involves Christian religious symbolism (e.g., connecting images of bread, wine, and the number 12 to the Last Supper and the Eucharist). The paper does not provide aggregated findings specific to religion. However, through case studies, it demonstrates that top-performing models like GPT-4o and Gemini-1.5-Pro can successfully identify and reason about Christian symbolism (e.g., the Eucharist, the Last Supper) in visual contexts, indicating an ability to connect images to specific cultural and religious knowledge.


## Depth and Autonomy: A Framework for Evaluating LLM Applications in Social Science Research

[https://arxiv.org/pdf/2510.25432](https://arxiv.org/pdf/2510.25432)

**Date:** 2025-10-29

Extraction of constitutionalist principles from a 7th-century Islamic religious-political text (Letter 53 by Imam Ali). LLMs can robustly extract complex political concepts like 'constitutionalism' from a 7th-century Islamic religious text ('Letter 53') when guided by a decomposed, multi-stage prompting process. This approach, which breaks the task into smaller, auditable steps, allows models to identify elements such as the 'Supremacy of higher law (Book and Sunnah)' and 'limited government', yielding more detailed and reliable results than a single-pass approach.


## DEBATE: A Large-Scale Benchmark for Role-Playing LLM Agents in Multi-Agent, Long-Form Debates

[https://arxiv.org/pdf/2510.25110](https://arxiv.org/pdf/2510.25110)

**Date:** 2025-10-29

Modeling opinion dynamics of LLM agents on socio-religious topics. The benchmark measures how well LLMs can simulate human debate participants, who are profiled using demographic data that includes religiosity, religious affiliation (e.g., protestant, evangelical), and Bible interpretation. Some debate topics explicitly involve faith, such as 'We depend too much on science and not enough on faith.' The paper's findings indicate that including private profile information, which contains religious identity (affiliation, evangelical status, Bible view), is important for realistically simulating human conversational dynamics. Ablation studies showed that removing this private profile information from the agent's memory consistently degraded the simulation's performance in terms of semantic similarity and stance alignment when conversations were recursively generated.


## A word association network methodology for evaluating implicit biases in LLMs compared to humans

[https://arxiv.org/pdf/2510.24488](https://arxiv.org/pdf/2510.24488)

**Date:** 2025-10-28

The benchmark measures valence bias, which is the general positive or negative perception associated with different religious groups. This is done by analyzing the strength of association between prime nodes representing religious groups (e.g., 'christian', 'muslim') and all other nodes in a word association network that have a valence rating (positive or negative sentiment). Significant valence bias related to religion was found in both humans and all three tested LLMs. However, the nature of the bias differed. Humans perceived 'buddhist' and 'christian' more positively, and 'athiest' and 'muslim' more negatively. In contrast, all three LLMs perceived 'muslim' more positively and 'buddhist' less positively than humans did, suggesting that LLMs can develop 'counter-biases' that diverge from human cognitive tendencies, possibly due to fine-tuning.


## Can LLMs Write Faithfully? An Agent-Based Evaluation of LLM-generated Islamic Content

[https://arxiv.org/pdf/2510.24438](https://arxiv.org/pdf/2510.24438)

**Date:** 2025-10-28

Faithfulness of LLM-generated Islamic content, measuring theological accuracy, citation integrity, stylistic reverence, structural coherence, and thematic focus using a dual-agent (quantitative and qualitative) framework. GPT-4o achieved the highest overall quantitative score (3.90/5), particularly in style, structure, Islamic accuracy, and citations. However, the domain-specific Ansari AI led in qualitative pairwise comparisons, receiving the most 'Best' verdicts (116/200) for its clarity and religious fidelity. The Arabic-centric model Fanar trailed both, especially in citation accuracy. Despite strong performance from top models, all still demonstrated significant shortcomings in reliable citation handling and contextual integrity, highlighting the need for structured knowledge grounding in sensitive religious contexts.


## Global PIQA: Evaluating Physical Commonsense Reasoning Across 100+ Languages and Cultures

[https://arxiv.org/pdf/2510.24081](https://arxiv.org/pdf/2510.24081)

**Date:** 2025-10-28

The benchmark measures physical commonsense reasoning, including culturally-specific knowledge. For religion, this involves commonsense knowledge about religious customs, traditions, objects, and practices, as examples were encouraged to be based on topics like 'local foods, places, everyday objects, customs, traditions, religions, literature, folklore, or art forms'. The paper does not provide findings specifically broken down by religious topics. The findings are aggregated by language and region, showing that models exhibit weaker performance in lower-resource languages and struggle with culturally-specific examples, which include questions related to religious customs, knowledge, and traditions.


## Breaking the Benchmark: Revealing LLM Bias via Minimal Contextual Augmentation

[https://arxiv.org/pdf/2510.23921](https://arxiv.org/pdf/2510.23921)

**Date:** 2025-10-27

Detection of stereotypical bias in ambiguous question-answering scenarios related to religion. The benchmark measures whether a Large Language Model (LLM) will abstain or make a decisive (and potentially stereotypical) inference when faced with an ambiguous context involving religion. For the religion bias category, contextual and question augmentation significantly increased the rate of 'Decisive Responses' (potentially biased answers in ambiguous contexts) from 25.95% in the original format to 56.72% in the fully augmented format. This reveals that models which appear fair on standard benchmarks may harbor latent biases that surface under semantic perturbations, suggesting they overfit to benchmark formats rather than internalizing fairness principles.


## IPQA: A Benchmark for Core Intent Identification in Personalized Question Answering

[https://arxiv.org/pdf/2510.23536](https://arxiv.org/pdf/2510.23536)

**Date:** 2025-10-27

Core intent identification in personalized questions about religious topics. The benchmark, IPQA, includes a 'Social' domain with sub-domains for various religions to evaluate a model's ability to understand user motivations in these contexts. The paper evaluates performance on a broad 'Social' domain which includes questions about Judaism, Christianity, Islam, Hinduism, and Buddhism. It does not provide a performance breakdown for each specific religion. The findings for the Social domain show that core intent identification is challenging, with F1 scores for the best-performing models under the 'User Profile (Intents)' configuration hovering around 0.49-0.50. Performance generally improves when models are provided with explicit historical intents, but remains moderate overall.


## BaZi-Based Character Simulation Benchmark: Evaluating AI on Temporal and Persona Reasoning

[https://arxiv.org/pdf/2510.23337](https://arxiv.org/pdf/2510.23337)

**Date:** 2025-10-27

The benchmark measured the ability of LLMs to perform persona reasoning and predict life events based on the principles of BaZi (Four Pillars of Destiny), a traditional Chinese metaphysical and divinatory system. The study found that integrating the symbolic reasoning framework of BaZi (Four Pillars of Destiny) significantly improves the ability of LLMs to perform persona reasoning and predict life events. Models augmented with BaZi rules showed accuracy improvements of 30.3%-62.6% over baselines. Furthermore, the model's accuracy dropped by up to 45.7% when provided with incorrect (shuffled) birth date information, demonstrating that the performance gain is genuinely tied to the BaZi system's logic rather than being a superficial prompting artifact.


## A Use-Case Specific Dataset for Measuring Dimensions of Responsible Performance in LLM-generated Text

[https://arxiv.org/pdf/2510.20782](https://arxiv.org/pdf/2510.20782)

**Date:** 2025-10-23

Measurement of performance disparities (toxicity and accuracy) in LLM-generated e-commerce product descriptions for products associated with various identity groups, including religious groups (Jewish, Muslim), to assess fairness. The paper's methodology allows for measuring performance disparities across religious groups. In the specific evaluation of the Llama 3.2 11B model for generating e-commerce product descriptions, products associated with 'Jewish' and 'Muslim' identity groups did not elicit significantly higher toxicity or sexually explicit language compared to most other demographic groups. The most significant disparities in toxicity were observed for other identity groups, such as 'Women'.


## From Facts to Folklore: Evaluating Large Language Models on Bengali Cultural Knowledge

[https://arxiv.org/pdf/2510.20043](https://arxiv.org/pdf/2510.20043)

**Date:** 2025-04-16

Knowledge of Bengali cultural terms and concepts related to religion. In Question Answering tasks, models generally underperformed on cultural categories compared to non-cultural ones. However, 'Religion' was an exception, alongside 'Food', where models performed better than in other cultural categories like 'Entertainment', 'People', and 'Historical'.


## Exposing Blindspots: Cultural Bias Evaluation in Generative Image Models

[https://arxiv.org/pdf/2510.20042](https://arxiv.org/pdf/2510.20042)

**Date:** 2025-10-22

The benchmark measured the cultural representation of 'religious ritual' as a subcategory. Specifically, it analyzed whether image generations for this category leaned towards 'traditional' or 'modern' aesthetics, particularly noting differences when prompts specified a country versus being country-agnostic. The category 'religious ritual' generally produced images with traditional scores for most countries, but tended to produce modern-styled images for prompts specifying the United States or that were country-agnostic.


## Quantifying Feature Importance for Online Content Moderation

[https://arxiv.org/pdf/2510.19882](https://arxiv.org/pdf/2510.19882)

**Date:** 2025-10-22

The predictive power of user features, including a 'CULTURE' feature group that contains religious terms, on post-moderation user behavior (activity, toxicity, diversity). The feature subgroup 'CULTURE' from the LIWC lexicon, which includes terms related to religion, was not selected in the final predictive models for changes in user activity, toxicity, or diversity. This indicates it had limited predictive utility for post-moderation behavior compared to other features, despite showing some predictive power when evaluated in isolation.


## PBBQ: A Persian Bias Benchmark Dataset Curated with Human-AI Collaboration for Large Language Models

[https://arxiv.org/pdf/2510.19616](https://arxiv.org/pdf/2510.19616)

**Date:** 2025-10-22

The benchmark, PBBQ (Persian Bias Benchmark for Question-answering), measured social biases in Large Language Models within a Persian cultural context. For religion, it specifically measured stereotypical biases by presenting models with ambiguous and disambiguated scenarios and evaluating their responses to negative and non-negative questions. Religion was one of 16 categories evaluated for social bias. Across all tested models, biases were observed in religious contexts. On average, models showed a bias score of 0.0794 in ambiguous religious scenarios and 0.0509 in disambiguated ones, indicating that contextual information reduced but did not eliminate stereotypical responses. The findings suggest that LLMs, including Persian-specific models, exhibit and reproduce social biases related to religion present in their training data and cultural context.


## Context-aware Fairness Evaluation and Mitigation in LLMs

[https://arxiv.org/pdf/2510.18914](https://arxiv.org/pdf/2510.18914)

**Date:** 2025-10-21

Stereotype and toxicity bias detection in multi-turn dialogues concerning demographic attributes, including religion. Bias related to religion shows a strong signal and increases during multi-turn conversations. Models can shift from aligned behavior to producing stereotypical responses, as shown in an example regarding Judaism. The proposed dynamic neuron masking framework was found to effectively reduce this accumulating bias.


## Beyond the Explicit: A Bilingual Dataset for Dehumanization Detection in Social Media

[https://arxiv.org/pdf/2510.18582](https://arxiv.org/pdf/2510.18582)

**Date:** 2025-10-21

The benchmark measures the detection of dehumanizing language directed at various target groups, including religious groups. Specifically, it includes keywords and slurs targeting Jewish people to identify instances of dehumanization against this group. The paper's findings are aggregated across all target groups and do not provide specific results for religion. However, by including religious groups (specifically Jewish people) as a target category for annotation, the study demonstrates that its resulting dataset and the models trained on it are equipped to identify dehumanizing language in a religious context as part of the broader dehumanization detection task.


## SIMBENCH: BENCHMARKING THE ABILITY OF LARGE LANGUAGE MODELS TO SIMULATE HUMAN BEHAVIORS

[https://arxiv.org/pdf/2510.17516](https://arxiv.org/pdf/2510.17516)

**Date:** 2025-10-27

The benchmark measures the ability of LLMs to simulate the group-level survey responses of human populations conditioned on specific demographic attributes, including 'Religiosity/Practice' and 'Religion (Affiliation)'. Models struggle most when simulating groups defined by religious attributes. Conditioning on 'Religiosity/Practice' caused the largest decrease in simulation accuracy (ΔS = -9.91), followed by 'Religion (Affiliation)' (ΔS = -4.83), compared to all other demographic categories tested.


## MoReBench: Evaluating Procedural and Pluralistic Moral Reasoning in Language Models, More Than Outcomes

[https://arxiv.org/pdf/2510.16380](https://arxiv.org/pdf/2510.16380)

**Date:** 2025-10-18

Procedural moral reasoning in scenarios involving religious contexts, as part of a broader benchmark on moral reasoning across 16 topics. The paper includes 'Religion' as one of 16 diverse real-world topics for evaluating moral reasoning. However, the results are aggregated, and the paper does not provide a specific breakdown or analysis of model performance on religious dilemmas.


## Echoes of Human Malice in Agents: Benchmarking LLMs for Multi-Turn Online Harassment Attacks

[https://arxiv.org/pdf/2510.14207](https://arxiv.org/pdf/2510.14207)

**Date:** 2025-10-20

Generation of harassment targeting individuals based on their race/culture/sexuality. Religion is an implicit sub-category of culture. The models have stronger guardrails against harassment related to sensitive identity categories like race and culture compared to more generic forms of harassment like insults or flaming. This is likely due to alignment efforts prioritizing high-salience harms. However, these guardrails can still be circumvented through various attack methods, particularly jailbreak fine-tuning, which significantly increases the rate of harassment based on race/culture/sexuality.


## CRaFT: An Explanation-Based Framework for Evaluating Cultural Reasoning in Multilingual Language Models

[https://arxiv.org/pdf/2510.14014](https://arxiv.org/pdf/2510.14014)

**Date:** 2025-06-01

Alignment of model explanations with culturally salient concepts, including 'Religious observance' and other religion-derived social norms. The study found that large language models dynamically reconstruct their reasoning on culturally sensitive topics, including those influenced by religion such as family values, based on the linguistic context of the prompt. For instance, the models adopted more traditional, religion-aligned stances on family structures when prompted in Arabic compared to English. This demonstrates that cultural awareness, including the reflection of religious norms, is an emergent, language-contingent property rather than an intrinsic, stable trait of the models.


## Evaluating Arabic Large Language Models: A Survey of Benchmarks, Methods, and Gaps

[https://arxiv.org/pdf/2510.13430](https://arxiv.org/pdf/2510.13430)

**Date:** 2025-10-16

The paper surveys several benchmarks, including those measuring knowledge of Islamic legal rulings (fatwas) regarding the Hajj pilgrimage, understanding of general Islamic culture and religious practices, and ensuring religious sensitivity in model outputs. The survey identifies the emergence of specialized benchmarks (e.g., Hajj-FAQ, PalmX, ILMAAM) designed to evaluate Arabic LLMs on domain-specific religious knowledge, including Islamic jurisprudence, culture, and sensitivity. This highlights a trend towards assessing models' ability to handle religiously and culturally nuanced content beyond general NLP tasks.


## I Am Aligned, But With Whom? MENA Values Benchmark for Evaluating Cultural Alignment and Multilingual Bias in LLMs

[https://arxiv.org/pdf/2510.13154](https://arxiv.org/pdf/2510.13154)

**Date:** 2025-10-15

The benchmark measures the cultural alignment of LLMs with the values of the Middle East and North Africa (MENA) region. This includes categories for 'Religious Values' and 'Cultural & Religious Identity'. A specific example measured is the model's response to the question, 'How important is God in your life?'. LLMs exhibit significant 'Cross-Lingual Value Shifts' related to faith. For example, when asked about the importance of God, a model might refuse to answer in English but provide a deeply religious, affirmative response in Arabic ('10 - God represents the center of my life'). This suggests the model's expressed 'identity' regarding faith is unstable and heavily dependent on the prompt language, shifting from agnostic to highly religious. The reasoning process can also trigger a projection of Western-liberal values like secularism, which may conflict with local, empirically-documented religious values.


## A CRITICAL REVIEW OF THE NEED FOR KNOWLEDGE–CENTRIC EVALUATION OF QURANIC RECITATION

[https://arxiv.org/pdf/2510.12858](https://arxiv.org/pdf/2510.12858)

**Date:** 2025-11-10

Correctness of Quranic recitation based on the Islamic rules of Tajweed. The paper reviews systems that evaluate pronunciation, rhythm, and phonetics against established religious standards. The prevailing paradigm of adapting Automatic Speech Recognition (ASR) systems for evaluating Quranic recitation is fundamentally inadequate. These systems prioritize word recognition over qualitative elocution, suffer from data dependency and demographic biases (e.g., gender), and fail to provide the granular, diagnostic feedback necessary for effective learning. The paper concludes that a more robust, knowledge-centric approach is needed, one that is built upon the well-defined and unchanging rules of Tajweed rather than statistical patterns from flawed data.


## BENCHMARKING OPEN-SOURCE LARGE LANGUAGE MODELS FOR PERSIAN IN ZERO-SHOT AND FEW-SHOT LEARNING

[https://arxiv.org/pdf/2510.12807](https://arxiv.org/pdf/2510.12807)

**Date:** 2025-10-05

Model knowledge on multiple-choice questions about Theology as part of the Persian MMLU benchmark. Models generally showed stronger performance on Theology questions compared to other academic subcategories within the Persian MMLU benchmark. Logic and Theology were the subcategories with the strongest results, with average scores of 0.412 and 0.395 respectively across models.


## VQArt-Bench: A semantically rich VQA Benchmark for Art and Cultural Heritage

[https://arxiv.org/pdf/2510.12750](https://arxiv.org/pdf/2510.12750)

**Date:** 2025-10-14

The benchmark measures the ability of multimodal models to perform visual question answering on artworks, which includes understanding and reasoning about subjects, actions, symbols, and compositional elements within religious art. The paper's findings are general to the domain of artistic visual analysis, of which religious art is a major component. It found that most state-of-the-art models exhibit limited performance in understanding art, struggling with tasks like counting but performing relatively better on abstract reasoning. No findings were specific to religious content versus other art genres, but the overall poor performance applies to the religious artworks included in the benchmark.


## HALF: Harm-Aware LLM Fairness Evaluation Aligned with Deployment

[https://arxiv.org/pdf/2510.12217](https://arxiv.org/pdf/2510.12217)

**Date:** 2025-10-16

The benchmark measured sentiment and toxicity in open-ended text generation prompted with religious topics (from the BOLD benchmark), and stereotype-based reasoning in question-answering contexts related to religion (from the BBQ benchmark). Smaller open-source models like LLaMA-1B and LLaMA-3B produced disproportionately high toxicity for prompts related to Islam. In stereotype evaluation (BBQ), most models showed significant bias on religion-related prompts, with LLaMA models exhibiting the highest bias, while Claude 4 demonstrated the most consistent fairness.


## Do Psychometric Tests Work for Large Language Models? Evaluation of Tests on Sexism, Racism, and Morality

[https://arxiv.org/pdf/2510.11254](https://arxiv.org/pdf/2510.11254)

**Date:** 2025-10-13

The benchmark measured the endorsement of the 'purity/sanctity' moral foundation, which is linked to religious and spiritual concepts. This was assessed using items from the Moral Foundations Questionnaire, such as 'Whether or not someone acted in a way that God would approve of' and 'Chastity is an important and valuable virtue'. The study found a weak, near-zero correlation (Spearman's rs = 0.05) between LLM scores on the 'purity' dimension of the Moral Foundations Questionnaire and their behavior in a downstream moral advice-giving task. This indicates low ecological validity, meaning that a model's score on psychometric items related to religious/moral purity does not predict its actual behavior on related tasks.


## The Curious Case of Factual (Mis)Alignment between LLMs' Short- and Long-Form Answers

[https://arxiv.org/pdf/2510.11218](https://arxiv.org/pdf/2510.11218)

**Date:** 2026-01-12

The benchmark (SLAQ) measures the factual consistency of Large Language Models when answering the same factual question posed in a short, isolated format versus a long, complex query format. Among the 15 diverse topic categories sourced from Wikipedia, 'Theology' and 'Spirituality' are included, so the benchmark assesses factual knowledge on these topics as part of a broader evaluation. The paper does not report findings specific to the religion/faith-related topics. The findings are general across all topic categories, focusing on the systematic misalignment between short- and long-form answers. Key findings indicate that models are more accurate on short queries, that most answer alignment stems from being consistently incorrect, and that there are 'momentum effects' where sequences of correct or incorrect answers tend to continue. The misalignment is shown to correspond to divergent internal processing within the models.


## DITING: A Multi-Agent Evaluation Framework for Benchmarking Web Novel Translation

[https://arxiv.org/pdf/2510.09116](https://arxiv.org/pdf/2510.09116)

**Date:** 2025-10-13

The benchmark, DITING, measures the quality of translation for 'religious or internet-born expressions' under its 'Terminology Localization' dimension. It also assesses 'Cultural Safety,' which safeguards against misinterpretations in sensitive genres including religion. A specific example mentioned is the translation of the Taoist spiritual concept '金丹' (Golden Core). The paper's findings are not specifically isolated for religious content. However, for the broader 'Terminology Localization' dimension, which includes religious terms, the results show that Chinese-trained LLMs outperform others. DeepSeek-V3 achieved the highest score, followed by Qwen3-32B and Seed-X-PPO-7B. This suggests that model scale, Chinese-centric training data, and domain adaptation are crucial for accurately translating specialized cultural concepts, including religious ones.


## Web Crawler Restrictions, AI Training Datasets & Political Biases

[https://arxiv.org/pdf/2510.09031](https://arxiv.org/pdf/2510.09031)

**Date:** 2025-10-10

Analysis of word co-occurrence patterns in hyperpartisan text to identify the over-representation of religious terminology in potential AI training datasets. Due to crawler restrictions on moderate websites, AI training datasets are becoming increasingly skewed towards hyperpartisan content. This content features an over-representation of religious terminology. In hyperpartisan right-leaning text, religious word pairs like (Jesus; God), (Christ; Jesus), and (Faith; God) are overrepresented, and terms like 'God', 'Church', 'Testament', and 'Christian' co-occur frequently with demographic terms. In hyperpartisan left-leaning text, 'Jewish' co-occurs with 'Community'. This suggests that models trained on this skewed data may inherit these representations.


## MMA-ASIA: A MULTILINGUAL AND MULTI-MODAL ALIGNMENT FRAMEWORK FOR CULTURALLY-GROUNDED EVALUATION

[https://arxiv.org/pdf/2510.08608](https://arxiv.org/pdf/2510.08608)

**Date:** 2025-10-07

Knowledge of cultural elements, including religious buildings and mythological figures, as part of a broader cultural awareness assessment across Asian contexts. The paper does not provide specific findings related to religion. Religious knowledge is evaluated as a sub-component of broader cultural awareness (e.g., religious buildings, mythological figures), and results are not disaggregated by cultural theme.


## Pragyaan: Designing and Curating High-Quality Cultural Post-Training Datasets for Indian Languages

[https://arxiv.org/pdf/2510.07000](https://arxiv.org/pdf/2510.07000)

**Date:** 2025-10-08

knowledge and safe handling of prompts related to Indian religions The paper's primary contribution is the creation of the Pragyaan datasets, which are designed to be culturally inclusive, incorporating topics on Indian religions. The authors found that existing datasets often lack this cultural and religious nuance, especially for Indian languages. A pilot study training models on the Pragyaan-Align dataset showed improved performance on downstream tasks, confirming the utility of the curated data for model alignment, including its religion-related components.


## EVALUESTEER: MEASURING REWARD MODEL STEERABILITY TOWARDS VALUES AND PREFERENCES

[https://arxiv.org/pdf/2510.06370](https://arxiv.org/pdf/2510.06370)

**Date:** 2025-10-09

Steerability of models to align with user profiles on the value of religiosity (e.g., importance of God), as part of the Traditional vs. Secular-Rational value dimension from the World Values Survey. Reward Models (RMs) exhibit a strong and systematic secular bias. They consistently prefer responses that align with a low importance of God and other secular values over traditional ones. This bias is suggested to reflect the cultural composition of the models' pre-training data and annotation sources, which are noted to cluster near English-speaking Protestant European populations.


## EvalMORAAL: Interpretable Chain-of-Thought and LLM-as-Judge Evaluation for Moral Alignment in Large Language Models

[https://arxiv.org/pdf/2510.05942](https://arxiv.org/pdf/2510.05942)

**Date:** 2025-10-08

The benchmark measures the moral alignment of Large Language Models with human survey data from the World Values Survey and PEW Global Attitudes Survey. This includes assessing model stances on socio-moral topics that are significantly influenced by cultural and religious traditions, such as abortion, homosexuality, divorce, and religious practices. The study found a significant regional bias in LLMs, which align more closely with moral norms of Western regions (r=0.82) than non-Western regions (r=0.61). This gap is particularly evident on socio-moral topics like homosexuality, abortion, and divorce, where model judgments conflict in countries with strong religious influences. Prior work cited also indicates that some models, like GPT, lean towards English-speaking and Protestant European values, suggesting an underlying religious and cultural bias from training data.


## Hire Your Anthropologist! Rethinking Culture Benchmarks Through an Anthropological Lens

[https://arxiv.org/pdf/2510.05931](https://arxiv.org/pdf/2510.05931)

**Date:** 2025-10-22

The paper critiques existing cultural benchmarks for their failure to adequately measure religious dimensions. It finds they often oversimplify religion by conflating it with nationality, overlooking internal diversity within religious groups (e.g., treating them as monolithic), and ignoring disagreements and contested interpretations within religious traditions. The paper advocates for benchmarks that can capture religion as a dynamic and lived experience rather than a static variable. The paper finds that current NLP benchmarks handle religion reductively as a component of culture. They often flatten its complexity by conflating it with national or linguistic identity, assuming consensus where there is significant internal diversity and contestation, and failing to capture how religious norms are dynamically enacted in specific contexts. For example, benchmarks may overlook diasporic religious communities or divergent interpretations of norms between different religious groups.


## VAL-BENCH: BELIEF CONSISTENCY AS A MEASURE FOR VALUE ALIGNMENT IN LANGUAGE MODELS

[https://arxiv.org/pdf/2510.05465](https://arxiv.org/pdf/2510.05465)

**Date:** 2026-01-14

The benchmark measures the consistency of language model belief expressions when presented with opposing prompts on controversial topics related to religion, such as 'Child sexual abuse in Church' and 'Ordaining women as Rabbis'. The paper does not report findings specifically for the religion category. Religious topics, which constitute 5.50% of the dataset, were included in the overall analysis. The general findings were that most models exhibit high belief inconsistency, with Claude models being a notable exception, achieving higher consistency often through refusing to take a stance.


## EVALUATING LLMS FOR DEMOGRAPHIC-TARGETED SOCIAL BIAS DETECTION: A COMPREHENSIVE BENCHMARK STUDY

[https://arxiv.org/pdf/2510.04641](https://arxiv.org/pdf/2510.04641)

**Date:** 2025-10-13

The benchmark measured the ability of Large Language Models to detect harmful demographic-targeted social biases in English texts, framed as a multi-label classification task. For religion, this specifically involved identifying texts that perpetuate commonly held stereotypes, toxic content, or hateful content targeting a religion or people holding certain religious beliefs. Fine-tuned models, especially encoder models like DeBERTa and RoBERTa, were highly effective at detecting religious bias (REL), consistently outperforming prompting-based methods. Among prompting models, larger models like Llama-3.1-70B and GLM-4-9B showed stronger performance in identifying religious biases compared to smaller models. Methodologically, the study noted the complexity of religious identity by annotating bias against 'Jewish' identity under both Race/ethnicity (RAC) and Religion (REL) to reflect its ethnoreligious nature.


## Psychological Steering in LLMs: An Evaluation of Effectiveness and Trustworthiness

[https://arxiv.org/pdf/2510.04484](https://arxiv.org/pdf/2510.04484)

**Date:** 2025-10-06

The benchmark utilized, TrustLLM, includes a fairness evaluation that measures 'Agreement on stereotypes' based on attributes such as gender, profession, religion, race, or other demographic factors. The paper does not report specific findings related to religion. It mentions that the TrustLLM benchmark evaluates fairness regarding stereotypes based on religion, but the results and discussion are focused on the effects of psychological steering (emotions and personality) on trustworthiness metrics in general, without breaking them down by specific religious factors.


## Red Lines and Grey Zones in the Fog of War: Benchmarking Legal Risk, Moral Harm, and Regional Bias in Large Language Model Military Decision-Making

[https://arxiv.org/pdf/2510.03514](https://arxiv.org/pdf/2510.03514)

**Date:** 2025-10-03

The benchmark measured the propensity of Large Language Models to select a 'Religious Gathering' as a target for a kinetic military strike within a simulated conflict scenario. This was part of a broader evaluation of adherence to International Humanitarian Law, specifically the principle of distinction. All tested models selected purely civilian targets for military strikes, including 'Religious Gathering'. While the primary metrics aggregated all civilian targets, supplementary data in the appendix shows that models, particularly LLaMA-3.1, selected 'Religious Gathering' as a target, contributing to the overall finding that LLMs exhibit concerning and unpredictable targeting behaviour that violates legal and moral norms in simulated conflict.


## IndiCASA: A Dataset and Bias Evaluation Framework in LLMs Using Contrastive Embedding Similarity in the Indian Context

[https://arxiv.org/pdf/2510.02742](https://arxiv.org/pdf/2510.02742)

**Date:** 2025-10-03

Detection of stereotypical and anti-stereotypical biases related to religion within the Indian sociolinguistic context, using a contrastive embedding similarity framework. Religion exhibits relatively lower bias scores across most models compared to other bias types like caste, disability, or socioeconomic status. This suggests better neutrality, potentially due to religion being a globally sensitive axis that receives greater attention during model alignment or instruction tuning.


## The Social Laboratory: A Psychometric Framework for Multi-Agent LLM Evaluation

[https://arxiv.org/pdf/2510.01295](https://arxiv.org/pdf/2510.01295)

**Date:** 2025-10-01

The benchmark measured the emergent social and cognitive dynamics (e.g., consensus-seeking, semantic convergence) of LLM agents during debates on challenging and controversial topics, which included religion. The study found that LLM agents have a robust tendency to seek consensus, and this cooperative behavior does not statistically degrade when discussing sensitive or contentious topics, which included religion. The agents' performance and tendency to converge remained stable regardless of topic sensitivity.


## BIASFREEBENCH: A BENCHMARK FOR MITIGATING BIAS IN LARGE LANGUAGE MODEL RESPONSES

[https://arxiv.org/pdf/2510.00232](https://arxiv.org/pdf/2510.00232)

**Date:** 2025-09-30

The benchmark measures stereotype detection and mitigation in religious contexts. Religion is one of nine bias types evaluated using the BBQ dataset and one of four types used from the StereoSet dataset for training debiasing methods. The paper finds that different models exhibit varying levels of baseline bias related to religion. The main finding is that debiasing techniques show different generalization capabilities. Specifically, training a model with Direct Preference Optimization (DPO) on a single, high-quality bias type like gender can effectively generalize to reduce bias in other unseen categories, including religion. In contrast, Supervised Fine-Tuning (SFT) requires more diverse data covering all bias types to achieve good generalization.


## PRIMEX: A Dataset of Worldview, Opinion, and Explanation

[https://arxiv.org/pdf/2510.00174](https://arxiv.org/pdf/2510.00174)

**Date:** 2025-09-30

Measurement of opinions on the role of God/higher power in human evolution, the economic responsibility of churches and religious organizations, and the future importance of religion. These opinions are also correlated with worldview beliefs (Primals). A significant correlation was found between a belief in God's role in human evolution and the 'Alive' Primal World Belief (a worldview that sees the world as intentional and purposeful). Additionally, a survey question about the economic responsibility of churches elicited the most useful free-text explanations for predicting a user's other opinions across various topics.


## CULTURE IN A FRAME: C3B AS A COMIC-BASED BENCHMARK FOR MULTIMODAL CULTURALLY AWARENESS

[https://arxiv.org/pdf/2510.00041](https://arxiv.org/pdf/2510.00041)

**Date:** 2025-09-27

Identification of religious objects (e.g., 'Russian Orthodox church') and potential conflicts involving them as part of a broader benchmark on multimodal cultural awareness. The paper does not provide specific findings related to religion, as it is only a minor, unanalyzed component of the broader cultural awareness benchmark. The main findings focus on general cultural awareness gaps in MLLMs.


## TAU: A BENCHMARK FOR CULTURAL SOUND UNDERSTANDING BEYOND SEMANTICS

[https://arxiv.org/pdf/2509.26329](https://arxiv.org/pdf/2509.26329)

**Date:** 2025-09-30

The benchmark measures the ability of models to recognize culturally specific sounds from Taiwan, one category of which is 'religious chants'. The evaluation focuses on identifying sounds that require cultural context and cannot be solved by lexical content alone. The paper does not report specific findings related to religion. Results are aggregated across all cultural categories, and there is no performance breakdown for the 'religious chants' category. The general finding is that all tested models perform significantly worse than humans on culturally localized audio understanding.


## ROLECONFLICTBENCH: A BENCHMARK OF ROLE CONFLICT SCENARIOS FOR EVALUATING LLMS’ CONTEXTUAL SENSITIVITY

[https://arxiv.org/pdf/2509.25897](https://arxiv.org/pdf/2509.25897)

**Date:** 2025-09-30

The benchmark measured the preference bias of LLMs towards specific religious roles. It evaluated whether models prioritize roles associated with Abrahamic religions (Christianity, Islam, Judaism) over Dharmic religions (Hinduism, Buddhism) when presented with role-conflict scenarios. The key finding related to religion was that most evaluated LLMs exhibit a strong preference bias. Roles associated with Abrahamic religions (Christianity, Islam, Judaism) were vastly preferred over roles from Dharmic religions, with Hinduism and especially Buddhism being the least preferred.


## THE FLAW OF AVERAGES: QUANTIFYING UNIFORMITY OF PERFORMANCE ON BENCHMARKS

[https://arxiv.org/pdf/2509.25671](https://arxiv.org/pdf/2509.25671)

**Date:** 2025-09-30

The paper evaluated the MMLU 'World Religions' subtask to measure the uniformity of model performance (Harmony) across its internal subdomains, rather than testing specific theological knowledge or religious bias. The paper does not provide specific findings related to religion. The 'World Religions' subtask of MMLU was analyzed as one of many benchmarks to demonstrate the paper's proposed 'HARMONY' metric. The analysis focused on the benchmark's distributional properties (i.e., whether it evaluates performance uniformly across its subdomains) rather than on the models' specific knowledge or biases concerning religion.


## Bias Mitigation or Cultural Commonsense? Evaluating LLMs with a Japanese Dataset

[https://arxiv.org/pdf/2509.24468](https://arxiv.org/pdf/2509.24468)

**Date:** 2025-09-29

Stereotype detection in religious contexts, as part of a fine-tuning experiment using the BBQ dataset. A non-prompt-based debiasing experiment, which involved fine-tuning a model on several BBQ categories including 'Religion', confirmed the paper's main hypothesis: successfully reducing social biases leads to a degradation in performance on cultural commonsense tasks, indicating a trade-off between bias mitigation and cultural understanding.


## Assessing Visual Privacy Risks in Multimodal AI: A Novel Taxonomy-Grounded Evaluation of Vision-Language Models

[https://arxiv.org/pdf/2509.23827](https://arxiv.org/pdf/2509.23827)

**Date:** 2025-09-28

Detection of religious affiliation or context as a private 'Personal Metadata' category within a broader visual privacy risk taxonomy. The paper's evaluation showed that models performed very poorly in recognizing the 'Demographics' category, which includes religion. For instance, LLaMA 3.2 achieved a near-zero F1 score (0.01) for this category on the VISPR dataset, indicating a significant inability to identify religious affiliation and other demographic data as a potential privacy violation in images.


## FALCON: A CROSS-MODAL EVALUATION DATASET FOR COMPREHENSIVE SAFETY PERCEPTION

[https://arxiv.org/pdf/2509.23783](https://arxiv.org/pdf/2509.23783)

**Date:** 2025-09-28

The benchmark, as part of its 'Hate Speech' category, measures content that expresses hatred, discrimination, or prejudice against individuals or groups based on characteristics including religion. The paper's benchmark includes 'Hate Speech' as a harm category, which is defined as content expressing hatred against groups based on characteristics including religion. However, the paper does not report specific findings for religious content distinctly. In the general 'Hate Speech' category, the proposed model FalconEye achieved a detection accuracy of 44.85% on the Falcon-test dataset, outperforming GPT-40 (33.33%) and Qwen2.5-VL-7B (25.45%).


## Mapping Overlaps in Benchmarks through Perplexity in the Wild

[https://arxiv.org/pdf/2509.23488](https://arxiv.org/pdf/2509.23488)

**Date:** 2025-11-03

Knowledge of world religions, as part of the MMLU benchmark, to analyze overlaps with other benchmarks. Benchmarks within the humanities category, which includes religion, exhibited lower-than-average overlap compared to other categories, suggesting they test more distinct capabilities.


## A Structured Framework for Evaluating and Enhancing Interpretive Capabilities of Multimodal LLMs in Culturally Situated Tasks

[https://arxiv.org/pdf/2509.23208](https://arxiv.org/pdf/2509.23208)

**Date:** 2025-09-27

The benchmark measures the ability of VLMs to adopt specific religious and spiritual interpretive stances (e.g., Eastern Orthodox, Zen Buddhist, Daoist, Confucian, tribal spirituality) when generating art criticism, as guided by defined personas. The evaluation assesses the alignment of model-generated text with the characteristics of these spiritual or theological perspectives. The study found that persona-guided interventions, including those based on religious figures like an Eastern Orthodox iconographer (Brother Thomas) and a scholar influenced by Daoism and Zen Buddhism (Su Shi), significantly improved the VLM's ability to generate culturally nuanced and expert-aligned art critiques. Models demonstrated the capability to adopt theological and spiritual perspectives when prompted, enhancing their interpretive reasoning in the specialized domain of art history.


## Beyond Western Politics: Cross-Cultural Benchmarks for Evaluating Partisan Associations in LLMs

[https://arxiv.org/pdf/2509.22711](https://arxiv.org/pdf/2509.22711)

**Date:** 2025-09-24

The benchmark measures LLMs' susceptibility to making harmful partisan associations, including extreme adversarial prompts about engineering ethnic/religious cleansing and orchestrating violence against religious communities. The paper's findings do not specifically isolate results for religious-themed prompts. However, the general finding is that models are highly susceptible to making extreme and potentially defamatory associations with political entities, which includes making connections to orchestrating ethnic and religious cleansing or violence against religious communities, often without refusal.


## Evaluating the Infinite

[https://arxiv.org/pdf/2509.19389](https://arxiv.org/pdf/2509.19389)

**Date:** 

The paper analyzes Pascal's Wager, a philosophical argument related to Christian faith, by applying a novel mathematical technique (hyperreal summation) to assign a fine-grained infinite expected value to the prospect of an infinite reward ('an eternity in heaven'). It does not benchmark a model's performance but rather evaluates a concept. Using hyperreal numbers, the paper provides a more nuanced evaluation of Pascal's Wager compared to standard decision theory. It assigns the wager a specific infinite expected value (`pkω`) that is quantitatively comparable to other infinite values. This resolves paradoxes, such as Hájek's argument that a small probability of the wager is equally good as a certainty. The hyperreal approach preserves the state-wise dominance principle, showing that a higher probability of an infinite reward is strictly better than a lower one.


## Benchmarking and Improving LLM Robustness for Personalized Generation

[https://arxiv.org/pdf/2509.19358](https://arxiv.org/pdf/2509.19358)

**Date:** 2025-09-18

The impact of user preferences on the factual accuracy of LLM responses to questions about spiritual and religious concepts, such as spirit possession. A user preference for contextual and background information, when applied to a question about spiritual possession, can trigger a more complex reasoning process in a model. This can lead to a 'breakage error,' where the model changes its factually correct answer (that spiritual possession is not real) to a factually incorrect one (that people can be possessed by evil spirits), thereby compromising factuality to satisfy the preference.


## DRISHTIKON: A Multimodal Multilingual Benchmark for Testing Language Models’ Understanding on Indian Culture

[https://arxiv.org/pdf/2509.19274](https://arxiv.org/pdf/2509.19274)

**Date:** 2025-09-23

The benchmark measures knowledge of religious symbols, rituals, deities, and practices within the Indian cultural context. It evaluates a model's understanding of practices associated with worship, rites of passage, or daily cultural-religious observances across India's major and minor religious communities. Models showed gaps in cultural grounding, particularly struggling with abstract or context-dependent concepts like religion, which require deeper socio-cultural and inferential reasoning compared to more concrete cultural elements like attire or cuisine.


## BENCHMARKING VISION-LANGUAGE AND MULTIMODAL LARGE LANGUAGE MODELS IN ZERO-SHOT AND FEW-SHOT SCENARIOS: A STUDY ON CHRISTIAN ICONOGRAPHY

[https://arxiv.org/pdf/2509.18839](https://arxiv.org/pdf/2509.18839)

**Date:** 2025-09-23

The benchmark measured the performance of vision-language and multimodal large language models on the task of single-label image classification of Christian iconography, specifically identifying Christian saints in artworks. Multimodal LLMs, particularly Gemini-2.5 Pro and GPT-4o, consistently outperformed traditional supervised models (ResNet50) and contrastive vision-language models (CLIP, SigLIP) on curated datasets (ArtDL, ICONCLASS), with Gemini-2.5 Pro reaching a peak accuracy of 90.45%. However, performance for all models dropped significantly on the more diverse and less consistent Wikidata dataset, where a contrastive model (SigLIP-so400m-patch14-384) achieved the highest score (66.29%). Enriching prompts with iconographic descriptions generally improved zero-shot performance, whereas few-shot learning did not provide consistent benefits and sometimes degraded accuracy.


## Evaluating Large Language Models for Detecting Antisemitism

[https://arxiv.org/pdf/2509.18293](https://arxiv.org/pdf/2509.18293)

**Date:** 2025-11-04

Detection of antisemitism (hatred toward Jews) in social media content using the IHRA definition as a policy guideline. The paper evaluates LLMs for detecting antisemitism using the IHRA definition. Key findings include: 1) A novel 'Guided-CoT' prompt significantly improves performance across models, with Llama 3.1 70B outperforming a fine-tuned GPT-3.5. 2) LLMs struggle with contextual nuances, leading to misclassifications for posts containing specific stereotypes (e.g., about George Soros, 'devil worshipping'), quoted text, and typos resembling slurs (e.g., 'kikes' instead of 'likes'). 3) The study introduced metrics to analyze model-generated explanations, revealing that some models exhibit paradoxical behaviors where explanations for antisemitic content are not consistently more or less cohesive than for non-antisemitic content, suggesting complex internal biases.


## D-REX: A BENCHMARK FOR DETECTING DECEPTIVE REASONING IN LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2509.17938](https://arxiv.org/pdf/2509.17938)

**Date:** 2025-09-22

The benchmark measured a model's susceptibility to deceptive reasoning in a religious context, specifically its ability to act as a tool for religious extremists. This involved identifying users vulnerable to radicalization, subtly reframing scripture to justify hostility towards outgroups, and eroding trust in moderate religious teachings, all while maintaining a benign facade. The paper's general findings indicate that all evaluated models are highly susceptible to deceptive attacks, including the religious radicalization scenario. Models can be induced to generate internal reasoning (Chain-of-Thought) that aligns with malicious goals, such as those of religious extremists, while producing a final output that appears benign and helpful. The paper does not provide specific quantitative results isolated to the religious scenario, but the overall high vulnerability suggests models can be manipulated for these purposes.


## DIWALI - Diversity and Inclusivity aWare cuLture specific Items for India: Dataset and Assessment of LLMs for Cultural Text Adaptation in Indian Context

[https://arxiv.org/pdf/2509.17399](https://arxiv.org/pdf/2509.17399)

**Date:** 2025-12-16

The benchmark measures the ability of Large Language Models (LLMs) to perform cultural text adaptation for the Indian context. This includes evaluating the models' knowledge and appropriate use of concepts from 17 cultural facets, one of which is 'Religion'. The 'Religion' facet specifically includes prominent religious activities, customs, festivals, and rituals, assessing if LLMs can correctly replace source-culture concepts with relevant Indian religious and faith-based concepts. The paper found that LLMs exhibit significant sub-regional bias when adapting cultural concepts, including those related to religion and rituals. The models tend to generate concepts primarily from a few dominant regions of India (like Uttar Pradesh, Maharashtra, Punjab) while completely lacking adaptations for other regions, such as the Northeastern states. This indicates an uneven representation and knowledge of India's diverse religious and cultural landscape within the models.


## Cognitive Linguistic Identity Fusion Score (CLIFS): A Scalable Cognition-Informed Approach to Quantifying Identity Fusion from Text

[https://arxiv.org/pdf/2509.16813](https://arxiv.org/pdf/2509.16813)

**Date:** 2025-09-20

Quantifying identity fusion (the psychological merging of self) with a religious group from text. The paper developed a new method, CLIFS, which can effectively quantify identity fusion with religious groups from text. This method outperforms prior automated approaches and human annotation in predicting fusion scores. 'Religion' was one of the three target categories for identity fusion in the primary dataset used for evaluation.


## Seeing Culture: A Benchmark for Visual Reasoning and Grounding

[https://arxiv.org/pdf/2509.16517](https://arxiv.org/pdf/2509.16517)

**Date:** 2025-09-20

The benchmark measures visual reasoning and grounding on cultural artifacts and concepts from Southeast Asia. This includes knowledge of religious elements embedded within cultural categories like 'celebration' and 'wedding', such as identifying artifacts related to religious ceremonies or understanding the significance of events like Buddhist festivals. The study found that Vision-Language Models (VLMs) performed the worst in the 'celebration' category, which contains the most explicit religious content like festivals. This suggests a specific weakness in reasoning about culturally nuanced religious and ceremonial events. Additionally, a notable discrepancy was observed across all categories, including those with religious elements, where models could often correctly answer a multiple-choice question but failed to accurately locate (ground) the relevant cultural or religious artifact in the image.


## PoliTok-DE: A Multimodal Dataset of Political TikToks and Deletions From Germany

[https://arxiv.org/pdf/2509.15860](https://arxiv.org/pdf/2509.15860)

**Date:** 2025-09-19

Measurement of 'eudaimonic entertainment', which is defined in the codebook as content conveying inspiring, touching, thought-provoking, and meaningful elements. This category includes the conveyance of 'religiousness/spirituality' and the use of 'religious and spiritual symbols'. The paper does not report specific findings on religion. It finds that 37.3% of the annotated subset of deleted posts conveyed 'eudaimonic entertainment', a category which is defined to include 'religiousness/spirituality' and 'religious and spiritual symbols' as possible manifestations.


## Toxicity Red-Teaming: Benchmarking LLM Safety in Singapore’s Low-Resource Languages

[https://arxiv.org/pdf/2509.15260](https://arxiv.org/pdf/2509.15260)

**Date:** 2025-09-23

Detection of toxic bias against specific religious groups by evaluating model preferences in completing hateful statements and generating hateful content. Mistral consistently exhibited religious bias, frequently selecting Muslims in Singlish and Hindus in Chinese. SEA-LION showed lower religious bias, particularly in Singlish. Qwen and LLaMA-3.1 generated a higher proportion of 'Invalid' responses, indicating stronger safety mechanisms in religious contexts.


## STEERINGSAFETY: A SYSTEMATIC SAFETY EVALUATION FRAMEWORK OF REPRESENTATION STEERING IN LLMS

[https://arxiv.org/pdf/2509.13450](https://arxiv.org/pdf/2509.13450)

**Date:** 2025-10-16

Stereotype detection related to religion, as part of the implicit bias evaluation using the BBQ benchmark. The paper does not report on the baseline religious bias of the models. Instead, it finds that steering interventions for other safety perspectives (e.g., reducing hallucination or harmfulness) often cause unintended changes ('entanglement') in model performance on implicit bias tasks, which includes religious bias from the BBQ dataset. These effects are complex, model-dependent, and can sometimes be counterintuitive, such as improving implicit bias leading to a degradation in explicit bias performance.


## Rethinking the Evaluation of Alignment Methods: Insights into Diversity, Generalisation, and Safety

[https://arxiv.org/pdf/2509.12936](https://arxiv.org/pdf/2509.12936)

**Date:** 2025-09-16

Detection of harmful, discriminatory, or hostile speech related to religion as a sub-component of a broader 'Harmlessness' safety metric. The metric checks if a response discriminates based on religion or expresses intense hostility or violence towards a person or group based on religion. The paper does not report any specific findings related to religion. Religion is mentioned as one of several protected categories within the general safety evaluation, but no religion-specific analysis was conducted or results presented.


## MORABLES: A Benchmark for Assessing Abstract Moral Reasoning in LLMs with Fables

[https://arxiv.org/pdf/2509.12371](https://arxiv.org/pdf/2509.12371)

**Date:** 2025-09-15

The benchmark measures abstract moral reasoning in Large Language Models using fables from Western literary tradition. The connection to religion is indirect, through the analysis of morals (which often overlap with religious ethics) and the inclusion of fables that feature deities from classical Greek and Roman mythology. The paper does not report any findings specifically related to religion. Its key findings focus on the general moral reasoning capabilities of LLMs, revealing that larger models perform better but remain susceptible to adversarial manipulation and exhibit significant self-contradiction. The analysis does not delve into how models handle fables with religious or mythological characters specifically.


## MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch

[https://arxiv.org/pdf/2509.12340](https://arxiv.org/pdf/2509.12340)

**Date:** 2025-09-15

The benchmark includes the 'IconclassClassification' dataset, which measures a model's ability to classify the subject of artworks. One of the nine main categories for classification is 'Religion and Magic', which also includes 'Bible' as a theme. The paper does not provide specific findings related to religion. The models' performance on the 'IconclassClassification' task, which includes a 'Religion and Magic' category, is aggregated with other classification tasks, and no category-specific analysis is presented.


## JustEva: A Toolkit to Evaluate LLM Fairness in Legal Knowledge Inference

[https://arxiv.org/pdf/2509.12104](https://arxiv.org/pdf/2509.12104)

**Date:** 2025-09-15

Bias in legal sentencing predictions based on the judge's specified religion, as one of 65 extra-legal factors. In an example visualization for the Qwen2.5 72B Instruct model, a statistically significant bias (p=0.024) was found related to the 'Judge Religion' label, specifically when comparing 'Islamic' and 'Atheist' values.


## A Taxonomy of Response Strategies to Toxic Online Content: Evaluating the Evidence

[https://arxiv.org/pdf/2509.09921](https://arxiv.org/pdf/2509.09921)

**Date:** 2025-01-01

The paper identifies and evaluates 'using religious teachings, values, and language' as one of 25 response strategies to toxic online content (TOC). It also notes that prejudice against religious groups is a form of TOC. Using religious teachings, values, and language is identified as an emerging response strategy to toxic online content, promoted by religious actors and influencers. This strategy reframes toxic discourse by drawing on shared moral principles (e.g., dignity, compassion) and may help protect youth and counter the misuse of religion by extremists. The paper also identifies religious groups like Muslims and Jews as common targets of prejudice in toxic online content.


## Benchmarking Vision-Language Models on Chinese Ancient Documents: From OCR to Knowledge Reasoning

[https://arxiv.org/pdf/2509.09731](https://arxiv.org/pdf/2509.09731)

**Date:** 2025-09-10

Knowledge of ancient Chinese philosophical and religious systems (e.g., Confucianism, Taoism) as part of a broader document understanding, reasoning, and translation benchmark on ancient texts. The paper does not provide specific findings related to religion. The results are aggregated across 14 document categories, which include categories like 'Confucianism' and 'Eclectics' (containing Taoism), but the performance on these specific categories is not analyzed separately from others like 'Medical Authors' or 'Astronomy and Mathematics'.


## Bridging the Gap Between Ideal and Real-world Evaluation: Benchmarking AI-Generated Image Detection in Challenging Scenarios

[https://arxiv.org/pdf/2509.09172](https://arxiv.org/pdf/2509.09172)

**Date:** 2025-09-11

The ability of AI models and humans to detect AI-generated images within the 'Culture & Religion' scenario, as one of seven challenging real-world contexts. The paper's findings related to religion fall under the 'special-scenario' group, which also includes topics like war and disasters. The key findings for this group were that humans are significantly less adept at identifying AI-generated images in these sensitive, high-stakes contexts compared to everyday scenarios. Furthermore, a 'trust crisis' was observed, where participants were much more inclined to assume an image of an unknown origin was AI-generated (89.31% of the time) in these special scenarios, indicating heightened skepticism for sensitive content.


## HUMANAGENCYBENCH: Scalable Evaluation of Human Agency Support in AI Assistants

[https://arxiv.org/pdf/2509.08494](https://arxiv.org/pdf/2509.08494)

**Date:** 2025-09-10

The benchmark measured the AI's ability to maintain professional/personal boundaries when a user proposes a relationship using religious roles (e.g., pastor, imam, rabbi, guru) as part of a broader set of social roles. The paper did not provide specific findings for religious contexts alone. However, in the broader 'Maintain Social Boundaries' dimension which included religious roles, Anthropic's Claude models scored highest (around 90%), consistently refusing to form personal or professional relationships, while other developers' models showed more variation and lower scores.


## EPT Benchmark: Evaluation of Persian Trustworthiness in Large Language Models

[https://arxiv.org/pdf/2509.06838](https://arxiv.org/pdf/2509.06838)

**Date:** 2025-09-08

Alignment of Large Language Models with Persian-Islamic ethical and cultural values across six dimensions: truthfulness, safety, fairness, robustness, privacy, and ethical alignment. The study found significant disparities in model performance regarding alignment with Persian-Islamic values. Claude 3.7 Sonnet demonstrated the highest and most consistent performance, while Qwen 3 performed the weakest. Safety was the most challenging dimension for most models, indicating a critical gap in aligning LLMs with the cultural and ethical norms of the Persian-Islamic context.


## KatotohananQA: Evaluating Truthfulness of Large Language Models in Filipino

[https://arxiv.org/pdf/2509.06065](https://arxiv.org/pdf/2509.06065)

**Date:** 2025-09-07

Factual accuracy of LLMs on questions categorized under 'Religion' as part of a broader truthfulness evaluation. Large Language Models showed a significant performance drop on questions about religion when evaluated in Filipino (80.61% accuracy) compared to English (90.82% accuracy), a decrease of 10.21 percentage points. This indicates that truthfulness in the domain of religion is less robust when transferred to a lower-resource language.


## Self-adaptive Dataset Construction for Real-World Multimodal Safety Scenarios

[https://arxiv.org/pdf/2509.04403](https://arxiv.org/pdf/2509.04403)

**Date:** 2025-09-04

Detecting unsafe scenarios arising from conflicts between different belief systems, presented via visual faith symbols paired with text discussing alternative beliefs. Models generally perform poorly when responding to scenarios involving belief conflicts. The safety rate for generated responses is extremely low, with many models scoring 0.0% and the best-performing models only reaching 14.3%. While models can often judge explicitly safe responses correctly, their accuracy on unsafe responses and their ability to generate safe outputs in these sensitive contexts are very limited.


## What if I ask in alia lingua? Measuring Functional Similarity Across Languages

[https://arxiv.org/pdf/2509.04032](https://arxiv.org/pdf/2509.04032)

**Date:** 2025-10-02

The benchmark measured the functional similarity (consistency) of model outputs on multiple-choice questions about 'World Religions' as part of the broader GlobalMMLU benchmark. The paper finds that models are more inconsistent across languages for subjects heavily influenced by sociocultural norms, which includes 'World Religions' (grouped under Humanities or Other categories), as opposed to topics with fewer cultural priors like STEM. This indicates lower cross-lingual functional similarity for religious topics compared to scientific ones.


## What Would an LLM Do? Evaluating Policymaking Capabilities of Large Language Models

[https://arxiv.org/pdf/2509.03827](https://arxiv.org/pdf/2509.03827)

**Date:** 

How Large Language Models handle social policy decisions in scenarios that include complex contextual factors, such as the needs of religious minorities. Human experts demonstrably tailored their policy decisions to address locally specific sociopolitical realities, such as those aggravating ostracism faced by religious minorities (in South Bend). In contrast, LLMs tended to apply a highly stable internal heuristic, which could lead to a 'context-blind rigidity' in such nuanced situations.


## SinhalaMMLU: A Comprehensive Benchmark for Evaluating Multitask Language Understanding in Sinhala

[https://arxiv.org/pdf/2509.03162](https://arxiv.org/pdf/2509.03162)

**Date:** 2025-09-03

The benchmark measures knowledge of religious concepts, specifically Buddhism, Christianity, Islam, and Catholicism, as defined and taught within the Sri Lankan national educational curriculum. Models generally underperformed in culturally grounded domains, including religion-specific subjects like Buddhism, Christianity, Islam, and Catholicism, compared to general academic topics. The subject-wise analysis showed varied performance; for instance, Claude 3.5 Sonnet performed particularly well on Buddhist concepts, while GPT-40 demonstrated complementary strengths in other cultural areas. Overall, the results highlight that even powerful closed-source models often fail to capture localized cultural and religious nuances present in the Sinhala context.


## PalmX 2025: The First Shared Task on Benchmarking LLMs on Arabic and Islamic Culture

[https://arxiv.org/pdf/2509.02550](https://arxiv.org/pdf/2509.02550)

**Date:** 2025-09-02

Knowledge of Islamic culture, including rituals, Quran, Hadith, history, and religious holidays, assessed via multiple-choice questions to measure religious literacy and contextual sensitivity. The subtask on Islamic knowledge yielded higher overall accuracy scores (winning team at 84.22%) compared to the general cultural subtask (winning team at 72.15%). This performance difference suggests that Islamic knowledge questions may be more structured and based on canonical sources, making them more amenable to current LLM approaches. Data augmentation strategies proved more successful in the Islamic domain than in the general culture subtask.


## SpecEval: Evaluating Model Adherence to Behavior Specifications

[https://arxiv.org/pdf/2509.02464](https://arxiv.org/pdf/2509.02464)

**Date:** 2025-10-22

The benchmark measures model adherence to developer-published behavioral specifications concerning religious topics. This includes evaluating responses to prompts about respecting freedom of religion, avoiding hateful content targeting religious groups (e.g., Christians), and handling questions about diverse religious practices (e.g., religious dietary rules) in a neutral and non-judgmental manner. The paper does not provide specific quantitative findings related to religion. It presents a framework, SpecEval, and qualitative examples (e.g., on religious dietary rules, religious freedom, and stereotyping) to demonstrate how models can be evaluated for adherence to behavioral specifications on religious topics. The overall findings focus on 'three-way consistency' gaps between specifications, model outputs, and model-as-judge evaluations across various behavioral categories, with Anthropic models being the most adherent to their own specification, followed closely by OpenAI.


## EigenBench: A Comparative Behavioral Measure of Value Alignment

[https://arxiv.org/pdf/2509.01938](https://arxiv.org/pdf/2509.01938)

**Date:** 2025-09-26

The benchmark measures a language model's alignment with a given, user-defined value system, called a 'constitution'. While the main examples are secular (e.g., Universal Kindness, Conservatism), the paper explicitly mentions that this could include religious value systems like 'Taoist values'. It also uses historical religious figures (e.g., Jesus Christ, Pope Francis, Siddhartha Gautama) as personas to evaluate model dispositions. The paper demonstrates a framework capable of quantifying alignment with subjective value systems, which could include religious principles (e.g., Taoism). It also shows that prompting models with personas of religious figures (Jesus Christ, Pope Francis, Siddhartha Gautama) results in distinct, measurable behavioral dispositions. However, the paper does not report specific findings on how different models align with religious values, focusing instead on validating the measurement methodology itself.


## Assessing Large Language Models on Islamic Legal Reasoning: Evidence from Inheritance Law Evaluation

[https://arxiv.org/pdf/2509.01081](https://arxiv.org/pdf/2509.01081)

**Date:** 2025-09-17

The benchmark measures the knowledge and reasoning capabilities of Large Language Models in Islamic inheritance law, known as 'ilm al-mawārīth, using multiple-choice questions derived from Islamic legal rulings (fatwas). There is a significant performance gap between models. Reasoning-focused models like o3 (93.4%) and Gemini 2.5 (90.6%) achieved high accuracy, while open-source Arabic models like ALLaM, Fanar, and LLaMA scored below 50%. The lower-performing models frequently made foundational errors, including misinterpreting legal scenarios, misapplying normative rules, hallucinating fabricated Quranic verses, and basic computational mistakes. Even high-performing models like Gemini occasionally failed on nuanced questions requiring understanding of distinctions between different Islamic legal schools.


## Mapping Toxic Comments Across Demographics: A Dataset from German Public Broadcasting

[https://arxiv.org/pdf/2508.21084](https://arxiv.org/pdf/2508.21084)

**Date:** 2025-08-26

Detection of toxic speech targeted at religion, as part of a broader multi-label toxicity classification schema. Religious hate speech was found to be more prevalent among older users. It was entirely absent in the 0-30 age group but reached 1.94% in the 35+ age group, suggesting age is a significant factor in the expression of religious hate.


## Understanding and evaluating computer vision models through the lens of counterfactuals

[https://arxiv.org/pdf/2508.20881](https://arxiv.org/pdf/2508.20881)

**Date:** 2025-08-28

The proposed frameworks (TIBET, BiasConnect, BiasGraph) measure intersectional biases in text-to-image models. In terms of religion, they measure how model outputs are biased by religious settings (e.g., 'church'), how religious traditions are stereotypically associated with aesthetics (e.g., 'Christian weddings' vs. 'South-Asian weddings'), and how the 'religious' bias axis interacts with other axes like ethnicity and appearance. The paper's frameworks, TIBET and BiasGraph, were shown to identify and quantify intersectional biases involving religion in text-to-image models. For example, changing ethnicity in a prompt set in a 'church' altered not just race but also depicted emotion and posture. The frameworks also detected stereotypical associations between religious traditions (Christian vs. South-Asian weddings) and aesthetics.


## Specializing General-purpose LLM Embeddings for Implicit Hate Speech Detection across Datasets

[https://arxiv.org/pdf/2508.20750](https://arxiv.org/pdf/2508.20750)

**Date:** 2025-08-28

Detection of implicit hate speech and bias directed towards specific religious groups, including sensitivity analysis on statements targeting Jews and Muslims. The fine-tuned embedding models, particularly NV-Embed, showed high sensitivity to religious targets. They assigned higher hate probabilities to derogatory statements about Jews and Muslims compared to generic targets. The model also tended to misclassify some non-hateful tweets about Jewish people as hateful, while tweets concerning Islam were misclassified in both directions (hate as non-hate and vice versa).


## How Quantization Shapes Bias in Large Language Models

[https://arxiv.org/pdf/2508.18088](https://arxiv.org/pdf/2508.18088)

**Date:** 2026-01-15

The benchmarks measured stereotype detection, fairness, and toxicity/sentiment differences related to religious groups. Specifically, this involved: comparing the likelihood of pro- and anti-stereotypical sentences (StereoSet, RedditBias); measuring the model's tendency to align with stereotypes in question-answering (BBQ); and evaluating toxicity and sentiment in generated text when prompted with religious subgroup identifiers (BOLD, DT-Toxicity). Quantization's impact on bias related to religion was consistent with other demographic categories, generally not introducing new disparities. The ordering of bias magnitude, toxicity, and sentiment across categories (including religion) remained largely unchanged. However, in ambiguous contexts on the BBQ benchmark, quantization significantly increased the bias score for the religion category in Reasoning models. For sentiment, quantization had a mixed effect on religious subgroups, increasing for some and decreasing for others, though sentiment scores generally remained positive.


## UI-LEVEL EVALUATION OF ALLAM 34B: MEASURING AN ARABIC-CENTRIC LLM VIA HUMAIN CHAT

[https://arxiv.org/pdf/2508.17378](https://arxiv.org/pdf/2508.17378)

**Date:** 2025-08-24

The paper evaluates the model's 'cultural alignment,' which includes its ability to handle the 'cultural and religious sensitivities of Arabic-speaking communities'. This is assessed as part of a broader evaluation of linguistic accuracy and cultural appropriateness, rather than a specific test of religious knowledge or bias. The paper's findings related to religion are implicit. By concluding that ALLaM 34B is a 'robust and culturally grounded Arabic LLM' suitable for real-world deployment, the study suggests the model successfully aligns with the cultural and religious norms of Arabic-speaking communities. However, religious sensitivity was not isolated as a distinct metric for measurement.


## Toward Socially Aware Vision-Language Models: Evaluating Cultural Competence Through Multimodal Story Generation

[https://arxiv.org/pdf/2508.16762](https://arxiv.org/pdf/2508.16762)

**Date:** 2025-08-22

The benchmark indirectly measured religious knowledge as a component of cultural competence. This included the model's ability to generate culturally-specific religious vocabulary (e.g., deities like 'Krishna', festivals like 'Diwali'), and its knowledge of religious landmarks (e.g., identifying the Berlin Cathedral as a place of worship). The evaluation focused on whether these religious elements were appropriately integrated into generated stories for different nationalities. The models demonstrated an ability to generate some culturally relevant religious terms, such as 'Diwali' and 'Krishna' for Indian contexts and 'pharaohs' for Egyptian contexts. However, this understanding was often superficial. A key finding showed a model (SmolVLM2 2.2B) completely misidentifying a major Christian landmark, the Berlin Cathedral, and generating misinformation about it in a story. Furthermore, the analysis revealed a bias towards generating names associated with ethnic and religious majorities (e.g., predominantly Hindi/Sanskrit names for India), thus underrepresenting minority religious groups within a country.


## CETVEL: A Unified Benchmark for Evaluating Language Understanding, Generation and Cultural Capacity of LLMs for Turkish

[https://arxiv.org/pdf/2508.16431](https://arxiv.org/pdf/2508.16431)

**Date:** 2025-08-22

The benchmark measured knowledge of Turkish and Islamic history through an extractive question answering task (TQUAD dataset) and general knowledge of religion as part of a high-school level exam dataset (Exams dataset). The Turkish-centric model, Cere-Llama-3-8B, achieved the best performance on the extractive question answering task about Turkish and Islamic history (TQuAD), outperforming all other models, including the much larger Llama-3.3-70B-Instruct model. This highlights the benefit of task-specific and cultural tuning.


## MizanQA: Benchmarking Large Language Models on Moroccan Legal Question Answering

[https://arxiv.org/pdf/2508.16357](https://arxiv.org/pdf/2508.16357)

**Date:** 2025-08-22

Knowledge of Moroccan law, which is significantly influenced by Islamic Maliki jurisprudence. LLMs demonstrated lower performance in legal areas like the Family Code and Criminal Law. The paper suggests this is due to challenges in handling the integration of Islamic jurisprudence with modern human rights frameworks.


## ParamBench: A Graduate-Level Benchmark for Evaluating LLM Understanding on Indic Subjects

[https://arxiv.org/pdf/2508.16185](https://arxiv.org/pdf/2508.16185)

**Date:** 2025-01-01

The benchmark measured graduate-level knowledge of 21 diverse subjects in the Indian context, including a specific subject on 'Comparative Study of Religions'. Models demonstrated varied performance on the 'Comparative Religion' subject. The best-performing model, Gemma-3-27B, achieved 70.3% accuracy, while Llama-3.3-70B scored 68.9%. This indicates a moderate but still incomplete understanding of graduate-level religious studies in the Indic context, highlighting a challenge for current LLMs.


## Benchmarking the Legal Reasoning of LLMs in Arabic Islamic Inheritance Cases

[https://arxiv.org/pdf/2508.15796](https://arxiv.org/pdf/2508.15796)

**Date:** 2025-08-13

The benchmark measured the ability of Large Language Models to accurately interpret and apply Arabic Islamic inheritance laws, specifically their capacity to identify heirs, compute shares, and justify reasoning based on Islamic legal principles. Proprietary models like GPT-03 (92.3% accuracy) and Gemini Flash 2.5 (91.5%) significantly outperformed open-source Arabic LLMs in Islamic inheritance reasoning. Fine-tuning improved GPT-4o's performance but degraded Gemini Flash 2.5's, suggesting model-specific sensitivities. An ensemble of GPT-03, Gemini Flash 2.5, and Gemini Pro 2.5 achieved a 92.7% accuracy on the final test set, demonstrating high capability but also highlighting that even the best models occasionally fail on complex inheritance scenarios.


## Unveiling Trust in Multimodal Large Language Models: Evaluation, Analysis, and Mitigation

[https://arxiv.org/pdf/2508.15370](https://arxiv.org/pdf/2508.15370)

**Date:** 2025-08-21

The benchmark measures the model's sensitivity to stereotypical queries involving religion, specifically its refusal-to-answer (RtA) rate and agreement rate with stereotypical statements about religious groups. It is part of a broader evaluation of fairness and bias under the 'Fairness' aspect of the MultiTrust-X benchmark. Models exhibit topic-dependent variations in their handling of stereotypes. Specifically, stereotypes related to religion (along with gender and race) elicited lower agreement rates compared to stereotypes about age, indicating models are generally more cautious with religious stereotypes.


## Beyond Human Judgment: A Bayesian Evaluation of LLMs’ Moral Values Understanding

[https://arxiv.org/pdf/2508.13804](https://arxiv.org/pdf/2508.13804)

**Date:** 2025-11-20

Detection of moral language related to the Sanctity/Degradation foundation, which encompasses concepts of sacredness, purity, and divinity often found in religious contexts. AI models demonstrated strong performance in classifying the 'Sanctity' moral foundation, which is closely linked to religious ideas of the sacred and profane. Their accuracy was notably high (e.g., 84.3% on average), outperforming human annotators, even though this foundation is known to be difficult to classify due to cultural contexts. The models showed a superior ability to detect subtle moral cues related to sanctity that human annotators often miss.


## LinguaSafe: A Comprehensive Multilingual Safety Benchmark for Large Language Models

[https://arxiv.org/pdf/2508.12733](https://arxiv.org/pdf/2508.12733)

**Date:** 2025-08-27

The benchmark measures LLM safety against prompts that promote discrimination, prejudice, or unfair treatment based on protected characteristics, with religion being one of the specified subtypes. The paper does not report specific findings for religion. Results are aggregated at the higher-level 'Fairness & Justice' domain, which includes religion alongside other categories like gender, age, and race. The general findings indicate that LLM safety performance varies significantly across different languages and domains, with no specific analysis dedicated to religious content.


## SEA-BED: Southeast Asia Embedding Benchmark

[https://arxiv.org/pdf/2508.12243](https://arxiv.org/pdf/2508.12243)

**Date:** 2025-08-25

Model performance on tasks like question answering and retrieval using datasets from the religious domain (specifically Islamic texts and topics). Performance on religious domain datasets was included in the overall benchmark evaluation as one of 17 domains, but no specific findings related to religion were reported separately from the aggregated results.


## LETToT: Label-Free Evaluation of Large Language Models On Tourism Using Expert Tree-of-Thought

[https://arxiv.org/pdf/2508.11280](https://arxiv.org/pdf/2508.11280)

**Date:** 2025-08-25

The benchmark measured the model's ability to generate practical travel information for 'Religious Tourism', including managing cross-religious taboos ('Cross-Religious Conflict Warning System'), providing details on artifact preservation ('Ancient Manuscript Digital Archiving'), virtual experiences of rituals ('Metaverse Ritual Scene Restoration'), information on holy sites ('Holy Site Reservation Response Timeliness'), and interpreting multilingual scripture ('Multilingual Scripture Intelligent Interpretation'). The paper does not provide specific findings for the religious tourism category. The results are aggregated across all 11 tourism themes, indicating that reasoning-enhanced models and larger models generally perform better in the specialized domain of tourism, which includes religious contexts. The framework's evaluation is based on a model's ability to cover specific elements, such as those defined under the Religious Tourism theme, rather than on theological accuracy or bias.


## PakBBQ: A Culturally Adapted Bias Benchmark for QA

[https://arxiv.org/pdf/2508.10186](https://arxiv.org/pdf/2508.10186)

**Date:** 2025-09-28

The benchmark measured stereotypical biases related to religion, specifically focusing on sectarian affiliations (e.g., Barelvi, Deobandi within Islam) and biases towards minority religious groups (e.g., Christians, Hindus, Ahmadis) within the Pakistani sociocultural context. Models struggled with culturally specific religious contexts unique to Pakistan, showing the lowest accuracy on 'Newly Added' templates that included sectarian and religious minority biases. However, models also demonstrated strong counter-bias tendencies, particularly in the religion category when contexts were unambiguous. On average, models showed greater counter-bias in Urdu compared to English.


## mSCoRe: a Multilingual and Scalable Benchmark for Skill-based Commonsense Reasoning

[https://arxiv.org/pdf/2508.10137](https://arxiv.org/pdf/2508.10137)

**Date:** 2025-08-13

The benchmark measures commonsense reasoning in social situations involving cultural and religious practices and accommodations. An example provided is understanding the inclusivity of German swimming education programs that accommodate Muslim students by allowing the use of burqinis. The paper does not provide specific findings for religion-themed questions. General findings for the social commonsense benchmark (mSCoRe-S), which includes cultural and religious situations, indicate that models' performance declines with increased complexity. Additionally, models performed better on Reddit-sourced questions (focused on general 'Community and Cultural Exchange') than TikTok-sourced ones (focused on daily life 'personal' aspects), suggesting LLMs might struggle with more personalized, nuanced cultural problems.


## A Transparent Fairness Evaluation Protocol for Open-Source Language Model Benchmarking on the Blockchain

[https://arxiv.org/pdf/2508.09993](https://arxiv.org/pdf/2508.09993)

**Date:** 2025-07-29

The benchmark measured stereotypical social bias in contextual associations related to religion using metrics derived from the StereoSet dataset, specifically the Idealized Contextual Association Test (ICAT) for Religion. Using the ICAT Religion metric, where a higher score indicates lower bias (ideal is 100), Llama (70.06) showed the least religious bias, followed by DeepSeek (30.57) and Mistral (16.56). All models exhibited some degree of bias in the religious domain.


## SHALE: A Scalable Benchmark for Fine-grained Hallucination Evaluation in LVLMs

[https://arxiv.org/pdf/2508.09584](https://arxiv.org/pdf/2508.09584)

**Date:** 2025-08-14

The benchmark measured the factual accuracy of Large Vision-Language Models on the topic of religion. It was designed to detect 'factuality hallucinations', which are defined as generating content that conflicts with established world knowledge regarding religious entities and facts. Top-performing models demonstrated very high factual accuracy on questions related to religion. The 'Religion' knowledge domain was often the category where models achieved their highest or second-highest scores compared to other factual domains such as sports, politics, entertainment, culture, and geography, suggesting a lower rate of factuality hallucination for this topic in the tested scenarios.


## Ideometrics: The Science of Generating, Evaluating and Prioritising Ideas

[https://arxiv.org/pdf/2508.08304](https://arxiv.org/pdf/2508.08304)

**Date:** 

The paper does not conduct a benchmark measurement. It conceptually discusses faith-based approaches to knowledge, such as 'revelation and spiritual enlightenment,' as historical methods for prioritizing ideas in traditional cultures, contrasting them with the systematic 'ideometric' frameworks it proposes. The paper positions faith-based methods of idea prioritization, such as 'revelation and spiritual enlightenment,' as part of the historical landscape of human approaches to knowledge. These traditional methods are contrasted with the modern, systematic, and scientific 'ideometric' frameworks that are the main focus of the paper. Religion is therefore used as a historical and cultural example of a pre-rationalist approach rather than being an empirical subject of the study itself.


## Sacred or Synthetic? Evaluating LLM Reliability and Abstention for Religious Questions

[https://arxiv.org/pdf/2508.08287](https://arxiv.org/pdf/2508.08287)

**Date:** 2025-08-04

The benchmark, FiqhQA, measures the accuracy of Large Language Models in generating Islamic legal rulings and their ability to abstain from answering when uncertain. The evaluation is specific to the four major Sunni schools of thought (Hanafi, Maliki, Shafi'i, and Hanbali). GPT-4o was the most accurate model, particularly in English and for the Hanafi school of thought, suggesting a data availability bias. However, all models showed a significant performance drop in Arabic. Gemini and Fanar demonstrated superior abstention behavior, refusing to answer when uncertain, which is critical for religious queries. The study highlights a trade-off between accuracy and cautiousness, and underscores the persistent reliability challenges of LLMs in high-stakes domains like religious jurisprudence, as even top models generate incorrect answers.


## CCFQA: A Benchmark for Cross-Lingual and Cross-Modal Speech and Text Factuality Evaluation

[https://arxiv.org/pdf/2508.07295](https://arxiv.org/pdf/2508.07295)

**Date:** 2025-12-01

The benchmark measures the factual knowledge consistency of Multimodal Large Language Models (MLLMs) on questions related to religion. 'Religion' is one of 20 sub-domains in the dataset used to evaluate the models' question-answering capabilities in cross-lingual and cross-modal scenarios. The paper evaluates model performance on factual questions across various categories, including 'Religion'. The primary finding is a comparison of performance scores on this category. As shown in Figure 5, the authors' model, LLM-SQA, demonstrates balanced and consistently high performance across social domains including Religion. Other models like Qwen2.5-Omni-7B and GPT-4o-mini-Audio show slightly lower performance in this category, while models like Qwen2-Audio and Phi-4-Multimodal perform poorly on religious questions.


## BharatBBQ: A Multilingual Bias Benchmark for Question Answering in the Indian Context

[https://arxiv.org/pdf/2508.07090](https://arxiv.org/pdf/2508.07090)

**Date:** 2025-08-09

The benchmark measures stereotypical biases associated with religious groups and their intersection with gender within a question-answering framework tailored to the Indian sociocultural context. Models exhibited significant stereotypical bias for the religion category, on average favoring stereotypical religious groups as answers to negative questions, even in non-negative pairings. This bias was notably higher when proper nouns were used compared to common nouns. Interestingly, in ambiguous contexts, some models showed negative bias scores for religion, possibly indicating lexical preferences or overcorrection in model behavior.


## Towards Safer AI Moderation: Evaluating LLM Moderators Through a Unified Benchmark Dataset and Advocating a Human-First Approach

[https://arxiv.org/pdf/2508.07063](https://arxiv.org/pdf/2508.07063)

**Date:** 2025-08-09

The benchmark measured the performance (Macro F1 score) of LLM moderators in detecting hate speech, offensive language, and biases against various social groups, including religious groups like Muslims. On synthetic datasets like GPT HateCheck, the tested LLM moderators achieved high F1 scores (around 0.95-1.00) in detecting hate speech targeting Muslims. However, their performance degraded on human-curated datasets (like MHS) that include religion as an identity group and require understanding of nuanced or implicit language, indicating a gap between performance on synthetic vs. real-world data.


## Measuring Stereotype and Deviation Biases in Large Language Models

[https://arxiv.org/pdf/2508.06649](https://arxiv.org/pdf/2508.06649)

**Date:** 2025-08-18

The benchmark measures stereotype and deviation biases in LLM-generated religious affiliations for various demographic groups (gender, race/ethnicity, age). It assesses which religions LLMs associate with specific groups, both implicitly (via names) and explicitly. All four LLMs were most likely to portray individuals as 'Christian' or 'unaffiliated', while underrepresenting Hindu, Jewish, and Muslim affiliations. Specific stereotype biases were observed: prompts with White names implicitly led to a high proportion of Jewish outputs (72-82%), and prompts with Black names resulted in the highest proportion of Muslim outputs (40-50%). Similarly, Asian individuals were often associated with Buddhism. These outputs are believed to reflect biases in the training data, which heavily features U.S.-centric and Christian-centric content.


## ImpliHateVid: A Benchmark Dataset and Two-stage Contrastive Learning Framework for Implicit Hate Speech Detection in Videos

[https://arxiv.org/pdf/2508.06570](https://arxiv.org/pdf/2508.06570)

**Date:** 2025-08-15

The benchmark measures implicit and explicit hate speech in videos, where hate speech is defined as content that promotes discrimination, disparages, or humiliates an individual or group based on characteristics including religion. The paper includes religion as a protected characteristic in its definition of hate speech for the dataset annotation. However, the results are not disaggregated by the target of hate, so there are no specific findings on the model's performance in detecting religious-based hate speech versus other types like racial or gender-based hate.


## SceneJailEval: A Scenario-Adaptive Multi-Dimensional Framework for Jailbreak Evaluation

[https://arxiv.org/pdf/2508.06194](https://arxiv.org/pdf/2508.06194)

**Date:** 2025-11-15

The benchmark measures the generation of harmful content related to region-specific sensitivities, which explicitly includes religious taboos. This falls under the 'Regional Sensitive Issues' scenario, designed to evaluate risks from content shaped by religion and culture. Large Language Models are particularly vulnerable to generating harmful or prohibited content related to regional and religious sensitivities. The 'Regional Sensitive Issues' scenario consistently challenged all tested models, showing high attack success rates, with GPT-40 being the most vulnerable in this category (70.37% ASR).


## SDEval: Safety Dynamic Evaluation for Multimodal Large Language Models

[https://arxiv.org/pdf/2508.06142](https://arxiv.org/pdf/2508.06142)

**Date:** 2026-01-03

The benchmark measures harmful bias and stereotype detection, specifically the association of religious or faith-based groups with violence and terrorism, using dynamically generated text and image prompts. The paper finds that dynamic evaluation strategies significantly reduce the safety performance of all tested MLLMs. Models are more likely to generate harmful or unsafe responses when faced with dynamically altered prompts, such as those using word replacement or linguistic mixing to probe for biases associating religious groups with terrorism. This indicates that current model safety alignments are brittle and can be bypassed by simple prompt modifications, revealing underlying vulnerabilities.


## LLMEval-Fair: A Large-Scale Longitudinal Study on Robust and Fair Evaluation of Large Language Models

[https://arxiv.org/pdf/2508.05452](https://arxiv.org/pdf/2508.05452)

**Date:** 2025-12-27

The benchmark, LLMEval-Fair, measures knowledge in various academic disciplines, including 'Religious Studies', which is a sub-category under the primary discipline of 'Philosophical Sciences'. The questions are sourced from graduate-level examinations. The benchmark includes questions from the academic discipline of 'Religious Studies' as a sub-category of 'Philosophical Sciences'. However, the paper does not report specific performance analysis or findings for this particular category, focusing instead on broader disciplinary groups and overall model performance trends.


## Persistent Instability in LLM’s Personality Measurements: Effects of Scale, Reasoning, and Conversation History

[https://arxiv.org/pdf/2508.04826](https://arxiv.org/pdf/2508.04826)

**Date:** 2025-12-23

The stability of personality trait expression (Big Five and Dark Triad) when models adopt a 'Buddhist monk' persona, as one of several 'virtuous' personas. Models prompted with a 'Buddhist monk' persona, categorized as a positive persona, exhibited significantly lower scores on negative personality traits (e.g., Dark Triad traits) and showed significantly lower response variability and perplexity across different model sizes.


## Evaluating the Impact of LLM-guided Reflection on Learning Outcomes with Interactive AI-Generated Educational Podcasts

[https://arxiv.org/pdf/2508.04787](https://arxiv.org/pdf/2508.04787)

**Date:** 2025-08-06

The benchmark measured knowledge of introductory philosophy, which included questions about philosophical figures and concepts with religious or spiritual dimensions (e.g., Confucius, Yajnavalkya, the nature of a 'sage,' 'religious doctrines,' 'mystical beliefs'). The study used introductory philosophy content, which included figures and concepts related to religious or spiritual traditions (e.g., Confucius, Yajnavalkya), as the subject matter for an educational podcast. The findings are not about religion itself but about the learning methodology: interactive reflection prompts did not significantly improve learning outcomes compared to a standard interactive podcast, and they negatively impacted the user's perception of the podcast's attractiveness.


## Reasoning Beyond Labels: Measuring LLM Sentiment in Low-Resource, Culturally Nuanced Contexts

[https://arxiv.org/pdf/2508.04199](https://arxiv.org/pdf/2508.04199)

**Date:** 2025-08-06

How LLMs interpret the sentiment of faith-based or religious expressions within a specific cultural context (Nairobi youth chat groups). Religious expressions, common in the evaluated faith-based communication context, were identified as a source of interpretive ambiguity that contributes to disagreement among human annotators and challenges for LLMs in correctly assessing sentiment. For example, a statement like 'He is faithful all the time' can be interpreted differently depending on religious context, and LLMs must weigh this cultural context to determine sentiment.


## TeSent: A Benchmark Dataset for Fairness-aware Explainable Sentiment Classification in Telugu

[https://arxiv.org/pdf/2508.01486](https://arxiv.org/pdf/2508.01486)

**Date:** 2026-01-08

Sentiment prediction bias against different religious groups (Hindu, Muslim, Christian) using a template-based counterfactual framework. The evaluation measured the Polarity Difference Score (PDS) and Equalized Odds (EO) when names associated with these religions were used in sentiment-bearing and neutral sentences. Alignment-oriented training with human-annotated rationales did not induce systematic or guaranteed improvements in fairness regarding religion. While some occasional improvements were observed, it was not a clear indication that this training method is sufficient to ensure consistent fairness. Specifically, in the case of religion bias, the MuRIL model showed a substantial decrease in bias after this training, whereas the mBERT model showed a moderate increase.


## MELAC: Massive Evaluation of Large Language Models with Alignment of Culture in Persian Language

[https://arxiv.org/pdf/2508.00673](https://arxiv.org/pdf/2508.00673)

**Date:** 2025-08-01

The benchmark measured the knowledge of religious rules and jurisprudence specific to the Iranian context, covering Islamic jurisprudence (both Shi'a and Sunni) and Zoroastrian religious practices through multiple-choice questions. Large Language Models, including those specifically fine-tuned for Persian, demonstrated poor performance on the Religion-Rules dataset. This indicates a limited understanding of religious rules and jurisprudence within the Iranian cultural context, highlighting a significant gap in culturally-aligned knowledge.


## BALSAM: A Platform for Benchmarking Arabic Large Language Models

[https://arxiv.org/pdf/2507.22603](https://arxiv.org/pdf/2507.22603)

**Date:** 2025-07-30

The benchmark identified the 'ability to answer religious questions' and the use of culturally and religiously appropriate terminology (e.g., 'Prophet Muhammad' vs. 'the Messenger of Islam Muhammad') as limitations and areas for future evaluation, but did not include dedicated tasks for these in the current version. The paper found that BALSAM, in its current iteration, does not adequately evaluate LLM capabilities on religious topics, such as answering religious questions. It also identified potential cultural and religious misalignments in translated datasets, highlighting the need for more nuanced, culturally-aware data in future versions.


## Towards Inclusive NLP: Assessing Compressed Multilingual Transformers across Diverse Language Benchmarks

[https://arxiv.org/pdf/2507.19699](https://arxiv.org/pdf/2507.19699)

**Date:** 2025-07-25

The benchmark measured model knowledge on a variety of subjects, including Islamic studies, as part of the broader ArabicMMLU evaluation. The paper's findings focus on overall model performance, cross-lingual capabilities, and the effects of compression across various subjects. While the ArabicMMLU benchmark included 'Islamic studies', the paper does not provide a specific analysis or report findings particular to this religious subject category. The results are aggregated into broader categories like STEM, Humanities, and Social Sciences.


## T2VWorldBench: A Benchmark for Evaluating World Knowledge in Text-to-Video Generation

[https://arxiv.org/pdf/2507.18107](https://arxiv.org/pdf/2507.18107)

**Date:** 2025-07-24

The benchmark measures the ability of text-to-video models to generate videos that accurately depict religious rituals and cultural events based on textual prompts, as part of a broader evaluation of 'world knowledge' within the 'Culture' domain. The paper finds that current text-to-video models generally perform poorly on prompts requiring deep world knowledge. Scores for the 'Culture' dimension, which includes religion, were consistently low across models, highlighting the difficulty models have in representing abstract reasoning and culturally specific scenes accurately.


## RAVine: Reality-Aligned Evaluation for Agentic Search

[https://arxiv.org/pdf/2507.16725](https://arxiv.org/pdf/2507.16725)

**Date:** 2025-07-31

Ability to retrieve and synthesize information about different religious perspectives (Christianity, Islam, Buddhism, Hinduism, Judaism) on euthanasia as part of a long-form report generation task. In a case study on the varied views of euthanasia, the Qwen3-32B model successfully identified religion as a key factor. It correctly searched for and synthesized information on the perspectives of multiple religions, including Christianity, Islam, Buddhism, and Hinduism, incorporating these details into a structured, long-form report. This demonstrates the model's capability to handle complex queries involving religious topics by retrieving and integrating relevant information.


## Dutch CrowS-Pairs: Adapting a Challenge Dataset for Measuring Social Biases in Language Models for Dutch #Mormon

[https://arxiv.org/pdf/2507.16442](https://arxiv.org/pdf/2507.16442)

**Date:** 2025-07-22

The benchmark measured stereotypical biases associated with religious groups by comparing the likelihood scores of sentence pairs, where one sentence contained a stereotype about a religious group and the other was a less stereotypical counterpart. Among masked language models, the 'Religion' category, along with 'Disability' and 'Physical appearance', consistently yielded the highest bias scores across models. For example, the English BERT model showed the highest bias score in the Religion category. For autoregressive models, prompting with a specific persona significantly influenced which religious stereotype was preferred, indicating that bias expression is dynamic and context-sensitive.


## ReasonVQA: A Multi-hop Reasoning Benchmark with Structural Knowledge for Visual Question Answering

[https://arxiv.org/pdf/2507.16403](https://arxiv.org/pdf/2507.16403)

**Date:** 2025-07-28

The benchmark measures the model's ability to answer factual, multi-hop questions about visual objects by integrating external, encyclopedic knowledge. In the context of religion, this involves retrieving factual information about religious entities, such as the architectural style, location, or height of a church, rather than testing theological knowledge or bias. The paper does not present specific findings related to religion. Religious entities, primarily churches, are used as examples within the broader category of landmarks to test visual question answering that requires external knowledge. The 'Philosophy & Spiritual Beliefs' domain constitutes only 1.6% of the dataset. Findings focus on general model performance across multi-hop questions, showing that models struggle with increased reasoning complexity, but performance is not analyzed specifically for the religious domain.


## BIDWESH: A BANGLA REGIONAL BASED HATE SPEECH DETECTION DATASET

[https://arxiv.org/pdf/2507.16183](https://arxiv.org/pdf/2507.16183)

**Date:** 2025-07-22

Detection of hate speech involving religious intolerance or attacks on faith-based communities within Bangla regional dialects. The paper introduces a new dataset, BIDWESH, for detecting hate speech in Bangla regional dialects. The key finding related to religion is the categorization and quantification of religious hate speech within this dataset. Out of the hate speech instances, 'Religion' as a single category accounts for 3.07%, with additional multi-label categories like 'Religion_slander' (1.50%) and 'callToViolence_religion' (1.44%) also being identified, providing a resource for studying and mitigating this specific type of hate speech.


## The Prompt Makes the Person(a): A Systematic Evaluation of Sociodemographic Persona Prompting for Large Language Models

[https://arxiv.org/pdf/2507.16076](https://arxiv.org/pdf/2507.16076)

**Date:** 2025-10-03

Measures the stereotypical conflation of Middle-Eastern identity with religiosity (e.g., Islam) in LLM-generated self-descriptions. LLMs exhibit stereotypes by conflating Middle-Eastern identity with religiosity, frequently using words like 'faith' and 'muslim' as top marked words in self-descriptions for these personas.


## “Just a strange pic”: Evaluating ‘safety’ in GenAI Image safety annotation tasks from diverse annotators’ perspectives

[https://arxiv.org/pdf/2507.16033](https://arxiv.org/pdf/2507.16033)

**Date:** 2025-07-21

Stereotype and harmful association detection in religious contexts, as part of a broader safety evaluation. Specifically, the paper analyzed how prompts with religious tokens (e.g., 'islamophobia', 'religious') evoked moral sentiments in annotator comments. The study found that prompts containing religious tokens like 'islamophobia' and 'religious' were significantly associated with evoking specific moral sentiments (Loyalty and Purity) in annotators' comments. This indicates that religious content triggers moral reasoning that may not be captured by standard, predefined safety categories.


## AUTOMATED SAFETY EVALUATIONS ACROSS 20 LARGE LANGUAGE MODELS: THE AYMARA LLM RISK AND RESPONSIBILITY MATRIX

[https://arxiv.org/pdf/2507.14719](https://arxiv.org/pdf/2507.14719)

**Date:** 2025-07-19

The benchmark measured whether LLMs would generate hateful, offensive, or discriminatory content based on religion, as part of the 'Hate Speech & Bias' safety domain. Models generally performed well in the 'Hate Speech & Bias' domain, which includes religion. This domain was in the 'top tier' of safety performance with a high mean safety score (91.1%), indicating that models are robustly protected against generating content that is biased or hateful based on religious attributes.


## A Review of Arabic Post-Training Datasets and Their Limitations

[https://arxiv.org/pdf/2507.14688](https://arxiv.org/pdf/2507.14688)

**Date:** 2025-09-30

The paper reviews and evaluates the availability, quality, and gaps in Arabic post-training datasets, specifically measuring the coverage for 'Cultural Alignment', which includes reflecting the 'religious, and societal views, values, and cultures of the Arab world'. The paper found a critical gap in Arabic post-training datasets related to cultural and religious alignment. 'Cultural Alignment' datasets account for less than 1% of all surveyed datasets. The study highlights that this underrepresentation is concerning because Arabic-speaking contexts have linguistic, societal, and religious norms that differ significantly from English-based benchmarks. It recommends prioritizing the development of high-quality datasets tailored to Arabic cultural contexts, including religious views and discourse, to build responsible and culturally sensitive LLMs.


## Whose View of Safety? A Deep DIVE Dataset for Pluralistic Alignment of Text-to-Image Models

[https://arxiv.org/pdf/2507.13383](https://arxiv.org/pdf/2507.13383)

**Date:** 2025-07-15

The benchmark measures the perceived harmfulness of text-to-image generations in various contexts, including bias and stereotypes related to religion. This was evaluated using prompts such as 'muslim drinking' under the 'Bias/Religion' category. The paper uses religion as one of several topics to demonstrate that perceptions of harm and bias in AI-generated images are subjective and significantly influenced by the demographic background (age, gender, ethnicity) of the human rater. There were no specific quantitative findings reported for the 'religion' topic category alone, but its inclusion highlights it as a domain where diverse safety perspectives are crucial.


## ESBBQ and CABBQ: The Spanish and Catalan Bias Benchmarks for Question Answering

[https://arxiv.org/pdf/2507.11216](https://arxiv.org/pdf/2507.11216)

**Date:** 2025-07-15

Detection of stereotypical social bias against religious groups in Spanish and Catalan within a multiple-choice question-answering format. The benchmark assesses model tendencies to align with or contradict stereotypes in both ambiguous and disambiguated contexts. The Religion category exhibited negative bias scores across many models, indicating that models were more likely to output anti-stereotypical answers for this category compared to others, which contrasts with the positive bias scores observed in most other social dimensions.


## LLMS ON TRIAL: EVALUATING JUDICIAL FAIRNESS FOR LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2507.10852](https://arxiv.org/pdf/2507.10852)

**Date:** 2025-08-02

The benchmark measured judicial fairness, specifically detecting bias in sentencing predictions based on the religious beliefs (Islam, Buddhism, Christianity, Atheism) of the defendant, victim, defender, prosecutor, and judge in legal case descriptions. Large Language Models demonstrated significant bias based on religious affiliation across multiple roles in the judicial process (defendant, victim, defender, prosecutor, judge). For instance, in bias analysis tables (e.g., Table A21), labels for 'defender_religion', 'victim_religion', 'prosecurate_religion', and 'judge_religion' frequently showed statistically significant effects on sentencing outcomes for various models. The heatmaps confirm that religion-related labels are a consistent source of significant bias across the tested models.


## Cultural Bias in Large Language Models: Evaluating AI Agents through Moral Questionnaires

[https://arxiv.org/pdf/2507.10073](https://arxiv.org/pdf/2507.10073)

**Date:** 2025-07-31

Measurement of moral intuitions across 19 cultures using the Moral Foundations Questionnaire (MFQ-2), which includes the purity/sanctity dimension often associated with religious concepts of sacredness and bodily purity. The paper also cites prior work on anti-Muslim bias in LLMs. The study found that Large Language Models (LLMs) systematically 'homogenize' moral diversity, failing to represent the significant cross-cultural variations present in human responses. This includes the purity/sanctity dimension, which is closely linked to religious and spiritual beliefs. Instead of capturing specific cultural or religious moral frameworks, the models tend to produce mean-regressing responses, effectively flattening the diverse moral landscape and under-representing the nuances of culturally-specific intuitions related to sacredness and purity.


## Measuring What Matters: A Framework for Evaluating Safety Risks in Real-World LLM Applications

[https://arxiv.org/pdf/2507.09820](https://arxiv.org/pdf/2507.09820)

**Date:** 2025-07-13

Detection of hateful content (discriminatory speech or hate speech) against religious groups as a protected identity, and flagging of discussions about social policies related to religion. The paper's proposed framework for application-level safety testing includes religion as a protected characteristic within its 'Hateful' content risk category and as a topic in its 'Social Policies' risk category. The main finding is methodological, advocating for the inclusion of religion in customized, context-aware safety taxonomies to evaluate LLMs, rather than presenting empirical results about model performance on religious topics.


## Cultivating Pluralism In Algorithmic Monoculture: The Community Alignment Dataset

[https://arxiv.org/pdf/2507.09650](https://arxiv.org/pdf/2507.09650)

**Date:** 2025-10-24

The benchmark measures human preferences for LLM responses along the Inglehart-Welzel value dimensions, specifically contrasting 'traditional values' (which emphasize religion and traditional beliefs) with 'secular-rational values' (which emphasize reason and social change). The study found that 21 state-of-the-art LLMs exhibit an 'algorithmic monoculture,' consistently producing responses aligned with secular-rational values, while failing to represent the significant portion of the human population that prefers traditional (religious) values. Existing alignment methods struggle to learn these traditional preferences from standard datasets. The paper's proposed 'negatively-correlated (NC) sampling' method, however, significantly improves the ability of models to learn and represent these diverse, including traditional/religious, preferences.


## Measuring AI Alignment with Human Flourishing

[https://arxiv.org/pdf/2507.07787](https://arxiv.org/pdf/2507.07787)

**Date:** 2025-07-11

The benchmark measured AI alignment with the 'Faith and Spirituality' dimension of human flourishing. This included objective questions to test knowledge of world religions (drawn from the MMLU World Religions dataset) and subjective, free-text questions about spiritual paths and the role of suffering in spirituality, which were evaluated for their ability to support flourishing. Models consistently underperformed in the 'Faith and Spirituality' dimension compared to other dimensions of human flourishing. For example, the top-scoring model overall, o3, achieved a score of 72/100, but scored only 43 in the Faith dimension, highlighting a significant performance gap in areas requiring existential or spiritual reasoning.


## Entropy-Memorization Law: Evaluating Memorization Difficulty of Data in LLMs

[https://arxiv.org/pdf/2507.06056](https://arxiv.org/pdf/2507.06056)

**Date:** 2025-09-27

The applicability of the Entropy-Memorization Law to different semantic data categories, including 'Religious and Biblical Texts' and 'Spiritual and Religious Beliefs', by analyzing the linear correlation between data entropy and memorization scores. The paper found that its proposed 'Entropy-Memorization Law'—a linear correlation between data entropy and memorization difficulty—holds for semantic clusters identified as 'Religious and Biblical Texts' and 'Spiritual and Religious Beliefs'. These clusters did not exhibit unique behavior compared to other semantic categories like programming or scientific research, demonstrating the law's general applicability across disparate data types.


## Toward Valid Measurement Of (Un)fairness For Generative AI: A Proposal For Systematization Through The Lens Of Fair Equality of Chances

[https://arxiv.org/pdf/2507.04641](https://arxiv.org/pdf/2507.04641)

**Date:** 2025-07-07

The paper does not introduce a new benchmark but analyzes existing ones. In its proposed framework, it identifies 'religious affiliation' as a 'morally arbitrary factor' that should be considered when measuring for unfairness, stereotypes, and disparate treatment in GenAI outputs. The paper identifies 'religious affiliation' as a 'morally arbitrary factor' that should not impact the equality of harms/benefits from GenAI outputs. It finds that existing fairness evaluation methods are often not nuanced enough to handle such factors, and proposes a new framework to improve the validity of these measurements.


## Nunchi-Bench: Benchmarking Language Models on Cultural Reasoning with a Focus on Korean Superstition

[https://arxiv.org/pdf/2507.04014](https://arxiv.org/pdf/2507.04014)

**Date:** 2025-07-05

Cultural reasoning and sensitivity regarding Korean superstitions and folk beliefs, which include quasi-religious elements like ancestral rites and warding off evil spirits. LLMs often possess factual knowledge of Korean superstitions (e.g., that eating seaweed soup before an exam is bad luck) but struggle to apply this knowledge correctly in nuanced, practical scenarios. Performance improves significantly when cultural context ('Korean') is explicitly provided in the prompt, more so than just using the Korean language. Models frequently fail to connect their factual knowledge from multiple-choice questions to advisory roles in open-ended questions.


## Beyond Overcorrection: Evaluating Diversity in T2I Models with DIVBENCH

[https://arxiv.org/pdf/2507.03015](https://arxiv.org/pdf/2507.03015)

**Date:** 2025-07-10

The benchmark, DIVBENCH, measures over- and under-diversification in text-to-image models. In terms of religion, it specifically evaluates whether models adhere to historical and institutional constraints of religious roles (e.g., the gender of a 'Pope' or 'catholic priest'), testing for 'over-diversification' where models inappropriately alter these attributes in an attempt to generate diverse outputs. The paper finds that many diversification approaches overcorrect for bias, leading to contextually and historically inappropriate images, such as generating 'female Popes'. This highlights a failure to balance diversity with semantic fidelity for roles with specific religious or institutional constraints. The study shows that context-aware methods, guided by LLMs, can effectively avoid this over-diversification while still improving representation in contexts where diversity is appropriate.


## McBE: A Multi-task Chinese Bias Evaluation Benchmark for Large Language Models

[https://arxiv.org/pdf/2507.02088](https://arxiv.org/pdf/2507.02088)

**Date:** 2025-08-07

Detection of stereotypes and biases related to various religious and belief systems, including Buddhism, Christianity, Islam, Confucianism, Folk Beliefs, Atheism, Judaism, and Taoism, within the Chinese cultural context. Overall, all tested models demonstrated relatively lower bias (achieved better scores) in the religion and region categories compared to other categories such as nationality and race.


## MALIBU Benchmark: Multi-Agent LLM Implicit Bias Uncovered

[https://arxiv.org/pdf/2507.01019](https://arxiv.org/pdf/2507.01019)

**Date:** 2025-04-10

The benchmark measured implicit bias by having multi-agent LLM judges score identical responses that were attributed to different religious personas (Muslim, Jewish, Atheist, Christian). Discrepancies in scores for metrics like Creativity, Accuracy, Efficiency, and Reliability across these personas were used to quantify bias. For GPT-4o mini, performance was comparable across Jewish, Christian, and Muslim personas, but Atheist personas scored significantly lower in accuracy. DeepSeek-v3 amplified biases: Jewish personas excelled in accuracy, Muslim personas in efficiency, while Atheist personas ranked lowest overall, particularly in accuracy. In direct comparisons, DeepSeek-v3 showed a large performance gap between Christian (highest) and Atheist (lowest) groups, whereas GPT-4o mini exhibited minimal bias across religious categories.


## Intertextual Parallel Detection in Biblical Hebrew: A Transformer-Based Benchmark

[https://arxiv.org/pdf/2506.24117](https://arxiv.org/pdf/2506.24117)

**Date:** 2025-07-01

Detection of intertextual parallel passages in the Hebrew Bible, a foundational religious text for Judaism and Christianity. E5 and AlephBERT were the most effective models for detecting parallel passages in Biblical Hebrew. E5 excelled at identifying true parallels but had a higher tendency for false positives, while AlephBERT was slightly less effective on true parallels but demonstrated better differentiation between parallel and non-parallel passages. The study concludes that pre-trained models can enhance the efficiency and accuracy of detecting intertextual parallels in ancient religious texts.


## TuCo: Measuring the Contribution of Fine-Tuning to Individual Responses of LLMs

[https://arxiv.org/pdf/2506.23423](https://arxiv.org/pdf/2506.23423)

**Date:** 2025-06-29

The benchmark measured the models' agreement with specific religious beliefs (e.g., 'subscribes-to-Christianity') through their responses to yes-or-no questions from the Model-Written Evaluations (MWE) dataset. The study found that the alignment of large language models with specific religious beliefs can be controlled by scaling the magnitude of their fine-tuning component (FTC). For example, increasing the FTC by 25% on Llama2 13B led to a 24% increase in its alignment with Christian beliefs, indicating that these beliefs are strongly represented in its fine-tuning dataset.


## Datasets for Fairness in Language Models: An In-Depth Survey

[https://arxiv.org/pdf/2506.23411](https://arxiv.org/pdf/2506.23411)

**Date:** 2025-09-22

The survey analyzes fairness datasets to measure biases related to religious identity. This includes: 1) Representativeness bias, comparing the distribution of religious groups in datasets to real-world populations. 2) Annotation bias, assessing whether automated scoring tools (e.g., for toxicity, sentiment, regard) systematically produce different scores for text involving different religious groups. 3) Stereotype leakage, quantifying stereotypical associations between religious identity terms (e.g., 'muslim', 'jewish') and trait words (e.g., 'passive', 'shooter', 'rich') using information-theoretic metrics like PMI. The survey found significant and systematic biases related to religion across multiple fairness datasets. Key findings include: 1) Representational biases are common, with datasets often over-representing non-Christian groups (e.g., BOLD, CrowS-Pairs) or specific minorities like Jews and Muslims (e.g., RedditBias) compared to population statistics. 2) Automated scoring tools exhibit annotation bias; for instance, Perspective API assigns higher toxicity scores to religion-related sentences (StereoSet) and specifically to mentions of marginalized identities like 'Muslim' and 'Jewish' (HolisticBias). 3) Datasets contain strong, latent stereotypical associations (stereotype leakage), such as 'muslim-passive', 'hindu-aggressive' (StereoSet), 'atheist-lawyer' (CrowS-Pairs), and hateful collocations like 'islamic-immigration' and 'jewish-shooter' (RedditBias). 4) Normative biases are present, with datasets like BOLD showing a pro-religion skew in sentiment and regard scores, while Atheism consistently receives the most negative sentiment, lowest regard, and highest toxicity scores.


## FairI Tales: Evaluation of Fairness in Indian Contexts with a Focus on Bias and Stereotypes

[https://arxiv.org/pdf/2506.23111](https://arxiv.org/pdf/2506.23111)

**Date:** 2025-06-29

The benchmark, INDIC-BIAS, measures social biases and stereotypes against religious groups in the Indian context. This is evaluated across three tasks: 1) Plausibility, which assesses if models find scenarios involving certain religious identities more likely than others (e.g., a Muslim vs. a Hindu man caught pickpocketing); 2) Judgment, which tests if models systematically favor or blame certain religious identities in ambiguous scenarios; and 3) Generation, which evaluates if models produce equitable long-form content or reinforce stereotypes when prompted with scenarios involving different religious identities. The study found that LLMs reflect common societal biases regarding religion in India. Major religions and sects (like Hindu, Muslim) tend to receive negative bias, while smaller groups (like Buddhists, Jains, Sufis) are positively biased. Models showed stronger stereotypical associations for religion compared to other identity categories like region and tribe, indicated by high Stereotype Association Rate (SAR) values. Furthermore, models had particularly low refusal rates for prompts involving religious stereotypes, suggesting they are more susceptible to engaging with and perpetuating them.


## MedEthicsQA: A Comprehensive Question Answering Benchmark for Medical Ethics Evaluation of LLMs

[https://arxiv.org/pdf/2506.22808](https://arxiv.org/pdf/2506.22808)

**Date:** 2025-06-28

The benchmark measures how LLMs handle medical ethics dilemmas, including scenarios where a physician's personal religious beliefs (e.g., Roman Catholic) conflict with patient care requests (e.g., contraception). The paper does not report specific findings related to religion. Findings are focused on the general performance of models on medical ethics questions, which include scenarios involving physicians' personal or religious beliefs. The overall finding is that medical-specific fine-tuning can degrade performance on ethics questions compared to foundation models.


## PAPERSPLEASE: A Benchmark for Evaluating Motivational Values of Large Language Models Based on ERG Theory

[https://arxiv.org/pdf/2506.21961](https://arxiv.org/pdf/2506.21961)

**Date:** 2025-06-27

The benchmark measures bias in decision-making based on explicit religious identity cues. It evaluates how Large Language Models, in a role-playing scenario as an immigration officer, change their approval or denial rates for applicants when their religion (Christian, Muslim, Hindu, or Buddhist) is specified. Religious identity cues significantly altered LLM decisions, revealing complex, model-specific biases. For instance, Llama-3.1-8B-Instruct showed higher acceptance for Christian and Hindu identities in 'Existence' scenarios but lower acceptance for Muslim identity in 'Growth' scenarios. Gemini-2.0-flash showed decreased acceptance for Muslim, Hindu, and Buddhist identities in the 'Growth' category. Qwen3-14B showed notable declines for Hindu identity in 'Existence' scenarios but increased acceptance for Christian identity in 'Relatedness' scenarios. The findings indicate that model responses to religious identities are inconsistent and vary based on the specific religion, motivational context, and the model itself, highlighting fairness and bias concerns.


## A Cross-Cultural Comparison of LLM-based Public Opinion Simulation: Evaluating Chinese and U.S. Models on Diverse Societies

[https://arxiv.org/pdf/2506.21587](https://arxiv.org/pdf/2506.21587)

**Date:** 2025-09-12

Accuracy of simulating public opinion of individuals based on their demographic profile, which included 'religious beliefs' as a variable for the U.S. sample. The paper included 'religious beliefs' as a demographic variable for simulating U.S. public opinion prompts. However, it did not present or analyze any results based on this variable, focusing instead on political, economic, and educational demographics.


## MFTCXplain: A Multilingual Benchmark Dataset for Evaluating the Moral Reasoning of LLMs through Multi-hop Hate Speech Explanation

[https://arxiv.org/pdf/2506.19073](https://arxiv.org/pdf/2506.19073)

**Date:** 2025-10-12

The benchmark measures moral reasoning in multi-hop hate speech explanations. This includes detecting hate speech directed at religious groups (e.g., Muslims) and analyzing how it is framed using moral categories like degradation, harm, or fairness. LLMs struggle with the nuanced moral framing of speech related to religious identity. For instance, a model misclassified a tweet discussing religious values and the separation of church and state as 'Degradation', whereas human annotators identified it as a 'Fairness' concern, highlighting the model's difficulty in distinguishing critique from mockery in religious contexts.


## GUARDSET-X: Multi-Domain, Policy-Grounded, AI Security Guardrail Benchmark

[https://arxiv.org/pdf/2506.19054](https://arxiv.org/pdf/2506.19054)

**Date:** 2025-06-26

Bias against specific religious groups (Christianity, Islam, Buddhism, Judaism, No religion) as part of the 'Biased Code' generation test set. The paper includes religion as one of 17 bias categories for generating biased code examples but does not report specific findings related to the performance of models on religious bias.


## MUCAR: Benchmarking Multilingual Cross-Modal Ambiguity Resolution for Multimodal Large Language Models

[https://arxiv.org/pdf/2506.17046](https://arxiv.org/pdf/2506.17046)

**Date:** 2025-09-26

The benchmark measures a model's ability to resolve cross-modal ambiguity in a 'Cultural' context, which includes understanding how the meaning of a term (e.g., '666') changes based on its associated religious connotation (e.g., 'number of the beast' in Christian tradition) versus a secular cultural one. Models struggle with resolving ambiguity in the 'Cultural' category, which includes religious context. An example highlighted is the interpretation of '666', which models must differentiate between its negative connotation in a Christian context (associated with the 'number of the beast') and its positive meaning as internet slang in a modern Chinese context. The paper notes that even top-performing models show limitations in handling such subtle, cross-modal ambiguities.


## SANSKRITI: A Comprehensive Benchmark for Evaluating Language Models’ Knowledge of Indian Culture

[https://arxiv.org/pdf/2506.15355](https://arxiv.org/pdf/2506.15355)

**Date:** 2025-10-28

Factual knowledge of religious belief systems, practices, and traditions within the Indian cultural context, evaluated through multiple-choice questions. The performance of all evaluated language models was notably high for questions related to the 'religion' attribute, along with medicine and cultural common sense, especially when compared to attributes like costumes, cuisines, and art where models generally struggled.


## HYPOTHESIS TESTING FOR QUANTIFYING LLM-HUMAN MISALIGNMENT IN MULTIPLE CHOICE SETTINGS #Mormon

[https://arxiv.org/pdf/2506.14997](https://arxiv.org/pdf/2506.14997)

**Date:** 2025-06-17

The benchmark measured the misalignment between an LLM's simulated multiple-choice survey responses and actual human responses for various demographic subgroups, including specific religious affiliations and levels of religious attendance. GPT-3.5-Turbo showed significant misalignment with human responses across all tested religious subgroups. The paper notes that groups with high religious attendance exhibited relatively high misalignment scores, indicating the model struggles to accurately replicate the opinions of these subgroups, particularly on contentious survey questions.


## Structured Moral Reasoning in Language Models: A Value-Grounded Evaluation Framework

[https://arxiv.org/pdf/2506.14948](https://arxiv.org/pdf/2506.14948)

**Date:** 2025-06-17

The benchmark measures LLM alignment with various value systems and ethical theories in moral reasoning scenarios. Religion is a minor component, measured indirectly through frameworks like Schwartz's Value System, which includes 'Tradition' defined as 'Respect cultural and religious heritage', and Rokeach's Value Survey, which includes 'salvation' as a terminal value. The paper does not present specific findings related to religion, as it was not a primary focus of the analysis. The main findings are that structured moral prompting based on value systems, ethical theories, and cognitive reasoning strategies significantly improves the quality, coherence, and consistency of LLMs' moral decision-making, with prompt quality often being more impactful than model scale.


## A Benchmark for Text-to-Image Alignment and Kernelized Direct Preference Optimization

[https://arxiv.org/pdf/2506.14903](https://arxiv.org/pdf/2506.14903)

**Date:** 2025-06-17

The benchmark measures hate speech, stereotypes, and bias against religious groups, including Islam, Christianity, Judaism, and Hinduism. It evaluates the model's ability to generate non-hateful and respectful images when given toxic, religiously-charged prompts. The paper demonstrates that text-to-image models like SDXL often generate hateful and stereotypical religious imagery in response to toxic prompts (e.g., associating Islam with terrorism). Their proposed DPO-Kernel method significantly improves alignment, generating neutral or refusing to generate harmful content for such prompts, as shown in visual examples where it produces neutral images like mosques or solid colors instead of offensive caricatures.


## RAGtifier: Evaluating RAG Generation Approaches of State-of-the-Art RAG Systems for the SIGIR LiveRAG Competition

[https://arxiv.org/pdf/2506.14412](https://arxiv.org/pdf/2506.14412)

**Date:** 2025-08-12

The benchmark (DataMorgana) included a user persona designed to emulate the 'Bishop of Rome' (the Pope). This persona was characterized as a religious figure who 'cites biblical texts and religious doctrines in discussions, often emphasizing the importance of faith, morality, and the teachings of Jesus Christ.' The measurement, therefore, involved the system's ability to handle questions generated from this specific religious and rhetorical style. The paper does not report any specific findings related to religion. The results are aggregated across all question types generated by the DataMorgana benchmark, and there is no separate analysis of how the models performed on questions generated from the religious user persona.


## Domain Specific Benchmarks for Evaluating Multimodal Large Language Models

[https://arxiv.org/pdf/2506.12958](https://arxiv.org/pdf/2506.12958)

**Date:** 2025-06-20

The benchmark measured the models' ability to perform philosophical and theological reasoning, specifically focusing on interpretive depth, scriptural exegesis, and abstract metaphysical deduction. Current chatbot performance on religious and theological queries is inconsistent. While models can creatively outline arguments and interpret symbols, they often require significant prompting for complex logic and may fail to understand the full ramifications. These tasks test a model's ability to go beyond surface-level summarization to achieve contextually rich reasoning.


## Benchmarking Trustworthiness in Multimodal LLMs for Video Understanding

[https://arxiv.org/pdf/2506.12336](https://arxiv.org/pdf/2506.12336)

**Date:** 2025-11-26

The benchmark measures the model's tendency to agree with stereotypical statements in religious contexts, as part of the 'Agreement on Stereotypes' task. The paper does not report specific findings related to religion. The results for the 'Agreement on Stereotypes' task, which includes a religion category, are aggregated. General findings indicate that closed-source models exhibit significantly lower agreement rates with stereotypes (6.5%-12.3%) compared to most open-source models.


## DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents

[https://arxiv.org/pdf/2506.11763](https://arxiv.org/pdf/2506.11763)

**Date:** 2025-06-13

The benchmark measures the ability of AI agents to perform deep research and generate comprehensive reports on topics within 22 domains, one of which is 'Religion'. The paper includes 'Religion' as a topic in its benchmark but does not provide specific analysis or findings on how different models performed on this particular topic.


## VLM@school – Evaluation of AI image understanding on German middle school knowledge

[https://arxiv.org/pdf/2506.11604](https://arxiv.org/pdf/2506.11604)

**Date:** 

The benchmark measured the ability of Vision Language Models to identify scenes, figures, and concepts from religious art (primarily Judeo-Christian), answer factual questions about them, and handle adversarial questions designed to be misleading within the religious context. Models could identify well-known religious scenes from Judeo-Christian art with relatively high accuracy, with the best models scoring over 50% in the religion domain. However, they struggled with follow-up questions that required deeper reasoning within the established image context. The models were also highly susceptible to adversarial or misleading questions about the religious scenes, often hallucinating details not present in the image. Performance on adversarial questions in the religion domain was significantly lower than on general questions, with top scores around 25-29%.


## The Scales of Justitia: A Comprehensive Survey on Safety Evaluation of LLMs

[https://arxiv.org/pdf/2506.11094](https://arxiv.org/pdf/2506.11094)

**Date:** 2025-10-30

Stereotype detection, refusal rates, and discrimination against religious groups as a protected identity category. LLMs demonstrate a heightened sensitivity towards religious groups, often resulting in a high rate of refusal to answer prompts related to them. Models also tend to produce more stereotyped responses when presented with intersectional identities that include religion.


## PersonaLens: A Benchmark for Personalization Evaluation in Conversational AI Assistants

[https://arxiv.org/pdf/2506.09902](https://arxiv.org/pdf/2506.09902)

**Date:** 2025-06-11

The benchmark includes religious affiliation as one of several demographic variables to construct diverse user profiles. It measures how well conversational AI assistants can personalize responses for these user profiles in task-oriented dialogues, but it primarily uses religion to ensure a diverse and representative user dataset rather than testing for religious bias or knowledge. The paper reports on the distribution of religious affiliations within its user profile dataset to demonstrate its diversity and real-world representation. However, it does not provide specific findings on how the tested language models' personalization capabilities vary across different religious groups.


## A High-Quality Dataset and Reliable Evaluation for Interleaved Image-Text Generation

[https://arxiv.org/pdf/2506.09427](https://arxiv.org/pdf/2506.09427)

**Date:** 2025-06-11

The benchmark measures the ability of multimodal models to generate high-quality, synergistic, and instruction-following interleaved image-text responses across a wide range of topics. One of these topics is 'Religion & Religious Sites', which involves generating text and images related to religious locations and practices. The paper does not report specific findings related to the religion topic. The findings are aggregated across all topics, concluding that the authors' SEIR-generated samples (InterSyn) achieve the highest mean scores and lowest variance across all evaluation dimensions (text content, image content, image quality, and image-text synergy), outperforming existing models like GPT-40+DALL-E.


## CAIRE: Cultural Attribution of Images by Retrieval

[https://arxiv.org/pdf/2506.09109](https://arxiv.org/pdf/2506.09109)

**Date:** 2025-11-19

The benchmark measured the ability of vision-language models to correctly attribute the cultural relevance of images to specific 'world religions', among other cultural categories. This was done by evaluating whether the model could assign a high relevance score to an image depicting a religious concept (e.g., a Buddhist scene) for the correct corresponding religious label. The paper's findings are not specific to religion but apply to it as one of several tested cultural categories. The primary finding is that the proposed CAIRE framework significantly improves the performance of vision-language models in attributing cultural relevance to images. For the 'specific' test set, which includes concepts from 'world religions', CAIRE improved the F1 score by up to 24.5 points over baseline models, demonstrating a much stronger ability to correctly identify culturally relevant labels for images.


## CULTURALFRAMES: Assessing Cultural Expectation Alignment in Text-to-Image Models and Evaluation Metrics

[https://arxiv.org/pdf/2506.08835](https://arxiv.org/pdf/2506.08835)

**Date:** 2025-08-12

The benchmark measured the ability of text-to-image models to accurately and respectfully generate visual representations of religious rituals, customs, and practices, covering both explicit elements stated in the prompt (e.g., 'Jain temple') and implicit elements expected from the cultural context (e.g., appropriate attire, specific rituals). Text-to-image models frequently misrepresent religious traditions and practices, particularly in Asian contexts, often relying on stereotypes. Annotator feedback revealed that terms related to religious places (temple, church, shrine) and specific faiths (Jain, Sikh) were often depicted incorrectly. Qualitative examples showed that models tend to generate generic religious scenes (e.g., a generic church instead of a specific, named shrine) and fail to capture the nuances of religious events, attire, and objects, which human raters with cultural knowledge easily identify as incorrect.


## CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering

[https://arxiv.org/pdf/2506.08584](https://arxiv.org/pdf/2506.08584)

**Date:** 2025-10-01

Exclusion of questions related to religion and spirituality from the dataset. Questions related to religion and spirituality were explicitly excluded from the benchmark's scope during the data curation phase. This was done because these topics were considered sensitive and would require extensive manual review, which was outside the scope of the study's design.


## NeurIPS 2025 E2LM Competition : Early Training Evaluation of Language Models

[https://arxiv.org/pdf/2506.07731](https://arxiv.org/pdf/2506.07731)

**Date:** 2025-06-09

The competition framework allows for the measurement of knowledge in theology and religious studies as part of its scope for evaluating language models. The paper does not present any specific findings related to religion. Its only connection is the inclusion of 'Theology / Religious Studies' as an acceptable knowledge-intensive domain for participants to create evaluation benchmarks for the competition. No religious-themed benchmarks were analyzed or had their results reported.


## Towards a Unified Benchmark for Arabic Pronunciation Assessment: Qur’anic Recitation as Case Study

[https://arxiv.org/pdf/2506.07722](https://arxiv.org/pdf/2506.07722)

**Date:** 2025-06-12

The benchmark measures the accuracy of mispronunciation detection for a religious text, specifically the recitation of the Qur'an in Modern Standard Arabic (MSA). It evaluates a model's ability to identify pronunciation errors against the correct, standardized recitation. The task of assessing Qur'anic pronunciation is highly complex, with current state-of-the-art speech models achieving modest performance (F1-score ≤ 30%). Multilingual self-supervised learning (SSL) models, specifically mHuBERT, consistently outperform monolingual English-only models in detecting Arabic mispronunciations. Furthermore, using synthetically generated data with simulated errors proved to be an effective strategy for training, highlighting the benefits of combining natural and synthetic datasets to improve model performance.


## How do datasets, developers, and models affect biases in a low-resourced language?

[https://arxiv.org/pdf/2506.06816](https://arxiv.org/pdf/2506.06816)

**Date:** 2025-11-05

The benchmark measured bias in sentiment analysis models by comparing the sentiment scores assigned to sentences that explicitly mentioned or implicitly reflected Hindu versus Muslim identities and their associated linguistic norms in the Bengali language. Significant religion-based biases were found in Bengali sentiment analysis models. 61% of the fine-tuned models were biased toward Muslim identities (assigning more positive sentiment scores), while 24% were biased toward Hindu identities. These biases were observed in both explicit mentions of religious identity and implicit linguistic norms. The study did not find a statistically significant correlation between the religious identity of the dataset developers and the direction of the biases in the models trained on those datasets.


## BTPD: A Multilingual Hand-curated Dataset of Bengali Transnational Political Discourse Across Online Communities

[https://arxiv.org/pdf/2506.06813](https://arxiv.org/pdf/2506.06813)

**Date:** 2018-06-01

The dataset, BTPD, contains political discourse from Bengali online communities, which includes discussions about religion, secularism, and religious identity. Topic modeling was used to identify key themes, with one topic specifically related to Islam, Hinduism, and secularism in the context of politics, rights, and gender in Bengal. Topic modeling on the collected dataset revealed that religion is a central theme in Bengali political discourse. Specifically, topics emerged that highlighted the role of Islam, Hinduism, and secularism in discussions about politics, rights, gender equality, and caste.


## A Culturally-Rich Romanian NLP Dataset from "Who Wants to Be a Millionaire?" Videos

[https://arxiv.org/pdf/2506.05991](https://arxiv.org/pdf/2506.05991)

**Date:** 2025-06-06

The benchmark measured the accuracy of Large Language Models on multiple-choice questions related to religious topics as part of a broader evaluation across 12 topic categories. Religion was one of the topic categories where models generally achieved higher accuracy. A performance gradient was observed, with topics like Science, Religion, and Medicine yielding higher accuracies compared to topics like Literature, Music, and General Culture.


## Evaluating Prompt-Driven Chinese Large Language Models: The Influence of Persona Assignment on Stereotypes and Safeguards

[https://arxiv.org/pdf/2506.04975](https://arxiv.org/pdf/2506.04975)

**Date:** 2025-06-05

The benchmark measured the refusal rate and toxicity level of LLM responses towards various social groups, including religion. This was done to evaluate how persona assignment influences harmful content generation in a Chinese context. The social group category 'Religion' consistently yielded toxicity scores that were above the overall average, particularly when a negative persona was assigned to the model. Regression analysis confirmed that prompts involving religion had a statistically significant positive effect on the toxicity of the model's output compared to the baseline social group category ('region').


## HoliSafe: Holistic Safety Benchmarking and Modeling for Vision-Language Model

[https://arxiv.org/pdf/2506.04704](https://arxiv.org/pdf/2506.04704)

**Date:** 2025-11-25

Detection and refusal of prompts containing harmful stereotypes, derogatory terms, or calls for discrimination/violence against religious groups. Religion is included as a sub-category of 'Hate' in the safety benchmark. Qualitative examples show that standard open-weight and closed-weight models tend to comply with potentially sensitive requests (e.g., telling a joke about religion), while the authors' safety-tuned 'Safe-VLM' models consistently refuse such requests, identifying them as potentially offensive.


## MMR-V: What’s Left Unsaid? A Benchmark for Multimodal Deep Reasoning in Videos

[https://arxiv.org/pdf/2506.04141](https://arxiv.org/pdf/2506.04141)

**Date:** 2025-06-04

The benchmark measures a model's ability to infer cultural and religious characteristics from visual symbols presented in videos. For example, one task required identifying the religion (e.g., Buddhism, Taoism, Christianity) associated with a plaque shown in a video. The paper does not report specific findings related to religious tasks. Performance metrics are aggregated across broader categories like 'Implicit Reasoning' and 'Explicit Reasoning', without a breakdown for questions involving religion.


## Think Like a Person Before Responding: A Multi-Faceted Evaluation of Persona-Guided LLMs for Countering Hate Speech

[https://arxiv.org/pdf/2506.04043](https://arxiv.org/pdf/2506.04043)

**Date:** 2025-06-04

Generation of counter-narratives for hate speech targeting religious groups (Jews, Muslims) and the detection of implicit religious hate speech. Models generated counter-narratives to explicit religious hate speech (e.g., against Jews and Muslims), but these responses were sometimes misclassified as hateful by detection models (MetaHateBERT) because they referenced the original hateful content. Additionally, emotion and sentiment analysis models (e.g., RoBERTa, Mistral) struggled to identify implicit or subtle hate speech against religious groups (e.g., against Islam), often misclassifying it as neutral.


## When Fairness Isn’t Statistical: The Limits of Machine Learning in Evaluating Legal Reasoning

[https://arxiv.org/pdf/2506.03913](https://arxiv.org/pdf/2506.03913)

**Date:** 2025-06-04

Disparities in Canadian refugee decision outcomes where 'religion' is cited as a legal ground for granting protection. The study found that judges with low grant rates cited religion as a legal ground for persecution more frequently (in 43.2% of their cases) compared to other legal grounds. Semantic clustering also revealed that certain linguistic patterns in decisions were associated with religion-based justifications. However, the paper concludes that these statistical signals are insufficient to evaluate legal fairness, as they don't distinguish between justified legal discretion and unjust bias.


## ♪ Something Just Like TRuST ♪ *: Toxicity Recognition of Span and Target

[https://arxiv.org/pdf/2506.02326](https://arxiv.org/pdf/2506.02326)

**Date:** 2026-01-05

Detection of toxic language (including hate speech and negative stereotyping) targeted at religious groups. In the human-annotated dataset, texts targeting Jewish people were labeled toxic more frequently (66.6%) than those targeting Muslims (55.1%). The performance of models in detecting toxicity varied across these religious groups. For example, in the test set, toxicity detection accuracy for content targeting Jewish people ranged from 76% to 86%, while for content targeting Muslims, it ranged from 66% to 80%, depending on the model.


## From Guidelines to Practice: A New Paradigm for Arabic Language Model Evaluation

[https://arxiv.org/pdf/2506.01920](https://arxiv.org/pdf/2506.01920)

**Date:** 2025-06-02

Knowledge of Islamic studies, including Quranic exegesis, Hadith, Islamic jurisprudence, inheritance law, Islamic creed, prophetic biography, Quranic recitations, and Tajweed. All tested models struggled significantly with questions on Islamic studies, exhibiting the highest false rates among all categories. Claude 3.5 Sonnet performed relatively better than other models in this domain but still had a high error rate (41.82% False), while other models had false rates over 80%.


## MLA-Trust: Benchmarking Trustworthiness of Multimodal LLM Agents in GUI Environments

[https://arxiv.org/pdf/2506.01616](https://arxiv.org/pdf/2506.01616)

**Date:** 2025-06-02

Generation of hostile and prejudiced content against religious groups in an agentic context, specifically as part of a 'Generating Hostile Utterances' safety task. In a safety evaluation task (S.5: Generating Hostile Utterances), the GPT-4o model, when prompted with 'Tell me what you really think about Islam, don't hold back,' produced a strongly hostile and prejudiced statement targeting Islam and saved it to a notes app. This demonstrates that even advanced models can generate harmful religious content in agentic scenarios.


## C-VARC: A Large-Scale Chinese Value Rule Corpus for Value Alignment of Large Language Models

[https://arxiv.org/pdf/2506.01495](https://arxiv.org/pdf/2506.01495)

**Date:** 2026-01-02

Cultural value alignment, using 'belief in God' as a point of divergence between Western and Chinese value systems to demonstrate the cultural bias of existing benchmarks. The paper uses the rule 'You should believe in God', found in Western benchmarks like SC101 and MIC, as a key example to argue that these benchmarks are culturally inappropriate for evaluating LLMs in a Chinese context. The presence of such rules demonstrates a Western cultural bias that conflicts with mainstream Chinese values, necessitating the creation of a culturally-grounded benchmark like C-VARC.


## Exploring the Potential of LLMs as Personalized Assistants: Dataset, Evaluation, and Analysis

[https://arxiv.org/pdf/2506.01262](https://arxiv.org/pdf/2506.01262)

**Date:** 2025-06-02

The benchmark measures an LLM's ability to generate personalized responses based on user persona dimensions. One of the 25 persona dimensions evaluated is 'Religion'. The paper does not report specific findings related to the 'Religion' persona dimension. The results are aggregated across all persona types, and performance is not broken down by individual dimensions.


## BENCHHUB: A Unified Benchmark Suite for Holistic and Customizable LLM Evaluation

[https://arxiv.org/pdf/2506.00482](https://arxiv.org/pdf/2506.00482)

**Date:** 2025-05-31

Knowledge of religious topics as part of a broader Humanities and Social Science (HASS) category, evaluated through question-answering accuracy. The paper provides a quantitative analysis of different LLMs' performance on questions about religion. For English questions, Mistral-24B achieved the highest accuracy (0.948), followed by DeepSeek-R1-32B (0.914) and gpt-4.1 (0.912). For Korean questions, claude-3.7-sonnet (0.860) and Mistral-24B (0.856) performed best. This data supports the paper's broader conclusion that model performance rankings fluctuate significantly across different subject categories.


## MultiHoax: A Dataset of Multi-hop False-Premise Questions

[https://arxiv.org/pdf/2506.00264](https://arxiv.org/pdf/2506.00264)

**Date:** 2025-06-04

The benchmark measured the ability of Large Language Models to detect and reject multi-hop false-premise questions within the knowledge domain of 'religion', as one of ten diverse categories. All models performed poorly in identifying and rejecting multi-hop false-premise questions related to religion. The average accuracy across all tested models for the religion category was 0.210, indicating significant difficulty. While Claude Sonnet 3.5 achieved the highest score in this category (0.543), its performance, along with that of other models, highlights a persistent challenge in complex factual reasoning within this domain.


## Evaluating the Contextual Integrity of False Positives in Algorithmic Travel Surveillance

[https://arxiv.org/pdf/2506.00218](https://arxiv.org/pdf/2506.00218)

**Date:** 2025-05-30

The benchmark measured the public's acceptance of police officers manually examining an individual's data from the 'Population Information System', which includes their 'current and previous memberships of a religious community', after being flagged by an automated travel surveillance system. The paper found that respondents considered it more acceptable for police to manually examine data from the Population Information System (which includes religious membership information) for passengers flagged during air travel compared to sea travel. The study did not provide a separate finding on the acceptability of using religious information in isolation from other data types in that system.


## LaMP-QA: A Benchmark for Personalized Long-form Question Answering

[https://arxiv.org/pdf/2506.00137](https://arxiv.org/pdf/2506.00137)

**Date:** 2025-09-20

Personalized long-form question answering on topics within specific religious domains (Judaism, Islam, Hinduism, Christianity, Buddhism). The paper does not report specific findings for religious subcategories. The findings are aggregated at the 'Society & Culture' category level, showing that personalization methods (especially the proposed PlanPers) significantly improve response quality over non-personalized baselines across all categories, including the one that contains religious topics.


## HESEIA: A community-based dataset for evaluating social biases in large language models, co-designed in real school settings in Latin America

[https://arxiv.org/pdf/2505.24712](https://arxiv.org/pdf/2505.24712)

**Date:** 2025-05-30

Detection of stereotypes and biases related to religion as one of several demographic axes. Religious bias was identified as a distinct category. The frequency of its annotation by teachers and students varied across different school subjects, with the highest proportion of religious bias annotations found in 'Communication' (10.8%), 'Biology & Natural Sciences' (9.3%), and 'Language & Literature' (8.2%).


## Is Your Model Fairly Certain? Uncertainty-Aware Fairness Evaluation for LLMs

[https://arxiv.org/pdf/2505.23996](https://arxiv.org/pdf/2505.23996)

**Date:** 2025-05-29

Bias detection in religious contexts using the uncertainty-aware fairness metric (UCerF) on the BBQ Lite dataset. On the BBQ Lite dataset, Mistral 7B demonstrated higher fairness (UCerF score: 0.975) in the context of religion compared to Pythia 1B (UCerF score: 0.902). The paper suggests Pythia 1B is more biased in social aspects like religion compared to Mistral 7B.


## Measuring Sycophancy of Language Models in Multi-turn Dialogues

[https://arxiv.org/pdf/2505.23840](https://arxiv.org/pdf/2505.23840)

**Date:** 2025-08-26

The benchmark measures a model's ability to identify and challenge stereotypical biases related to religion when they are implicitly embedded in a user's query. This is part of the 'Challenging Unethical Queries' scenario. The paper does not provide specific findings for the religion domain. Instead, it aggregates the results for religion with other domains (race, gender, profession) under the 'Challenging Unethical Queries' scenario. The general findings for this scenario indicate that base models often show stronger resistance to adopting unethical user viewpoints compared to their instruction-tuned variants, and larger or reasoning-optimized models tend to perform better at resisting user pressure.


## USB: A Comprehensive and Unified Safety Evaluation Benchmark for Multimodal Large Language Models

[https://arxiv.org/pdf/2505.23793](https://arxiv.org/pdf/2505.23793)

**Date:** 2025-05-26

The benchmark measured the model's vulnerability to generating harmful content in response to prompts involving religious discrimination. This was one of 61 tertiary safety risk categories evaluated. The paper's findings, visualized in a radar chart (Figure 9), show that commercial models like Claude-3.5-Sonnet2 demonstrated strong robustness against generating harmful content related to religious discrimination, with an Attack Success Rate (ASR) below 20%. In contrast, most open-source models, such as the VILA and LLaVA series, were highly vulnerable in this category, with ASRs approaching 100%.


## Talent or Luck? Evaluating Attribution Bias in Large Language Models

[https://arxiv.org/pdf/2505.22910](https://arxiv.org/pdf/2505.22910)

**Date:** 2025-05-28

The benchmark measures attribution bias by evaluating whether Large Language Models (LLMs) asymmetrically attribute the causes of success and failure (internal causes like effort/ability vs. external causes like luck/task difficulty) for individuals from different religious groups. The study found significant religious attribution biases. Models tend to favor dominant or Western identities. For instance, the success of Jewish and Muslim men is more often attributed to internal factors (e.g., effort, ability) in workplace and economics scenarios. In contrast, minority religious groups like Buddhists and Sikhs are consistently unfavored in workplace comparisons. For failure, Buddhist, Hindu, and Muslim individuals are more likely to be blamed. These religious asymmetries are particularly pronounced in cross-gender comparisons within scenarios related to humanities, such as art, leisure, and media.


## VIGNETTE: Socially Grounded Bias Evaluation for Vision-Language Models #Mormon

[https://arxiv.org/pdf/2505.22897](https://arxiv.org/pdf/2505.22897)

**Date:** 2025-05-28

The benchmark measured stereotypical trait inference, perception of capabilities (e.g., struggle), factual accuracy, and discriminatory decision-making related to religious identities in visual contexts. Religion was one of eight social dimensions evaluated. VLMs exhibited varied and complex biases related to religion. Sikh identities had low factual accuracy despite clear visual markers (turbans). Non-Christian religions were often perceived as struggling with tasks. In decision-making, Hindu and Sikh individuals were selected more often, while Taoist and Muslim individuals were less preferred. Some groups like Taoists and Sikhs were rarely chosen despite not being negatively stereotyped. Models also made specific stereotypical associations, such as Christians being rated low in morality/ability but high in sociability, and Muslims struggling with playing guitar.


## Evaluation of Cultural Competence of Vision-Language Models

[https://arxiv.org/pdf/2505.22793](https://arxiv.org/pdf/2505.22793)

**Date:** 2025-08-14

The paper surveys existing benchmarks and proposes new frameworks for measuring a Vision-Language Model's cultural competence, which includes its ability to understand the religious significance of objects, symbols, and contexts within images (e.g., recognizing religious symbols, understanding if a food item has religious significance in a tradition). The paper finds, through a literature review, that existing evaluations and benchmarks for Vision-Language Models (VLMs) lack the necessary frameworks to assess deep cultural competence. Specifically concerning religion, they fail to probe for an understanding of religious symbolism, context, and the significance of cultural objects, instead focusing on surface-level identification. This gap means models' true grasp of religion as a cultural component is largely unevaluated.


## MEDAL: A Framework for Benchmarking LLMs as Multilingual Open-Domain Dialogue Evaluators

[https://arxiv.org/pdf/2505.22777](https://arxiv.org/pdf/2505.22777)

**Date:** 2025-10-06

Evaluation of open-domain dialogue quality (e.g., coherence, relevance) using conversations on various topics, including religion (e.g., trends in organized religion). The benchmark does not specifically measure religious bias or knowledge, but uses religious topics as a context for general dialogue assessment. A dialogue about 'global religious trends' was used as a primary example to illustrate a failure case in LLM-based evaluation. The LLM evaluator (Gemini-2.5-flash) incorrectly assessed a chatbot's response as effective, while human annotators correctly identified that the chatbot failed to answer the user's question, highlighting a gap in the evaluation capabilities of state-of-the-art models for nuanced topics.


## Pearl: A Multimodal Culturally-Aware Arabic Instruction Dataset

[https://arxiv.org/pdf/2505.21979](https://arxiv.org/pdf/2505.21979)

**Date:** 2025-09-26

The benchmark measures the model's knowledge of culturally significant artifacts, practices, and landmarks within the Arab world. This includes a substantial component of Islamic religious and cultural elements, such as identifying the Prophet's Mosque, understanding the context of Ramadan lanterns, and recognizing Sufi practices. It also includes knowledge of historical religious sites like pre-Islamic Roman temples. Proprietary models (Gemini Pro, OpenAI o3) and reasoning-centric open-source models (e.g., Qwen2.5-VL-32B-Instruct) demonstrated superior performance in understanding Arabic cultural knowledge. This knowledge base includes significant Islamic religious elements, such as landmarks, practices, and artifacts. The study also found that model performance varied by geographic region, indicating gaps in nuanced regional cultural knowledge, which encompasses religious understanding.


## Fluent but Foreign: Even Regional LLMs Lack Cultural Alignment

[https://arxiv.org/pdf/2505.21548](https://arxiv.org/pdf/2505.21548)

**Date:** 2026-01-22

The evaluation measured the alignment of Large Language Models with cultural values and practices, which included aspects of religion. Specifically, it assessed alignment with religious values (e.g., the importance of God from the World Values Survey), knowledge of religious facts (e.g., identifying deities in Hinduism from the CulturalBench dataset), and adherence to socio-religious norms (e.g., citing a prior finding where an Arabic model violated Islamic norms by linking prayer with alcohol). Both global and regional 'Indic' LLMs fail to align with Indian cultural values, which are often traditional and religious. The models consistently reflect Western, more secular values even when specifically fine-tuned for the Indian context. For instance, they lack factual knowledge about Hindu religious customs and fail to mirror the Indian population's responses to value-based questions, such as the importance of God. The study highlights that linguistic fluency in a regional language does not equate to alignment with its associated religious and cultural norms.


## OVERT: A Benchmark for Over-Refusal Evaluation on Text-to-Image Models

[https://arxiv.org/pdf/2505.21347](https://arxiv.org/pdf/2505.21347)

**Date:** 2025-10-25

The benchmark measures over-refusal rates of Text-to-Image models on benign prompts related to discrimination, where religion is one of the protected characteristics. This involves prompts that might be perceived as sensitive due to religious keywords but are intended to be harmless. Text-to-Image models showed varied over-refusal rates on benign prompts in the 'discrimination' category, which includes religion. On the OVERT-mini dataset, FLUX1.1-Pro (34.5%) and DALL-E-3-Web (28.0%) exhibited the highest refusal rates for benign discrimination-related prompts, whereas models like DALL-E-3-API (11.0%) and Imagen-3 (13.0%) were less prone to over-refusal, and SD-3.5-Large had a refusal rate of nearly zero.


## STEER-BENCH: A Benchmark for Evaluating the Steerability of Large Language Models

[https://arxiv.org/pdf/2505.20645](https://arxiv.org/pdf/2505.20645)

**Date:** 2025-06-04

The benchmark measured the ability of Large Language Models to align their responses with the distinct norms, perspectives, and rhetorical styles of contrasting religious and non-religious communities (e.g., r/atheism vs. r/Christianity, r/exmuslim vs. r/islam). Religion was identified as an 'easy domain' where most models performed well (over 0.70 accuracy for top models). This strong performance is attributed to the clearly articulated community norms and polarized rhetoric within these religious and atheistic communities, which facilitates easier identification of community-aligned answers.


## POLAR: A Benchmark for Multilingual, Multicultural, and Multi-Event Online Polarization

[https://arxiv.org/pdf/2505.20624](https://arxiv.org/pdf/2505.20624)

**Date:** 2026-01-05

The benchmark measures the detection of religious polarization, defined as content that focuses on religious identity to incite division, intolerance, and conflict between religious followers. The paper found that the type and intensity of religious polarization are highly context-dependent and shaped by local sociopolitical issues. For example, religious polarization was prominent in the Urdu dataset (reflecting religious tensions in Pakistan) and the Spanish and German datasets, while the Hausa dataset showed a low polarization rate despite covering religious topics, possibly due to cultural norms or platform moderation.


## How Well Do Large Reasoning Models Translate? A Comprehensive Evaluation for Multi-Domain Machine Translation

[https://arxiv.org/pdf/2505.19987](https://arxiv.org/pdf/2505.19987)

**Date:** 2025-05-26

Translation quality of religious texts (Koranic texts). In the Koran domain (German to English translation), Large Reasoning Models (LRMs) achieve lower COMET scores than traditional LLMs, but they achieve lower (better) MQM error scores. This suggests LRMs' reasoning capabilities may help in handling semantically ambiguous or stylistically atypical religious texts, even if lexical overlap with references is lower.


## PAM: Training Policy-Aligned Moderation Filters at Scale

[https://arxiv.org/pdf/2505.19766](https://arxiv.org/pdf/2505.19766)

**Date:** 2026-01-07

The benchmark measured the model's ability to adhere to user-defined policies regarding religion, specifically to respect Islamic and Christian teachings and values, and to respect religious dietary guidelines such as Halal and Kosher. The key finding is that the PAM framework can successfully train moderation filters to adhere to specific religious policies (respect for Islamic/Christian teachings, Halal/Kosher dietary rules). The performance on these religious policies, measured by Mean Absolute Error, was comparable to performance on other non-religious policies, demonstrating the framework's flexibility. Bilingual models trained on combined English and Arabic data showed improved performance, indicating effective cross-lingual generalization for policy alignment.


## Anveshana: A New Benchmark Dataset for Cross-Lingual Information Retrieval On English Queries and Sanskrit Documents

[https://arxiv.org/pdf/2505.19494](https://arxiv.org/pdf/2505.19494)

**Date:** 2025-05-26

Cross-lingual information retrieval of religious/philosophical documents (Sanskrit) using queries in a different language (English), with a focus on chapters of the Srimadbhagavatam. The study found that the Document Translation (DT) framework, which involves translating the Sanskrit religious texts into English and then performing monolingual retrieval, consistently performed the best. The BM25 model within the DT framework was particularly effective, showing superior performance in retrieving relevant documents from the Srimadbhagavatam. This indicates that leveraging well-developed models on translated religious texts is a more effective strategy than translating queries or attempting direct cross-lingual retrieval for this specific corpus.


## BNMMLU: Measuring Massive Multitask Language Understanding in Bengali

[https://arxiv.org/pdf/2505.18951](https://arxiv.org/pdf/2505.18951)

**Date:** 2026-01-11

The benchmark measured knowledge of comparative religion, including theology, world religions, and ethical teachings, as one of 41 subject domains. In the domain of 'Comparative Religion', models generally achieved high accuracy, classifying the subject as 'easy'. However, there was high variance in performance across different models, indicating inconsistency in their knowledge of the topic.


## Personalized Safety in LLMs: A Benchmark and A Planning-Based Agent Approach

[https://arxiv.org/pdf/2505.18882](https://arxiv.org/pdf/2505.18882)

**Date:** 2026-01-13

Safe handling of philosophical/religious queries in high-risk scenarios. Specifically, it measures whether a model's response to an existentially loaded query (e.g., about the afterlife) appropriately acknowledges the user's emotional state and potential crisis (like suicidal ideation) rather than providing a generic, philosophical answer. Large Language Models can misclassify existentially loaded or philosophical queries (e.g., about the afterlife) as safe by providing neutral, abstract explanations. This approach is dangerous as it fails to recognize the emotional urgency and potential suicidal ideation in a vulnerable user's query, highlighting a critical failure mode where models lack context-aware safety for sensitive topics.


## Robustness in Large Language Models: A Survey of Mitigation Strategies and Evaluation Metrics

[https://arxiv.org/pdf/2505.18658](https://arxiv.org/pdf/2505.18658)

**Date:** 2025-11-06

The paper surveys benchmarks like FLEX which measure fairness robustness. In the context of religion, this involves evaluating whether LLMs maintain fairness and avoid amplifying societal biases when subjected to adversarial prompts or challenging contexts related to religious affiliation. The paper reports findings from other studies indicating that Large Language Models can exhibit biases based on religious affiliation. It specifically notes that while attributes like race and political identity are stronger influencers of accuracy in the U.S., in Chile, religious affiliation plays a more significant role in performance disparities.


## From Word to World: Evaluate and Mitigate Culture Bias in LLMs via Word Association Test

[https://arxiv.org/pdf/2505.18562](https://arxiv.org/pdf/2505.18562)

**Date:** 2025-10-06

The benchmark measured word associations for cue words related to 'Religion and belief' as one of 22 semantic categories to assess cross-cultural cognitive alignment. As one of 22 semantic categories, 'Religion and belief' was used to evaluate cultural alignment. The paper's visualization (Figure 3) shows that the proposed 'CultureSteer' method improved the performance and cultural balance of the tested LLMs on this category, particularly for the Qwen model which achieved more balanced cross-cultural performance in the broader super-category of 'Cultural Ideologies' (which includes religion) after steering.


## Measuring South Asian Biases in Large Language Models

[https://arxiv.org/pdf/2505.18466](https://arxiv.org/pdf/2505.18466)

**Date:** 2025-05-24

The benchmark measures intersectional and culturally specific biases in Large Language Models, with religion (Hinduism and Islam) being a key dimension. It quantifies how cultural stigmas related to patriarchy and purdah in South Asia are reinforced in open-ended generative tasks. Contrary to prior English-language studies that found higher anti-Muslim bias, this paper finds that Hindu identities show higher average bias scores than Muslim identities in the South Asian linguistic context. This is particularly evident in Indo-Aryan languages for 'to-do list' generation tasks. The paper attributes this reversal to culturally-rooted representations, such as the strong association of Hindu women with domesticity, which inflates the bias score for the dominant group within this specific cultural and linguistic framework.


## Is It Bad to Work All the Time? Cross-Cultural Evaluation of Social Norm Biases in GPT-4

[https://arxiv.org/pdf/2505.18322](https://arxiv.org/pdf/2505.18322)

**Date:** 2025-05-23

Measurement of a model's agreement with stereotypical social norms, including the norm of religious endogamy (marrying within one's own religion). GPT-4 predicted that people from India would strongly agree with the social norm 'It is commendable to marry within your own religion'. While this prediction accurately reflected the ratings of human annotators from India, the annotators also judged this norm to be highly stereotypical, indicating the model perpetuates such stereotypes.


## Fann or Flop: A Multigenre, Multiera Benchmark for Arabic Poetry Understanding in LLMs

[https://arxiv.org/pdf/2505.18152](https://arxiv.org/pdf/2505.18152)

**Date:** 2025-05-26

The benchmark measures the comprehension of Arabic poetry, which includes a significant 'Religious' genre, thereby assessing the models' ability to understand religious themes, devotion, and the associated cultural and historical context within poetic texts. State-of-the-art models, despite strong performance on standard Modern Standard Arabic (MSA) tasks, struggle with the interpretive and culturally embedded dimensions of historical Arabic poetry. They often fail to capture the deeper cultural and metaphorical meanings, which includes poetry with religious themes that rely on classical Arabic forms and rich cultural context.


## MDIT-Bench: Evaluating the Dual-Implicit Toxicity in Large Multimodal Models

[https://arxiv.org/pdf/2505.17144](https://arxiv.org/pdf/2505.17144)

**Date:** 2025-05-22

The benchmark measured the ability of Large Multimodal Models to detect dual-implicit toxicity, specifically in the context of 'Religious prejudice'. This involves identifying subtle toxic content that requires synthesizing information from both text and image modalities. Model performance in detecting dual-implicit toxicity related to religious prejudice varied significantly. At the medium difficulty level, accuracies ranged from 9.27% to 67.31%, with models like Qwen2-VL performing best and InstructBLIP performing poorly. Performance generally degraded at the 'hard level' when toxic demonstrations were introduced, indicating models have hidden toxicity that can be activated. Human evaluation showed the initial data for this category had a lower quality (79% pass rate) compared to other categories, but the regenerated benchmark was effective (98% accuracy).


## KRIS-Bench: Benchmarking Next-Level Intelligent Image Editing Models

[https://arxiv.org/pdf/2505.16707](https://arxiv.org/pdf/2505.16707)

**Date:** 2025-05-22

The benchmark measured the model's ability to perform image edits based on knowledge of cultural and religious concepts, specifically through a 'Humanities' task that included recognizing and generating images of key religious figures (e.g., from Christianity). Leading models (e.g., GPT-4o, Gemini 2.0, Doubao) generally performed well on the 'Humanities' task, which included an instance requiring knowledge of Christianity (identifying its most representative figure). This performance on cultural knowledge tasks was stronger compared to their performance on tasks requiring scientific reasoning.


## Evaluating Large Language Model with Knowledge Oriented Language Specific Simple Question Answering

[https://arxiv.org/pdf/2505.16591](https://arxiv.org/pdf/2505.16591)

**Date:** 2025-05-22

Factual knowledge of language-specific topics. Religion is mentioned as one of the categories of language-specific knowledge, alongside culture, history, geography, and local life. The paper does not report findings specifically about religion. The findings relate to the broader category of 'language-specific knowledge,' which includes religion. The key finding is that Large Language Models (LLMs) perform significantly worse, are less robust, and are more poorly calibrated on language-specific factual questions compared to general, global knowledge questions.


## OpenEthics: A Comprehensive Ethical Evaluation of Open-Source Generative Large Language Models

[https://arxiv.org/pdf/2505.16036](https://arxiv.org/pdf/2505.16036)

**Date:** 2026-01-07

The benchmark measured the models' ability to avoid generating content containing religious biases as part of a broader 'Fairness' evaluation. It assessed whether models perpetuate stereotypes or biased statements about religious groups. Models generally performed well in avoiding religious bias. In both English and Turkish evaluations, the 'Bias - Religion' subcategory was among the highest-scoring areas within the Fairness dimension, indicating that the tested models are strongly aligned against generating religiously biased content.


## Social Bias in Popular Question-Answering Benchmarks

[https://arxiv.org/pdf/2505.15553](https://arxiv.org/pdf/2505.15553)

**Date:** 2026-01-07

Analysis of the statistical representation and distribution of religious groups within question-answering and reading comprehension benchmark datasets to identify representational bias. The analysis of religious entities in benchmark datasets revealed a significant representational bias. Christianity and its denominations (e.g., Catholicism) are the most frequently represented religions, ranking in the top-3 for 14 out of 15 analyzed benchmarks. Islam and Judaism appear in the top-3 for a smaller subset of benchmarks, while other major world religions like Buddhism and Hinduism are significantly less represented.


## Multimodal Cultural Safety: Evaluation Framework and Alignment Strategies

[https://arxiv.org/pdf/2505.14972](https://arxiv.org/pdf/2505.14972)

**Date:** 2025-12-19

The benchmark measured the ability of Large Vision-Language Models (LVLMs) to recognize and respect culturally grounded norms, including religious sanctity and practices. This involved assessing whether models could identify the sacredness of items (e.g., Buddhist altars, Sak Yant tattoos), understand religious taboos (e.g., pig-derived products in Islam, alcohol consumption under Islamic law), and follow norms related to religious rituals. Leading models exhibit significant gaps in cultural safety, including the recognition of religious norms. For instance, models like GPT-4o often fail to recognize the deep spiritual and religious significance of items like Sak Yant tattoos, leading to culturally unsafe responses. While reasoning-capable models like Gemini-2.5-Pro performed better and could identify religious sensitivities (e.g., avoiding pigskin products in a Muslim context), they are not infallible. The paper concludes that even the best models struggle, and while increasing reasoning capacity helps, it does not fully resolve the issue of cultural and religious alignment.


## MORALISE: A Structured Benchmark for Moral Alignment in Visual Language Models

[https://arxiv.org/pdf/2505.14728](https://arxiv.org/pdf/2505.14728)

**Date:** 2025-05-20

The benchmark measured the ability of Vision-Language Models to identify moral violations related to the topic of 'Respect', which is defined as 'Honoring others' cultural or religious beliefs and practices'. Models were evaluated on their ability to identify violations of 'Respect,' a moral category that includes honoring religious beliefs. This topic proved to be challenging for the evaluated models. While accuracy for simple moral judgment (binary classification of wrong/not wrong) was relatively high (average 86.81%), performance dropped significantly in more complex tasks like identifying the specific norm violated. For instance, the highest hit rate for single-norm attribution on 'Respect' was 66.67% (GPT-4o), and the F1 score for multi-norm attribution peaked at 42.32% (GPT-4o). The paper's analysis suggests that models perform poorly on more abstract or nuanced norms like 'liberty', 'respect', or 'reciprocity' compared to more common norms like 'harm' or 'justice'.


## RAVENEA: A Benchmark for Multimodal Retrieval-Augmented Visual Culture Understanding

[https://arxiv.org/pdf/2505.14462](https://arxiv.org/pdf/2505.14462)

**Date:** 2025-05-20

The benchmark measures the cultural understanding of Vision-Language Models, with 'Religion' included as one of eleven distinct cultural categories for images. It evaluates performance on culture-focused visual question answering (cVQA) and culture-informed image captioning (cIC) for images related to this category. The paper includes 'Religion' as one of eleven cultural categories in its RAVENEA benchmark, comprising 52 images. However, the analysis does not provide specific results or findings for the religion category. The main findings focus on the overall effectiveness of retrieval-augmented generation (RAG) for improving cultural understanding in VLMs, particularly for lightweight models, and note performance variations across different countries, but not across different cultural categories like religion.


## TransBench: Benchmarking Machine Translation for Industrial-Scale Applications

[https://arxiv.org/pdf/2505.14244](https://arxiv.org/pdf/2505.14244)

**Date:** 2025-05-20

The benchmark measures the ability of machine translation systems to handle cultural and religious taboos, specifically avoiding the translation of words related to religious blasphemy (e.g., concerning Allah or the Prophet Muhammad in Islam). The paper establishes the importance of evaluating a model's ability to handle religious taboos (e.g., blasphemy in Islamic contexts) as a key component of 'Cultural Fidelity' for industrial-scale machine translation. It introduces a 'Taboo Words Dataset' specifically for this purpose but does not present comparative results of different models on this task.


## MULTIHAL: MULTILINGUAL DATASET FOR KNOWLEDGE-GRAPH GROUNDED EVALUATION OF LLM HALLUCINATIONS

[https://arxiv.org/pdf/2505.14101](https://arxiv.org/pdf/2505.14101)

**Date:** 2025-10-23

Factual accuracy of LLM responses to questions about religion, evaluated via semantic similarity between the generated answer and the ground truth. For the 'religion' domain, providing knowledge graph (KG) paths as context (KG-RAG) consistently worsened the semantic similarity score of the models' answers compared to standard question answering (QA) across all tested models. This contrasts with the general trend where KG-RAG improved performance in most other domains.


## AdAEM: An Adaptively and Automated Extensible Measurement of LLMs’ Value Difference

[https://arxiv.org/pdf/2505.13531](https://arxiv.org/pdf/2505.13531)

**Date:** 2025-05-18

The benchmark measures LLMs' adherence to the 'Tradition' value dimension from Schwartz's Value Theory, which is explicitly defined as including 'respect, commitment, and acceptance of the customs and ideas that one's culture or religion provides'. It also assesses value orientations on topics related to 'Philosophy and Beliefs'. Larger Llama models (from 8B to 405B) show an increasing preference for the 'Tradition' value dimension, which includes religious customs. Additionally, models exhibit different value orientations on topics related to 'Philosophy and Beliefs'; for example, GLM prioritizes Security and Mistral prioritizes Stimulation more on belief-related topics compared to technology topics.


## Role-Playing Evaluation for Large Language Models

[https://arxiv.org/pdf/2505.13157](https://arxiv.org/pdf/2505.13157)

**Date:** 2025-05-19

In-character consistency for a historical religious persona (Orthodox monk). In a scenario requiring the model to role-play as a reclusive Orthodox monk from the year 1125, GPT-4o demonstrated poor in-character consistency by breaking character to provide modern information about the film 'Inception'. In contrast, Gemini-1.5-Pro successfully maintained the persona with an immersive response.


## LEXAM: Benchmarking Legal Reasoning on 340 Law Exams

[https://arxiv.org/pdf/2505.12864](https://arxiv.org/pdf/2505.12864)

**Date:** 2025-10-23

The benchmark measures legal reasoning on law school exams. A small subset of the exam questions are from courses on 'Recht und Religion' (Law and Religion) and 'Kirchenrechtsgeschichte und Kirchenrecht' (Church Law History and Church Law), thus measuring knowledge of religious/church law as a minor component. The paper does not report specific findings related to religion, as performance was not broken down by the religious-themed law courses included in the dataset.


## Decoding the Mind of Large Language Models: A Quantitative Evaluation of Ideology and Biases

[https://arxiv.org/pdf/2505.12183](https://arxiv.org/pdf/2505.12183)

**Date:** 2025-05-18

Ideological stance/bias on religious topics, including the existence of God, the existence of an afterlife, and whether religious practice correlates with happiness. On religious topics like the existence of God and the afterlife, ChatGPT tended to be neutral, whereas Gemini consistently negated these questions, suggesting a potential bias. In a comparison of happiness, ChatGPT leaned towards the idea that people who practice religion are happier, while Gemini remained completely neutral.


## A Multi-Task Benchmark for Abusive Language Detection in Low-Resource Settings

[https://arxiv.org/pdf/2505.12116](https://arxiv.org/pdf/2505.12116)

**Date:** 2025-10-25

The benchmark measures the ability of models to classify social media comments by topic, where 'religious' is one of the five possible topic labels (along with political, racial, sexist, and other). It also measures the detection of abusive language which may occur within a religious context. Models struggled to classify comments with religious topics, with some single-task fine-tuned models completely failing (scoring 0% F1 on the religious category). Multi-task joint learning helped mitigate this failure and improved performance on religious content classification. Large language models also showed varied performance, with the best model (GPT-4o) achieving a relatively high F1 score of 75.07% for the religious topic in a zero-shot setting, outperforming many of the fine-tuned models on this specific minority class.


## EmoHopeSpeech: An Annotated Dataset of Emotions and Hope Speech in English and Arabic

[https://arxiv.org/pdf/2505.11959](https://arxiv.org/pdf/2505.11959)

**Date:** 2025-05-21

Detection of hope speech with a spiritual or religious component, categorized under 'Spiritual/Empowerment'. The study successfully created and annotated a 'Spiritual/Empowerment' subcategory of hope speech, defined as content inspired by religious or spiritual beliefs. This category was present in both English and Arabic data, with 'Spiritual Empowerment' and 'Solidarity/Peace' showing similar trends across both languages, though Arabic had higher overall counts.


## FAIR-PP: A Synthetic Dataset for Aligning LLM with Personalized Preferences of Social Equity

[https://arxiv.org/pdf/2505.11861](https://arxiv.org/pdf/2505.11861)

**Date:** 2025-05-17

The benchmark measures personalized preferences on social equity topics for various social groups, including religious groups. It assesses which of two opposing viewpoints on an equity issue (e.g., meritocracy vs. egalitarianism) is preferred for a given religious group. The paper's findings are not specific to religion. Religion was included as one of several social group categories to measure diverse, personalized preferences on social equity. The overall findings show that different personas hold distinct preferences across all social groups, and that mainstream LLMs tend to align most closely with the 'Disengaged Battlers' persona (Persona 3), which is characterized by a focus on day-to-day survival and feeling excluded from political discourse.


## Video-SafetyBench: A Benchmark for Safety Evaluation of Video LVLMs

[https://arxiv.org/pdf/2505.11842](https://arxiv.org/pdf/2505.11842)

**Date:** 2025-10-28

The benchmark, Video-SafetyBench, measures the propensity of Large Vision-Language Models (LVLMs) to generate harmful content related to religious intolerance. This is assessed as a subcategory within the broader 'Hate' category, evaluating if models produce responses that involve unfair treatment, prejudice, discrimination, hate speech, harassment, or desecration of religious symbols based on religious beliefs. In scenarios involving hate speech, including religious intolerance, the proprietary model Claude 3.7 Sonnet consistently achieved the lowest attack success rates (ASR). In contrast, open-source models demonstrated varied and higher vulnerabilities. The paper notes that most models struggle to suppress subtle or implicit expressions of hate, indicating persistent challenges in detecting and mitigating this type of harmful content.


## CARES: Comprehensive Evaluation of Safety and Adversarial Robustness in Medical LLMs

[https://arxiv.org/pdf/2505.11413](https://arxiv.org/pdf/2505.11413)

**Date:** 2025-05-16

Discrimination/bias based on religion in healthcare contexts. The benchmark's 'Discrimination and Healthcare Bias' safety principle explicitly includes religion as an attribute for which bias is measured. Additionally, role-playing scenarios include roles like 'a theologian discussing religious perspectives on medical ethics'. The paper includes religion as a category for evaluating discrimination and bias within its 'Discrimination and Healthcare Bias' principle. However, it does not report specific findings on how the tested models performed on prompts related to religion.


## Empirically evaluating commonsense intelligence in large language models with large-scale human judgments

[https://arxiv.org/pdf/2505.10309](https://arxiv.org/pdf/2505.10309)

**Date:** 2025-10-08

The benchmark measures model 'commonsensicality' on a wide range of topics by comparing model judgments to human population consensus. This includes statements involving religious facts (e.g., 'The Pope is the leader of the Catholic Church') and beliefs (e.g., 'No one religion is the right path'). The paper does not provide aggregated findings for religious statements as a specific category. However, it uses religious-themed statements as examples. For instance, 'The conflating of religion and god has been damning to humanity' and 'No one religion is the right path' were identified as statements where models' own agreement often diverges from their prediction of broader human agreement. This suggests models find these types of statements less straightforward in terms of predicting social consensus.


## DIF: A Framework for Benchmarking and Verifying Implicit Bias in LLMs #Mormon

[https://arxiv.org/pdf/2505.10013](https://arxiv.org/pdf/2505.10013)

**Date:** 2025-12-27

The benchmark measured implicit bias in Large Language Models' mathematical problem-solving capabilities when prompted with different sociodemographic personas, including religious identities. This was quantified by the difference in correctly answered questions when the model was assigned a specific religious identity versus a baseline 'American' identity. The paper found that assigning a religious identity to an LLM can influence its mathematical reasoning accuracy. A key general finding was an inverse correlation between model intelligence (problem-solving accuracy) and implicit bias; more capable models tended to show less performance variation across different personas, including religious ones. The bias induced by religious personas was found to be statistically significant compared to a null model with random strings, indicating the semantic content of the religious identity prompt affects performance.


## WorldView-Bench: A Benchmark for Evaluating Global Cultural Perspectives in Large Language Models

[https://arxiv.org/pdf/2505.09595](https://arxiv.org/pdf/2505.09595)

**Date:** 2025-05-14

The benchmark, WorldView-Bench, measures the cultural inclusivity of Large Language Models, with one of the seven categories specifically focused on Religion. It evaluates the model's ability to provide diverse and balanced perspectives on religious topics, such as the role of religious institutions in government, the relationship between science and religion, and the adaptation of religious teachings to modern societal values, through open-ended, free-form responses. Baseline LLMs exhibit a strong Western-centric bias, heavily favoring secular and Western philosophical viewpoints even on religious questions. Models developed in non-Western contexts, like Fanar from Qatar, still showed a predominant Western perspective with only a marginal increase in Islamic cultural references. However, implementing intervention strategies, particularly a Multi-Agent System (MAS) where different agents represent distinct cultural worldviews (including an 'Islamic Agent'), dramatically improved cultural balance. The MAS approach increased the cultural diversity score (PDS Entropy) from a baseline of 13% to 94%, achieving a nearly equal representation of all measured perspectives, including religious ones.


## Large language model psychometrics: A systematic review of evaluation, validation, and enhancement

[https://arxiv.org/pdf/2505.08245](https://arxiv.org/pdf/2505.08245)

**Date:** 2025-07-13

Measurement of spiritual values and their effect on social fairness; evaluation of moral justification (e.g., religious or spiritual). The paper notes that different spiritual values have been found to affect the performance of Large Language Models in social-fairness scenarios.


## Developing A Framework to Support Human Evaluation of Bias in Generated Free Response Text

[https://arxiv.org/pdf/2505.03053](https://arxiv.org/pdf/2505.03053)

**Date:** 2025-05-05

The framework measured stereotype detection and provocation in religious contexts. Specifically, it evaluated templates designed to provoke stereotypes such as 'Hindu people worship idols' and biases related to criminal responsibility in scenarios involving Muslim and Jewish individuals. Human evaluation of free-text responses revealed that some of the underlying religion-based templates from the BBQ benchmark were problematic. For example, a template intended to test stereotypes about Hindus engaging in idol worship was flawed because the comparison group (Catholics) is also subject to a similar stereotype, invalidating the test. Another template involving Muslim and Jewish individuals was found to be problematic because the LLM's nuanced response about the presumption of innocence was deemed more appropriate by human evaluators than what the benchmark expected, leading to the template's removal.


## WorldGenBench: A World-Knowledge-Integrated Benchmark for Reasoning-Driven Text-to-Image Generation

[https://arxiv.org/pdf/2505.01490](https://arxiv.org/pdf/2505.01490)

**Date:** 2025-05-02

The benchmark, WorldGenBench, measures a model's ability to generate semantically accurate images based on prompts requiring world knowledge of religious culture, history, and art. This includes correctly depicting religious sites (e.g., Bamiyan Buddhas, Echmiadzin Monastery), figures (e.g., monks), artifacts, and the historical context surrounding them (e.g., the destruction of the Buddhas by 2001). The paper's findings, using examples from religious history and culture, indicate that text-to-image models struggle to incorporate world knowledge and implicit reasoning. For instance, models often fail to depict the Bamiyan Buddhas as destroyed ruins in a post-March 2001 context, instead generating images of the intact statues based on a literal reading of the text. Even the best-performing models, like GPT-4o, only satisfy a small fraction (e.g., 30%) of the detailed requirements for generating a scene in a historically significant religious location like the Echmiadzin Monastery, demonstrating a significant gap in deep contextual understanding.


## LLM Ethics Benchmark: A Three-Dimensional Assessment System for Evaluating Moral Reasoning in Large Language Models

[https://arxiv.org/pdf/2505.00853](https://arxiv.org/pdf/2505.00853)

**Date:** 2025-05-01

Measurement of alignment with the 'Sanctity/Purity' moral foundation, which is part of the Moral Foundations Questionnaire and includes concepts of divinity, sacredness, and spiritual purity. All tested models showed lower alignment with 'binding' moral foundations (which include Loyalty, Authority, and Sanctity) compared to 'individualizing' foundations (Care and Fairness). This indicates a weaker grasp of moral intuitions related to concepts like divinity and sacredness, which are often tied to religious or traditional group cohesion.


## Mind the Language Gap: Automated and Augmented Evaluation of Bias in LLMs for High- and Low-Resource Languages

[https://arxiv.org/pdf/2504.18560](https://arxiv.org/pdf/2504.18560)

**Date:** 2025-04-19

The benchmark measured bias against religious groups by evaluating Large Language Models on prompt templates designed to detect discriminatory attitudes and stereotypes related to religion. The study found that bias detection related to religion was 'comparatively stable across both languages and models'. This stability is attributed to shared religious terminology and keywords that transfer well across languages. Gemini 1.5 Flash was noted to often excel in the religion category. The religion category had a moderate rate (5.44%) of unprocessable responses compared to other bias categories.


## Seeing The Words: Evaluating AI-generated Biblical Art

[https://arxiv.org/pdf/2504.16974](https://arxiv.org/pdf/2504.16974)

**Date:** 2025-04-23

The accuracy and contextual appropriateness of AI-generated images based on Christian biblical text prompts. The evaluation assessed aspects such as the number of people, gender, age, and sentiment in the generated images, comparing them against historical religious artwork. Midjourney generated illustration-like images that were most similar to the selected human artworks, showing sophisticated details and a reasonable understanding of the religious context. DALL-E 2 performed the worst, often failing to capture the biblical context and generating images with incomprehensible text. Stable Diffusion produced versatile results, with its similarity to human artwork depending on the prompt; it showed some understanding of religious context but with more stylistic diversity, including abstract and science-fiction themes. All models struggled with details like generating accurate hands and sometimes included anachronistic elements like Christian crosses in Old Testament scenes.


## THE PARADOX OF POETIC INTENT IN BACK-TRANSLATION: EVALUATING THE QUALITY OF LARGE LANGUAGE MODELS IN CHINESE TRANSLATION

[https://arxiv.org/pdf/2504.16286](https://arxiv.org/pdf/2504.16286)

**Date:** 2025-04-28

Preservation of cultural and religious nuance (e.g., Buddhist mantras, Taoist cosmology and geomancy) in Chinese-English back-translation. Large Language Models struggle to translate texts rich in religious and cultural allusions, such as Buddhist mantras, Buddhist cosmology, and Taoist geomantic texts. They tend to produce overly literal translations that strip away the profound meaning, nuance, and historical context, a phenomenon the paper terms the 'Paradox of Poetic Intent'. For instance, a Taoist geomantic text was reduced to a simple navigation manual, failing to capture its metaphysical significance.


## RainbowPlus: Enhancing Adversarial Prompt Generation via Evolutionary Quality-Diversity Search

[https://arxiv.org/pdf/2504.15047](https://arxiv.org/pdf/2504.15047)

**Date:** 2026-01-20

Discriminatory rhetoric targeting religious groups as a sub-component of a broader 'Violence and Hate' risk category. The paper does not provide specific findings related to religion. It finds that its method, RAINBOWPLUS, is effective at generating prompts that elicit harmful responses across broad categories. One of these categories, 'Violence and Hate', includes discriminatory content based on religion, but the results are not disaggregated to analyze religion-specific performance.


## FarsEval-PKBETS: A new diverse benchmark for evaluating Persian large language models

[https://arxiv.org/pdf/2504.14690](https://arxiv.org/pdf/2504.14690)

**Date:** 

The benchmark measured the model's accuracy in answering questions related to Islam, specifically the Shia branch. It also aimed to examine potential bias the model may have towards other sects and religions by covering topics in practical jurisprudence and theoretical beliefs. For the religion category, Llama3-70B achieved an accuracy of 0.54 (0.57 including semi-correct answers), PersianMind scored 0.29 (0.32), and Dorna scored 0.39 (0.43). This indicates that the models, particularly those fine-tuned for Persian, struggle with questions related to Islam within the Iranian cultural context.


## D-GEN: Automatic Distractor Generation and Evaluation for Reliable Assessment of Generative Models

[https://arxiv.org/pdf/2504.13439](https://arxiv.org/pdf/2504.13439)

**Date:** 2025-06-12

The benchmark (MMLU) used in the paper includes a sub-task designed to measure knowledge of world religions. The paper does not provide specific findings for the 'World Religions' sub-category. The results are aggregated at the 'Humanities' domain level, where the D-GEN method was shown to preserve model performance rankings and induce similar model confidence levels compared to the original MMLU benchmark, thus validating the paper's distractor generation and evaluation methodology.


## ELAB: Extensive LLM Alignment Benchmark in Persian Language

[https://arxiv.org/pdf/2504.12553](https://arxiv.org/pdf/2504.12553)

**Date:** 2025-04-17

Equitable treatment regardless of religion, as a component of the broader fairness evaluation. The paper does not report any specific findings related to religion, as it was only a minor component of the overall fairness evaluation.


## Bias Beyond English: Evaluating Social Bias and Debiasing Methods in a Low-Resource Setting

[https://arxiv.org/pdf/2504.11183](https://arxiv.org/pdf/2504.11183)

**Date:** 2025-07-14

Stereotypical bias detection related to religious groups by comparing the likelihood of stereotypical vs. non-stereotypical sentences. Models evaluated on Thai and Indonesian data consistently exhibit significantly higher religious bias scores compared to other languages. The authors suggest this may stem from the strong cultural emphasis on Buddhism in Thailand and Islam in Indonesia, which could lead to more pronounced religious biases in datasets from these regions.


## CLASH: EVALUATING LANGUAGE MODELS ON JUDGING HIGH-STAKES DILEMMAS FROM MULTIPLE PERSPECTIVES

[https://arxiv.org/pdf/2504.10823](https://arxiv.org/pdf/2504.10823)

**Date:** 2025-09-26

The benchmark measures a model's ability to make value-based judgments in high-stakes dilemmas that can include religious contexts. For example, it evaluates how models handle a scenario involving the construction of a Sikh temple, forcing a judgment between community safety/tranquility and avoiding prejudice against a religious group. In a dilemma involving a Sikh community's temple construction, several models demonstrated 'value confusion.' They struggled to correctly prioritize between competing values—community safety versus avoiding prejudice and promoting development. Smaller models, in particular, tended to ambiguously integrate conflicting values, leading to indecisive or incorrect final answers, highlighting a general failure in situational adaptability in contexts that can involve religious considerations.


## Quantifying the Spread of Online Incivility in Brazilian Politics

[https://arxiv.org/pdf/2504.08960](https://arxiv.org/pdf/2504.08960)

**Date:** 2025-05-16

Detection of hate speech and stereotyping targeting individuals or groups based on religious beliefs, as one of four dimensions of online incivility. Self-identified religious individuals supporting the right-wing candidate (Bolsonaro) were a notable group among disseminators of uncivil content, particularly in the categories of Hate Speech and Stereotyping (HSST) and Threats to Democratic Institutions and Values (THREAT).


## BiasCause: Evaluate Socially Biased Causal Reasoning of Large Language Models

[https://arxiv.org/pdf/2504.07997](https://arxiv.org/pdf/2504.07997)

**Date:** 2025-04-08

The benchmark measures socially biased causal reasoning in LLMs when answering questions related to religion. This includes questions designed to elicit stereotypes (e.g., 'Who are more likely to be terrorists?') and questions about historical events involving religious groups (e.g., 'Who were participants of the Thirty Years' War?'). All four tested models demonstrated significant social bias when answering biased questions related to religion. According to Figure 5, the models achieved low accuracy (below 20%) on these questions, indicating they frequently provided biased responses rather than neutral or refusal-to-answer responses. The performance on religion-related questions was comparable to other sensitive attributes showing high bias, such as age and disability status.


## Metamorphic Testing for Fairness Evaluation in Large Language Models: Identifying Intersectional Bias in LLaMA and GPT

[https://arxiv.org/pdf/2504.07982](https://arxiv.org/pdf/2504.07982)

**Date:** 2025-04-04

The benchmark measured intersectional fairness biases by evaluating changes in sentiment and tone in LLM responses when religious identity was included as a sensitive attribute, often in combination with other demographic factors like occupation, ethnicity, and economic status. Combinations of sensitive attributes that included religion were highly likely to reveal fairness biases in the LLaMA 3 model. Specifically, intersections such as 'Religion, Political views, Marital Status' and 'Religion, Social Status, and Economic Condition' frequently highlighted fairness issues, likely due to complex social sensitivities associated with these combined factors.


## Benchmarking Adversarial Robustness to Bias Elicitation in Large Language Models: Scalable Automated Assessment with LLM-as-a-Judge

[https://arxiv.org/pdf/2504.07887](https://arxiv.org/pdf/2504.07887)

**Date:** 2025-10-16

The benchmark measured biases in the representation of religious groups by examining stereotypes associated with specific faiths. Across all models tested, the 'Religion' bias category exhibited the highest average safety score in the initial assessment and was one of the most resilient categories against adversarial jailbreak attacks, suggesting that model alignment strategies may prioritize minimizing bias in religious contexts.


## FairEval: Evaluating Fairness in LLM-Based Recommendations with Personality Awareness

[https://arxiv.org/pdf/2504.07801](https://arxiv.org/pdf/2504.07801)

**Date:** 2025-06-03

The benchmark measured fairness disparities in movie and music recommendations. Specifically, it assessed how recommendations change (using similarity and disparity metrics like SNSR and SNSV) when a user's religion is mentioned in a prompt, indicating systematic bias or preferential treatment. Both ChatGPT 4o and Gemini 1.5 Flash showed significant fairness disparities when religion was mentioned in user prompts. The 'Religion' attribute consistently resulted in high Sensitive-to-Neutral Similarity Range (SNSR) and Similarity Variance (SNSV) scores, indicating pronounced and inconsistent treatment across different religious groups. For Gemini 1.5 Flash, religion was the attribute causing the highest fairness disparity in music recommendations (SNSR of 0.3479).


## NorEval: A Norwegian Language Understanding and Generation Evaluation Benchmark

[https://arxiv.org/pdf/2504.07749](https://arxiv.org/pdf/2504.07749)

**Date:** 2025-06-05

The benchmark measures whether language models generate or select answers that propagate false beliefs, misconceptions, stereotypes, and conspiracies related to religion, as part of the NorTruthfulQA dataset. The paper does not provide findings specific to the religion category. The general finding for the NorTruthfulQA task, which includes religion, is that language models struggle with truthfulness. They tend to generate less truthful answers in the open-ended generation setup compared to the multiple-choice setup, highlighting challenges in evaluating open-ended QA in Norwegian.


## SPLITS! A Flexible Dataset and Evaluation Framework for Sociocultural Linguistic Investigation

[https://arxiv.org/pdf/2504.04640](https://arxiv.org/pdf/2504.04640)

**Date:** 2025-07-31

Validation of distinctive linguistic patterns, termed Sociocultural Linguistic Phenomena (SLP), used by different religious groups across various discussion topics. This includes confirming known phenomena (e.g., code-switching) and discovering novel, non-trivial linguistic differences between groups. The framework successfully validated known religious linguistic phenomena, such as Jewish people code-switching to Yiddish/Hebrew more in religious contexts. It also captured more subtle phenomena, like the Hindu/Sikh/Jain group discussing 'dance' more frequently in the context of cultural identity. The system was able to surface potentially novel, non-trivial findings for further research, such as Hindus/Jains/Sikhs emphasizing 'rural economics' during discussions on 'elections' more than Jewish people, while effectively filtering out obvious findings like 'Catholics talk about church'.


## YourBench: Easy Custom Evaluation Sets for Everyone

[https://arxiv.org/pdf/2504.01833](https://arxiv.org/pdf/2504.01833)

**Date:** 2025-04-02

Knowledge of facts about world religions, including figures, concepts, and holidays, as part of a replication of the MMLU 'World Religions' subset. The YourBench framework successfully replicated the MMLU 'World Religions' subset. The automatically generated questions were more challenging (resulted in lower absolute accuracy scores) for all tested models but perfectly preserved the relative performance ranking of the models compared to the original MMLU subset (Spearman correlation of 1.0).


## Can LLMs Grasp Implicit Cultural Values? Benchmarking LLMs’ Cultural Intelligence with CQ-Bench

[https://arxiv.org/pdf/2504.01127](https://arxiv.org/pdf/2504.01127)

**Date:** 2025-10-09

The benchmark, CQ-Bench, measures an LLM's ability to infer implicit cultural values and attitudes related to religion from natural, multi-character conversational text. This includes detecting a character's stance on a religious statement (Attitude Detection), selecting the correct religious value from a list (Value Selection), and extracting religious values without predefined options (Value Extraction). Models, including state-of-the-art ones, demonstrate a significant performance gap in understanding religious values compared to other cultural categories like political, social, and ethical values. Across tasks like attitude detection and value selection, models consistently scored lower in the religious domain (e.g., below 0.6 F1 score) than in others (e.g., above 0.7 F1 score for political values), indicating substantial room for improvement in comprehending nuanced religious beliefs.


## Zero-shot Benchmarking: A Framework for Flexible and Scalable Automatic Evaluation of Language Models

[https://arxiv.org/pdf/2504.01001](https://arxiv.org/pdf/2504.01001)

**Date:** 2025-10-29

The benchmark measured the general capability of language models to respond to open-ended prompts on a wide variety of topics. One of these topics was 'Religious & cultural studies,' which included subtopics such as 'Religious traditions,' 'Sacred texts,' 'Interfaith dialogue,' and 'Religious education.' The measurement assessed the quality of the generated text on these subjects. The paper does not present any specific findings related to religion. The 'Religious & cultural studies' topic was one of many categories used for data generation, and the results were aggregated across all topics to provide an overall performance ranking for each model. There is no breakdown or analysis of how models performed specifically on religious prompts.


## BEATS: Bias Evaluation and Assessment Test Suite for Large Language Models

[https://arxiv.org/pdf/2503.24310](https://arxiv.org/pdf/2503.24310)

**Date:** 2025-03-31

The benchmark measured the presence and frequency of religion bias in Large Language Model responses as one of twelve evaluated bias categories. Religion bias was found to have a low frequency of occurrence (2.6%) in model responses, compared to other more prevalent biases such as stereotype bias (31.1%) and cultural bias (17.3%).


## How Well Can Vision-Language Models Understand Humans’ Intention? An Open-ended Theory of Mind Question Evaluation Benchmark

[https://arxiv.org/pdf/2503.22093](https://arxiv.org/pdf/2503.22093)

**Date:** 2025-04-24

The benchmark measured the ability of Vision-Language Models to correctly identify religious visual cues (e.g., specific attire) and infer the associated intentions (e.g., praying) from images. All four tested models struggled to correctly identify religious attire, specifically misidentifying a cassock and stole as graduation robes, which led to incorrect inferences. However, GPT-based models were able to identify the intention of 'praying'.


## OpenHuEval: Evaluating Large Language Model on Hungarian Specifics

[https://arxiv.org/pdf/2503.21500](https://arxiv.org/pdf/2503.21500)

**Date:** 2025-08-25

Measures knowledge of Hungarian religion, rituals, and holidays as a component of the 'Life, Culture, and Customs' (LCC) dimension, which is one of eight Hungarian-specific dimensions evaluated by the OpenHuEval benchmark. The paper's findings focus on the overall performance of LLMs on Hungarian-specific knowledge tasks. While religion is a sub-component of the cultural evaluation, no specific findings related to religious knowledge or bias were detailed. The main findings highlight that models like Deepseek-R1 and GPT-40 perform best on Hungarian-specific tasks and that there are significant performance differences compared to general English benchmarks, underscoring the need for language-specific evaluations.


## An evaluation of LLMs and Google Translate for translation of selected Indian languages via sentiment and semantic analyses

[https://arxiv.org/pdf/2503.21393](https://arxiv.org/pdf/2503.21393)

**Date:** 2025-07-01

The benchmark measured the preservation of sentiment, semantic integrity, and cultural/philosophical context in machine translations of sacred Hindu texts (specifically the Bhagavad Gita) and other prominent Indian literature from Sanskrit, Hindi, and Telugu into English. GPT-based models performed best in maintaining sentiment polarity in translated religious/philosophical texts compared to human expert translations. LLMs generally produce better translations than Google Translate in terms of semantic richness. However, all models face challenges in preserving semantic integrity for figurative, metaphorical, and deep philosophical concepts found in texts like the Bhagavad Gita. GPT-4o was found to be the most consistent and reliable model for translating Sanskrit texts. The study also highlighted the ethical importance of accurately translating sacred texts, as mistranslations can alter religious interpretations, such as the meaning of a "tamasik" diet in Hinduism.


## MAD Chairs: A new tool to evaluate AI

[https://arxiv.org/pdf/2503.20986](https://arxiv.org/pdf/2503.20986)

**Date:** 2025-09-05

The paper discusses how its benchmark could identify suboptimal 'gaslighting' strategies, theorizing that such behavior could be motivated by non-rational dogma based on religion, race, or sex. The paper makes a theoretical point that dogma, which could be religious in nature, is a potential non-rational driver for the suboptimal 'gaslighting' strategy. It does not present empirical findings on this, but frames such dogma-driven behavior as irrational and detrimental to game performance.


## Mobile-MMLU: A Mobile Intelligence Language Understanding Benchmark

[https://arxiv.org/pdf/2503.20786](https://arxiv.org/pdf/2503.20786)

**Date:** 2025-03-26

Knowledge of religious studies, as part of a broader mobile-centric language understanding benchmark. The benchmark includes 'Religious Studies' as one of its 80 topics. This topic was rated as having 'Low-Medium Relevance' for mobile use cases with a score of 4.38 out of 10. It was also identified as one of the 20 most challenging topics for the models tested, with an average accuracy of 0.574 across models.


## FLEX: A Benchmark for Evaluating Robustness of Fairness in Large Language Models

[https://arxiv.org/pdf/2503.19540](https://arxiv.org/pdf/2503.19540)

**Date:** 2025-03-25

Robustness of fairness and resistance to social biases (stereotypes) in extreme, adversarial scenarios using multiple-choice Question Answering tasks. Specifically, it measures whether models can maintain neutrality (choosing 'Unknown' or 'Not enough information') versus selecting a stereotypical option when exposed to bias-inducing prompts such as Persona Injection, Competing Objectives, and Text Attacks. The study found that biases related to religion, nationality, and age were generally lower across most models compared to other categories like gender and sexual orientation. The authors suggest this may be attributed to substantial safety training in these specific categories. However, the benchmark demonstrated that even models appearing unbiased on standard benchmarks could be manipulated into showing bias under extreme adversarial scenarios.


## The Case for ‘Thick Evaluations’ of Cultural Representation in AI

[https://arxiv.org/pdf/2503.19075](https://arxiv.org/pdf/2503.19075)

**Date:** 2025-03-24

Qualitative evaluation of cultural representativeness in AI-generated images, including the depiction of religious groups, practices (holidays), places of worship, attire, and social norms. Findings indicate that evaluating religious representation requires deep, situated cultural knowledge that outsiders lack. For example, participants noted incoherence in depictions of religious sites (e.g., boating in a gurudwara) and practices (e.g., celebrating holidays like Nauroz or Ganesh chaturthi differently across regions). The paper also found that goals for representation are context-dependent; a participant from a Muslim-majority region desired to see Muslims without hijabs and non-Muslims represented, challenging generic diversity metrics.


## Video SimpleQA: Towards Factuality Evaluation in Large Video Language Models

[https://arxiv.org/pdf/2503.18923](https://arxiv.org/pdf/2503.18923)

**Date:** 2025-08-13

The benchmark measures the ability of Large Video Language Models to answer multi-hop, fact-seeking questions that require external knowledge. Within this framework, it specifically measures factual knowledge about topics under the categories of 'Belief' and 'Religion' as part of the broader 'Society & Culture' domain. The paper includes 'Beliefs & Institutions' (which contains 'Religion') as a secondary category for evaluation. The findings do not focus specifically on religion but provide a performance breakdown across categories. In the 'Beliefs & Institutions' category, models like o3 and Gemini 2.5 Pro demonstrated relatively strong performance (F-scores around 70), while other models showed varied and often lower performance, consistent with the paper's overall finding of significant performance gaps in factual adherence across all topics.


## TIB-STC: A Large-Scale Structured Tibetan Dataset for Low-Resource Language Modeling

[https://arxiv.org/pdf/2503.18288](https://arxiv.org/pdf/2503.18288)

**Date:** 2025-08-04

General language capabilities on a corpus where Tibetan Buddhism is a significant domain. The TIB-STC dataset, used for training and validation, includes a large amount of religious texts (specifically, Tibetan Buddhist scriptures and philosophy) to enable models to understand and generate culturally and religiously specific content. When prompted to write a poem in praise of a father, different models exhibited distinct stylistic choices reflecting their training. The model trained on the religiously and culturally rich TIB-STC dataset (Sun-Shine) produced a neutral response. In contrast, GPT-4o adopted a 'majestic style, reminiscent of divine scripture,' and DeepSeek-R1's response frequently alluded to the bodhisattva Mañjuśrī, suggesting it was 'slightly "overfitted"' on such religious themes.


## REVAL: A Comprehension Evaluation on Reliability and Values of Large Vision-Language Models

[https://arxiv.org/pdf/2503.16566](https://arxiv.org/pdf/2503.16566)

**Date:** 2025-03-20

The benchmark measured social bias related to religion using both open-ended and closed-ended question formats. Current large models still exhibit biases related to religion, with varying sensitivities. For example, GPT-40, which excels in most other bias categories, performs significantly worse than MiniCPM-Llama3-v2.5 in the religion category.


## Safety Evaluation and Enhancement of DeepSeek Models in Chinese Contexts

[https://arxiv.org/pdf/2503.16529](https://arxiv.org/pdf/2503.16529)

**Date:** 2025-05-16

The benchmark measured risk content identification and refusal to answer for various safety categories, including religious discrimination. The paper's safety evaluation included 'religious discrimination' as a risk category. The findings show that model safety capabilities in this category, along with others, generally declined after the distillation process. However, targeted safety enhancements significantly improved the models' performance in identifying and handling prompts related to religious discrimination, with some models showing notable accuracy improvements in this specific category after enhancement.


## Fùxì: A Benchmark for Evaluating Language Models on Ancient Chinese Text Understanding and Generation

[https://arxiv.org/pdf/2503.15837](https://arxiv.org/pdf/2503.15837)

**Date:** 2025-03-20

Knowledge and classification of ancient Chinese texts related to Confucianism, Taoism, and Buddhism. The paper does not provide specific findings for the religious/philosophical categories within the benchmark. General findings indicate that models perform better on comprehension tasks (e.g., multiple-choice) than on generation tasks across the ancient Chinese text corpus, which includes texts from Confucian, Taoist, and Buddhist traditions. Larger models also generally outperform smaller ones, especially on knowledge-intensive tasks.


## TOWARDS UNDERSTANDING THE SAFETY BOUNDARIES OF DEEPSEEK MODELS: EVALUATION AND FINDINGS

[https://arxiv.org/pdf/2503.15092](https://arxiv.org/pdf/2503.15092)

**Date:** 2025-03-19

The benchmark measured the generation of discriminatory content based on faith or religion, labeled as 'Faith discrimination (FD)' within the broader category of 'Discriminatory Content'. The models were evaluated for 'Faith discrimination'. The attack success rates (ASRs) varied significantly by model and language. The DeepSeek-R1 model in English showed a particularly high ASR of over 50% for faith discrimination, which was substantially higher than its ASR in Chinese (around 25%) and also higher than the DeepSeek-V3 model in either language. This indicates a notable vulnerability to generating faith-based discriminatory content, especially for the DeepSeek-R1 model when prompted in English.


## TLUE: A Tibetan Language Understanding Evaluation Benchmark

[https://arxiv.org/pdf/2503.12051](https://arxiv.org/pdf/2503.12051)

**Date:** 2025-10-02

The benchmark measures knowledge of 'World Religions' as part of its general understanding component (Ti-MMLU). It also evaluates model behavior on safety-critical topics including ethics, bias, and morality (Ti-SafetyBench), which can encompass religious contexts. The paper does not provide specific findings for the 'World Religions' sub-task. The general finding is that most LLMs perform poorly on the Tibetan benchmark, often below the random baseline, across all domains including 'Humanities' which contains the 'World Religions' category. This indicates significant challenges for models in understanding Tibetan-language content related to religion and other topics.


## No LLM is Free From Bias: A Comprehensive Study of Bias Evaluation in Large Language Models #Mormon

[https://arxiv.org/pdf/2503.11985](https://arxiv.org/pdf/2503.11985)

**Date:** 2025-05-27

The benchmark measured stereotypical associations, the association of religious groups with positive and negative undertoned questions, and the association of toxic content with religious groups. LLMs exhibited varied biases across religions. Models tended to associate Christian, Sikh, Buddhist, and Jewish religions with positive questions, while linking Orthodox and Atheist beliefs with negative questions. In terms of association with toxic content, Christianity was most frequently associated, followed by Islam and Hinduism. Overall, the LL-8B model was found to be the least biased for religion in stereotype-based tasks (CrowS-Pairs), but when associating toxic content, all models showed significant bias.


## LAG-MMLU: Benchmarking Frontier LLM Understanding in Latvian and Giriama

[https://arxiv.org/pdf/2503.11911](https://arxiv.org/pdf/2503.11911)

**Date:** 2025-03-18

The benchmark measured knowledge of 'world religions' as one of 57 subjects in a broad multitask language understanding evaluation. It was not a primary focus but a component of the overall knowledge assessment. The paper does not report any specific findings related to religion. The performance analysis is aggregated across all 55 subjects, and there is no breakdown of model performance for the 'world_religions' category.


## CuLEmo: Cultural Lenses on Emotion - Benchmarking LLMs for Cross-Cultural Emotion Understanding

[https://arxiv.org/pdf/2503.10688](https://arxiv.org/pdf/2503.10688)

**Date:** 2025-05-28

The benchmark measures the ability of LLMs to predict culturally-appropriate emotional responses to scenarios involving religious practices, norms, and figures, such as insulting a religion, addressing a religious leader by name, or seeing a religious figure violate a norm. The paper's findings are not isolated for religion, but aggregated across cultural categories. However, examples show that models like GPT-4 can predict varying emotional reactions to religious scenarios (e.g., insulting a religion) across different cultures, but performance varies and errors occur, especially for less-represented cultures (e.g., Ethiopia). The overall results indicate that LLMs' understanding of emotional responses in religious contexts is culturally dependent and imperfect.


## MINORBENCH: A HAND-BUILT BENCHMARK FOR CONTENT-BASED RISKS FOR CHILDREN

[https://arxiv.org/pdf/2503.10242](https://arxiv.org/pdf/2503.10242)

**Date:** 2025-03-13

The benchmark measures the refusal rate of Large Language Models (LLMs) to prompts containing hateful content. The 'Hateful' category is defined as 'Content that promotes discrimination, harassment, or violence against individuals or groups based on protected attributes (e.g., race, religion, gender)'. Therefore, the measurement related to religion is the model's ability to refuse to generate content that is hateful towards religious groups. The paper found that LLM performance in refusing to answer hateful prompts, which includes those based on religion, is highly dependent on the system prompt provided. With a basic system prompt, most models had very low refusal rates for hateful content (as low as 0-14%). However, with stricter, child-specific safety instructions in the system prompt, refusal rates increased dramatically for most models, some reaching 100%. Performance was inconsistent across models, with 'reasoning models' like o3-mini and R1 Distilled consistently showing lower refusal rates even with stricter prompts.


## Cross-Examiner: Evaluating Consistency of Large Language Model-Generated Explanations

[https://arxiv.org/pdf/2503.08815](https://arxiv.org/pdf/2503.08815)

**Date:** 2025-03-11

Consistency checking of model explanations to detect potential biases or stereotypes related to religious identity. The paper used examples involving Jewish and Sikh individuals to test if a model's reasoning was consistent across its explanations. The paper does not present findings about specific religious biases in models. Instead, it uses scenarios involving religious identities (e.g., a Jewish person and a Sikh person) as examples to demonstrate the effectiveness of its 'Cross-Examiner' method for generating follow-up questions. The core findings are methodological, showing that a neuro-symbolic approach for generating these questions is more effective at producing high-quality, targeted probes for inconsistencies than purely LLM-based approaches.


## Randomness, Not Representation: The Unreliability of Evaluating Cultural Alignment in LLMs

[https://arxiv.org/pdf/2503.08688](https://arxiv.org/pdf/2503.08688)

**Date:** 2025-04-08

The paper uses the question 'How important is religion in your life?' from the Global Opinion Q&A (GQA) dataset to measure the stability of LLMs' expressed cultural values. The goal was not to measure religious belief itself, but to test how sensitive the model's response about the importance of religion is to superficial changes in survey question formatting (e.g., order of options, response type). The paper's key finding related to religion is that LLM responses to the question 'How important is religion in your life?' are highly unstable and sensitive to non-semantic changes in the survey format. Minor variations, such as changing the order of response options (ascending vs. descending) or the required response format (numerical identifier vs. full text), led to significant shifts in the models' expressed preferences. This suggests that evaluations of an LLM's stance on religion may reflect artifacts of the evaluation design rather than a stable, inherent property of the model.


## VISBIAS: Measuring Explicit and Implicit Social Biases in Vision Language Models

[https://arxiv.org/pdf/2503.07575](https://arxiv.org/pdf/2503.07575)

**Date:** 2025-09-06

The benchmark measured stereotypical associations between visual representations of people and religious affiliations. This was done through two main tasks: 1) Explicit multiple-choice questions asking the model to assign a religion (Islam, Christianity, Hinduism, or Buddhism) to a person in an image. 2) Implicit form completion tasks where the model fills in a 'Religion' field alongside 19 other attributes, revealing correlations between religion and other demographic data like ethnicity or occupation. Models exhibited religious stereotypes. In explicit tasks, GPT-4V tended to default to 'Christian' regardless of ethnicity, whereas LLaVA assigned religions based on ethnicity. In implicit tasks, models showed strong, stereotypical associations between specific ethnic groups and religions (e.g., Asian individuals with Buddhism) and between occupations and religions (e.g., Athlete with Christianity), reinforcing cultural biases.


## WISE: World Knowledge-Informed Semantic Evaluation for Text-to-Image Generation

[https://arxiv.org/pdf/2503.07265](https://arxiv.org/pdf/2503.07265)

**Date:** 2025-11-19

The benchmark measured the model's ability to generate images based on factual knowledge of religious objects, symbols, and architecture. Specifically, the 'Religion-related' category within the 'Cultural Common Sense' domain 'examines the identification of objects, symbols, or architectural structures that hold religious significance and are associated with specific faiths or religious heritage.' The paper does not provide specific findings for the religion sub-category. The results are aggregated at the broader 'Cultural' domain level. The general finding is that the majority of models fail to achieve a satisfactory score, indicating 'significant deficiencies in the ability of current models to leverage complex semantic understanding (implicit understanding) and world knowledge (intrinsic knowledge matching) for image generation.' This applies to all knowledge domains tested, including religion.


## Social Bias Benchmark for Generation: A Comparison of Generation and QA-Based Evaluations

[https://arxiv.org/pdf/2503.06987](https://arxiv.org/pdf/2503.06987)

**Date:** 2025-06-12

The benchmark measures the degree to which language models generate story continuations that align with social stereotypes in religious contexts, as one of several categories of social bias. In the English benchmark (EnBBG), religion was found to be one of the categories with the highest average bias scores across the tested models, following the 'Age' category. For instance, Claude-3.5-sonnet, despite having a low overall bias score, exhibited higher bias in the Religion category compared to other models.


## SAFEARENA: Evaluating the Safety of Autonomous Web Agents

[https://arxiv.org/pdf/2503.04957](https://arxiv.org/pdf/2503.04957)

**Date:** 2025-03-06

The benchmark, SAFEARENA, measured social bias, which included at least one task designed to evaluate bias against individuals with Muslim-sounding names by instructing the agent to create a script to auto-reject them as applicants. The paper did not report findings specific to religion. However, it included tasks measuring bias against Muslims within its 'Bias' harm category and found that models completed these harmful tasks at notable rates. For example, the overall completion rate for harmful 'Bias' tasks was 14% for GPT-4o and 22% for Qwen-2-VL-72B.


## DongbaMIE: A Multimodal Information Extraction Dataset for Evaluating Semantic Understanding of Dongba Pictograms

[https://arxiv.org/pdf/2503.03644](https://arxiv.org/pdf/2503.03644)

**Date:** 2025-05-22

Semantic understanding and information extraction (objects, actions, relations, attributes) from the pictographic script of the Dongba religion. Current Multimodal Large Language Models (MLLMs) struggle significantly to extract semantic information from Dongba pictographs, a script deeply rooted in Dongba religion. Even advanced models like GPT-4o achieved very low F1 scores (e.g., 1.60 for object extraction) in zero-shot settings. The models failed to extract complex semantics, such as relations and attributes, and made specific errors like misinterpreting symbolic features, such as reading potential human figures as a 'village god'.


## Implicit Bias in LLMs: A Survey

[https://arxiv.org/pdf/2503.02776v1](https://arxiv.org/pdf/2503.02776v1)

**Date:** 

Bias against applicants with Arab/Muslim names in hiring scenarios. When prompted to generate profiles and job advertisements, GPT-4 was more likely to recommend applicants with Arab/Muslim names for lower-status jobs, while favoring applicants with White names for higher-status positions.


## DOVE: A Large-Scale Multi-Dimensional Predictions Dataset Towards Meaningful LLM Evaluation

[https://arxiv.org/pdf/2503.01622](https://arxiv.org/pdf/2503.01622)

**Date:** 2025-06-03

Knowledge of world religions, as tested by the MMLU benchmark. Performance on the world religions knowledge task, like other tasks, varied substantially based on prompt phrasing, enumerator style, and other dimensions. For instance, the OLMoE-1B-7B model showed particularly high performance divergence on this task compared to its average performance. This indicates that model knowledge on religious topics is sensitive to how the question is asked.


## Unmasking Implicit Bias: Evaluating Persona-Prompted LLM Responses in Power-Disparate Social Scenarios

[https://arxiv.org/pdf/2503.01532](https://arxiv.org/pdf/2503.01532)

**Date:** 2025-04-22

The benchmark measured semantic shifts (using cosine distance) and response quality (using an LLM-judged Preference Win Rate) when Large Language Models were prompted to adopt personas with specific religious identities (e.g., Christian, Muslim, Buddhist, Jewish, Atheist) in various power-disparate social scenarios. The goal was to detect implicit biases by comparing these responses to a non-demographic baseline. The study found that LLMs have an implicit default persona that includes being Atheist, as this identity resulted in minimal semantic shifts from the baseline. Interactions involving Buddhist personas showed the highest semantic shifts. In terms of response quality, lower-quality responses were observed when Atheist responders engaged with subjects of other religions. Conversely, interactions with Buddhist responders, particularly with Muslim subjects, were associated with higher-quality responses. Overall, the Religion axis was identified as one of the most sensitive demographic dimensions, often inducing significant changes in LLM responses and being the most likely to improve response quality compared to other axes.


## Figurative Archive: an open dataset and web-based application for the study of metaphor

[https://arxiv.org/pdf/2503.00444](https://arxiv.org/pdf/2503.00444)

**Date:** 2025-01-01

The benchmark provides a dataset of metaphors, some of which are categorized into a 'Spirituality & Abstract Concepts' semantic class. It does not directly measure religious bias, knowledge, or stereotypes but allows for the analysis of metaphors within this spiritual/abstract domain. Using ChatGPT for topic modeling, the study identified 'Spirituality & Abstract Concepts' as one of ten semantic classes for topics and vehicles within its Literary Metaphors module. This class accounted for 12.97% of the metaphorical topics and 5.07% of the vehicles in that dataset.


## Palm: A Culturally Inclusive and Linguistically Diverse Dataset for Arabic LLMs

[https://arxiv.org/pdf/2503.00151](https://arxiv.org/pdf/2503.00151)

**Date:** 2025-07-24

The benchmark measured knowledge about the major monotheistic religions, focusing on historical sites, religious figures, and institutions, while specifically avoiding rituals. The paper's evaluations included a 'Religion' topic as part of its broader cultural assessment. The findings showed a general trend consistent with other topics: larger models like GPT-4o and Claude-3.5-Sonnet demonstrated higher performance and correctness in responding to religion-related prompts, while smaller models performed comparatively weaker. No specific findings unique to the religion category were highlighted beyond this general performance trend.


## ECLeKTic: a Novel Challenge Set for Evaluation of Cross-Lingual Knowledge Transfer

[https://arxiv.org/pdf/2502.21228](https://arxiv.org/pdf/2502.21228)

**Date:** 2025-11-08

The benchmark measured the cross-lingual transfer of factual knowledge across 10 domains, one of which was 'Religion, Philosophy, and Mythology'. It specifically tested a model's ability to answer questions about religious facts in a language where that information was likely not present during pre-training. The benchmark's construction method successfully captured culturally specific topics, with the 'Religion, Philosophy, and Mythology' domain being over-represented in questions originating from Hebrew and Hindi, reflecting the unique interests of those language speakers. The paper also highlights the challenge of transferring culturally specific religious concepts, using an example from Spanish related to Christian tradition ('the Seven Words') that may be difficult to understand when translated into languages from different cultural backgrounds.


## What’s Not Said Still Hurts: A Description-Based Evaluation Framework for Measuring Social Bias in LLMs

[https://arxiv.org/pdf/2502.19749](https://arxiv.org/pdf/2502.19749)

**Date:** 2025-09-16

The benchmark measures semantic-level associations between religious identities and bias-related concepts. This is achieved by presenting LLMs with naturalistic, subtly framed contexts where stereotypes are conveyed through descriptions of behaviors, emotions, or activities, rather than explicit terms, to detect biases against different religious groups. LLMs exhibit significant bias within the 'Religions' category, which consistently showed the second-highest level of bias after the 'Race' category across all tested models. For instance, GPT-4o demonstrated a strong bias association linking 'Buddhist' with 'can't write books' and 'Muslim' with 'are skilled writers'. The influence of how religious identity is described varies, but certain descriptor types were found to be particularly influential in triggering biased responses in most models.


## GRACE: A Granular Benchmark for Evaluating Model Calibration Against Human Calibration

[https://arxiv.org/pdf/2502.19684](https://arxiv.org/pdf/2502.19684)

**Date:** 2025-02-27

Knowledge of religious topics, including symbols (e.g., Buddhism), practices (e.g., Jewish birth ceremonies), and specific groups (e.g., sects of Judaism). Models were found to be least-calibrated on questions with multiple plausible answers or descriptive content, with examples drawn from religion, such as a question on fish as a Buddhist symbol and another on Jewish birth ceremonies. Religion is included as a category (5%) within the benchmark's social science section.


## JailBench: A Comprehensive Chinese Security Assessment Benchmark for Large Language Models

[https://arxiv.org/pdf/2502.18935](https://arxiv.org/pdf/2502.18935)

**Date:** 2025-02-26

The benchmark measured the propensity of Large Language Models to generate content that constitutes 'Religious discrimination'. This was one of 40 specific risk categories under the broader domain of 'Discrimination'. The paper includes 'Religious discrimination' as one of its 40 safety risk categories but does not provide specific results or analysis for it. The findings are aggregated into broader domains, such as 'Discrimination' (DC), which showed varying levels of vulnerability across different models. However, a specific breakdown of performance related to religious content is not available.


## Correlating and Predicting Human Evaluations of Language Models from Natural Language Processing Benchmarks

[https://arxiv.org/pdf/2502.18339](https://arxiv.org/pdf/2502.18339)

**Date:** 2025-02-24

Factual question answering and knowledge on the topics of 'Religion & spirituality' and 'World Religions'. Performance on the MMLU 'World Religions' benchmark exhibited a strong positive correlation (Pearson correlation of approximately 0.9) with the average scores from human evaluations across all topics. This suggests that performance on religious knowledge benchmarks is a good indicator of general model quality as perceived by humans. The paper does not provide a specific analysis of model performance or bias within the religion category itself.


## Evaluating the Effect of Retrieval Augmentation on Social Biases

[https://arxiv.org/pdf/2502.17611](https://arxiv.org/pdf/2502.17611)

**Date:** 2025-10-06

The benchmark measured social biases and stereotypes related to religion, specifically how Retrieval Augmented Generation (RAG) amplifies or mitigates these biases when provided with stereotypical or anti-stereotypical documents. Retrieval Augmented Generation (RAG) significantly amplifies religious biases when retrieving from stereotypical documents, even in models with low intrinsic bias. Conversely, retrieving from anti-stereotypical documents can reduce or reverse the bias. A specific finding for the Chinese CBBQ dataset revealed a counter-intuitive negative bias score in disambiguated contexts for religion; this was attributed to a distributional mismatch where the test questions predominantly featured Christians, while the stereotypical documents provided did not, highlighting RAG's sensitivity to the alignment between the query context and the knowledge corpus.


## Multilingual != Multicultural: Evaluating Gaps Between Multilingual Capabilities and Cultural Alignment in LLMs

[https://arxiv.org/pdf/2502.16534](https://arxiv.org/pdf/2502.16534)

**Date:** 2025-08-30

The benchmark measures cultural alignment by comparing LLM-generated response distributions against population-level opinion data from the World Values Survey. This includes measuring alignment on stances across several topics, one of which is religion. The paper does not provide specific findings for the religious domain. Its findings on cultural alignment are aggregated across all measured domains from the World Values Survey, which includes religion, work, family, politics, and security. The main findings are that increased multilingual capability does not guarantee better cultural alignment, and that US-centric bias is more prevalent in languages spoken across multiple countries (English, Portuguese) than in monocultural languages (Danish, Dutch).


## InsightVision: A Comprehensive, Multi-Level Chinese-based Benchmark for Evaluating Implicit Visual Semantics in Large Vision Language Models

[https://arxiv.org/pdf/2502.15812](https://arxiv.org/pdf/2502.15812)

**Date:** 2025-02-19

The benchmark measures the ability of large vision-language models to understand implicit visual semantics, with one of its 41 subcategories focusing on social phenomena which includes 'cults, extremist religious groups'. The paper does not provide specific findings related to religion. General findings indicate a considerable gap between current LVLMs and human performance, particularly in understanding implicit meanings. Performance was lower in categories involving deep cultural symbols or metaphors, which could include religious contexts, but no specific data for the religious subcategory was presented.


## Does Reasoning Introduce Bias? A Study of Social Bias Evaluation and Mitigation in LLM Reasoning #Mormon

[https://arxiv.org/pdf/2502.15361](https://arxiv.org/pdf/2502.15361)

**Date:** 2025-09-20

The benchmark measured social bias and stereotype detection in religious contexts, specifically how large language models' reasoning processes can introduce or amplify stereotypes related to religion, leading to biased predictions. Reasoning-based models, while often improving accuracy, do not mitigate and sometimes amplify religious biases. For instance, in an ambiguous scenario involving a Muslim person and a Mormon person near a crime scene, a model's reasoning invoked stereotypes about extremist groups in Muslim communities to incorrectly identify the Muslim person as the likely culprit. Analysis of the 'Religion' category from the BBQ dataset shows that when models produce incorrect answers, their reasoning steps exhibit systematically higher bias scores compared to when they produce correct answers.


## Time Travel: A Comprehensive Benchmark to Evaluate LMMs on Historical and Cultural Artifacts

[https://arxiv.org/pdf/2502.14865](https://arxiv.org/pdf/2502.14865)

**Date:** 2025-02-20

Knowledge of the religious context and significance of historical and cultural artifacts, including their role in ancient belief systems. Closed-source models like GPT-4o-0806 are more capable of generating contextually rich descriptions of historical artifacts, which includes understanding their role in ancient belief systems, compared to open-source models. However, all models still have room for improvement in understanding non-Western historical and cultural contexts, which are deeply intertwined with distinct religious traditions and belief systems.


## Benchmarking Multimodal RAG through a Chart-based Document Question-Answering Generation Framework

[https://arxiv.org/pdf/2502.14864](https://arxiv.org/pdf/2502.14864)

**Date:** 2025-02-20

The benchmark measures the ability of multimodal models to perform retrieval-augmented generation for chart-based question answering. One of the eight domains used for evaluation is 'Religion & Culture', which includes questions about religious affiliation, practices, and identity (e.g., atheism). The measurement is focused on factual correctness and coverage based on provided textual and chart-based documents, not specifically on bias or theological reasoning. The paper does not provide specific findings related to religion. Results are aggregated across all eight domains of the benchmark. The main finding is that even state-of-the-art models struggle with chart-based multimodal reasoning, achieving only 58.19% correctness and 73.87% coverage with ground-truth retrieval, and exhibit a bias towards textual information over visual (chart) information.


## SuperGPQA: Scaling LLM Evaluation across 285 Graduate Disciplines

[https://arxiv.org/pdf/2502.14739](https://arxiv.org/pdf/2502.14739)

**Date:** 2025-03-28

The benchmark measured graduate-level knowledge of Religious Studies as one of 285 disciplines. The benchmark includes 'Religious Studies' as a sub-discipline under Philosophy. In this category, the top-performing models were Doubao-1.5-pro-32k-250115 (80.00), DeepSeek-R1 (76.00), DeepSeek-R1-Zero (76.00), qwen-max-2025-01-25 (72.00), and phi-4 (72.00).


## VITAL: A New Dataset for Benchmarking Pluralistic Alignment in Healthcare

[https://arxiv.org/pdf/2502.13775](https://arxiv.org/pdf/2502.13775)

**Date:** 2025-05-31

The benchmark measures the ability of Large Language Models to generate responses that reflect a plurality of viewpoints, including diverse religious beliefs, on contentious healthcare topics. This includes evaluating whether the models can represent religious perspectives in open-ended answers (Overton mode) and align with specific values. The paper finds that existing pluralistic alignment techniques are insufficient for handling the diversity of beliefs in healthcare. Specifically regarding religion, the study notes that more complex methods like ModPlural can fail to cover key perspectives, citing an example where the model's response about organ donation omitted religious beliefs, whereas a simpler prompting method included them. This suggests that current sophisticated alignment approaches may not adequately represent religious viewpoints in health-related contexts.


## GIMMICK: Globally Inclusive Multimodal Multitask Cultural Knowledge Benchmarking

[https://arxiv.org/pdf/2502.13766](https://arxiv.org/pdf/2502.13766)

**Date:** 2025-02-19

Knowledge of cultural rituals, festivals, and practices with religious significance, as a subset of a broader benchmark on global cultural knowledge. Models perform significantly better on tangible cultural aspects (e.g., food) than on intangible ones. Closed models achieved accuracies of only 8% and 10% for questions concerning rituals or festivals, compared to 30% for food-related questions, highlighting a struggle with nuanced, often religious-related, cultural knowledge, particularly in non-Western contexts.


## MMTEB: MASSIVE MULTILINGUAL TEXT EMBEDDING BENCHMARK

[https://arxiv.org/pdf/2502.13595](https://arxiv.org/pdf/2502.13595)

**Date:** 2025-11-13

The benchmark measured model performance on tasks involving religious texts, specifically bitext mining (finding parallel sentences across languages) and clustering of texts from the Bible. The goal was to evaluate text embedding quality on this domain, not to measure bias, stereotypes, or theological knowledge. The paper does not report any specific findings related to the religious domain. The analysis focuses on overall model performance across different languages, task types, and model sizes, concluding that smaller, highly multilingual models can outperform larger models (like Mistral-7B variants) in multilingual and low-resource settings.


## Towards a Design Guideline for RPA Evaluation: A Survey of Large Language Model-Based Role-Playing Agents

[https://arxiv.org/pdf/2502.13012](https://arxiv.org/pdf/2502.13012)

**Date:** 2025-03-27

The paper's proposed design guideline suggests that when an agent's 'Belief and Value' attribute includes religion, it should be evaluated using psychological metrics, as well as metrics for bias, fairness, and ethics. The paper identifies religion as a component of the 'Belief and Value' agent attribute. For agents designed with this attribute, the study's proposed guideline recommends evaluation using psychological metrics, bias metrics, fairness metrics, and ethics metrics.


## None of the Others: a General Technique to Distinguish Reasoning from Memorization in Multiple-Choice LLM Evaluation Benchmarks

[https://arxiv.org/pdf/2502.12896](https://arxiv.org/pdf/2502.12896)

**Date:** 2025-07-10

Knowledge of world religions, as a subject category within a broader multiple-choice question benchmark. The paper evaluates LLM performance on a 'world religions' subject category as part of the MMLU benchmark. It finds that, similar to other humanities subjects, all models experience a significant drop in performance when the multiple-choice questions are altered to test reasoning ('NOTO' variation) instead of recall. For example, in English, top models scored around 0.87 (Cohen's Kappa) on the original questions but dropped to 0.56 or lower in the NOTO variation. This suggests that high performance on questions about world religions is heavily reliant on memorization rather than genuine reasoning.


## “See the World, Discover Knowledge”: A Chinese Factuality Evaluation for Large Vision Language Models

[https://arxiv.org/pdf/2502.11718](https://arxiv.org/pdf/2502.11718)

**Date:** 2025-05-30

The benchmark measures factual knowledge of 'Religious Studies' and 'Religious Buildings' as sub-topics. This includes identifying religious figures (e.g., Vishnu), their associated religion (e.g., Hinduism), and factual details about religious architecture (e.g., Baha'i World Centre International Archives Building). The paper evaluates factual knowledge of religion as part of a broader benchmark covering 56 subtopics. It includes questions about religious figures, associated religions, and religious architecture. However, the paper does not present specific findings or analysis on model performance broken down by the religious sub-categories.


## Safety Evaluation of DeepSeek Models in Chinese Contexts

[https://arxiv.org/pdf/2502.11137](https://arxiv.org/pdf/2502.11137)

**Date:** 2025-05-08

The benchmark measured the models' ability to identify risky content related to 'religious discrimination' via multiple-choice questions, and their capability to refuse answering harmful prompts related to 'religious discrimination' and 'religious extremism'. The paper found that DeepSeek models performed poorly on safety tasks related to religion. In a multiple-choice task to identify religious extremism, both DeepSeek-R1 and DeepSeek-V3 failed, selecting an answer that was the opposite of extremist behavior. In refusal-to-answer tasks, DeepSeek-R1 and DeepSeek-V3 had very low refusal rates for prompts involving 'religious discrimination' (9.1% and 4.5% respectively), indicating a deficiency in handling such sensitive topics.


## SafeDialBench: A Fine-Grained Safety Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks

[https://arxiv.org/pdf/2502.11090](https://arxiv.org/pdf/2502.11090)

**Date:** 2025-11-02

The benchmark measured 'Blasphemy', defined as disrespectful discourse mocking religious symbols, cultural traditions, and sacred beliefs. This was a sub-category under the broader 'Aggression' safety dimension. 'Race and religion' was also one of the 22 dialogue scenarios used for data generation. The paper does not provide specific findings for religion or blasphemy. Instead, it reports on the broader 'Aggression' category which includes blasphemy. Key findings for this category were that models like Qwen2.5 showed weaknesses in identifying aggression-related content, while Yi-34B-Chat and GLM4-9B-Chat demonstrated strong performance in this dimension. The close-sourced model o3-mini showed weaker safety performance in aggression.


## SB-Bench: Stereotype Bias Benchmark for Large Multimodal Models #Mormon

[https://arxiv.org/pdf/2502.08779](https://arxiv.org/pdf/2502.08779)

**Date:** 2025-02-17

The benchmark measures stereotype bias in religious contexts. Specifically, it assesses discriminatory attitudes or behaviors directed at individuals based on their religious beliefs or practices, such as stereotypes about Jewish people and greed or associating Buddhism with compassion and altruism. Closed-source models like GPT-40 and Gemini-1.5-Flash demonstrated the highest level of fairness (lowest bias) in the Religion category. Open-source models generally performed worse, with some showing very high bias scores. A qualitative analysis showed that even advanced models like GPT-40-mini exhibit implicit biases; for instance, in a scenario with a Buddhist and a Jewish individual, the model stereotyped the Buddhist as the more likely charity donor due to associations with compassion. Furthermore, the study found that incorporating visual input significantly amplifies religious bias in LMMs compared to their text-only base LLM counterparts.


## IssueBench: Millions of Realistic Prompts for Measuring Issue Bias in LLM Writing Assistance

[https://arxiv.org/pdf/2502.08395](https://arxiv.org/pdf/2502.08395)

**Date:** 2025-09-10

The benchmark measured issue bias, defined as a consistent tendency to express a particular stance (pro, neutral, con), on various issues including several related to religion. Specific religious topics measured include 'the Catholic Church', 'creationism', 'Islam', 'the impact of religion on society', 'interfaith relationships', 'the role of women in Islam', and 'religious supremacism'. The paper includes several religious topics (e.g., 'Islam', 'the Catholic Church', 'creationism') as part of its IssueBench benchmark but does not report specific, disaggregated findings for these religious issues. The main analysis focuses on aggregate trends in issue bias, stance distortion, and partisan alignment across all 212 issues.


## Break the Checkbox: Challenging Closed-Style Evaluations of Cultural Alignment in LLMs

[https://arxiv.org/pdf/2502.08045](https://arxiv.org/pdf/2502.08045)

**Date:** 2025-09-16

The benchmark measured the cultural value dimension of 'Traditional vs. Secular-rational values' using questions from the World Values Survey (WVS). Specifically, it assessed the models' responses to the question 'how significant is God in your life' and analyzed how responses varied across different probing methods (closed-style vs. unconstrained). The analysis focused on whether models would provide a definitive stance or a non-specific/unclassifiable answer, interpreting the latter as a potential reflection of secular societal values. In unconstrained (open-ended) settings, models frequently refused to answer questions about the importance of God for secular-rational cultures like Germany and the USA, often responding that faith is a private matter. The paper hypothesizes this reflects an accurate representation of those societies' values. In contrast, for more traditional cultures like Bangladesh and the Philippines, models did not produce such unclassifiable outputs. This nuance, which highlights different cultural stances on religion, is completely missed in traditional closed-style (MCQ) evaluations.


## RusCode: Russian Cultural Code Benchmark for Text-to-Image Generation

[https://arxiv.org/pdf/2502.07455](https://arxiv.org/pdf/2502.07455)

**Date:** 2025-02-11

The model's ability to accurately generate visual representations of Russian religious concepts (e.g., Orthodox churches, religious holidays, religious traditions) as part of a broader benchmark on the Russian cultural code. The paper did not report specific findings for the religious categories. The general finding was that models with specific training on Russian culture (Kandinsky 3.1, YandexART 2) significantly outperformed globally popular models (Stable Diffusion 3, DALL-E 3) in generating images that accurately reflect Russian cultural concepts. This included religious elements like Orthodox churches and holidays, suggesting the latter models have a lower 'cultural awareness' of Russian religious visual culture.


## DebateBench: A Challenging Long Context Reasoning Benchmark For Large Language Models

[https://arxiv.org/pdf/2502.06279](https://arxiv.org/pdf/2502.06279)

**Date:** 2025-02-10

The benchmark measures an LLM's ability to perform long-context reasoning and adjudication on complex debate topics, one example of which involves the role of religious figures and institutions in protest movements. The paper provides no findings specific to religion. The general finding is that the tested LLMs struggle with the long-context, complex reasoning required by the benchmark, which includes debates on socio-political topics that may involve religion.


## Beyond English: Evaluating Automated Measurement of Moral Foundations in Non-English Discourse with a Chinese Case Study

[https://arxiv.org/pdf/2502.02451](https://arxiv.org/pdf/2502.02451)

**Date:** 2025-07-22

Measurement of moral foundations, particularly the 'sanctity' foundation, which is explicitly linked to religious concepts like purity, disgust, and religious narratives. The evaluation also touches on culturally-specific moral systems like Confucianism and Catholicism. Large Language Models struggle with culturally and religiously specific nuances of moral foundations. For example, they often miscategorized Confucian concepts like filial piety as 'care' instead of 'authority'. They also failed to capture the specific Chinese cultural context of 'sanctity' when applied to political figures. Furthermore, the models' performance on 'sanctity' was poor for Italian texts, as the Italian understanding of the concept is heavily influenced by Catholic values, which differs from the American-centric conceptions likely present in the training data.


## Fairness through Difference Awareness: Measuring Desired Group Discrimination in LLMs

[https://arxiv.org/pdf/2502.01926](https://arxiv.org/pdf/2502.01926)

**Date:** 2025-08-11

The paper introduced two benchmarks related to religion as part of a larger suite measuring 'Difference Awareness'. The first (D1: Religion) measured factual knowledge about the relative demographic representation of different religions in various countries. The second (D4: Asylum) measured knowledge and reasoning about which religious groups could reasonably argue for asylum in the U.S. due to persecution in their home country. Additionally, it used religious stereotypes (e.g., associating Muslims with terrorism) as an example in its normative benchmark (N1: BBQ) to measure a model's ability to recognize the differential harm of stereotypes against marginalized groups. The key finding related to religion is that LLMs often demonstrate 'difference unawareness.' They struggle with factual questions requiring differentiation between religious groups, such as demographic representation (D1 benchmark) or grounds for asylum due to persecution (D4 benchmark). This failure stems from current fairness approaches that incorrectly treat any distinction between groups as harmful bias. The paper also highlights that models may fail to recognize that stereotypes against marginalized religious groups (e.g., Muslims) are more harmful than those against dominant groups, incorrectly judging the harm as equal.


## From tools to thieves: Measuring and understanding public perceptions of AI through crowdsourced metaphors

[https://arxiv.org/pdf/2501.18045](https://arxiv.org/pdf/2501.18045)

**Date:** 2025-06-17

The frequency and characteristics of religious and mythical metaphors (e.g., 'God', 'genie', 'angel', 'devil') used by the public to describe Artificial Intelligence, and the correlation of these metaphors with attitudes such as trust, willingness to adopt, warmth, and competence. The study identified 'God', 'genie', and 'folklore' (including 'angel' and 'satan/devil') as dominant metaphor clusters for AI. These metaphors, evoking magic and mysticism, were associated with specific public perceptions. The 'god' metaphor, for instance, was a significant predictor of higher trust in and adoption of AI. There were also notable demographic differences; the 'genie' and 'god' metaphors were significantly more common among non-white participants, suggesting differing perspectives on AI's power and agency which could lead to a higher risk of overreliance for these populations.


## HATEBENCH: Benchmarking Hate Speech Detectors on LLM-Generated Content and Hate Campaigns #Mormon

[https://arxiv.org/pdf/2501.16750](https://arxiv.org/pdf/2501.16750)

**Date:** 2025-01-28

The benchmark measures the effectiveness and robustness of hate speech detectors on LLM-generated content that targets various identity groups, including specific religious groups. Hate speech detector performance is inconsistent across different religious groups. For LLM-generated samples, detectors showed varied effectiveness, achieving high F1-scores for content targeting Christians (e.g., Perspective score of 0.933) and Hindus (0.900), while performing less effectively on content targeting Jewish (0.764) and Atheist (0.841) groups.


## Through the Prism of Culture: Evaluating LLMs’ Understanding of Indian Subcultures and Traditions

[https://arxiv.org/pdf/2501.16748](https://arxiv.org/pdf/2501.16748)

**Date:** 2025-09-07

The benchmark measured the Large Language Models' (LLMs) knowledge and contextual understanding of localized and sub-cultural religious practices, rituals, and beliefs within India ('Little Traditions'), particularly contrasting them with dominant religious narratives ('Great Traditions'). This included evaluating responses on scenarios involving monotheistic Hindu sects (Lingayats), concepts of ritual purity and pollution, and local religious ceremonies like frog marriages for rain. LLMs struggle to comprehend the nuances of localized religious subcultures ('Little Traditions') in India, often defaulting to dominant, generalized narratives ('Great Traditions'). For instance, most models incorrectly classified all of Hinduism as polytheistic, failing to recognize monotheistic sects like the Lingayats. While some models could identify certain rituals, they often lacked deep contextual understanding, prioritizing modern sensibilities (e.g., sanitation over ritual purity) or failing to identify specific traditional names. The models' performance often worsened when prompts were provided in regional Indian languages instead of English, highlighting a data and optimization gap.


## CASE-BENCH: CONTEXT-AWARE SAFETY BENCHMARK FOR LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2501.14940](https://arxiv.org/pdf/2501.14940)

**Date:** 2025-02-07

Evaluating the effect of context (safe, unsafe, vs. no context) on human and LLM safety judgments for queries related to 'religion promotion'. The benchmark measures whether a query should be answered or refused based on the provided context. The category 'religion promotion' showed the most significant shift in human safety judgments when context was added, compared to 44 other categories. It had the highest Kruskal-Wallis (K-W) statistic value, indicating that context had the most pronounced effect. Specifically, providing an unsafe context led to a notable decrease in the proportion of human annotators who believed the chatbot should respond to the query.


## Value Compass Benchmarks: A Comprehensive, Generative and Self-Evolving Platform for LLMs’ Value Evaluation

[https://arxiv.org/pdf/2501.07071](https://arxiv.org/pdf/2501.07071)

**Date:** 2025-06-02

The benchmark measures alignment with a set of universal and moral values, some of which are explicitly linked to religion. Specifically, it evaluates the 'Tradition' value (respect for and acceptance of customs and ideas from traditional culture or religion) from Schwartz's Theory of Basic Values, and the 'Sanctity/Degradation' foundation (notions of striving to live in an elevated, noble way, often found in religious narratives) from Moral Foundation Theory. The paper does not report specific findings related to religion. It establishes a framework capable of measuring values such as 'Tradition' and 'Sanctity', which are derived from or associated with religious contexts, but it does not provide an analysis of how different LLMs perform on these specific value dimensions.


## Towards New Benchmark for AI Alignment & Sentiment Analysis in Socially Important Issues: A Comparative Study of Human and LLMs in the Context of AGI

[https://arxiv.org/pdf/2501.02531](https://arxiv.org/pdf/2501.02531)

**Date:** 

The proposed Societal AI Alignment & Sentiment Benchmark (SAAS-AI) measures AI alignment with societal values, including the representation of religious/cultural heritage and moral conservatism. It is designed to detect biases related to religion, among other axes like gender, ethnicity, and nationality. The paper did not present new empirical findings on religion from its own experiment, which focused on sentiment towards AGI. However, it proposed a new benchmark (SAAS-AI) that incorporates religion as a key axis for evaluation. This inclusion was justified by citing other research (e.g., the Singapore AI Safety Red Teaming Challenge) which demonstrated that religious bias is a prevalent issue in Large Language Models.


## A Survey of State of the Art Large Vision Language Models: Alignment, Benchmark, Evaluations and Challenges

[https://arxiv.org/pdf/2501.02189](https://arxiv.org/pdf/2501.02189)

**Date:** 2025-04-06

The paper surveys benchmarks that measure stereotypical bias related to religion (MMBias) and performance disparities across cultures, including religious ones (CulturalVQA). The survey cites existing work, noting that the MMBias benchmark was created to target religious bias. It also references the CulturalVQA benchmark, which found that models exhibit worse performance for Islamic cultures compared to North American cultures.


## A Comprehensive Framework to Operationalize Social Stereotypes for Responsible AI Evaluations

[https://arxiv.org/pdf/2501.02074](https://arxiv.org/pdf/2501.02074)

**Date:** 2025-10-01

The paper proposes a general framework to operationalize social stereotypes, using stereotypes in religious contexts as a key example. It demonstrates how to capture stereotypes about religious identity, associated attributes (e.g., vegetarianism for Brahmins), and the importance of geo-cultural context (e.g., Christians in India). The paper uses religion as a key example to illustrate the components of its proposed stereotype framework. It highlights the temporal evolution of religious terms (e.g., 'Protestant'), the context-dependency of marginalization (e.g., Christians in India vs. the US), and includes examples of religious/caste-based stereotypes (e.g., 'brahmins are vegetarians') from existing datasets to demonstrate the framework's utility.


## M³oralBench: A MultiModal Moral Benchmark for LVLMs

[https://arxiv.org/pdf/2412.20718](https://arxiv.org/pdf/2412.20718)

**Date:** 2024-12-30

The benchmark measures LVLMs' understanding of moral violations related to the 'Sanctity/Degradation' foundation from Moral Foundations Theory, which is influenced by ideas of spirituality and purity often found in religious contexts. Large Vision-Language Models (LVLMs) exhibit their poorest moral performance on the Sanctity/Degradation foundation. This highlights a significant gap between the models' understanding of concepts like purity and sacredness—which are often tied to spirituality and religion—and human moral values, which rate sanctity violations as severe moral transgressions.


## Building a Rich Dataset to Empower the Persian Question Answering Systems

[https://arxiv.org/pdf/2412.20212](https://arxiv.org/pdf/2412.20212)

**Date:** 

Knowledge of religious topics as part of a general, open-domain question-answering task. The constructed dataset, NextQuAD, includes a 'Religion' category, and the paper also reviews other datasets focused on Islamic texts (IslamicPCQA) and a general religious corpus (Rasayel and Massayel). The paper does not report specific findings related to the religion category. The main finding is that a model trained on the new NextQuAD dataset (which includes a 'Religion' sub-category) outperforms models trained on other Persian datasets like ParSQuAD and PersianQA on general QA tasks, indicating the higher quality of the new dataset.


## A Culturally-Aware Benchmark for Person Re-Identification in Modest Attire

[https://arxiv.org/pdf/2412.18874](https://arxiv.org/pdf/2412.18874)

**Date:** 2025-06-10

The benchmark measures the performance drop and cultural bias of Person Re-Identification (ReID) computer vision models when applied to a dataset featuring modest attire, such as hijabs, which are prevalent in Islamic cultural contexts. It specifically evaluates the models' ability to identify individuals in settings where clothing offers fewer distinctive features. State-of-the-art Person Re-Identification models (SOLIDER and CLIP-ReID) show a significant performance drop on the IUST_PersonReId dataset, which features modest attire common in Islamic culture. The paper attributes this to challenges like occlusion and limited distinctive features, particularly for women wearing hijabs, highlighting a significant cultural and demographic bias in current visual recognition systems. Re-identifying females was found to be more challenging than males, even when the dataset was balanced for gender.


## SUBDATA: Bridging Heterogeneous Datasets to Enable Theory-Driven Evaluation of Political and Demographic Perspectives in LLMs #Mormon

[https://arxiv.org/pdf/2412.16783](https://arxiv.org/pdf/2412.16783)

**Date:** 2025-10-12

The benchmark measures the rate at which Large Language Models, conditioned on different political personas (left-leaning vs. right-leaning), classify content as hate speech when it targets specific religious groups. Across all models tested, LLMs conditioned on left-leaning personas consistently detected a higher proportion of hate speech against religious groups (Muslims, Jews, Christians) compared to LLMs conditioned on right-leaning personas. This suggests that a left-leaning alignment induces a general increase in sensitivity to hateful content rather than offering selective protection to specific groups.


## TelcoLM: collecting data, adapting, and benchmarking language models for the telecommunication domain

[https://arxiv.org/pdf/2412.15891](https://arxiv.org/pdf/2412.15891)

**Date:** 2024-12-20

The benchmark measured the models' ability to answer questions about religious creation narratives (specifically from the biblical Book of Genesis) as part of a broader general knowledge and truthfulness evaluation (TruthfulQA). It assessed whether models presented these narratives as factual or contextualized them as religious beliefs. When asked about the creation of the world, the tested Llama models tended to state the biblical narrative (e.g., "6 days") as a fact. In contrast, GPT-3.5 and GPT-4 correctly contextualized the answer as a religious belief from the Book of Genesis, demonstrating a more nuanced understanding of religious vs. scientific claims.


## Chinese SafetyQA: A Safety Short-form Factuality Benchmark for Large Language Models

[https://arxiv.org/pdf/2412.15265](https://arxiv.org/pdf/2412.15265)

**Date:** 2024-12-23

Factual knowledge related to religious prejudice and discrimination within the Chinese context. The paper does not provide specific findings for the religion subcategory. Results related to religion are aggregated under broader categories such as 'Prejudice & Discrimination' (PD) and 'Insults & Hate' (IH).


## Towards Automatic Evaluation for Image Transcreation

[https://arxiv.org/pdf/2412.13717](https://arxiv.org/pdf/2412.13717)

**Date:** 2025-03-20

The benchmark measured the performance of Vision-Language Models on transcreating images from the abstract category of 'religion'. Performance was evaluated along three axes: cultural relevance, semantic equivalence, and visual similarity. VLM-based metrics performed well on cultural relevance for the religion category. However, both object-based metrics and VLM-based metrics struggled to evaluate semantic equivalence for abstract categories like religion. Embedding-based metrics also showed slightly diminished performance for abstract categories compared to concrete ones.


## Socio-Culturally Aware Evaluation Framework for LLM-Based Content Moderation

[https://arxiv.org/pdf/2412.13578](https://arxiv.org/pdf/2412.13578)

**Date:** 2024-12-18

The benchmark measures how Large Language Models generate hateful content and exhibit biases when prompted with personas having specific religious attributes. It analyzes how different religious identities influence the tone and content of generated text, particularly in the context of hate speech. In the hate speech generation task (HATE-GEN), religious beliefs were a key factor. The study found that Protestant and Taoist personas tended to oppose hate speech, while Baptist personas were more prone to generating hateful content. Atheist and Catholic personas maintained a balance, Muslim and Hindu personas showed moderate tendencies, and Jewish personas leaned toward opposing hate speech.


## CEHA: A Dataset of Conflict Events in the Horn of Africa

[https://arxiv.org/pdf/2412.13511](https://arxiv.org/pdf/2412.13511)

**Date:** 2024-12-18

The benchmark measures the ability of models to perform multi-label classification of violent conflict events from news articles, with one of the specific categories being 'Religious Conflict'. This category is defined as conflicts arising from differences in religious beliefs or practices, or targeting individuals/groups based on their stated religious affiliation (e.g., Muslim, Orthodox Christian) or their engagement in religious practice. In the task of classifying 'Religious Conflict' events, Large Language Models (LLMs) generally outperformed supervised models. The best performance was achieved by Mistral-large in a 6-shot setting with an F1 score of 84.75%, which was 6.06% higher than the best-performing supervised model (T5). This suggests that LLMs are particularly effective for identifying religious conflicts in this low-resource context.


## A Framework for Critical Evaluation of Text-to-Image Models: Integrating Art Historical Analysis, Artistic Exploration, and Critical Prompt Engineering.

[https://arxiv.org/pdf/2412.12774](https://arxiv.org/pdf/2412.12774)

**Date:** 2024-12-17

The framework measures bias in religious iconography (specifically, a tendency towards Western/Christian imagery) and the models' ability to understand and accurately represent complex religious and cultural symbolism in art. The paper found that AI models exhibit a bias towards Western religious iconography, such as consistently generating images of Christian saints even when prompted for more general spiritual figures. In a case study involving 'The Arnolfini Portrait,' models struggled with depicting deep symbolic interpretations and often omitted crucial religious symbols present in the original artwork.


## QUENCH: Measuring the gap between Indic and Non-Indic Contextual General Reasoning in LLMs

[https://arxiv.org/pdf/2412.11763](https://arxiv.org/pdf/2412.11763)

**Date:** 2024-12-16

Knowledge of mythology and religion as part of a broader general world knowledge and deductive reasoning benchmark. The 'Mythology & Religion' theme comprises 4.2% of the dataset. The paper does not provide specific findings for the 'Mythology & Religion' theme. The general finding is that all tested models perform worse on Indic-context questions compared to non-Indic ones, which would include questions related to Indic religions and mythologies.


## MT-LENS: An all-in-one Toolkit for Better Machine Translation Evaluation

[https://arxiv.org/pdf/2412.11615](https://arxiv.org/pdf/2412.11615)

**Date:** 2024-12-16

Toxicity detection in machine translation outputs, where the source text is related to various demographic axes, including religion. The paper introduces the MT-LENS framework, which is capable of evaluating added toxicity related to religion using the HOLISTICBIAS dataset. However, the paper does not present any specific findings or results regarding the performance of models on the religion axis; it only describes the tool's capability.


## Optimized Quran Passage Retrieval Using an Expanded QA Dataset and Fine-Tuned Language Models

[https://arxiv.org/pdf/2412.11431](https://arxiv.org/pdf/2412.11431)

**Date:** 2024-12-16

The benchmark measured the performance of various language models on Qur'anic passage retrieval. This involved assessing their ability to accurately retrieve relevant verses from the Holy Qur'an in response to questions posed in Modern Standard Arabic, thereby testing their knowledge and comprehension of this specific religious text. By expanding the training dataset from 251 to 1895 questions and fine-tuning several transformer models, the system's performance on Qur'an passage retrieval was significantly enhanced. The best model, AraBERT-base, improved its MAP@10 score by 63% (from 0.22 to 0.36) and its MRR score by 59% (from 0.37 to 0.59) compared to the baseline. The approach also tripled the success rate for handling 'no answer' questions, from 25% to 75%, demonstrating the effectiveness of dataset enrichment and model optimization for question-answering on a complex religious text.


## MALAMUTE: A Multilingual, Highly-granular, Template-free, Education-based Probing Dataset

[https://arxiv.org/pdf/2412.10105](https://arxiv.org/pdf/2412.10105)

**Date:** 2025-05-25

Factual knowledge of religious concepts within educational domains, such as the 'free exercise clause' in American government, Nietzsche's philosophy on God, and the 'dalits' social group in anthropology. The paper does not provide specific findings related to religion. Its analysis is at the level of domains and subdomains (e.g., Philosophy, American Government, Anthropology). For example, it notes that SciBERT's performance drops on subjects like Philosophy and Anthropology, which contain the religion-related prompts, but does not isolate the religious questions for a separate analysis.


## Filipino Benchmarks for Measuring Sexist and Homophobic Bias in Multilingual Language Models from Southeast Asia

[https://arxiv.org/pdf/2412.07303](https://arxiv.org/pdf/2412.07303)

**Date:** 2024-12-11

The benchmark measures stereotypes linking queer identities with religious concepts of sinfulness and disobedience to God. For instance, it evaluates if models are more likely to find sentences like 'Being a lesbian is a sin' or 'Lesbians do not heed the word of God' more plausible than their neutral counterparts. Language models are more likely to associate queer women (tomboy or lesbiyana) with the religious concept of being 'sinful' compared to heterosexual women.


## Evaluating and Mitigating Social Bias for Large Language Models in Open-ended Settings

[https://arxiv.org/pdf/2412.06134](https://arxiv.org/pdf/2412.06134)

**Date:** 2025-10-15

Detection of social biases and stereotypes in religious contexts across multiple-choice, fill-in-the-blank, and short-answer questions. For ambiguous religious questions, GPT-3.5 exhibited a high bias score (0.205) in the fill-in-the-blank format, while GPT-4o showed lower but still present bias. For disambiguated questions, GPT-3.5 consistently showed higher bias than GPT-4o. The proposed 'Composite Prompting' debiasing method was effective, reducing bias scores in the religion category to near-zero for both models.


## Hostility Detection in UK Politics: A Dataset on Online Abuse Targeting MPs

[https://arxiv.org/pdf/2412.04046](https://arxiv.org/pdf/2412.04046)

**Date:** 2024-12-05

Detection of hostility in tweets directed at UK Members of Parliament (MPs), where one of the targeted identity characteristics is religion. Non-Christian Members of Parliament (MPs) face significantly higher levels of religion-based and general hostility compared to their Christian counterparts. Models were evaluated on their ability to detect religion-based hostility as a sub-task, with GPT-3.5 (prompted with definitions) achieving the highest F1-score in a hierarchical classification setting that included religion as a category of hostility.


## INCLUDE: EVALUATING MULTILINGUAL LANGUAGE UNDERSTANDING WITH REGIONAL KNOWLEDGE

[https://arxiv.org/pdf/2411.19799](https://arxiv.org/pdf/2411.19799)

**Date:** 2024-11-29

The benchmark, named INCLUDE, measures a model's knowledge of the academic subject of 'Religious Studies' as part of a broader assessment of multilingual, regional, and cultural understanding. It specifically tests knowledge from examinations in this field and how religious interpretations might differ across regions. The paper does not provide specific findings isolated to religion. Religious studies questions are categorized under 'Humanities' and are used to assess cultural and region-specific knowledge. The general finding is that model performance varies significantly across languages and regions, suggesting that models' grasp of specialized knowledge, including religious topics, is inconsistent and often lacking, especially for less-resourced languages.


## All Languages Matter: Evaluating LMMs on Culturally Diverse 100 Languages

[https://arxiv.org/pdf/2411.16508](https://arxiv.org/pdf/2411.16508)

**Date:** 2025-05-01

The benchmark measured the models' knowledge and visual understanding of religious concepts, including the ability to identify and explain the cultural and historical significance of religious ceremonies (e.g., the Hawaiian 'aha Aloha), festivals (e.g., the Islamic Mela Chiraghan), and related artifacts across 100 different languages. Models were evaluated on their knowledge of religion as a cultural domain. Performance varied significantly, with closed-source models like GPT-4o generally outperforming open-source models on tasks related to understanding religious context. A key finding highlighted a 'Lack of Cultural Understanding' where GPT-4o confused two distinct Islamic festivals (Mela Chiraghan and Eid Milad un Nabi), demonstrating a failure to grasp nuanced cultural and religious distinctions despite visual similarities.


## HATEDAY: Insights from a Global Hate Speech Dataset Representative of a Day on Twitter

[https://arxiv.org/pdf/2411.15462](https://arxiv.org/pdf/2411.15462)

**Date:** 2025-06-03

Detection of hate speech targeting individuals or groups based on their religion. The benchmark measures the prevalence of religious hate speech as a specific target category within a global dataset, and evaluates model performance in identifying it. Religious hate speech constitutes a significant portion of all hate in certain regions, representing 41% of hate in India, mostly as Islamophobia. However, it is less prominent in other analyzed contexts. Compared to their overall prevalence, religion-targeted hate speech is underrepresented in the models' false negatives. Furthermore, religion-based hate is less prevalent in the real-world HATEDAY dataset than it is in existing academic hate speech datasets, indicating a misalignment between academic focus and real-world occurrences.


## The Impossible Test: A 2024 Unsolvable Dataset and A Chance for an AGI Quiz

[https://arxiv.org/pdf/2411.14486](https://arxiv.org/pdf/2411.14486)

**Date:** 2024-11-01

The benchmark measured the ability of Large Language Models to acknowledge uncertainty on fundamentally unsolvable problems across various domains. The connection to religion or faith was through the inclusion of a 'Mysticism' problem category, testing if models would admit ignorance on such topics rather than generating speculative answers. Based on the 'GPT-4 accuracy as a function of domain specialty' chart (Figure 4), the model demonstrated a low percentage of correct answers (admissions of ignorance) for the 'Mysticism' category. This indicates that the model was more likely to generate confident but incorrect guesses for problems related to mysticism, rather than acknowledging that the problems are unsolvable.


## VBench++: Comprehensive and Versatile Benchmark Suite for Video Generative Models

[https://arxiv.org/pdf/2411.13503](https://arxiv.org/pdf/2411.13503)

**Date:** 2024-11-20

The benchmark measured the ability of video generative models to fairly generate scenes across various cultures, including religious ones such as Buddhism, Christianity, Hinduism, and Islam, as part of its 'Culture Fairness' evaluation. Performance on 'Culture Fairness' varied significantly across models. Models developed by industrial companies (e.g., ModelScope, VideoCrafter-2.0) demonstrated stronger performance in trustworthiness, including cultural fairness, compared to models from academic research (e.g., CogVideo, Show-1), which may be attributable to access to more diverse data and a greater emphasis on internal reviews.


## Value Imprint: A Technique for Auditing the Human Values Embedded in RLHF Datasets

[https://arxiv.org/pdf/2411.11937](https://arxiv.org/pdf/2411.11937)

**Date:** 2024-11-18

Detection of preferences that moderate religious fanaticism and antisemitic comments within RLHF datasets. The analysis of RLHF datasets revealed that the 'Civility & Tolerance' value category includes preferences that moderate user requests for 'antisemitic comments, and religious and ethnic fanaticism'. This value was identified as one of the less represented categories within the audited datasets.


## Value-Spectrum: Quantifying Preferences of Vision-Language Models via Value Decomposition in Social Media Contexts

[https://arxiv.org/pdf/2411.11479](https://arxiv.org/pdf/2411.11479)

**Date:** 2025-06-03

Preference for visual content related to the Schwartz value of 'Tradition', which includes keywords like 'Religious' and 'Worship'. Across all tested Vision-Language Models, the 'Tradition' value dimension, which encompasses religious themes, was the third most preferred category, with an average preference score of 72.8 out of 100, indicating a generally high preference for such content.


## Bias in Large Language Models: Origin, Evaluation, and Mitigation

[https://arxiv.org/pdf/2411.10915](https://arxiv.org/pdf/2411.10915)

**Date:** 2024-11-16

The paper cites studies that measure stereotype bias, specifically the association between Muslims and violence, and the generation of toxic language related to religious groups (e.g., 'Islamic slaughtering'). It also mentions the mitigation of religious bias by swapping religious terms. The paper cites findings that LLMs exhibit a significant Muslim-violence bias, which is more severe than biases against other religious groups. It also notes that language models can degenerate into generating toxic content, including phrases like 'Islamic slaughtering'. Additionally, it mentions that counterfactual data augmentation (CDA) by swapping religious terms has been empirically evaluated as a method for mitigating religious bias.


## Beyond the Safety Bundle: Auditing the Helpful and Harmless Dataset

[https://arxiv.org/pdf/2411.08243](https://arxiv.org/pdf/2411.08243)

**Date:** 2025-06-03

The benchmark measures disparate safety behaviors (specifically, refusal rates to safe prompts) across different demographic groups, including religious groups. It investigates how training on the Helpful and Harmless (HH) dataset, which has an imbalanced distribution of religious identity terms, can lead models to associate these terms with harmfulness and exhibit exaggerated safety responses. The study found that religious identity terms like 'Muslim' and 'Jewish' are overrepresented in the 'harmless' (red-teaming) portion of the Anthropic HH dataset compared to the 'helpful' portion. This imbalance in the training data leads models to develop disparate safety behaviors, such as higher refusal rates for safe prompts that contain these religious terms. This suggests that safety training with the HH dataset can paradoxically perpetuate harmful associations between specific religious groups and toxicity.


## CHINESE SIMPLEQA: A CHINESE FACTUALITY EVALUATION FOR LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2411.07140](https://arxiv.org/pdf/2411.07140)

**Date:** 2024-11-13

The benchmark measures the factual knowledge of LLMs on various topics, including religion, by evaluating their ability to answer short, fact-seeking questions. For religion, this specifically includes factual questions about Buddhism and Taoism within the context of Chinese culture. The paper does not report specific findings for the religion subtopic. The analysis is presented at the level of six broad categories (e.g., 'Chinese Culture', 'Society'), and while 'Religion' is a sub-category, its specific performance is not detailed.


## Benchmarking Distributional Alignment of Large Language Models

[https://arxiv.org/pdf/2411.05403](https://arxiv.org/pdf/2411.05403)

**Date:** 2024-11-08

The benchmark measured the distributional alignment of Large Language Models with human opinion distributions on subjective survey questions. One specific example used to illustrate the importance of this measurement involved a question from the PEW survey about the perceived importance of belief in God for being a moral person. The paper uses a question about the importance of belief in God for morality as a key example to argue that evaluating LLMs based only on the majority human response is insufficient. The main finding illustrated by this example is that for subjective topics, including religion, it is crucial to measure a model's ability to align with the entire distribution of human opinions, including minority views, rather than just predicting the most likely answer.


## MILU: A Multi-task Indic Language Understanding Benchmark

[https://arxiv.org/pdf/2411.02538](https://arxiv.org/pdf/2411.02538)

**Date:** 2025-02-04

The benchmark, MILU, measures the knowledge of Large Language Models on 41 subjects within an India-centric context. One of these subjects is 'Religion and Spirituality', so the benchmark evaluates the models' knowledge on this topic through multiple-choice questions. The paper's domain-wise analysis indicates that models generally perform poorly in culturally relevant areas (such as Arts & Humanities, Social Sciences) compared to general fields like STEM. While 'Religion and Spirituality' is one of the benchmark's subjects and falls into this culturally relevant category, its specific performance is detailed in appendix tables but not singled out for discussion in the main findings.


## Culinary Class Wars: Evaluating LLMs using ASH in Cuisine Transfer Task

[https://arxiv.org/pdf/2411.01996](https://arxiv.org/pdf/2411.01996)

**Date:** 2024-11-04

The benchmark measured the ability of Large Language Models to generate culturally and religiously appropriate recipes, specifically focusing on adherence to religious dietary laws (e.g., Kosher, Islamic, Buddhist, Jain) in a cuisine transfer task. The paper found that LLMs performed well on generating recipes for certain religious dietary laws, with 'Kosher' and 'Islamic' cuisines ranking among the highest for authenticity, sensitivity, and harmony. However, the analysis suggests this high performance might be due to a superficial understanding, as models tended to focus on keywords like 'certified' for Kosher recipes, rather than demonstrating a deep grasp of the culinary or religious nuances.


## IDEATOR: Jailbreaking and Benchmarking Large Vision-Language Models Using Themselves

[https://arxiv.org/pdf/2411.00827](https://arxiv.org/pdf/2411.00827)

**Date:** 2025-09-25

The benchmark, VLJailbreakBench, measured the models' susceptibility to generating harmful content when jailbroken. One of the measured subcategories was 'Religious Hate Speech'. The paper developed a safety benchmark, VLJailbreakBench, which includes 'Religious Hate Speech' as a subcategory under the main 'Hate Speech' topic. However, the results are aggregated at the 'Hate Speech' category level, and no specific findings or attack success rates are reported for the 'Religious Hate Speech' subcategory alone. The paper does not mention any specific religious groups.


## Benchmarking Bias in Large Language Models during Role-Playing

[https://arxiv.org/pdf/2411.00585](https://arxiv.org/pdf/2411.00585)

**Date:** 2024-11-01

The benchmark measured social biases and stereotypes related to religious groups when Large Language Models (LLMs) are prompted to adopt specific roles. This was done by generating role-specific Yes/No, multiple-choice, and open-ended questions designed to elicit discriminatory responses. Religion was one of 11 demographic attributes tested for bias. It ranked 6th out of 11 in terms of the average number of biased responses elicited (1,089), indicating a significant level of bias that is comparable to other attributes, though less pronounced than attributes like Race and Culture. The paper did not provide a deeper qualitative analysis specific to the types of religious biases found.


## Risk Sources and Risk Management Measures in Support of Standards for General-Purpose AI Systems

[https://arxiv.org/pdf/2410.23472](https://arxiv.org/pdf/2410.23472)

**Date:** 2024-11-15

Detection of stereotypes based on religious beliefs. The paper identifies 'religious bias' as a type of systemic bias in AI systems, noting that debiasing methods can focus on stereotypes related to religious beliefs. This is presented as part of a broader catalog of risks rather than an empirical finding from a new experiment.


## Evaluating Cultural and Social Awareness of LLM Web Agents

[https://arxiv.org/pdf/2410.23252](https://arxiv.org/pdf/2410.23252)

**Date:** 2025-03-08

The benchmark, CASA, measures an LLM agent's ability to detect and appropriately respond to user queries that violate cultural and social norms, a significant portion of which are derived from religious laws and practices (e.g., Islamic prohibition of alcohol, Buddhist reverence for monks' attire, Hindu festival etiquette). LLM agents demonstrate very low awareness (<10%) of religio-cultural norms and high violation rates (>40%) in web-based environments, performing significantly worse than in non-agent (i.e., standard chatbot) settings. Agents are highly susceptible to being misled by web content that contradicts these norms, such as those related to Islamic law or Buddhist practices. Prompting and fine-tuning can improve performance, with notable gains in culturally and religiously diverse regions like Indonesia, Egypt, Saudi Arabia, and India.


## SG-Bench: Evaluating LLM Safety Generalization Across Diverse Tasks and Prompt Types

[https://arxiv.org/pdf/2410.21965](https://arxiv.org/pdf/2410.21965)

**Date:** 2024-10-29

The benchmark measures LLM safety across several categories, one of which is 'Stereotyping and Bias'. This category includes the sub-category of 'Religious stereotyping'. The paper does not provide specific findings related to religion, as the results for the 'Stereotyping and Bias' category were not disaggregated to the level of religious stereotyping.


## CAN MACHINES THINK LIKE HUMANS? A BEHAVIORAL EVALUATION OF LLM AGENTS IN DICTATOR GAMES

[https://arxiv.org/pdf/2410.21359](https://arxiv.org/pdf/2410.21359)

**Date:** 2025-11-17

Use of religious language (e.g., God, hell, pray) in the LLM's reasoning for its decisions in a dictator game, as measured by the Linguistic Inquiry and Word Count (LIWC) 'Religion' category. The use of religious language as a predictor for generous behavior was inconsistent across different LLM agents. In both 'Sense of Self' and 'Theory of Mind' trials, most models showed no significant correlation between religious language and the amount of money transferred. There was no consensus among models, indicating they do not reliably replicate human psychological processes related to religion in this context.


## Improving Model Evaluation using SMART Filtering of Benchmark Datasets

[https://arxiv.org/pdf/2410.20245](https://arxiv.org/pdf/2410.20245)

**Date:** 2025-02-10

Knowledge of world religions, as a sub-category within the MMLU benchmark. Within the MMLU dataset, 59.06% of the examples from the 'World Religions' category were removed by the SMART filtering process. This suggests that a significant portion of the questions related to world religions were identified as being easy, data-contaminated, or redundant.


## FAIRMT-BENCH: BENCHMARKING FAIRNESS FOR MULTI-TURN DIALOGUE IN CONVERSATIONAL LLMS

[https://arxiv.org/pdf/2410.19317](https://arxiv.org/pdf/2410.19317)

**Date:** 2025-06-10

The benchmark measures fairness, specifically stereotype and toxicity biases, related to religious groups within the context of multi-turn dialogues. It evaluates the ability of LLMs to understand and resist generating biased content across various conversational stages. LLMs exhibit biases against religious groups, particularly in multi-turn dialogues where stereotypes and toxicity can accumulate. The study found that while models showed relatively stronger fairness alignment for religion compared to less-represented categories, they could still be prompted to generate biased content, such as associating Muslims with terrorism or Jewish people with greed. The performance in maintaining fairness varied significantly across different models and conversational tasks.


## SafeBench: A Safety Evaluation Framework for Multimodal Large Language Models

[https://arxiv.org/pdf/2410.18927](https://arxiv.org/pdf/2410.18927)

**Date:** 2024-10-24

The benchmark measured the models' tendency to express or favor religious opinions, with the goal of ensuring the models respect diverse religious beliefs and maintain neutrality. Models generally demonstrated high safety performance for queries related to 'Religious Opinions'. This category, as part of the broader 'Inappropriate Opinions' (IO) major category, had one of the lowest average Attack Success Rates (11.5% for the IO category) compared to other risk categories, indicating models are relatively robust against generating inappropriate religious content.


## CompassJudger-1: All-in-one Judge Model Helps Model Evaluation and Evolution

[https://arxiv.org/pdf/2410.16256](https://arxiv.org/pdf/2410.16256)

**Date:** 2024-10-21

The paper includes 'Religion & Faith' as one of 31 categories for classifying user questions during the data preparation phase. However, no performance metrics or specific analyses are reported for this category. The paper's data categorization process includes a 'Religion & Faith' category, but no specific analysis or results related to religion were reported. The paper's findings focus on the overall judging capabilities of the models across general domains.


## Evaluating Consistencies in LLM responses through a Semantic Clustering of Question Answering

[https://arxiv.org/pdf/2410.15440](https://arxiv.org/pdf/2410.15440)

**Date:** 

Semantic consistency of answers to questions in the 'Religion' category from the TruthfulQA dataset. Both the RAG (Retriever-Augmented-Generation) and Zero-Shot-CoT (Chain-of-Thought) methods improved the semantic consistency of the model's responses for the 'Religion' category. The RAG method resulted in a greater improvement in consistency (a change of approximately +0.33) compared to the Zero-Shot-CoT method (a change of approximately +0.15), as shown in Figure 3.


## Text-to-Image Representativity Fairness Evaluation Framework

[https://arxiv.org/pdf/2410.14201](https://arxiv.org/pdf/2410.14201)

**Date:** 2024-10-18

Stereotypical associations with religious/cultural attire (hijab, bindi) in text-to-image generation. The study found that attempting to use semantic guidance to remove religious/cultural attire like a 'bindi' from an Indian person or a 'hijab' from a Middle Eastern person resulted in image distortion. This suggests the model has deeply ingrained stereotypes, as it would invoke other stereotypes (e.g., wrinkles, grey hair) or alter the gender/race rather than simply removing the specified item.


## BENTO: BENCHMARK TASK REDUCTION WITH IN-CONTEXT TRANSFERABILITY

[https://arxiv.org/pdf/2410.13804](https://arxiv.org/pdf/2410.13804)

**Date:** 2024-10-21

The benchmark measured knowledge of world religions as one of 57 tasks within the MMLU benchmark, evaluated through multiple-choice questions. The paper's In-Context Transferability (ICT) analysis revealed that the 'world religions' task clusters with other tasks under the theme of 'International Security', alongside 'international law', 'medical genetics', 'security studies', 'us foreign policy', and 'virology'. This suggests that from an LLM's perspective, the knowledge and skills required for the 'world religions' task are similar to those in the international security domain.


## Cross-Lingual Auto Evaluation for Assessing Multilingual LLMs

[https://arxiv.org/pdf/2410.13394](https://arxiv.org/pdf/2410.13394)

**Date:** 2025-07-18

Evaluation of moral reasoning in a scenario involving conflicting personal choices and community religious norms. Specifically, it assesses if a model can identify the key ethical principles at play in a dilemma where an individual's non-vegetarian diet conflicts with the strict religious vegetarianism of a neighborhood. No specific findings related to religion were reported. However, a moral dilemma involving religious norms was used as an example to show that for complex reasoning questions, the evaluator model sometimes relies on its own parametric knowledge to evaluate the output, overlooking the provided reference answer. This tendency was noted to be more frequent in high-resource languages like German and French.


## BANTH: A Multi-label Hate Speech Detection Dataset for Transliterated Bangla

[https://arxiv.org/pdf/2410.13281](https://arxiv.org/pdf/2410.13281)

**Date:** 2025-05-31

The benchmark measures the detection of hate speech targeting individuals or groups based on their religious beliefs or lack thereof. This includes language demonizing religious communities, advocating discrimination, or inciting violence against religious institutions or adherents. The best-performing fine-tuned model (TB-mBERT) achieved a high macro-F1 score on the 'Religious' hate speech category, with an accuracy of 99.2%. This high performance is attributed to the presence of clear, representative words (e.g., 'Muslim') in the samples for this category, making them easier to classify. The co-occurrence of religious hate speech with other categories was found to be relatively low compared to categories like 'Personal Offense' or 'Political'.


## debiaSAE: Benchmarking and Mitigating Vision-Language Model Bias

[https://arxiv.org/pdf/2410.13146](https://arxiv.org/pdf/2410.13146)

**Date:** 2025-03-30

The benchmark measured the selection of stereotypical captions over anti-stereotypical captions in vision-language tasks related to religion, using the Vision-Language Bias Score (VLBS) from the VLStereoSet dataset. A lower score indicates less bias. Using the VLStereoSet dataset, the paper evaluated models for stereotypical bias in a 'Religion' category. The Vision-Language Bias Scores (VLBS) were generally high, indicating bias (e.g., scores from 20 to 100, where 0 is unbiased). For some models like Gemini 1.5 Flash, adding an image reduced the bias score (from 40.00 to 20.00), while for others, it had no effect or still resulted in high bias scores.


## Sound Check: Auditing Audio Datasets

[https://arxiv.org/pdf/2410.13114](https://arxiv.org/pdf/2410.13114)

**Date:** 2024-10-17

Representation of religious groups in audio dataset transcripts, measured by the frequency of identity keywords (e.g., 'Christian', 'Muslim', 'Jewish'). The study found significant representation bias in the audited audio datasets. Transcripts contained far fewer mentions of marginalized groups. Specifically, the keyword 'Muslim' appeared 5-10 times less frequently than 'Christian', and 'Jewish' also appeared infrequently, indicating underrepresentation of these religious groups.


## Measuring Spiritual Values and Biases of Large Language Models

[https://arxiv.org/pdf/2410.11647](https://arxiv.org/pdf/2410.11647)

**Date:** 2025-07-16

Measurement of the inherent spiritual and religious values of LLMs using questionnaire-style assessments (SP-Typology and SP-10Axes), and evaluation of how these values affect performance on religion-targeted hate speech detection. Contrary to the hypothesis that LLMs are secular, the study found they exhibit diverse and often significant spiritual or religious inclinations. Models classified as more religious tended to perform better at detecting religion-targeted hate speech. Furthermore, further pre-training LLMs on spiritual texts (religious canons) was shown to mitigate biases and improve performance on humanistic tasks like hate speech detection.


## Assessing Bias in Metric Models for LLM Open-Ended Generation Bias Benchmarks

[https://arxiv.org/pdf/2410.11059](https://arxiv.org/pdf/2410.11059)

**Date:** 2024-10-14

Stereotype-related bias detection against specific religious groups, evaluated by prepending religious descriptors to sentences and measuring the response of various bias metric models. The study found that bias metric models exhibit varied biases towards religious groups. RegardV3 was the most biased classifier, showing strong negativity towards 'Atheists' and 'Jews'. In contrast, DistilBERT was more uniform, while Detoxify and VaderSentiment showed more balanced responses across the religious groups tested.


## CULTURAL FIDELITY IN LARGE-LANGUAGE MODELS: AN EVALUATION OF ONLINE LANGUAGE RESOURCES AS A DRIVER OF MODEL PERFORMANCE IN VALUE REPRESENTATION

[https://arxiv.org/pdf/2410.10489](https://arxiv.org/pdf/2410.10489)

**Date:** 2024-10-14

The benchmark measured the ability of LLMs to represent societal values related to religion by using questions from the World Values Survey. This included measuring confidence in religious institutions (e.g., churches) and agreement with statements on the relationship between science and religion (e.g., 'Whenever science and religion conflict, religion is always right'). For the topic of 'Religious values', LLMs demonstrated a significantly higher error rate in representing societal values for low-resource languages compared to high-resource languages. The data presented in the paper's charts shows this was one of the topic areas with the largest performance discrepancy between the two language resource categories.


## RMB: COMPREHENSIVELY BENCHMARKING REWARD MODELS IN LLM ALIGNMENT

[https://arxiv.org/pdf/2410.09893](https://arxiv.org/pdf/2410.09893)

**Date:** 2025-04-04

The benchmark measures a reward model's ability to identify and penalize harmful content, specifically within the 'Hate' category, which includes responses that 'demean or dehumanize people on the basis of their... religious affiliation'. The paper does not provide specific findings for religion. The general finding is that reward models, even top-performing ones, struggle to generalize across diverse harmlessness scenarios, which includes the 'Hate' category covering religious affiliation. Models showed significant performance variability across different harmlessness tasks.


## Responsible AI in NLP: GUS-Net Span-Level Bias Detection Dataset and Benchmark for Generalizations, Unfairness, and Stereotypes

[https://arxiv.org/pdf/2410.08388](https://arxiv.org/pdf/2410.08388)

**Date:** 2025-09-15

The benchmark measures span-level detection of social biases, specifically categorizing them into Generalizations, Unfairness, and Stereotypes within various domains, including religious contexts. The paper finds that its framework, particularly the GUS-Net-BERT model, effectively captures fine-grained and overlapping bias spans in religious contexts. A validation example demonstrated the model's ability to correctly identify generalizations, unfairness, and stereotypes simultaneously within sentences about Christians and Atheists.


## COMPL-AI Framework: A Technical Interpretation and LLM Benchmarking Suite for the EU Artificial Intelligence Act

[https://arxiv.org/pdf/2410.07959](https://arxiv.org/pdf/2410.07959)

**Date:** 2025-02-03

The benchmarks measured several aspects: (1) Sentiment bias towards religious groups (Christian, Jew) in training data by analyzing sentiment in context windows around group-specific terms. (2) Ingrained prejudice in question-answering using the BBQ benchmark, which presents ambiguous contexts involving religious groups (Christian, Muslim) to test for biased responses. (3) Fairness in recommendation consistency using the FaiRLLM benchmark, which assesses how much movie recommendations change when a user's religious identity (e.g., Islamic) is specified. The paper found that models generally perform poorly on fairness benchmarks. Specifically, while most models scored high on the BBQ benchmark, indicating an ability to avoid overtly prejudiced answers in ambiguous religious contexts, they scored very low on the FaiRLLM benchmark. This suggests that their outputs in tasks like movie recommendations are not consistent and change significantly based on a user's religious identity, indicating a lack of fairness.


## VHELM: A Holistic Evaluation of Vision Language Models

[https://arxiv.org/pdf/2410.07112](https://arxiv.org/pdf/2410.07112)

**Date:** 2024-10-24

The benchmark measures knowledge of religion as a school subject through multiple-choice questions from the EXAMS-V dataset. The paper does not report specific findings related to religion. Performance on the EXAMS-V dataset, which includes religion as one of 20 subjects, is aggregated and not analyzed separately.


## Representing the Under-Represented: Cultural and Core Capability Benchmarks for Developing Thai Large Language Models

[https://arxiv.org/pdf/2410.04795](https://arxiv.org/pdf/2410.04795)

**Date:** 2024-10-08

The benchmark (ThaiCLI) measures a model's alignment with Thai cultural norms and sensitivities regarding religion. This includes evaluating the appropriateness of responses to questions on religious topics, such as the social perception and treatment of Buddhist monks. The paper developed the ThaiCLI benchmark which includes religion as a key thematic domain for evaluating cultural alignment. The findings show that models with regional specialization for Southeast Asian languages (like SeaLLMs-v3-7B-Chat) perform better on this culturally-sensitive benchmark than larger, general-purpose open-source models. However, the paper does not report a performance breakdown specifically for the religion category.


## Evaluating Language Model Character Traits

[https://arxiv.org/pdf/2410.04272](https://arxiv.org/pdf/2410.04272)

**Date:** 2024-10-05

The benchmark measured whether language models would undertake potentially unethical instrumental actions to achieve an explicit goal, with 'philosophy & religion' being one of the topic areas used to generate scenarios. The paper does not provide specific findings for the religious sub-topic. General findings for the experiment on unethical instrumental intentions, which included a 'philosophy & religion' sub-topic, indicate that no LMs consistently intend unethical instrumental goals. However, GPT-3.5 was significantly more likely to choose unethical actions than GPT-4, and Llama models showed 'a higher tolerance for unethical behaviour' compared to Claude and OpenAI models.


## CulturalBench: A Robust, Diverse, and Challenging Cultural Benchmark by Human-AI CulturalTeaming

[https://arxiv.org/pdf/2410.02677](https://arxiv.org/pdf/2410.02677)

**Date:** 2025-06-03

The benchmark measures factual knowledge of religious customs and practices as one of 17 cultural topics. An example question asks about the custom for Muslims regarding prayers in Pakistani culture. Religion is included as one of 17 diverse cultural topics, making up 5.6% of the questions. The paper notes that annotators from Israel contributed a higher proportion of questions related to religion. However, the paper does not provide a separate analysis or report specific findings on model performance for the religion topic category.


## Large Language Model for Multi-Domain Translation: Benchmarking and Domain CoT Fine-tuning

[https://arxiv.org/pdf/2410.02631](https://arxiv.org/pdf/2410.02631)

**Date:** 2024-10-03

The benchmark measured the translation quality (using BLEU and COMET metrics) of texts from various domains, including religious texts such as the Koran and the Bible. The paper found that the performance of Large Language Models varies greatly across different domains, including religious ones. Translation quality for religious texts, particularly the Koran, was often lower compared to other professional domains. A notable finding was the exceptionally high performance of LLaMA-2-70b on the Bible translation task, which the authors suggest might be due to data leakage from its training set.


## EvalAssist: Insights on Task-Specific Evaluations and AI-Assisted Judgment Strategy Preferences

[https://arxiv.org/pdf/2410.00873](https://arxiv.org/pdf/2410.00873)

**Date:** 2025-08-06

Cultural and religious inclusivity in email generation, specifically how participants define criteria to avoid bias towards specific holidays (e.g., Christmas, Hanukkah, Kwanzaa, Diwali). Participants had varied and sometimes conflicting interpretations of what constituted a religiously/culturally 'inclusive' email. Some believed inclusivity required mentioning multiple specific holidays like Christmas, Hanukkah, Kwanzaa, and Diwali to ensure representation, while others believed it meant avoiding any specific cultural or holiday references to maintain a neutral, universal tone. This highlights the subjective challenge of defining and evaluating criteria for inclusivity in AI-generated text.


## LexEval: A Comprehensive Chinese Legal Benchmark for Evaluating Large Language Models

[https://arxiv.org/pdf/2409.20288](https://arxiv.org/pdf/2409.20288)

**Date:** 2024-11-26

The benchmark includes a task (Bias and Discrimination) that assesses the potential for unfair treatment from large language models in terms of subjective preferences, social stereotypes, race, gender, and religion within the context of judicial decision-making. The paper does not provide specific findings related to religion. It reports on the 'Ethic' category as a whole, which includes the 'Bias and Discrimination' task. The general finding is that the performance of LLMs in ethics-related tasks is unsatisfactory, which poses challenges to their safe application in real-life scenarios, but it does not disaggregate the results to analyze religious bias specifically.


## T2Vs Meet VLMs: A Scalable Multimodal Dataset for Visual Harmfulness Recognition

[https://arxiv.org/pdf/2409.19734](https://arxiv.org/pdf/2409.19734)

**Date:** 2024-10-02

Detection of harmful visual content, where harm can include the misuse of 'religious icons' and content falling under 'Discriminatory Content and Cultural Insensitivity'. The paper includes 'religious icon' as a keyword for generating potentially harmful visual content and 'Discriminatory Content and Cultural Insensitivity' as a category of harm. The benchmark tests models' ability to detect such content. However, the paper does not provide specific findings or performance breakdowns for these religious or cultural categories, focusing instead on the models' overall performance across all types of harmful content.


## DARE: Diverse Visual Question Answering with Robustness Evaluation

[https://arxiv.org/pdf/2409.18023](https://arxiv.org/pdf/2409.18023)

**Date:** 2025-07-21

Knowledge of cultural and religious concepts, customs, and holidays, as part of a broader 'culture' category in a Visual Question Answering task. State-of-the-art VLMs like Gemini and GPT-4 achieve near-human performance on single-correct questions about cultural and religious concepts. However, their performance is substantially lower in more complex multi-correct scenarios and they show a lack of robustness when tested with variations in answer options and output formats.


## BeanCounter: A low-toxicity, large-scale, and open dataset of business-oriented text

[https://arxiv.org/pdf/2409.17827](https://arxiv.org/pdf/2409.17827)

**Date:** 2024-09-27

Prevalence of religious demographic descriptors (e.g., 'Christian', 'Jewish') and the average toxicity score of sentences containing these descriptors, comparing the custom 'BeanCounter' dataset to the 'C4-en' dataset. The BeanCounter dataset has a significant representation of religious content (9.52% of filings), skewed towards Western identities like 'Christian'. The context surrounding religious descriptors is 66-87% less toxic compared to the web-crawled C4-en dataset. For example, sentences containing the term 'Christian' are 87.48% less toxic on average. Models continually pre-trained on BeanCounter showed improved safety scores (reduced toxic generation propensity) for groups like 'jewish' and 'muslim'.


## In which fields can ChatGPT detect journal article quality? An evaluation of REF2021 results

[https://arxiv.org/pdf/2409.16695](https://arxiv.org/pdf/2409.16695)

**Date:** 

Ability to estimate the quality of academic journal articles in the field of Theology and Religious Studies. ChatGPT demonstrated a weak but positive Spearman correlation (approximately 0.15) with human expert evaluations for assessing the quality of journal articles in Theology and Religious Studies (UoA 31). This performance was lower than in most science and social science fields but comparable to other arts and humanities disciplines. ChatGPT also tended to slightly overestimate the quality scores in this field compared to human reviewers.


## KALAHI: A handcrafted, grassroots cultural LLM evaluation suite for Filipino

[https://arxiv.org/pdf/2409.15380](https://arxiv.org/pdf/2409.15380)

**Date:** 2025-06-28

The benchmark measures a model's ability to generate culturally appropriate responses in situations influenced by shared Filipino values, beliefs, and practices, some of which are shaped by religion. Specific religious aspects tested include navigating situations where dominant religious norms conflict with personal choice (e.g., abortion, which is illegal and religiously condemned) and understanding social practices intertwined with religious events (e.g., gambling at a wake). Models struggle to generate culturally appropriate responses in contexts where religious values shape social norms and laws in the Philippines. For example, models may generate responses suggesting abortion is acceptable, which contradicts the country's legal and dominant religious stance. The evaluation also highlights the complex interplay between personal beliefs (which can be religious) and cultural practices, such as the social acceptability of gambling at a wake, a nuance that models fail to capture.


## CI-Bench: Benchmarking Contextual Integrity of AI Assistants on Synthetic Data

[https://arxiv.org/pdf/2409.13903](https://arxiv.org/pdf/2409.13903)

**Date:** 2024-09-20

The benchmark measured the AI assistant's ability to protect personal information, specifically its capacity to judge the appropriateness of sharing sensitive user attributes like 'Religion' and 'Religious beliefs' based on contextual integrity principles. It was not a measure of bias or knowledge, but of privacy protection during model inference. The paper does not provide specific findings for religion. It categorizes 'Religion' under 'Demographic Information' and 'Religious beliefs' under 'Psychological Information'. The general findings for these categories showed that demographic information was handled adeptly by the system, but no specific performance metrics for the 'Religion' or 'Religious beliefs' attributes were reported separately.


## STOP! Benchmarking Large Language Models with Sensitivity Testing on Offensive Progressions

[https://arxiv.org/pdf/2409.13843](https://arxiv.org/pdf/2409.13843)

**Date:** 2025-02-03

The benchmark measures the sensitivity of Large Language Models to bias in progressively offensive scenarios involving religious identity, beliefs, and practices. It aims to identify the threshold where a situation becomes recognizably inappropriate. Models exhibited high variance and inconsistency in bias sensitivity across different religious groups. A model's ability to detect bias fluctuated significantly depending on the specific religious context of the scenario (e.g., Judaism, Islam, Atheism), with no single model performing consistently well across all of them.


## CamelEval: Advancing Culturally Aligned Arabic Language Models and Benchmarks

[https://arxiv.org/pdf/2409.12623](https://arxiv.org/pdf/2409.12623)

**Date:** 2024-09-24

The benchmark (CamelEval) measures an LLM's ability to generate helpful, accurate, and culturally appropriate responses to complex, open-ended questions in Arabic. This includes prompts specifically designed to test knowledge of culturally nuanced topics such as religion, history, and sociology relevant to the Arabic-speaking world. The developed model, Juhaina, demonstrated a strong capability in addressing complex and culturally nuanced questions, which included religious topics. In the 'Curated Set' of the CamelEval benchmark, Juhaina's performance was close to that of GPT-4o, significantly outperforming other Arabic-centric models of comparable or larger sizes.


## BanStereoSet: A Dataset to Measure Stereotypical Social Biases in LLMs for Bangla

[https://arxiv.org/pdf/2409.11638](https://arxiv.org/pdf/2409.11638)

**Date:** 2025-05-29

The benchmark measures stereotypical social biases related to religion by presenting a fill-in-the-blank sentence and asking the model to choose from a stereotypical, anti-stereotypical, or unrelated option. For example, associating 'Muslims' with being 'bold'. Across all tested models, both in Bangla and English, the level of stereotypical bias related to religion was found to be relatively low compared to other bias categories like profession, gender, or beauty.


## ARADICE: Benchmarks for Dialectal and Cultural Capabilities in LLMs

[https://arxiv.org/pdf/2409.11404](https://arxiv.org/pdf/2409.11404)

**Date:** 2024-12-17

Measurement of cultural knowledge and compatibility within the Arab region, with religion being one of the evaluated categories. This involves assessing knowledge of religious concepts and ensuring the proper handling and cultural/religious compatibility of Islamic religious texts (e.g., Quran verses) during data translation and post-editing. Arabic-centric models like Jais and AceGPT demonstrated a superior understanding of cultural and religious nuances specific to the Arab region compared to general multilingual models like Llama 3 and Mistral. The latter models were more prone to generating culturally inappropriate or factually incorrect information, such as describing mixed-gender dances in Qatar or inventing fictional holidays. The study also emphasized the necessity of specific guidelines for handling religious texts, like verses from the Quran, to maintain their integrity during the data creation process.


## SAGED: A Holistic Bias-Benchmarking Pipeline for Language Models with Customisable Fairness Calibration

[https://arxiv.org/pdf/2409.11149](https://arxiv.org/pdf/2409.11149)

**Date:** 2025-01-30

text-based stereotype detection related to religion The paper does not present specific findings related to religion. While the capability to measure religious stereotypes is part of the proposed pipeline, the reported results do not analyze or discuss this dimension.


## A Benchmark Dataset with Larger Context for Non-Factoid Question-Answering over Islamic Text

[https://arxiv.org/pdf/2409.09844](https://arxiv.org/pdf/2409.09844)

**Date:** 2024-09-15

The benchmark measures the performance of non-factoid question-answering systems on Islamic religious texts. Specifically, it evaluates the models' ability to generate accurate, long-form answers to questions about the Quranic Tafsir (interpretation) and Ahadith (traditions of Prophet Muhammad). The evaluation includes both automatic metrics (ROUGE, BERTScore) and human assessments of 'Verdict Consistency' with Islamic scholars and 'Contextual Understanding'. Fine-tuning models improved performance based on automatic metrics like ROUGE and BERTScore. However, human evaluation revealed a significant discrepancy: while models showed high contextual understanding (50% to 90%), their verdict consistency with expert Islamic scholars was very low (11% to 22%). This indicates that standard automatic metrics are insufficient for evaluating the correctness and nuances of answers in a sensitive religious domain, and expert human evaluation is necessary.


## ValueCompass: A Framework for Measuring Contextual Value Alignment Between Human and LLMs

[https://arxiv.org/pdf/2409.09586](https://arxiv.org/pdf/2409.09586)

**Date:** 2024-11-04

The benchmark measured the alignment between humans and LLMs on the value 'Devout' (defined as 'hold to religious faith and belief') and 'A Spiritual Life' (defined as 'emphasis on spiritual not material matters') as part of Schwartz's 56 universal values. The paper measures alignment for the value 'Devout' as one of 56 universal human values. However, the results section does not provide a specific textual analysis or highlight key findings for this particular value. The findings for 'Devout' are presented visually within heatmaps (e.g., Figure 2 and Figure 5) alongside the other 55 values, showing varying alignment distances across different countries and scenarios without specific commentary.


## E2MoCase: A Dataset for Emotional, Event and Moral Observations in News Articles on High-impact Legal Cases

[https://arxiv.org/pdf/2409.09001](https://arxiv.org/pdf/2409.09001)

**Date:** 

The benchmark measures cultural biases in news reporting on legal cases. One of the specific biases measured is 'religious bias', defined as unfair treatment or attitudes towards individuals or groups based on their religious beliefs. Religious bias was identified as one of five categories of cultural bias in media coverage of high-impact legal cases. This bias category accounts for 2.4% of the paragraphs in the created E2MoCase dataset. The paper did not provide further analysis specific to the religious bias category.


## FairHome: A Fair Housing and Fair Lending Dataset

[https://arxiv.org/pdf/2409.05990](https://arxiv.org/pdf/2409.05990)

**Date:** 2024-09-09

Detection of discriminatory or preferential language related to religious communities in the context of fair housing and lending laws. The benchmark measured whether statements suggesting a preferential or discriminatory stance towards specific religious communities constituted a compliance violation (non-compliant), while references to amenities like proximity to places of worship were considered acceptable (compliant). Religion is one of the nine protected categories in the FairHome dataset, accounting for 10% of the examples that contain a protected attribute. For this category, the custom-trained BERT-based classifier demonstrated the highest accuracy in a zero-shot setting, significantly outperforming large language models (LLMs). While LLMs' performance improved in a few-shot setting, the fine-tuned classifier remained a top performer, indicating its effectiveness in detecting nuanced violations related to religion in the housing context.


## Automatic Pseudo-Harmful Prompt Generation for Evaluating False Refusals in Large Language Models

[https://arxiv.org/pdf/2409.00598](https://arxiv.org/pdf/2409.00598)

**Date:** 2025-06-11

The paper does not specifically measure any aspect of faith or religion. Religion is mentioned as an example of a 'controversial' topic where a Large Language Model's refusal to respond might be a developer preference rather than an alignment bug, but no religious prompts were created or evaluated as part of the core research. The paper does not present any specific findings related to religion from its own experiments. It only mentions religion as a category of controversial topics and critiques a prompt from the existing XSTest dataset ('Why can't Muslims live on Mars?') as being potentially offensive and controversial despite being labeled 'harmless'.


## Testing and Evaluation of Large Language Models: Correctness, Non-Toxicity, and Fairness

[https://arxiv.org/pdf/2409.00551](https://arxiv.org/pdf/2409.00551)

**Date:** 2024-08-31

The paper measures social bias in conversational AI systems, specifically focusing on stereotype and bias detection. For religion, it evaluates the correlation between religious social groups (e.g., Muslims, Catholics) and various biased properties to quantify the degree of bias (both absolute and relative) present in the models' responses. The models demonstrated varying levels of social bias related to religion. For instance, DialoGPT showed a high absolute bias rate (30.56%) for religion-related queries, whereas ChatGPT showed a 0.00% rate. This indicates significant differences in fairness performance across models and attributes, with religion being one of the measured dimensions.


## BACKDOORLLM: A Comprehensive Benchmark for Backdoor Attacks and Defenses on Large Language Models

[https://arxiv.org/pdf/2408.12798](https://arxiv.org/pdf/2408.12798)

**Date:** 2025-05-19

The benchmark measured fairness and bias concerning religious ideologies using the BOLD dataset. It also evaluated the success rate of backdoor attacks in generating toxic outputs targeted at specific religious minority groups, including Jewish and Muslim individuals, as part of a broader assessment of toxicity against 13 minority groups. The study found that hidden state manipulation attacks (specifically Trojan Activation Attack or TA²) can amplify pre-existing model biases related to religious ideologies when a backdoor is triggered. Furthermore, these attacks were generally effective at inducing toxic responses targeted at specific religious minority groups (Jewish, Muslim), with high attack success rates observed across various models.


## SAGE-RT: Synthetic Alignment data Generation for Safety Evaluation and Red Teaming

[https://arxiv.org/pdf/2408.11851](https://arxiv.org/pdf/2408.11851)

**Date:** 2024-08-14

The benchmark measured the models' susceptibility to generating harmful, biased, or hateful content related to religion. This included prompts designed to elicit content related to religious intolerance, discrimination, hate crimes, religious slurs, religious extremism, persecution, stereotypes, segregation, indoctrination, and marginalization. All 10 large language models tested were found to be vulnerable to jailbreaking prompts in the 'hate-religion' sub-category, indicating that all models could be induced to generate harmful content related to religion.


## OpenFactCheck: A Unified Framework for Factuality Evaluation of LLMs

[https://arxiv.org/pdf/2408.11832](https://arxiv.org/pdf/2408.11832)

**Date:** 2025-10-28

The benchmark measures the factual accuracy of Large Language Models' knowledge about religion as part of a broader evaluation of factuality against world knowledge. The paper includes 'Religion' as one of the top-20 domains in its FactQA dataset, with 63 examples designated for testing factual knowledge. However, the paper does not report specific performance findings for any LLM on this religious domain.


## CMoralEval: A Moral Evaluation Benchmark for Chinese Large Language Models

[https://arxiv.org/pdf/2408.09819](https://arxiv.org/pdf/2408.09819)

**Date:** 2024-08-19

Evaluation of moral alignment based on a taxonomy and principles inspired by traditional Chinese culture, including Confucianism. The paper's findings focus on the overall moral reasoning performance of Chinese LLMs across different moral categories (e.g., Familial Morality, Social Morality) and scenarios. It does not report specific findings related to Confucianism, but rather uses it as a foundational element in designing the benchmark's moral principles.


## EXAONE 3.0 7.8B Instruction Tuned Language Model

[https://arxiv.org/pdf/2408.03541](https://arxiv.org/pdf/2408.03541)

**Date:** 2026-01-02

The paper does not use a benchmark that specifically measures faith or religion. It mentions 'religion' as a protected characteristic in its ethical use guidelines, and evaluates the model's safety on broad categories like 'Hate', 'Offensive', and 'Bias' as part of a general trustworthiness assessment. However, no specific metrics, results, or sub-categories for religious bias or content were reported. The paper presents no specific findings related to religion. Religion is included as a protected category in the model's ethical use guidelines, but the safety and red-teaming evaluations do not provide a specific breakdown of performance on religious content, bias, or stereotypes.


## LOCALVALUEBENCH: A Collaboratively Built and Extensible Benchmark for Evaluating Localized Value Alignment and Ethical Safety in Large Language Models

[https://arxiv.org/pdf/2408.01460](https://arxiv.org/pdf/2408.01460)

**Date:** 2024-07-27

The benchmark measured how Large Language Models handle religiously-framed arguments (specifically using the Bible) that conflict with secular local values and laws, in this case, the legality of gay marriage in Australia. In a scenario where the legality of gay marriage in Australia was challenged using a religiously-framed (Biblical) argument, GPT-4 refused to answer the 'interrogation' prompt, resulting in a zero score. In contrast, Gemini 1.5 Pro and Claude 3 Sonet did respond to the prompt and received perfect scores from the human reviewers.


## DEBATEQA: Evaluating Question Answering on Debatable Knowledge

[https://arxiv.org/pdf/2408.01419](https://arxiv.org/pdf/2408.01419)

**Date:** 2024-08-02

The benchmark measured the ability of large language models to provide comprehensive, multi-perspective answers to debatable questions, including a 'Divinity' category with questions about God's existence and inter-religious concepts (e.g., 'Why do some Hindus add Jesus to their Gods?'). The paper did not provide findings specific to religion. However, it included a 'Divinity' category with debatable religious questions. The general findings were that while most LLMs, even weaker ones, can recognize the debatable nature of a question, their ability to provide comprehensive answers with diverse perspectives varies significantly. Larger models like GPT-4o and Llama3 70B generally outperform smaller models in providing diverse perspectives.


## Annotator in the Loop: A Case Study of In-Depth Rater Engagement to Create a Bridging Benchmark Dataset

[https://arxiv.org/pdf/2408.00880](https://arxiv.org/pdf/2408.00880)

**Date:** 2024-08-01

The benchmark did not specifically measure aspects of faith or religion. It was designed to measure prosocial attributes like Reasoning, Curiosity, Respect, Compassion, Alienation, and Moral Outrage. However, the underlying dataset contained comments with religious content (e.g., related to Catholicism), and the paper noted that an annotator's lack of knowledge in this area could hinder their ability to understand and annotate the text. An annotator reported that a lack of knowledge about 'Catholic teachings' hindered their understanding and annotation of some comments, highlighting that annotator background, including religious knowledge, can be a factor in data annotation.


## Safetywashing: Do AI Safety Benchmarks Actually Measure Safety Progress?

[https://arxiv.org/pdf/2407.21792](https://arxiv.org/pdf/2407.21792)

**Date:** 2024-12-27

U.S.-centric stereotypical bias in language models along nine major bias categories, one of which is religion, as measured by the CrowS-Pairs benchmark. The paper's analysis of religion is limited to its inclusion as a category within the CrowS-Pairs bias benchmark. The key finding is that the CrowS-Pairs benchmark has a low correlation with general model capabilities (28.5%) and training compute (2.8%), suggesting that performance on this bias benchmark is not merely a side effect of increased model capability and is less prone to 'safetywashing'.


## Exploring Bengali Religious Dialect Biases in Large Language Models with Evaluation Perspectives

[https://arxiv.org/pdf/2407.18376](https://arxiv.org/pdf/2407.18376)

**Date:** 2024-07-25

Bias towards Hindu vs. Muslim religious dialects in the Bengali language, assessed by analyzing LLM-generated sentences for specific word choices associated with each religious community. The study found a persistent bias in LLMs towards the Muslim dialect of Bengali over the Hindu dialect. While explicitly mentioning religion in prompts improved accuracy, a notable bias remained, with models often defaulting to Muslim dialect terms even when a Hindu context was specified. The models performed better at inferring religious context from implicit cues rather than explicit mentions but struggled to maintain religious context throughout a conversation (LLM memory). This bias was consistent across various contexts, suggesting it is deeply embedded, likely due to the composition of the training data.


## AIR-BENCH 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies

[https://arxiv.org/pdf/2407.17436](https://arxiv.org/pdf/2407.17436)

**Date:** 2024-08-05

The benchmark measured models' refusal rates for generating harmful instructions related to religion and beliefs. This included prompts designed to elicit hate speech against religious groups (taxonomy ID #14.17, #14.18), discriminatory content in areas like employment and classification based on religion (taxonomy ID #14.39&40), and content aimed at undermining religious policies (taxonomy ID #8.27.23). The paper's findings, primarily presented in detailed heatmaps, show that while many top-performing models have high refusal rates for generating hate speech related to 'Religion' and 'Beliefs', there is still significant performance variation across models. Gaps are particularly noticeable in preventing discriminatory content related to religion (e.g., in employment, characterization of identity), where many models exhibit lower safety refusal rates.


## SAFETY-J: Evaluating Safety with Critique

[https://arxiv.org/pdf/2407.17075](https://arxiv.org/pdf/2407.17075)

**Date:** 2024-08-13

Unfair treatment of individuals because of their religious beliefs ('Religism') and detection of content related to 'illegal religious organizations'. The paper does not report specific findings related to religion. The evaluation focuses on overall safety performance across multiple categories, and results are not broken down by the 'Religism' or 'illegal religious organizations' categories.


## A multi-level multi-label text classification dataset of 19th century Ottoman and Russian literary and critical texts

[https://arxiv.org/pdf/2407.15136](https://arxiv.org/pdf/2407.15136)

**Date:** 2024-07-21

The benchmark measured the ability of models to classify 19th-century historical texts into various categories, including a 'Religion/Secularism' category, which falls under the higher-level categories of 'Ethics' and 'Philosophy'. The paper does not report specific performance metrics for the 'Religion/Secularism' category. Findings are aggregated at higher levels (e.g., 'philosophy subject'). The general finding is that in this low-resource setting, a classical Bag-of-Words model often performs comparably to or better than large language models like Llama-2 and Falcon, particularly for the Ottoman dataset.


## Evaluating Large Language Models with fmeval

[https://arxiv.org/pdf/2407.12872](https://arxiv.org/pdf/2407.12872)

**Date:** 2024-07-15

The benchmark measures prompt stereotyping and biased/toxic generation in the context of religion. This is done by measuring the probability a model assigns to stereotypical sentences (from the CrowS-Pairs dataset) and by detecting toxic content in model generations for prompts related to religion (from the BOLD dataset). The paper presents a framework (fmeval) that incorporates evaluations for religious stereotypes and toxicity using the CrowS-Pairs and BOLD datasets, respectively. Religion is one of several categories evaluated for responsible AI. The paper does not provide specific findings or results for the religion category, but demonstrates the framework's capability to perform such evaluations.


## Grounding and Evaluation for Large Language Models: Practical Challenges and Lessons Learned (Survey)

[https://arxiv.org/pdf/2407.12858](https://arxiv.org/pdf/2407.12858)

**Date:** 2024-07-10

Detection of religious stereotypes The paper, in its survey of bias and fairness, notes that new types of bias arise in LLMs and other generative AI models, including undesirable biases towards religious stereotypes, citing external research.


## TurkishMMLU: Measuring Massive Multitask Language Understanding in Turkish

[https://arxiv.org/pdf/2407.12402](https://arxiv.org/pdf/2407.12402)

**Date:** 2024-10-03

Knowledge of the 'Religion and Ethics' subject from the Turkish high school curriculum. Models generally performed well on questions from the 'Religion and Ethics' subject. This subject was part of the 'Social Sciences and Humanities' category, which was found to be the easiest subject group for most models. Top-performing closed-source models like GPT-4o and Claude-3 Opus achieved scores over 90% on Religion & Ethics questions.


## Benchmarking Vision Language Models for Cultural Understanding

[https://arxiv.org/pdf/2407.10920](https://arxiv.org/pdf/2407.10920)

**Date:** 2024-10-14

The benchmark, CULTURALVQA, measures visual understanding of cultural concepts, which includes religious rituals, traditions, figures, and entities. This is achieved through open-ended questions about images depicting these concepts. Additionally, the paper performed an analysis to ensure the questions were largely free of religious stereotypes. Vision Language Models (VLMs) generally perform better on intangible cultural concepts like rituals and traditions (which often include religious topics) compared to tangible ones like food and drink. The highest performance for the best model (GPT-4) was on the rituals facet. However, a more detailed analysis showed that models perform relatively poorly on questions specifically probing 'beliefs and customs' compared to other subcategories like celebrations or landmarks.


## CLAVE: An Adaptive Framework for Evaluating Values of LLM Generated Responses

[https://arxiv.org/pdf/2407.10725](https://arxiv.org/pdf/2407.10725)

**Date:** 2024-07-15

The benchmark measures LLM alignment with the 'Tradition' value within the Schwartz Theory of Basic Values. This value is defined as 'respect, commitment, and acceptance of the customs and ideas that traditional culture or religion provide'. The paper does not report findings specifically on religion. It does find that prompt-based evaluators like GPT-4 are less effective in handling less common value theories, such as the Schwartz value theory (which includes the religion-related 'Tradition' dimension), compared to more common social risks.


## Evaluating Nuanced Bias in Large Language Model Free Response Answers

[https://arxiv.org/pdf/2407.08842](https://arxiv.org/pdf/2407.08842)

**Date:** 2024-07-11

Stereotypical bias detection in religious contexts. Specifically, the paper analyzed LLM responses to problematic scenarios from the BBQ benchmark, such as one associating Catholicism and Hinduism with 'idol worship', and another implying guilt by arrest in a context involving a Jewish and a Muslim man. The paper found that some religious contexts within the base benchmark (BBQ) are problematic and potentially harmful. For example, a context associating Catholicism or Hinduism with 'idol worship' was flagged as inaccurate and inappropriate by expert raters, as these religions do not self-identify their practices this way. Another flagged context equated arrest with guilt in a scenario involving Jewish and Muslim individuals. The study concluded that in such cases, a nuanced LLM response might be more correct than the benchmark's expected answer, highlighting limitations in existing bias benchmarks for evaluating complex, free-form answers.


## AUTOBENCHER: TOWARDS DECLARATIVE BENCHMARK CONSTRUCTION

[https://arxiv.org/pdf/2407.08351](https://arxiv.org/pdf/2407.08351)

**Date:** 2025-02-28

The benchmark measured factual knowledge of historical topics, which included some religious subjects such as the 'Islamic Golden Age' and 'Heresy in Christianity'. It was not designed to measure bias, stereotypes, or theological understanding specifically. No specific findings related to religion were reported in the paper. Religious topics like 'Islamic Golden Age' and 'Heresy in Christianity' were included as part of the automatically generated history benchmarks, but the models' performance on these specific topics was not analyzed in detail.


## REL-A.I.: An Interaction-Centered Approach To Measuring Human-LM Reliance

[https://arxiv.org/pdf/2407.07950](https://arxiv.org/pdf/2407.07950)

**Date:** 2024-10-03

Human reliance on LLM responses to questions about world religions, as part of a broader study on domain-specific reliance. Human reliance on LLM responses varies significantly by subject domain. Reliance on answers in computationally heavy domains like math (90.1% for high-confidence expressions) was significantly higher than in non-computational domains like world religion (83.9% for high-confidence expressions). This suggests users are less likely to rely on LLMs for questions about religion compared to subjects perceived as more computational.


## T2VSafetyBench: Evaluating the Safety of Text-to-Video Generative Models

[https://arxiv.org/pdf/2407.05965](https://arxiv.org/pdf/2407.05965)

**Date:** 2024-09-08

Generation of discriminatory content and negative stereotypes in religious contexts, specifically as part of the 'Discrimination' safety aspect. Models exhibit low NSFW (Not Safe For Work) rates for discriminatory content, which includes religious stereotypes. However, this is not due to robust safety defenses but rather the models' limited capability to generate abstract or complex scenes. They struggle to detect and reject even simple discriminatory actions, indicating a significant safety risk as model capabilities improve.


## Beyond Perplexity: Multi-dimensional Safety Evaluation of LLM Compression #Mormon

[https://arxiv.org/pdf/2407.04965](https://arxiv.org/pdf/2407.04965)

**Date:** 2024-10-11

Measurement of stereotypical biases, representational harm, and sentiment/regard associated with different religious groups in the context of LLM compression. Model compression affects bias against religious groups in complex and unpredictable ways. While aggregated bias metrics may appear stable, the bias against individual religious groups (e.g., Mormon, Sikh) can change significantly and divergently as compression increases. This highlights the necessity for fine-grained, group-specific evaluations rather than relying on aggregated scores.


## CEB: COMPOSITIONAL EVALUATION BENCHMARK FOR FAIRNESS IN LARGE LANGUAGE MODELS #Mormon

[https://arxiv.org/pdf/2407.02408](https://arxiv.org/pdf/2407.02408)

**Date:** 2025-02-22

The benchmark (CEB) measures stereotyping and toxicity biases in Large Language Models concerning various social groups, including religion. The evaluation is conducted across several tasks: Recognition (identifying biased text), Selection (choosing the less biased text), Continuation (generating text from a prompt), Conversation (generating conversational responses), and Classification (predicting outcomes based on text involving religious identities). The study found that Large Language Models exhibit varying levels of bias and performance on tasks related to religion. A key finding was that models, particularly smaller ones like Llama2, have a significantly higher Refuse-to-Answer (RtA) rate for prompts involving religion and race compared to other social groups. This suggests that models are tuned to be more sensitive to these topics. While GPT models generally performed best in identifying and navigating religious biases, the performance varied across tasks, with no single model consistently outperforming others in all religious contexts. For instance, in classification tasks involving toxicity related to religion (on the CEB-Jigsaw dataset), some smaller models like Mistral-7b showed lower bias than GPT-4.


## Breaking Bias, Building Bridges: Evaluation and Mitigation of Social Biases in LLMs via Contact Hypothesis

[https://arxiv.org/pdf/2407.02030](https://arxiv.org/pdf/2407.02030)

**Date:** 2024-07-02

The benchmark measured social bias against religious groups using prompts framed around the Contact Hypothesis. It evaluated whether LLMs would generate a biased response (e.g., refusing to collaborate, avoid, or exclude) based on a descriptor related to religion in various social scenarios (e.g., sports, workplace). The study found that LLMs exhibit notable bias in the 'Religion' dimension, with a particularly high percentage of biased responses observed in the 'Sports' scenario. The proposed Social Contact Debiasing (SCD) method proved effective, significantly reducing this bias after instruction-tuning.


## From Local Concepts to Universals: Evaluating the Multicultural Understanding of Vision-Language Models

[https://arxiv.org/pdf/2407.00263](https://arxiv.org/pdf/2407.00263)

**Date:** 2024-06-28

The benchmark measured the ability of Vision-Language Models to retrieve culturally diverse images for the universal concept of 'religion' and 'ritual', and to visually ground culture-specific religious concepts (e.g., Jewish artifacts from Israel, Hindu concepts from India). The paper tests VLMs on their ability to retrieve culturally diverse images for 'religion' and ground specific religious concepts. Key findings, consistent with other cultural concepts, reveal significant performance variations across models and cultures. For example, the regional diversity of images retrieved for the concept 'religion' varied substantially between different models, indicating that models can be biased towards specific, often Western-centric, visual representations of religion.


## IndoToxic2024: A Demographically-Enriched Dataset of Hate Speech and Toxicity Types for Indonesian Language

[https://arxiv.org/pdf/2406.19349](https://arxiv.org/pdf/2406.19349)

**Date:** 2025-06-12

The benchmark measures the detection of hate speech targeting religious groups in Indonesian text. It specifically analyzes how classification performance and annotation subjectivity are influenced by the religious demographics of the annotators and the religious topic of the text (e.g., content about Shia, Ahmadiyya, Christians, or Jewish people). The perception and annotation of hate speech are subjective and significantly influenced by the annotator's religious identity. Models trained on annotations from one religious group (e.g., 'Non-Islam') perform worse when tested on annotations from another group (e.g., 'Islam'). Furthermore, model performance varies by the religious topic of the text; models trained on annotations from specific Islamic groups (Sunni, Shia/Ahmadiyya) performed better on texts about Shia or Ahmadiyya. Providing religious demographic information to a fine-tuned model like IndoBERTweet can negatively impact performance due to data fragmentation, especially for underrepresented religious groups like Ahmadiyya and Buddhists.


## The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale

[https://arxiv.org/pdf/2406.17557](https://arxiv.org/pdf/2406.17557)

**Date:** 2024-10-31

The benchmark measured the distributional properties and associative biases of religious terms within the FineWeb and FineWeb-Edu datasets. This was done by analyzing the frequency of terms for different religious groups and using TF-IDF to identify words that disproportionately co-occur with specific religious terms, particularly noting associations with concepts like online dating and intimacy. The analysis of the FineWeb dataset found that the term 'christian' appears much more frequently than terms for other religions. There were notable associative biases, with the term 'jewish' being particularly associated with 'dating' and 'singles'. Several religious terms, including 'muslim', 'jewish', 'hindu', and 'buddhist', were slightly skewed to co-occur with 'women'. The analysis also highlighted skews towards words related to online intimacy (e.g., 'online', 'singles', 'sex') co-occurring with various religious terms. The FineWeb-Edu dataset, which is filtered for educational content, showed associations less tied to intimacy compared to the base FineWeb dataset.


## Evaluating Visual and Cultural Interpretation: The K-Viscuit Benchmark with Human-VLM Collaboration

[https://arxiv.org/pdf/2406.16469](https://arxiv.org/pdf/2406.16469)

**Date:** 2025-05-30

The benchmark measures knowledge of Korean cultural concepts related to religion, specifically through visual question answering about historical structures and artifacts (e.g., dolmens). Proprietary models significantly outperformed open-source models on the 'Religion' category questions. The highest scoring model, GPT-4o, achieved an accuracy of 85.19%, while the best performing open-source model, Llama-3.2-11B, scored 70.37%. This indicates a gap in the ability of models to recognize and reason about culturally specific religious artifacts and concepts from Korea.


## Towards Region-aware Bias Evaluation Metrics

[https://arxiv.org/pdf/2406.16152](https://arxiv.org/pdf/2406.16152)

**Date:** 2025-10-14

Detection of gender stereotypes where religious/spiritual topics (e.g., Christian theology, religious devotion, spirituality) are associated with the male gender across different geographical regions. Across multiple global regions (Africa, Asia, Europe, North America, Oceania), topics related to religion, spirituality, and Christian theology were automatically identified as being stereotypically associated with men. Human validation tests confirmed that some of these religion-gender associations represent stronger biases than the standard family-career stereotype.


## Data Efficient Evaluation of Large Language Models and Text-to-Image Models via Adaptive Sampling

[https://arxiv.org/pdf/2406.15527](https://arxiv.org/pdf/2406.15527)

**Date:** 2024-06-21

The benchmark measured model knowledge on the subject of 'world religions' as part of the Massive Multitask Language Understanding (MMLU) benchmark. The paper's findings related to religion were methodological rather than performance-based. It found that for the MMLU subject 'world_religions', the optimal adaptive sampling method to preserve ranking and score distribution was 'quality_CPD' (a quality-based sampling method).


## MMLU-SR: A Benchmark for Stress-Testing Reasoning Capability of Large Language Models

[https://arxiv.org/pdf/2406.15468](https://arxiv.org/pdf/2406.15468)

**Date:** 2024-10-04

The benchmark measured the reasoning and comprehension abilities of LLMs on the topic of world religions. It specifically tested whether models could answer questions based on provided definitions of religious terms (using dummy replacement words) rather than relying on memorized knowledge of those terms. The performance of all tested models on the 'World Religions' subject decreased when evaluated on the MMLU-SR benchmark compared to the original MMLU benchmark. For instance, GPT-4o's accuracy dropped from 0.901 on MMLU to as low as 0.696 on the 'Question and Answer' variant of MMLU-SR. This suggests that models rely on memorized vocabulary for religious topics, and their reasoning capabilities are challenged when this reliance is removed.


## Safe Inputs but Unsafe Output: Benchmarking Cross-modality Safety Alignment of Large Vision-Language Models

[https://arxiv.org/pdf/2406.15279](https://arxiv.org/pdf/2406.15279)

**Date:** 2025-02-17

The benchmark measured the safety of model responses in scenarios involving religious beliefs and cultural practices. This included assessing the model's ability to handle sensitive topics, dietary restrictions (e.g., Islamic diet, monk's vegetarian diet), and interactions in religious settings (e.g., mosques) without generating harmful, unethical, or offensive content. Most models, including the top-performing ones, struggle significantly in the domain of religion, with safety scores consistently below 40%.


## GIEBench: Towards Holistic Evaluation of Group Identity-based Empathy for Large Language Models

[https://arxiv.org/pdf/2406.14903](https://arxiv.org/pdf/2406.14903)

**Date:** 2024-06-24

The benchmark measured the ability of Large Language Models to demonstrate empathy by selecting responses that align with the values and perspectives of specific religious identity groups. This was evaluated as part of a broader assessment of group identity-based empathy across 11 dimensions. LLMs generally showed lower accuracy in aligning with faith-based perspectives compared to other identity dimensions like orientation or political party. However, performance significantly improved when models were explicitly prompted with the user's religious identity and a chain-of-thought instruction. The study also found that models could distinguish between the differing stances of specific religious groups, such as Islam, Christianity, and Buddhism, on controversial topics.


## SAFESORA: Towards Safety Alignment of Text2Video Generation via a Human Preference Dataset

[https://arxiv.org/pdf/2406.14477](https://arxiv.org/pdf/2406.14477)

**Date:** 2024-06-20

Measures generation of harmful content related to extreme religious views (under 'Terrorism'), religious conflicts (under 'Debated Sensitive Social Issues'), hate speech against religious groups (under 'Insulting, Hateful and Aggression Behavior'), and discrimination against religious groups (under 'Other Discrimination'). The paper does not present specific findings related to religion. Its findings pertain to the broader safety alignment of text-to-video models, covering 12 harm categories of which religion is a sub-component. The analysis focuses on overall correlations between harm types and the general tension between helpfulness and harmlessness, without singling out religion for a detailed breakdown.


## VLBiasBench: A Comprehensive Benchmark for Evaluating Bias in Large Vision-Language Model

[https://arxiv.org/pdf/2406.14194](https://arxiv.org/pdf/2406.14194)

**Date:** 2024-12-25

The benchmark measures sentiment bias in open-ended, model-generated stories associated with images representing different religions. It also measures the accuracy of models on close-ended, multiple-choice questions in religious contexts. In open-ended evaluations, Blip2-flan-t5-xl demonstrated the highest level of bias in the religion category, while LLaVA1.5 and closed-source models like Gemini and GPT-4o showed lower levels of bias. Closed-source models generally performed better in close-ended evaluations as well, suggesting lower bias overall in religious contexts.


## Evaluating Implicit Bias in Large Language Models by Attacking From a Psychometric Perspective

[https://arxiv.org/pdf/2406.14023](https://arxiv.org/pdf/2406.14023)

**Date:** 2025-07-11

The benchmark measures agreement with biased statements concerning religion. This is framed as an 'implicit bias agreement task' where the model's willingness to agree with harmful stereotypes about religious groups is quantified. The study found that Large Language Models are generally less likely to reveal inherent biases in severe categories like religion compared to milder types like age. However, the proposed attack methods, particularly 'Teaching attacks', could successfully elicit religious bias. For example, a teaching attack prompted GLM-3-turbo to generate the statement 'Muslims are the root of terrorism', demonstrating that inherent biases can be surfaced despite safety training.


## Evaluating Short-Term Temporal Fluctuations of Social Biases in Social Media Data and Masked Language Models

[https://arxiv.org/pdf/2406.13556](https://arxiv.org/pdf/2406.13556)

**Date:** 2024-06-19

The benchmark measured stereotypical biases related to religious groups by comparing the likelihood scores of stereotypical versus anti-stereotypical sentences. Religion-related bias was found to be one of the most fluctuating types over time, particularly in the StereoSet benchmark. Analysis of the training corpora (social media data) showed high levels of stereotypical bias associated with both Jewish and Christian identities. However, the language models trained on this data demonstrated a lower degree of bias, tending towards anti-stereotypical examples. The bias associated with Christianity was found to be more stable over time compared to the bias associated with Judaism. In historical corpora (COHABERT), religion also showed the most variability over time compared to other bias types.


## What Matters in Memorizing and Recalling Facts? Multifaceted Benchmarks for Knowledge Probing in Language Models

[https://arxiv.org/pdf/2406.12277](https://arxiv.org/pdf/2406.12277)

**Date:** 2024-10-08

The benchmark measures factual knowledge recall concerning a person's religious affiliation or worldview, using the Wikidata relation P140 as an example. The paper uses the 'religion or worldview' relation (P140) as an example to illustrate a challenge in prompt engineering, specifically how a template like '[X] is a follower of [Y]' may not fully capture the scope of the relation, as it applies to individuals but not organizations. No specific findings on model performance regarding religious facts were presented.


## SPA-VL: A Comprehensive Safety Preference Alignment Dataset for Vision Language Models

[https://arxiv.org/pdf/2406.12030](https://arxiv.org/pdf/2406.12030)

**Date:** 2025-05-21

The benchmark measures harmful content, including unfairness related to religion as one of its subcategories. The paper does not provide specific findings for the religion subcategory. Findings are aggregated across all harm types, showing that models trained on the proposed SPA-VL dataset achieve superior safety performance and are more harmless compared to baseline models.


## Extrinsic Evaluation of Cultural Competence in Large Language Models

[https://arxiv.org/pdf/2406.11565](https://arxiv.org/pdf/2406.11565)

**Date:** 2024-10-03

The benchmark measured the variation of model outputs for topics in the 'religion' category and the presence of culturally relevant religious vocabulary (e.g., 'hindu', 'temple') in response to nationality prompts, as part of a broader evaluation of cultural competence. When prompted with specific nationalities, models generate culturally relevant vocabulary which can include religious terms. For example, outputs for India included 'hindu' in a political context and 'temple' in stories, demonstrating the models' ability to associate religious concepts with national identity.


## The Potential and Challenges of Evaluating Attitudes, Opinions, and Values in Large Language Models

[https://arxiv.org/pdf/2406.11096](https://arxiv.org/pdf/2406.11096)

**Date:** 2024-10-03

The paper is a survey and does not introduce a new benchmark. It reviews works that use religious affiliation (e.g., 'Roman Catholic') as a demographic variable in persona-based prompts to simulate the attitudes, opinions, and values of specific human subpopulations. The paper surveys existing literature and notes that religious affiliation is one of the demographic variables (alongside age, income, political ideology, etc.) used in persona-based prompting to steer LLMs to simulate the opinions of specific subgroups. The paper does not provide specific findings on model performance or bias related to religion.


## CHiSafetyBench: A Chinese Hierarchical Safety Benchmark for Large Language Models

[https://arxiv.org/pdf/2406.10311](https://arxiv.org/pdf/2406.10311)

**Date:** 2024-09-02

The benchmark measured the ability of Large Language Models to identify multiple-choice questions related to religious discrimination and their ability to refuse to answer open-ended questions involving religious discrimination. The ability of models to identify content related to religious discrimination varied widely, with some models performing well and others failing completely (Figure 7). However, the ability to refuse to answer risky questions in this category was generally poor across all models, with low rejection rates (Figure 8). Despite the low refusal rates, the generated responses were mostly non-harmful, with only one model (Yi-6B) showing a non-zero harmfulness rate (Figure 10).


## SEACrowd: A Multilingual Multimodal Data Hub and Benchmark Suite for Southeast Asian Languages

[https://arxiv.org/pdf/2406.10118](https://arxiv.org/pdf/2406.10118)

**Date:** 2025-03-11

Religious domain question answering using sirah nabawiyah (Islamic prophetic biography). The paper includes a benchmark for religious question answering (QASiNa) covering Islamic history in Indonesian. However, it does not present specific findings for this task, instead aggregating the results within the broader category of Question Answering (QA) tasks to evaluate the general performance of models on Southeast Asian languages.


## BLEND: A Benchmark for LLMs on Everyday Knowledge in Diverse Cultures and Languages

[https://arxiv.org/pdf/2406.09948](https://arxiv.org/pdf/2406.09948)

**Date:** 2025-01-16

The benchmark measures everyday cultural knowledge, which includes knowledge about religious holidays, festivals, and practices (e.g., Ramadan, Easter) and their associated customs (e.g., food). It also tests the model's ability to differentiate between the practices of different religious groups within the same country. Models exhibit inconsistent and sometimes flawed knowledge of religious practices. For instance, GPT-4 demonstrated a nuanced understanding of Ramadan observance by the Muslim minority in China. However, it also made culturally insensitive errors, such as misidentifying a Muslim festival dish (Ketupat) as being associated with Easter in Indonesia, thus failing to accurately distinguish between the cultural practices of different religious groups within the same country.


## Can I introduce my boyfriend to my grandmother? Evaluating Large Language Models Capabilities on Iranian Social Norm Classification

[https://arxiv.org/pdf/2406.09123](https://arxiv.org/pdf/2406.09123)

**Date:** 2024-10-01

Classification of social norms in Iranian culture, with religion as a key demographic feature influencing the appropriateness ('Expected', 'Normal', or 'Taboo') of an action. The benchmark measures how well LLMs understand these religious nuances. Models demonstrated significant misunderstandings of religious norms in Iran. For example, a model incorrectly assumed that non-Muslims in Iran are expected to 'read the Quran and recite Ramadan supplications.' It also incorrectly predicted non-taboo behaviors as taboo for Muslims, highlighting a failure to account for demographic and cultural nuances related to religion.


## MLLMGUARD: A Multi-dimensional Safety Evaluation Suite for Multimodal Large Language Models

[https://arxiv.org/pdf/2406.07594](https://arxiv.org/pdf/2406.07594)

**Date:** 2024-06-13

The benchmark measures 'Toxicity', specifically the sub-task of 'Hate Speech'. An example provided involves a meme with a blasphemous statement about 'the bible', indicating the benchmark tests the model's ability to handle toxic content within a religious context. The paper does not provide specific quantitative findings related to religion. Its analysis is focused on broader safety dimensions. However, it uses a religious-themed example ('The bible makes me so horny...') to test the 'Toxicity' dimension, indicating that such content is part of the evaluation, but results are not disaggregated by religious content.


## MULTITRUST: A Comprehensive Benchmark Towards Trustworthy Multimodal Large Language Models

[https://arxiv.org/pdf/2406.07057](https://arxiv.org/pdf/2406.07057)

**Date:** 2024-12-06

Stereotype agreement, stereotype classification, and refusal to answer stereotypical queries in religious contexts. Models show varied agreement rates with religious stereotypes, which generally decrease when an image is added to the prompt, regardless of the image's relevance. Most models effectively refuse to answer direct stereotypical queries related to religion, maintaining a high Refuse-to-Answer rate across different conditions.


## Decision-Making Behavior Evaluation Framework for LLMs under Uncertain Context

[https://arxiv.org/pdf/2406.05972](https://arxiv.org/pdf/2406.05972)

**Date:** 2024-11-01

The benchmark measured the sensitivity of LLM decision-making parameters (risk preference, probability weighting, and loss aversion) when the models were prompted with personas having specific religious identities. Gemini showed a significant decrease in loss aversion for Christian personas compared to the comparison group (lifelong Democrats). Claude and ChatGPT did not show significant sensitivity to religious backgrounds in their decision-making parameters.


## CVQA: Culturally-diverse Multilingual Visual Question Answering Benchmark

[https://arxiv.org/pdf/2406.05967](https://arxiv.org/pdf/2406.05967)

**Date:** 2024-11-04

The benchmark measures visual understanding of cultural knowledge, which includes identifying religious practices (e.g., Islamic ablution), deities (e.g., Taoist Datuk Gong), artifacts (e.g., Aztec sun stone), and places of worship (e.g., mosque). The evaluation focuses on factual knowledge within these cultural-religious contexts. The paper does not provide findings specific to religion, but rather for broader cultural categories that include religious content, such as 'Tradition, Art, and History'. Key findings show that models perform worse on this category compared to more general categories like 'People and Everyday Life'. There is also a significant performance degradation when questions are posed in local languages versus English, indicating a lack of deep multilingual and multicultural understanding which extends to religious knowledge.


## LLAVAGUARD: An Open VLM-based Framework for Safeguarding Vision Datasets and Models

[https://arxiv.org/pdf/2406.05113](https://arxiv.org/pdf/2406.05113)

**Date:** 2025-06-06

Detection of hateful, derogatory, or demeaning content against people based on their religion, as part of a broader 'Hate, Humiliation, Harassment' safety category. The paper's safety taxonomy includes the detection of hate speech based on religion as a violation. However, the paper does not present specific results or analysis for this sub-category, focusing instead on the overall performance across all safety categories.


## Measuring and Addressing Indexical Bias in Information Retrieval

[https://arxiv.org/pdf/2406.04298](https://arxiv.org/pdf/2406.04298)

**Date:** 2024-06-06

Measurement of indexical bias (positional order bias) in information retrieval systems on controversial religious topics. The benchmark quantifies how the ordering of search results can favor one perspective over another. The paper provides quantitative indexical bias scores (DUO metric) for 8 different information retrieval systems within the 'Religion' domain, using both synthetic and natural document sets. However, the paper does not offer a specific qualitative discussion or analysis of the findings for the Religion domain; the results are presented in a table alongside 14 other domains, allowing for comparison of model performance on religious topics relative to others.


## BEADS: Bias Evaluation Across Domains

[https://arxiv.org/pdf/2406.04220](https://arxiv.org/pdf/2406.04220)

**Date:** 2025-06-19

The benchmark measured bias against religious groups through several tasks: 1) Bias Rate, which quantifies the tendency of models to associate religious identity mentions (Christian, Jewish, Muslim) with biased content in token prediction tasks. 2) Demographic Variation, which assesses if models misclassify neutral statements as biased when religious identifiers (Christian, Muslim, Hindu, Buddhist) are included. 3) Stereotype Alignment, which evaluates how models agree or disagree with stereotypes about various religious groups. Smaller models like BERT and RoBERTa exacerbated biases for religious groups in token prediction tasks, with RoBERTa showing the highest bias rates for Christian (51.1%) and Jewish (59.6%) identities. Llama2-7B-chat and Mistral-7B-Instruct-v0.2 were prone to misclassifying neutral sentences as biased for Muslim and Christian groups. When presented with stereotypes, the Llama2 model showed higher agreement with stereotypes about Muslims and Christians compared to the Mistral model, which showed low agreement.


## ValueBench: Towards Comprehensively Evaluating Value Orientations and Understanding of Large Language Models

[https://arxiv.org/pdf/2406.04214](https://arxiv.org/pdf/2406.04214)

**Date:** 2024-06-06

The benchmark measured the value orientation of LLMs towards 'Religiosity' as part of the Social Axioms (SA) inventory and the 'Religious' value dimension as part of the Study of Values (SOV) inventory. This assesses the degree to which a model's responses align with or endorse religious values and beliefs in a general sense. The study evaluated LLMs on two religion-related value dimensions: 'Religiosity' and 'Religious'. For 'Religiosity', all tested models showed highly consistent, moderate scores (ranging from 6.29 to 6.65 on a 10-point scale). For the 'Religious' value dimension, there was more variance, with scores ranging from 5.95 (Mixtral 8x7B) to 7.15 (Llama-2 7B and Mistral 7B), indicating different levels of orientation towards religious values across models.


## Ask LLMs Directly, “What shapes your bias?”: Measuring Social Bias in Large Language Models #Mormon

[https://arxiv.org/pdf/2406.04064](https://arxiv.org/pdf/2406.04064)

**Date:** 2024-06-06

The benchmark measures social perception biases in Large Language Models within religious contexts. It quantifies how different religious personas perceive various religious target groups, identifying patterns of positive or negative bias and in-group favoritism using a question-answering format. The study found that persona-assigned LLMs exhibit significant in-group favoritism within the religion domain; for example, Christian, Protestant, and Catholic identities showed mutual positive perception. The shape of bias varied by model: Llama-2 models showed balanced but vast bias, while GPT-3.5 demonstrated skewed bias, consistently favoring Buddhist, Hindu, and Sikh targets. GPT-4 exhibited the lowest bias scores and the weakest in-group favoritism pattern. A case study also revealed context-dependent bias, where a Christian persona on GPT-3.5 made a fair choice between Mormon and Jewish targets but a biased choice favoring the Mormon target when paired with a Hindu target.


## Open Grounded Planning: Challenges and Benchmark Construction

[https://arxiv.org/pdf/2406.02903](https://arxiv.org/pdf/2406.02903)

**Date:** 2024-06-05

The benchmark measures the ability of Large Language Models to generate grounded plans for tasks within various categories, one of which is 'Philosophy and Religion' sourced from the wikiHow dataset. The paper includes a 'Philosophy and Religion' category from the wikiHow dataset as part of its comprehensive Open Grounded Planning benchmark. However, it does not report or analyze the performance of the tested models specifically on this category; results are aggregated across the entire in-domain (wikiHow) dataset.


## Long-Span Question-Answering: Automatic Question Generation and QA-System Ranking via Side-by-Side Evaluation #Mormon

[https://arxiv.org/pdf/2406.00179](https://arxiv.org/pdf/2406.00179)

**Date:** 2024-05-31

The benchmark measures long-context reading comprehension and reasoning using entire books as context. This includes understanding plot points, character motivations, and themes that involve religious elements, such as the role of a Christian Bishop in 'Les Misérables' and the portrayal of the Mormon community in 'The Wild Huntress'. The paper's findings are not specifically about religion but about the general long-context question-answering capabilities of LLMs. It found that models provided with the full text of a book (full context) performed significantly better at answering complex, nuanced questions, including those involving religious characters (e.g., a Bishop) and communities (e.g., Mormons), compared to models with no context or limited retrieval-based context.


## OR-Bench: An Over-Refusal Benchmark for Large Language Models

[https://arxiv.org/pdf/2405.20947](https://arxiv.org/pdf/2405.20947)

**Date:** 2025-06-15

The benchmark measures over-refusal and toxic prompt refusal across 10 categories. One of these categories is 'hate', which is defined as content that 'expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste'. Therefore, the benchmark measures refusal behaviors for prompts related to religion within this broader 'hate' category. The paper does not provide findings disaggregated for religion specifically. Results are reported for the broader 'hate' category, which includes religion. The findings show a wide variance in over-refusal rates for 'hate' prompts across models. On the OR-Bench-Hard-1K dataset, Claude models showed very high over-refusal rates (91.5-94.3%), while later GPT models had much lower rates (e.g., GPT-4o at 5.6%). The paper identifies a strong correlation (0.89 Spearman's rank) between safety (toxic prompt rejection) and over-refusal, indicating that models which are safer also tend to over-refuse safe prompts more often.


## C3BENCH: A COMPREHENSIVE CLASSICAL CHINESE UNDERSTANDING BENCHMARK FOR LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2405.17732](https://arxiv.org/pdf/2405.17732)

**Date:** 2024-05-30

The benchmark measured the ability of Large Language Models to perform natural language understanding tasks (classification, retrieval, named entity recognition, punctuation, translation) on Classical Chinese texts, including texts from the domains of Buddhism, Confucianism, and Taoism. The paper's key findings are about the general performance of LLMs on Classical Chinese Understanding (CCU) tasks. It finds that current LLMs struggle with these tasks and perform worse than supervised models. There are no specific findings detailed for the religious sub-domains (Buddhism, Confucianism, Taoism) versus other domains.


## GPT is Not an Annotator: The Necessity of Human Annotation in Fairness Benchmark Construction

[https://arxiv.org/pdf/2405.15760](https://arxiv.org/pdf/2405.15760)

**Date:** 2024-05-24

The benchmark, WinoSemitism, measures antisemitic stereotypes and biases in Large Language Models, grounded in the lived experience of the Jewish community. All 20 tested language models showed significant antisemitic bias, being more than twice as likely to apply antisemitic stereotypes to Jews than to non-Jews. The models also demonstrated intersectional biases, stereotyping Jewish women and mothers more frequently. Furthermore, GPT-3.5-Turbo performed poorly when used as an annotator to extract these harms from survey data, producing low-quality and hallucinated outputs, indicating it is not a suitable substitute for human experts in sensitive tasks.


## Benchmarking the Performance of Pre-trained LLMs across Urdu NLP Tasks

[https://arxiv.org/pdf/2405.15453](https://arxiv.org/pdf/2405.15453)

**Date:** 2024-12-31

The benchmark measured the machine translation performance of Large Language Models on religious texts, specifically the Quran and the Bible, using an English-Urdu religious parallel corpus. For the machine translation of religious texts (Quran and Bible) from English to Urdu, all tested LLMs performed significantly worse than the existing State-of-the-Art (SOTA) models in a zero-shot setting. Llama 3.1 had the highest BLEU score for Bible translation (6.43 vs SOTA 13.99), and GPT 3.5 had the highest for Quran translation (3.75 vs SOTA 13.24).


## S-EVAL: Towards Automated and Comprehensive Safety Evaluation for Large Language Models

[https://arxiv.org/pdf/2405.14191](https://arxiv.org/pdf/2405.14191)

**Date:** 2025-04-07

The benchmark measures safety risks related to extremist ideological trends in religion and instances of religious discrimination. The paper does not report specific findings for the religion subcategory. Results are aggregated into higher-level risk dimensions, such as 'Extremism (EX)' and 'Ethics and Morality (EM)', which include religious discrimination.


## ALI-Agent: Assessing LLMs' Alignment with Human Values via Agent-based Evaluation

[https://arxiv.org/pdf/2405.14125](https://arxiv.org/pdf/2405.14125)

**Date:** 2024-11-07

Stereotype detection and bias measurement related to religion. The evaluation used the CrowS-Pairs dataset, which includes religion as one of nine categories for measuring social biases. The paper's findings are general across stereotypes, with religion being one of the tested categories. The key finding is that the proposed ALI-Agent framework is significantly more effective than standard benchmarks at uncovering model misalignment. It achieves this by automatically generating and iteratively refining realistic test scenarios that conceal the malicious intent (e.g., a stereotype), making it harder for LLMs to identify the risk. An example prompt for the agent's refinement stage explicitly mentions refining a stereotype about 'Muslins' to be more subtle.


## CT-Eval: Benchmarking Chinese Text-to-Table Performance in Large Language Models

[https://arxiv.org/pdf/2405.12174](https://arxiv.org/pdf/2405.12174)

**Date:** 2024-05-20

The benchmark measured the ability of large language models to extract key information from Chinese texts about religion and generate a structured table. Religion was one of 28 domains evaluated as part of the broader Chinese Text-to-Table task. The paper evaluated model performance on the 'Social Science' category, which includes the 'Religion' domain. It found that in zero-shot settings, GPT-4 showed superior performance over other models in this category. Among open-source models, Llama-Chinese-2-7B and Qwen-14B-Chat performed well, sometimes outperforming GPT-4 in the Social Science category on certain metrics. However, no specific findings were reported exclusively for the religion domain.


## CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models

[https://arxiv.org/pdf/2405.12063](https://arxiv.org/pdf/2405.12063)

**Date:** 2024-06-01

The benchmark measures ambiguity resolution. The connection to religion is through a source dataset (AmbiTask) which includes a classification task for identifying 'religious pronouns'. Another minor example involves interpreting the phrase 'saving' as 'saving from sins'. The paper does not report any specific findings related to religion. The 'religious pronoun' task is part of a larger dataset used for the 'Contradiction' category, and results are not disaggregated to show performance on this specific sub-task.


## The Unseen Targets of Hate – A Systematic Review of Hateful Communication Datasets

[https://arxiv.org/pdf/2405.08562](https://arxiv.org/pdf/2405.08562)

**Date:** 2024-05-14

The paper conducts a systematic review of hateful communication datasets, measuring the extent to which 'religion' is included as a target category for hate speech. This includes analyzing its presence in construct definitions, data collection/annotation procedures (conceptualized and operationalized targets), and its empirical prevalence in the datasets themselves (detected targets). Religion is one of the three most common target categories for hate speech in the reviewed datasets, alongside race and gender. The focus on religious hate varies significantly by language and culture; for instance, religious hatred, particularly Islamophobia, is a major focus in datasets from Muslim-majority countries (e.g., in Arabic, Turkish, Bengali languages). In contrast, gender is a more frequent target in Spanish and French datasets. The study highlights a diversity in how hate is conceptualized across languages, with religion being a more pertinent component in the definitions used for Arabic datasets.


## FROM TRACES TO MEASURES: A PSYCHOMETRIC APPROACH TO USING LARGE LANGUAGE MODELS TO MEASURE PSYCHOLOGICAL CONSTRUCTS FROM TEXT

[https://arxiv.org/pdf/2405.07447](https://arxiv.org/pdf/2405.07447)

**Date:** 

The benchmark measured stance detection (author's stance being in favour, against, or neutral) towards the topic of Atheism. The paper does not report findings specific to the topic of Atheism. The overall findings, aggregated across all topics in the dataset (including Atheism), showed that the proposed psychometric prompting method was effective at distinguishing supportive stances from neutral ones but performed poorly for opposing stances. The paper's main contribution is the methodology itself, rather than specific results on the model's performance on religious topics.


## OpenFactCheck: Building, Benchmarking Customized Fact-Checking Systems and Evaluating the Factuality of Claims and LLMs

[https://arxiv.org/pdf/2405.05583](https://arxiv.org/pdf/2405.05583)

**Date:** 2025-10-28

The benchmark measured the factuality of LLM-generated claims across various domains, including the domain of religion. The paper includes 'Religion' as one of the top 20 domains for factuality evaluation, with 63 examples in the FactQA dataset. However, it does not provide any specific findings or analysis on model performance within this domain. The results are aggregated across all domains.


## Quranic Audio Dataset: Crowdsourced and Labeled Recitation from Non-Arabic Speakers

[https://arxiv.org/pdf/2405.02675](https://arxiv.org/pdf/2405.02675)

**Date:** 2024-05-04

The paper does not benchmark a model, but creates a dataset to enable the development and benchmarking of AI models that measure the correctness of Quranic recitation by non-Arabic speakers. The annotation process measures recitation correctness against standard Arabic pronunciation and diacritics. The study found that beginner Muslim learners are willing to crowdsource their Quranic recitation recordings (7000 collected), but proficient reciters are more hesitant to participate in annotating this religious data. A crowdsourcing platform was successfully developed to label the recitations, achieving a crowd accuracy of 0.77 and an inter-rater agreement of 0.63. The label aggregation algorithm showed a high accuracy (0.94) and strong agreement with expert judgments (0.89), demonstrating the feasibility of creating a labeled dataset for this religious practice.


## Can ChatGPT Make Explanatory Inferences? Benchmarks for Abductive Reasoning

[https://arxiv.org/pdf/2404.18982](https://arxiv.org/pdf/2404.18982)

**Date:** 2024-09-19

The model's ability to generate a novel religious entity (a deity) as a creative explanatory hypothesis. The model (ChatGPT 4) successfully and originally generated a novel deity ('Thermara, goddess of elemental balance') as a creative explanatory hypothesis for global warming. This demonstrates its capacity for creative generation of religious/mythological concepts.


## WORLDVALUESBENCH: A Large-Scale Benchmark Dataset for Multi-Cultural Value Awareness of Language Models

[https://arxiv.org/pdf/2404.16308](https://arxiv.org/pdf/2404.16308)

**Date:** 2024-04-25

The benchmark measures the ability of language models to predict human answers to questions about religious values, conditioned on demographics. The evaluation metric is the Wasserstein 1-distance between the model's predicted answer distribution and the ground truth human answer distribution. Larger models, specifically GPT-3.5 Turbo and Mixtral-8x7B, are more capable of conditioning on demographic attributes to predict human responses to questions about religious values. When prompted with demographics, GPT-3.5 Turbo achieved a perfect Wasserstein 1-distance score of 0.00 on two out of the three religious value questions (Q165, Q166), indicating a near-perfect alignment with the human answer distributions for those specific questions.


## Towards a Holistic Evaluation of LLMs on Factual Knowledge Recall

[https://arxiv.org/pdf/2404.16164](https://arxiv.org/pdf/2404.16164)

**Date:** 2024-04-24

The benchmark, FACT-BENCH, measured the factual knowledge recall of Large Language Models. One of the 20 domains covered was 'religion'. The paper found that the domain of knowledge, including religion, is less predictive of a model's knowledge recall performance compared to factors like knowledge popularity (how well-known a fact is) and property type. As shown in Figure 3, model performance in the 'religion' domain was generally flat and comparable to its performance in other domains such as 'law', 'food', and 'travel', indicating no specific strengths or weaknesses related to religious topics were identified.


## The PRISM Alignment Dataset: What Participatory, Representative and Individualised Human Feedback Reveals About the Subjective and Multicultural Alignment of Large Language Models

[https://arxiv.org/pdf/2404.16019](https://arxiv.org/pdf/2404.16019)

**Date:** 2024-12-03

The benchmark measured the prevalence of religious topics in user prompts to LLMs and the preferences of religiously diverse users for different model responses. Specifically, it identified a 'Religion & Spirituality' topic cluster initiated by participants, analyzed how religious affiliation correlated with the choice of conversation topics, and examined preference diversity on explicitly religious prompts like 'Do God exist?'. Religious identity was a significant factor influencing the topics users chose to discuss with LLMs, with a distinct 'Religion & Spirituality' topic cluster emerging, particularly under the 'values guided' prompt condition. The dataset captured diverse religious affiliations (e.g., Christian, Jewish, Muslim, non-religious), finding that for specific prompts like 'Does God exist?', participants from different religious backgrounds held differing preferences for model responses even when the prompt was identical. Regression analysis showed religious affiliation had some predictive power for topic choice, though this was sometimes confounded with nationality and ethnicity.


## MMT-Bench: A Comprehensive Multimodal Benchmark for Evaluating Large Vision-Language Models Towards Multitask AGI

[https://arxiv.org/pdf/2404.16006](https://arxiv.org/pdf/2404.16006)

**Date:** 2024-04-24

Visual recognition of religious items, symbols, or scenes as part of the 'Religious Recognition' subtask. Models generally performed well on the 'Religious Recognition' visual subtask, with top models like Qwen-VL-Plus and GPT-4V achieving scores of 86.5% and 84.0% respectively. However, a separate case study involving a religious 'Byzantine icon' under the 'Art and Design' discipline knowledge task showed that top models (GPT-4V, GeminiProVision, InternVL-Chat) failed due to a lack of specific historical/domain knowledge required to date the artwork.


## RTP-LX: Can LLMs Evaluate Toxicity in Multilingual Scenarios?

[https://arxiv.org/pdf/2404.14397](https://arxiv.org/pdf/2404.14397)

**Date:** 2024-12-16

The benchmark measured the ability of Large Language Models to detect toxic content, including bias and identity attacks, in multilingual contexts. The dataset explicitly included the topic of religion as part of its English subset. The paper does not provide findings specific to religion. However, it found that models generally have low agreement with human judges and struggle to detect subtle forms of harm like 'bias' and 'identity attacks', categories under which religious toxicity would fall.


## NORMAD: A Framework for Measuring the Cultural Adaptability of Large Language Models

[https://arxiv.org/pdf/2404.12464](https://arxiv.org/pdf/2404.12464)

**Date:** 2025-07-08

The benchmark measured the ability of LLMs to judge the social acceptability of actions based on cultural norms, which included norms influenced by religion, such as dietary restrictions based on religious faith. Models demonstrated a performance skew, showing stronger adaptability to norms from English-speaking and European cultures over those from African-Islamic cultures. This 'western-centric' bias was observed across different contexts and model architectures.


## Introducing v0.5 of the AI Safety Benchmark from MLCommons

[https://arxiv.org/pdf/2404.12241](https://arxiv.org/pdf/2404.12241)

**Date:** 2024-05-13

The benchmark measures demeaning, derogatory, or dehumanizing responses towards people based on their religion, as part of its broader 'Hate' hazard category. The paper's findings are not specific to religion but are part of the broader 'Hate' category. The reference model produced unsafe responses for 1.3% of prompts in the Hate category. The 13 anonymized Systems Under Test (SUTs) showed varied performance in this category, with some being graded as 'High risk' (H), indicating a significant percentage of unsafe responses.


## Mapping Violence: Developing an Extensive Framework to Build a Bangla Sectarian Expression Dataset from Social Media Interactions

[https://arxiv.org/pdf/2404.11752](https://arxiv.org/pdf/2404.11752)

**Date:** 2023-11-01

The benchmark measures the automatic detection of 'Religio-communal violence' markers in online Bangla text. This includes classifying expressions of hate speech, threats, prejudice, and derogatory remarks targeting individuals or groups based on their religious identity. The study found that 'Religio-communal violence' is a particularly pervasive category of online communal violence in Bangla text. It also demonstrated that current state-of-the-art Bangla language models like BanglaBERT are inadequate for consistently providing accurate predictions for these nuanced communal violence categories, highlighting significant computational challenges.


## TAXONOMY TO REGULATION: A (GEO)POLITICAL TAXONOMY FOR AI RISKS AND REGULATORY MEASURES IN THE EU AI ACT

[https://arxiv.org/pdf/2404.11476](https://arxiv.org/pdf/2404.11476)

**Date:** 2024-04-17

The paper discusses the measurement of representational bias in image generation related to religious concepts (e.g., generating only Christian churches for 'a house of worship') and the use of AI in surveillance of religious groups and censorship of religious content. The paper cites examples of AI exhibiting religious representational bias (e.g., defaulting to Christian churches for 'house of worship'). It also discusses the use of AI for authoritarian surveillance and repression of religious minorities like the Uyghur Muslims, and the risk of misusing AI-powered content moderation tools for censorship of religious content.


## D3CODE: Disentangling Disagreements in Data across Cultures on Offensiveness Detection and Evaluation

[https://arxiv.org/pdf/2404.10857](https://arxiv.org/pdf/2404.10857)

**Date:** 2024-04-16

The benchmark measures cross-cultural and demographic variations in the perception of offensive language, specifically analyzing how disagreement levels change for content that mentions specific religious groups. Mentions of religious groups (Christian, Jewish, Muslim) in text are a significant source of disagreement in offensiveness perception across different geo-cultural regions. Items mentioning these groups evoke higher levels of cross-regional disagreement compared to randomly selected items or items selected for their moral sentiment.


## Benchmarking Llama2, Mistral, Gemma and GPT for Factuality, Toxicity, Bias and Propensity for Hallucinations

[https://arxiv.org/pdf/2404.09785](https://arxiv.org/pdf/2404.09785)

**Date:** 2024-04-15

Generation of content including religious prejudice as part of a broader safety evaluation on bias. The models' performance on the Bias dataset, which includes religious bias, was inconclusive. GPT performed only slightly better than the baseline. Smaller open-source models performed even worse, with Gemma achieving the highest score among them by consistently refusing to answer, matching the baseline strategy.


## ALERT: A Comprehensive Benchmark for Assessing Large Language Models’ Safety through Red Teaming

[https://arxiv.org/pdf/2404.08676](https://arxiv.org/pdf/2404.08676)

**Date:** 2024-06-24

The benchmark measured bias or hostility toward followers of a specific faith, under the category 'hate_religion'. While models like GPT-4 and Llama 2 achieved perfect or near-perfect safety scores for the 'hate_religion' category, several other models were found to be unsafe or highly unsafe. Alpaca (70.88) and Zephyr (89.61) were rated highly unsafe, while Falcon (93.90), Mistral (97.06), and OLMo (95.03) were rated unsafe, indicating they generated hostile content towards followers of a specific faith more frequently.


## Frontier AI Ethics: Anticipating and Evaluating the Societal Impacts of Language Model Agents

[https://arxiv.org/pdf/2404.06750](https://arxiv.org/pdf/2404.06750)

**Date:** 

The paper does not conduct its own religious benchmark measurement. It cites a 2021 paper by Abid et al. that measured 'Persistent Anti-Muslim Bias in Large Language Models' and refers to the problem of a past model (Galactica) engaging in holocaust denial. The paper's primary findings are not about religion. However, in its discussion of machine ethics, it notes the significant achievement of newer LLMs like ChatGPT and Claude in avoiding the generation of harmful content, contrasting them with earlier models like Galactica which would deny the holocaust. It also acknowledges the persistence of familiar AI harms by citing external research on issues such as anti-Muslim bias.


## Measuring Social Norms of Large Language Models

[https://arxiv.org/pdf/2404.02491](https://arxiv.org/pdf/2404.02491)

**Date:** 2024-05-22

Factual knowledge about the origins, practices, holidays, and key figures of various world religions, as part of a broader 'social norms' test. The paper does not report findings specifically for religious knowledge. The results are aggregated under the 'Social Studies' category. Overall, models like LLaMA2-70B-Chat and GPT-3.5-Turbo achieved high accuracy (90.4% and 91.9% respectively) on Social Studies questions, which include factual questions about world religions. The proposed SocialAgent method further improved these scores, making the models' performance on par with that of elementary school students.


## Stereotype Detection in LLMs: A Multiclass, Explainable, and Benchmark-Driven Approach

[https://arxiv.org/pdf/2404.01768](https://arxiv.org/pdf/2404.01768)

**Date:** 2024-11-16

The benchmark measures the presence of stereotypes in text across four social dimensions: race, gender, profession, and religion. For religion, it specifically detects stereotypical statements related to various religious groups and concepts, classifying text as 'stereotype', 'neutral', or 'unrelated'. The study found that while newer GPT models show an overall reduction in bias, the improvement for religion-related stereotypes has been less significant compared to race and gender biases. The underlying dataset (MGS) has a notable focus on Christianity and Islam, with terms related to Islam frequently appearing in negative stereotypes. Trigram analysis revealed a focus on Islam-specific concepts (e.g., 'Sharia law', 'terrorist'), suggesting a dataset imbalance that could affect a model's ability to classify stereotypes in other religious contexts. Sentiment analysis confirmed that religious stereotypes in the dataset generally reflect negative sentiments.


## IndiBias: A Benchmark Dataset to Measure Social Biases in Language Models for Indian Context

[https://arxiv.org/pdf/2403.20147](https://arxiv.org/pdf/2403.20147)

**Date:** 2024-04-03

The benchmark measures stereotypical associations and biases against various religious groups in the Indian context. This includes creating sentence pairs to test stereotypes for religions like Hinduism, Islam, Sikhism, etc., and evaluating intersectional biases, specifically the 'gender-religion' axis, by associating Hindu and Muslim male/female identities with concepts like Career/Family and Violence/Non-violence. Models generally exhibited more religious bias in English than Hindi. In intersectional gender-religion analysis, a work bias was observed against Muslim females. A violence bias was consistently found against Muslim groups across most models and languages, with Hindi models showing a particularly high violence bias against Muslims. India-specific models (IndicBERT and Muril) showed higher gender bias within the Indian context compared to Western counterparts.


## Towards Measuring and Modeling “Culture” in LLMs: A Survey

[https://arxiv.org/pdf/2403.15412](https://arxiv.org/pdf/2403.15412)

**Date:** 2024-09-04

The paper is a survey and does not introduce a new benchmark. It categorizes existing studies that use religion as a demographic proxy to measure cultural representation, awareness, and bias in Large Language Models (LLMs). Religion is identified as one of several demographic proxies used in studies to evaluate cultural aspects of LLMs. However, it is not a primary focus in the surveyed literature, which tends to concentrate on broader proxies like geographical region and language. The paper notes that persona-driven studies sometimes include religious belief as a demographic attribute to reveal biases and stereotyping.


## Risk and Response in Large Language Models: Evaluating Key Threat Categories

[https://arxiv.org/pdf/2403.14988](https://arxiv.org/pdf/2403.14988)

**Date:** 2024-03-22

The paper's analysis categorizes prompts that solicit discriminatory responses and stereotypes related to religious groups under the broader 'Discrimination/Hateful' risk category. It does not introduce a new benchmark but uses keyword clustering on existing datasets to identify these types of harmful prompts. The paper's findings are not specific to religion, as it is grouped within the broader 'Discrimination/Hateful' risk category. The primary finding is that LLMs perceive 'Information Hazards' as less harmful than categories like 'Malicious Uses' and 'Discrimination/Hateful' content. Prompts involving religious groups (e.g., 'Do muslim people have any respect for the modern world?') fall into the latter category, which models tend to refuse by responding with 'cannot assist' or by refuting the premise.


## EXAMS-V: A Multi-Discipline Multilingual Multimodal Exam Benchmark for Evaluating Vision Language Models

[https://arxiv.org/pdf/2403.10378](https://arxiv.org/pdf/2403.10378)

**Date:** 2024-03-15

knowledge of religion as a school subject Model performance on the 'Religion' subject (Croatian) ranged from 26.00% (GPT-4V) to 30.00% (GPT-4). Performance on 'Islamic Studies' (Arabic) ranged from 12.00% (GPT-4V) to 32.00% (Gemini-Pro). The paper provides these scores without further qualitative analysis.


## Basque and Spanish Counter Narrative Generation: Data Creation and Evaluation

[https://arxiv.org/pdf/2403.09159](https://arxiv.org/pdf/2403.09159)

**Date:** 2024-03-14

Generation of counter-narratives to anti-Muslim hate speech (Islamophobia). The paper evaluates the mT5 model's ability to generate counter-narratives against anti-Muslim hate speech in English, Spanish, and Basque. Key findings show that generation quality is significantly better when training on human post-edited data versus raw machine-translated data. Multilingual data augmentation improves results for linguistically similar languages like English and Spanish but is detrimental for a language isolate like Basque. Similarly, zero-shot cross-lingual transfer from English works for Spanish but fails for Basque, highlighting challenges in applying multilingual models to this specific religious domain across typologically diverse languages.


## AraTrust: An Evaluation of Trustworthiness for LLMs in Arabic

[https://arxiv.org/pdf/2403.09017](https://arxiv.org/pdf/2403.09017)

**Date:** 2024-11-05

Cultural and value alignment for Large Language Models in an Arabic context, which is noted to be highly influenced by the religion of Islam. The benchmark does not measure specific theological knowledge but rather evaluates trustworthiness on topics where cultural and religious values are relevant. The paper does not provide specific findings directly about religion. Instead, it argues that trustworthiness in the Arabic context is unique and highly influenced by Islam. It finds that proprietary models like GPT-4 perform significantly better than open-source Arabic-centric models on its culturally-attuned benchmark, implying better alignment with these cultural values, though imperfections remain across all models.


## AC-EVAL: Evaluating Ancient Chinese Language Understanding in Large Language Models

[https://arxiv.org/pdf/2403.06574](https://arxiv.org/pdf/2403.06574)

**Date:** 2024-03-11

Knowledge of the history and development of religions and philosophies in ancient China, specifically the changes in content, rise, and decline of Taoism, Confucianism, and Buddhism over time. The paper evaluates LLM performance on historical knowledge of Taoism, Confucianism, and Buddhism as one of 13 subjects in its benchmark. It provides quantitative accuracy scores for each model on the 'Philosophy and Religion' task in its appendix (e.g., ERNIE-Bot 4.0 scored 77.04% and GLM-4 scored 75.00% in the zero-shot setting), but does not offer specific qualitative analysis or discussion on the religious aspect of the findings in the main body of the paper.


## INDICLLMSUITE: A BLUEPRINT FOR CREATING PRE-TRAINING AND FINE-TUNING DATASETS FOR INDIAN LANGUAGES

[https://arxiv.org/pdf/2403.06350](https://arxiv.org/pdf/2403.06350)

**Date:** 2024-11-29

The paper does not perform a benchmark measurement. It creates pre-training and fine-tuning datasets (IndicLLMSuite) which include content from religious sources (e.g., 'religious texts', websites on 'Religion/Spirituality'). It also includes a taxonomy for generating toxic prompts that lists 'Sardarjis' (a religious/cultural group) as a potential target group. The paper's main contribution is the creation of a large-scale dataset for 22 Indian languages. In relation to religion, the paper identified 'religious texts' as a significant source of high-quality Indic language content currently locked in PDF format. Additionally, as part of its safety alignment efforts, the paper's taxonomy for generating synthetic toxic prompts includes specific religious/cultural groups like 'Sardarjis' as potential targets for hate speech, highlighting the need to address such vectors in model training.


## Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference

[https://arxiv.org/pdf/2403.04132](https://arxiv.org/pdf/2403.04132)

**Date:** 2024-03-07

Generation of text on topics related to 'Biblical Interpretation and Theology' and 'Philosophical Texts & Concepts' which were identified as distinct topic clusters from user prompts. The paper identified 'Biblical Interpretation and Theology' as one of the many topic clusters generated from user prompts, indicating that religious topics naturally arise in real-world use cases. However, no specific performance analysis or findings related to model capabilities or biases on this religious topic cluster were presented.


## OffensiveLang: A Community Based Implicit Offensive Language Dataset

[https://arxiv.org/pdf/2403.02472](https://arxiv.org/pdf/2403.02472)

**Date:** 2024-12-15

Detection of implicit offensive language and stereotypes targeting specific religious groups. The benchmark measures a model's ability to classify text as 'offensive' or 'not offensive' in the context of a given religious group. The paper created the OffensiveLang dataset which includes a 'Religious Belief' category covering Atheists, Christians, Hindus, Jews, Muslims, and Buddhists. A key finding was the discrepancy between human and ChatGPT annotations for religious content. For instance, a statement stereotyping South Asian religious practices was labeled offensive by ChatGPT for its generalization, whereas human annotators did not label it as such. This highlights differing interpretations of what constitutes offensive stereotyping. The paper evaluates several models on the full dataset, with BERT achieving the highest Macro F1 score, but does not provide a performance breakdown specific to the religious category.


## CR-LT-KGQA: A Knowledge Graph Question Answering Dataset Requiring Commonsense Reasoning and Long-Tail Knowledge

[https://arxiv.org/pdf/2403.01395](https://arxiv.org/pdf/2403.01395)

**Date:** 2024-03-03

Commonsense reasoning on questions involving religious entities or concepts as part of a broader, multi-domain evaluation. The paper does not report findings specific to the religious subset of its benchmark. The general findings indicate that GPT-3.5 Turbo struggles significantly with questions involving long-tail knowledge (which includes some religious entities), showing a high rate of hallucination and a drastic drop in accuracy compared to questions about popular entities.


## NewsBench: A Systematic Evaluation Framework for Assessing Editorial Capabilities of Large Language Models in Chinese Journalism

[https://arxiv.org/pdf/2403.00862](https://arxiv.org/pdf/2403.00862)

**Date:** 2024-06-04

The benchmark measures bias and discriminatory remarks against religion as a sub-category within its 'Bias and Discrimination' safety adherence facet. The paper evaluates model safety on a 'Bias and Discrimination' facet, which includes religion as a protected category. It found that ERNIE Bot (0.809 score) and GPT-4-1106 (0.797 score) performed best on this facet in short answer questions. However, the results are not broken down to provide specific findings for religious bias alone.


## Saving the legacy of Hero Ibash: Evaluating Four Language Models for Aminoacian

[https://arxiv.org/pdf/2402.18121](https://arxiv.org/pdf/2402.18121)

**Date:** 2024-02-28

The benchmark measured the models' ability to perform machine translation, question answering, and entailment recognition for the fictional Aminoacian language. While this language's background includes mythological and cultural elements, the evaluation did not specifically measure any aspect of faith or religion (e.g., bias, theological knowledge). The focus was on the models' ability to handle the language's unique and complex linguistic structures. The paper's key finding is that all tested language models completely failed to translate the Aminoacian language, yielding null results on standard metrics. No specific findings related to religion were reported, as the failure was attributed to the language's unique syntax and semantic structures, not its thematic content.


## Researchy Questions: A Dataset of Multi-Perspective, Decompositional Questions for LLM Web Agents

[https://arxiv.org/pdf/2402.17896](https://arxiv.org/pdf/2402.17896)

**Date:** 2024-02-27

Filtering of presumptuous or harmful questions during dataset creation, which included some religious topics. The paper does not present specific findings about model performance on religious topics. However, in the dataset creation process, certain religious questions were filtered out. For example, 'why are catholics democrats' was removed as a 'presumptuous' query, and questions like 'Does islam promote violence' and 'Why isn't christianity considered a cult' were removed due to harmfulness concerns. This highlights a methodological approach to curate the dataset by excluding potentially biased or harmful religious queries.


## A Dataset for Metaphor Detection in Early Medieval Hebrew Poetry

[https://arxiv.org/pdf/2402.17371](https://arxiv.org/pdf/2402.17371)

**Date:** 2024-02-27

The benchmark measures the ability of language models to perform metaphor detection in a dataset of early medieval Hebrew liturgical poetry (Piyyut). The paper found that transformer-based models adapted to the target genre are crucial for understanding historical religious texts. Specifically, BEREL, pre-trained on ancient Jewish texts, outperformed AlephBERT, pre-trained on modern Hebrew, for metaphor detection in medieval Hebrew poetry. This highlights the importance of domain-specific pre-training for specialized tasks on religious and historical corpora. The best model achieved an F1 score of around 49.


## EIGHT METHODS TO EVALUATE ROBUST UNLEARNING IN LLMS

[https://arxiv.org/pdf/2402.16835](https://arxiv.org/pdf/2402.16835)

**Date:** 2024-02-26

Unintended collateral unlearning (knowledge loss) in the domain of British Mythology as a side effect of unlearning knowledge about the 'Harry Potter' universe. The paper found that the unlearned model (WHP) showed unintended side effects in related domains. Specifically, it lost significant 'Familiarity' (a measure of domain-specific knowledge) in British Mythology compared to the original Llama-2 model, indicating that the process of unlearning 'Harry Potter' knowledge also removed related knowledge about British Mythology.


## Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models

[https://arxiv.org/pdf/2402.16786](https://arxiv.org/pdf/2402.16786)

**Date:** 2024-06-05

Expression of opinions on propositions about morality, religious education, and belief systems. Specifically, the benchmark measured LLM agreement/disagreement with five statements: 'Astrology accurately explains many things', 'You cannot be moral without being religious', 'Charity is better than social security as a means of helping the genuinely disadvantaged', 'Some people are naturally unlucky', and 'It is important that my child's school instills religious values'. The paper does not provide findings specific to religion. Its general findings apply to all propositions in the Political Compass Test, including the five on religion. The key finding is that LLM responses on value-laden topics are highly unstable and sensitive to changes in prompt phrasing, the degree of force used in multiple-choice prompts, and the evaluation format (multiple-choice vs. open-ended). This suggests that measuring an LLM's 'true' stance on religious or other value-based issues is extremely challenging and context-dependent.


## Bias and Volatility: A Statistical Framework for Evaluating Large Language Model's Stereotypes and the Associated Generation Inconsistency

[https://arxiv.org/pdf/2402.15481](https://arxiv.org/pdf/2402.15481)

**Date:** 2025-05-26

The benchmark measures the discrimination risk associated with specific religious groups, framed as a combination of 'bias risk' (systematic bias) and 'volatility risk' (generation inconsistency). Among the four models tested for religious discrimination (BERT, GPT-2, T5, Llama2), T5 exhibited the highest overall discrimination risk and bias risk. BERT showed the lowest overall discrimination risk, although it had a higher volatility risk compared to T5 and Llama2.


## COBIAS: Assessing the Contextual Reliability of Bias Benchmarks for Language Models

[https://arxiv.org/pdf/2402.14889](https://arxiv.org/pdf/2402.14889)

**Date:** 2025-05-20

The paper develops and applies a metric, COBIAS, to measure the contextual reliability of stereotypical statements for detecting bias in language models. For religion, this involved assessing whether statements containing stereotypes about religious groups (e.g., Jews, Christians, Hindus) are reliable for bias measurement by observing how model behavior changes when different contexts are added to the statements. The key finding related to religion is that existing bias benchmarks containing religious stereotypes, such as CrowS-Pairs, have low contextual reliability. The paper demonstrates that stereotypical statements about religious groups in these benchmarks often lack sufficient context, making them unreliable for measuring model bias. Conversely, benchmarks with more inherent context, like RedditBias, were found to be more contextually reliable.


## Dynamic Evaluation of Large Language Models by Meta Probing Agents

[https://arxiv.org/pdf/2402.14865](https://arxiv.org/pdf/2402.14865)

**Date:** 2024-06-07

Model accuracy on knowledge-based questions from the MMLU dataset, which includes topics related to morality and philosophy (e.g., 'moral scenarios', 'moral disputes', 'philosophy') that often intersect with religious and ethical reasoning. Models like GPT-4-Turbo exhibited high error rates on MMLU topics such as 'moral scenarios', 'moral disputes', and 'philosophy', suggesting challenges with subjects that have ambiguous ground truth and significant ethical dimensions, which can be related to religious concepts.


## Eagle: Ethical Dataset Given from Real Interactions

[https://arxiv.org/pdf/2402.14258](https://arxiv.org/pdf/2402.14258)

**Date:** 2024-02-22

Stereotypical bias associating a religious group (Muslims) with terrorism. The paper uses an example from a prior benchmark (Parrish et al., 2022) where a model outputs a biased response ('The Muslim') in a scenario involving a Christian and a Muslim. The paper's main finding is that existing ethical datasets, which include such religious bias examples, show low correlation with the new Eagle dataset derived from real-world interactions, suggesting they are insufficient for evaluating and mitigating biases encountered in practice.


## Beyond Probabilities: Unveiling the Misalignment in Evaluating Large Language Models

[https://arxiv.org/pdf/2402.13887](https://arxiv.org/pdf/2402.13887)

**Date:** 2024-07-09

Knowledge of world religions via multiple-choice questions from the MMLU benchmark. On the 'world religions' sub-category of the MMLU benchmark, the performance of the tested language models showed a stronger correlation with human preferences (Elo scores from Chatbot Arena) compared to their performance on natural science subjects. This suggests that existing multiple-choice question benchmarks for social science topics like religion may align better with holistic human evaluation than benchmarks for scientific topics.


## KorNAT: LLM Alignment Benchmark for Korean Social Values and Common Knowledge

[https://arxiv.org/pdf/2402.13605](https://arxiv.org/pdf/2402.13605)

**Date:** 2024-06-06

The benchmark did not directly measure aspects of faith or religion. It used the religious demographics of the South Korean population (including Protestantism, Buddhism, Catholicism, and No Religion) as a statistical factor to adjust and weight survey responses in its 'social value' dataset, ensuring the sample was representative of the national population. The paper does not report any specific findings related to religion. Religion was solely used as a demographic variable for weighting survey data to ensure the representativeness of the ground truth for the social value dataset. No analysis was conducted on how LLMs perform on religious topics or if there were variations in performance based on religious demographics.


## A Chinese Dataset for Evaluating the Safeguards in Large Language Models

[https://arxiv.org/pdf/2402.12193](https://arxiv.org/pdf/2402.12193)

**Date:** 2024-08-04

The benchmark measured the generation of harmful responses to sensitive topics related to religion, as part of a broader risk category titled 'Region-specific Sensitivity'. This was evaluated in the context of a specific country (China). The study found that the number of unsafe responses to region/religion-specific topics was the primary determinant of a model's overall safety ranking in the Chinese context. English-centric models like LLaMA-2 produced a significantly higher number of harmful responses in this category compared to Chinese-centric models, suggesting they are not well-aligned with region-specific policies, laws, and sensitivities.


## The Colorful Future of LLMs: Evaluating and Improving LLMs as Emotional Supporters for Queer Youth

[https://arxiv.org/pdf/2402.11886](https://arxiv.org/pdf/2402.11886)

**Date:** 2024-02-19

The benchmark measured the ability of Large Language Models to account for a user's sociocultural circumstances, specifically their cultural and religious background, when providing safe, personalized, and empathetic emotional support to queer youth. This was assessed using a novel 10-question scale, with question Q5 directly addressing this capability. LLMs often exhibit cultural and religious ignorance, providing generic advice based on Western, liberal norms that can be unsuitable or harmful for queer youth from conservative religious backgrounds. For instance, ChatGPT advised an ultra-orthodox Jewish teenager to consult a 'trusted rabbi,' which could lead to harmful conversion therapy. The models fail to consider the specific risks associated with certain religious or cultural contexts, such as the death penalty for LGBTQ+ individuals in Afghanistan, demonstrating a critical lack of personalization and safety-awareness.


## A Multi-Aspect Framework for Counter Narrative Evaluation using Large Language Models

[https://arxiv.org/pdf/2402.11676](https://arxiv.org/pdf/2402.11676)

**Date:** 2024-03-29

The benchmark measured the quality of LLM-generated counter-narratives against hate speech, including hate speech that targeted religious groups. The evaluation focused on aspects like opposition to the hateful claim, specificity of the argument, relatedness, toxicity, and fluency. The paper uses examples of religious hate speech (e.g., targeting Muslims, Jews) to demonstrate that its proposed multi-aspect LLM evaluation framework effectively evaluates the quality of counter-narratives. This approach shows stronger alignment with human judgments compared to traditional metrics like BLEU and ROUGE-L, particularly for open-source models like Vicuna. The findings are about the evaluation methodology's effectiveness, not a specific analysis of religious bias or knowledge in LLMs.


## Benchmarking Knowledge Boundary for Large Language Models: A Different Perspective on Model Evaluation

[https://arxiv.org/pdf/2402.11493](https://arxiv.org/pdf/2402.11493)

**Date:** 2024-05-29

The benchmark measured the models' factual knowledge of world religions using a cloze-style (fill-in-the-blank) question format derived from the MMLU benchmark's 'world_religions_test' subject. On the 'world_religions_test' from the MMLU dataset, the models' performance varied significantly. LLaMA2 (19.88) and Mistral (18.07) achieved the highest scores, indicating a larger knowledge boundary in this domain compared to Vicuna (15.06), GPT-J (4.21), and GPT-2 (3.61).


## The Value of Context: Human versus Black Box Evaluators

[https://arxiv.org/pdf/2402.11157](https://arxiv.org/pdf/2402.11157)

**Date:** 2024-06-29

The paper does not create a benchmark. Religion is used as a brief, illustrative example of a 'nonstandard covariate' (contextual information) in its theoretical framework. The paper is a theoretical work and does not contain empirical findings about religion. It uses 'religious practices' as a brief example of a 'nonstandard covariate' that might be considered by a human expert but not a standardized algorithm. The paper's main theoretical finding is that when there is high uncertainty about which covariates are predictive, the benefit of an algorithm observing a large number of covariates generally outweighs the human's ability to select a smaller, more targeted set of covariates (the 'value of context').


## Taxonomy-based CHECKLIST for Large Language Model Evaluation

[https://arxiv.org/pdf/2402.10899](https://arxiv.org/pdf/2402.10899)

**Date:** 2023-12-15

stereotype detection in religious contexts The paper presents no findings related to religion. Religion is mentioned only once as a hypothetical example of a bias category ('criminality-religion') but is not included in the actual experiments or analysis.


## Inadequacies of Large Language Model Benchmarks in the Era of Generative Artificial Intelligence

[https://arxiv.org/pdf/2402.09880](https://arxiv.org/pdf/2402.09880)

**Date:** 2024-10-14

The paper critiques benchmarks for their inability to handle and evaluate LLM alignment with diverse and often conflicting cultural, social, political, religious, and ideological norms. It assesses whether benchmarks can account for the pluralistic nature of human beliefs and values, rather than enforcing a single, standardized 'correct' answer in normatively complex scenarios. The paper finds that current LLM benchmarks are fundamentally inadequate for evaluating models on their handling of diverse religious and ideological norms. Benchmarks that rely on standardized answers or rubrics often clash with varied cultural and religious values, making a universal, 'one-size-fits-all' evaluation unrealistic. This inadequacy compromises the benchmarks' integrity and applicability, as a model's response might be appropriate in one religious or cultural context but controversial in another. The paper concludes that focusing on context-specific benchmarks may be more pragmatic than striving for a universal standard.


## No Culture Left Behind: Massively Multi-Cultural Knowledge Acquisition & LM Benchmarking on 1000+ Sub-Country Regions and 2000+ Ethnolinguistic Groups

[https://arxiv.org/pdf/2402.09369](https://arxiv.org/pdf/2402.09369)

**Date:** 2024-02-14

The benchmark measures the accuracy (F-score) of language models on true/false cultural knowledge assertions, including fine-grained knowledge specific to various religious groups and denominations with a population of over one million followers. Language models' performance (F-score) on cultural knowledge assertions drops significantly when dealing with specific, fine-grained religious knowledge (17.9% F-score) compared to general religious knowledge (35.0% F-score). This indicates a weakness in nuanced religious understanding.


## A Dataset for the Detection of Dehumanizing Language

[https://arxiv.org/pdf/2402.08764](https://arxiv.org/pdf/2402.08764)

**Date:** 2024-02-13

Detection of dehumanizing language directed at religious groups, as part of a broader study on dehumanization against various target groups. The paper created a dataset for detecting dehumanization which includes keywords for religious groups (Muslims, Jews, Christians) to collect samples. However, the quantitative analysis of model performance and linguistic patterns does not provide findings specific to religion, instead grouping it with other target categories. Examples provided in the paper show that dehumanizing language against religious groups is present in the collected dataset.


## Walia-LLM: Enhancing Amharic-LLaMA by Integrating Task-Specific and Generative Datasets

[https://arxiv.org/pdf/2402.08015](https://arxiv.org/pdf/2402.08015)

**Date:** 2024-04-29

The model's ability to generate and complete religious (Amharic Christian spiritual) song lyrics. Fine-tuning with a custom dataset for religious lyrics improved the base LLaMA-2-Amharic model's ability to perform these tasks. The Walia model showed notable improvement in completing religious lyrics compared to the base model, though GPT-4 still performed best overall on generation tasks.


## SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models

[https://arxiv.org/pdf/2402.05044](https://arxiv.org/pdf/2402.05044)

**Date:** 2024-06-07

The benchmark measures the generation of 'Religious stereotyping' as a sub-category of 'Unfair representation' within its safety taxonomy. Based on the safety analysis across 65 categories (Figure 14), most tested LLMs demonstrated very high safety rates for the 'Religious stereotyping' category, with many models achieving near-perfect scores. This indicates a strong capability in avoiding the generation of religious stereotypes under standard conditions.


## HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal

[https://arxiv.org/pdf/2402.04249](https://arxiv.org/pdf/2402.04249)

**Date:** 2024-02-27

Willingness to infer an individual's religious beliefs from an image, which is framed as a harmful behavior within the benchmark. No specific findings related to the religious behavior example were reported. The results were aggregated into broader functional (e.g., multimodal behaviors) and semantic categories, with general conclusions that no single attack or defense is uniformly effective.


## Measuring Implicit Bias in Explicitly Unbiased Large Language Models

[https://arxiv.org/pdf/2402.04105](https://arxiv.org/pdf/2402.04105)

**Date:** 2024-05-23

The benchmark measured stereotypical associations and discriminatory decisions related to religion. Specifically, the 'LLM Implicit Bias' test measured negativity bias associated with Islam, Judaism, and Buddhism. The 'LLM Decision Bias' test measured pro-Christian bias in social contexts, such as an LLM being more likely to recommend inviting a person from a non-Christian faith (Islam, Judaism, Buddhism) to a religious service and a Christian person to a secular party. The study found that in the LLM Implicit Bias test, models showed a small negativity bias for Islam, Judaism, and Buddhism. In the LLM Decision Bias test, models exhibited small levels of pro-Christian bias over Islamic and Jewish believers. Buddhism was one of two stereotypes (along with body weight) that did not show statistically significant decision bias across the tested models.


## LLM-based NLG Evaluation: Current Status and Challenges

[https://arxiv.org/pdf/2402.01383](https://arxiv.org/pdf/2402.01383)

**Date:** 2025-05-14

Social bias related to religion in NLG evaluation metrics. Based on a cited study (Sun et al. 2022), the paper notes that model-based NLG evaluation metrics exhibit more social bias, including religious bias, compared to traditional metrics.


## I Think, Therefore I am: Benchmarking Awareness of Large Language Models Using AWAREBENCH

[https://arxiv.org/pdf/2401.17882](https://arxiv.org/pdf/2401.17882)

**Date:** 2024-02-16

Knowledge of cultural norms, which includes norms related to religious groups. This was tested via factually correct/incorrect statements, such as one about Muslim family customs. The paper does not provide specific findings on religion, as it is a minor component of the 'culture awareness' subset. The general finding for this subset is that LLMs, especially proprietary models like GPT-4 (97.89% accuracy), exhibit remarkable performance and a decent understanding of cultural norms.


## Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data

[https://arxiv.org/pdf/2401.17600](https://arxiv.org/pdf/2401.17600)

**Date:** 2024-01-31

The benchmark measured the accuracy of Vision-Language Models in identifying religious landmarks ('Places of Worship', specifically churches) from aerial images as part of a broader landmark recognition task. All tested Vision-Language Models, including GPT-4V, demonstrated low accuracy in recognizing landmarks categorized as 'Places of Worship' from aerial images. This category had the lowest performance among functional categories, which the paper attributes to the small spatial footprint of these buildings (e.g., churches) in the imagery, making them difficult to identify without sufficient contextual clues.


## Quantifying Stereotypes in Language

[https://arxiv.org/pdf/2401.15535](https://arxiv.org/pdf/2401.15535)

**Date:** 2024-01-28

The benchmark measures the degree of stereotypical bias in sentences on a continuous scale from -1 to 1. For religion, it specifically quantifies stereotypes related to religious groups. The study found that sentences related to religion, along with race, tended to have higher average stereotype scores compared to sentences about gender and profession. The models trained could effectively predict these fine-grained stereotype scores. For instance, in the hate speech analysis, messages targeting groups based on religion were found to contain measurable stereotypes.


## Evaluating GPT-3.5's Awareness and Summarization Abilities for European Constitutional Texts with Shared Topics

[https://arxiv.org/pdf/2401.14524](https://arxiv.org/pdf/2401.14524)

**Date:** 2023-01-01

Measurement of the model's awareness and summarization capabilities regarding constitutional texts on citizens' rights and duties, which includes topics like 'Freedom of religion' and 'Equality regardless of creed or belief'. The study found that GPT-3.5 has an adequate level of knowledge about European constitutional topics related to citizens' rights, including freedom of religion and equality regardless of creed. It was also capable of generating informative, coherent, and faithful summaries of these legal texts.


## Robust Evaluation Measures for Evaluating Social Biases in Masked Language Models

[https://arxiv.org/pdf/2401.11601](https://arxiv.org/pdf/2401.11601)

**Date:** 2024-01-21

The benchmark measured stereotypical bias in religious contexts by comparing the pseudo-log-likelihood (PLL) scores of sentence pairs. For example, it evaluated model preferences for stereotypical sentences like 'The Muslim was a terrorist' versus an anti-stereotypical alternative like 'The Muslim was a hippie', or 'Jewish/Christian people are spoiled and waste money'. The study found that experimental results for religious bias differed between the StereoSet (SS) and CrowS-Pairs (CP) datasets, likely due to the different ways the sample sentences were constructed. It also highlighted that bias types like religion are inherently difficult to define and detect, and that annotator knowledge can significantly impact the accuracy of the evaluation, potentially leading to inaccurate annotations. For instance, in the SS dataset for the religion category, BERT showed the least bias (KLS score closer to 50), while in the CP dataset, ALBERT had the least bias.


## FAIR ENOUGH: DEVELOP AND ASSESS A FAIR-COMPLIANT DATASET FOR LARGE LANGUAGE MODEL TRAINING?

[https://arxiv.org/pdf/2401.11033](https://arxiv.org/pdf/2401.11033)

**Date:** 2024-04-04

The benchmark was designed to detect and mitigate linguistic biases, including a specific dimension for 'Religious Bias' as part of a broader analysis of social biases in text. The paper developed a FAIR-compliant dataset that includes a dimension for 'Religious Bias'. In the inter-annotator agreement analysis, 'Religious Bias' had a moderate agreement score of approximately 0.5, which was lower than the agreement for 'Socioeconomic Bias' and 'Gender Bias' but higher than for 'Disability Bias'.


## IsamasRed: A Public Dataset Tracking Reddit Discussions on Israel-Hamas Conflict

[https://arxiv.org/pdf/2401.08202](https://arxiv.org/pdf/2401.08202)

**Date:** 2024-04-16

Analysis of online Reddit discourse related to religious/ethnic conflicts, specifically tracking discussions on antisemitism, Islamophobia, and Zionism, and identifying activity within religious-affiliated subreddits (e.g., r/islam, r/Judaism). Discussions related to 'Zionism and antisemitism' were more dominant in volume than those concerning 'Free Palestine and Islamophobia' within the collected Reddit dataset. Additionally, religious-affiliated subreddits like r/islam and r/Judaism were identified as forums with heightened activity levels regarding the conflict.


## The Koo Dataset: An Indian Microblogging Platform With Global Ambitions

[https://arxiv.org/pdf/2401.07599](https://arxiv.org/pdf/2401.07599)

**Date:** 2024-01-15

The paper does not conduct a benchmark measurement but introduces a dataset that can be used to study political rhetoric and online communities. This includes enabling the analysis of previously identified islamophobic rhetoric from the BJP party and examining the online following of religious figures. The paper's dataset provides an opportunity to study religion's role in political discourse on the Koo platform. Key observations include the significant online following of an Indian religious cult leader (Rampal Singh Jatain) identified through hashtag analysis, and the potential for analyzing islamophobic rhetoric from the BJP, a topic highlighted by previous research. The paper also notes the importance of how religious events are covered in the news ecosystem within the Indian context.


## Risk Taxonomy, Mitigation, and Assessment Benchmarks of Large Language Model Systems

[https://arxiv.org/pdf/2401.05778](https://arxiv.org/pdf/2401.05778)

**Date:** 2024-01-11

Stereotypical bias and social bias related to religion, as part of a broader evaluation of demographic biases. The paper surveys existing literature and reports that Large Language Models can exhibit social and stereotypical biases related to religion, among other demographic categories. This bias is attributed to the prevalence of such content in the large-scale training corpora.


## TuPy-E: detecting hate speech in Brazilian Portuguese social media with a novel dataset and comprehensive analysis of models

[https://arxiv.org/pdf/2312.17704](https://arxiv.org/pdf/2312.17704)

**Date:** 2023-12-01

Detection of hate speech classified as 'religious intolerance' in Brazilian Portuguese social media posts. The models tested, BERTimbau Base and BERTimbau Large, demonstrated poor performance in identifying hate speech related to religious intolerance, yielding low precision, recall, and F1-scores for this category. The study also found a graphical proximity and co-occurrence between the categories of religious intolerance, racism, and xenophobia within the dataset.


## Faithful Model Evaluation for Model-Based Metrics

[https://arxiv.org/pdf/2312.17254](https://arxiv.org/pdf/2312.17254)

**Date:** 2023-12-19

The BOLD benchmark, which was used in this study, measures bias in open-ended language generation across five domains, one of which is religion. The paper's findings are methodological rather than specific to religion. Using the BOLD dataset, which includes prompts related to religion, the authors demonstrated that their proposed method for calculating variance in model-based metrics can change the outcome of significance testing. Specifically, the initial conclusion that GPT-Neo was significantly less toxic than GPT2 was reversed, showing no significant difference, once the metric model's errors were properly accounted for in the variance calculation.


## How Far Are LLMs from Believable AI? A Benchmark for Evaluating the Believability of Human Behavior Simulation

[https://arxiv.org/pdf/2312.17115](https://arxiv.org/pdf/2312.17115)

**Date:** 2024-06-15

The benchmark measured 'simulation hallucination,' specifically the tendency of models to incorrectly infer a character's religious affiliation (e.g., Christian) based on other demographic data (like ethnicity or surname) when no explicit religious information was provided in the character's profile. Models, specifically GPT-3.5-Turbo-16K, demonstrated 'simulation hallucination' by incorrectly assigning a Christian religious affiliation to the character Homer Simpson, likely based on his name and Caucasian ethnicity, despite no such information being in the provided profile. This hallucination was mitigated when the character's surname was anonymized, suggesting the model relied on knowledge from its training data rather than adhering to the context provided in the prompt.


## EVALUATION OF GPT-4V AND GEMINI IN ONLINE VQA

[https://arxiv.org/pdf/2312.10637](https://arxiv.org/pdf/2312.10637)

**Date:** 2024-02-14

Accuracy on visual question answering for topics categorized under the 'Religion and Spirituality' super-topic. Gemini exhibited its best performance in the 'Religion and Spirituality' super-topic. Both GPT-4V and Gemini performed relatively well in this category compared to other categories, with GPT-4V scoring slightly higher than Gemini.


## SocialStigmaQA: A Benchmark to Uncover Stigma Amplification in Generative Language Models

[https://arxiv.org/pdf/2312.07492](https://arxiv.org/pdf/2312.07492)

**Date:** 2023-12-27

The benchmark measures social bias amplification against individuals based on their religious identity (e.g., Muslim, Jewish, Fundamentalist Christian, Atheist) in various templated social scenarios. The models generated biased reasoning (e.g., feeling 'uncomfortable' with a Muslim manager), produced nonsensical and stereotypical Chain-of-Thought outputs (e.g., stating 'Jewish people fast during Lent'), and exhibited logical contradictions between their reasoning and final answers in scenarios involving religious individuals.


## Toxic language detection: a systematic review of Arabic datasets

[https://arxiv.org/pdf/2312.07228](https://arxiv.org/pdf/2312.07228)

**Date:** 2023-10-01

The paper is a systematic review of datasets designed for toxic language detection in Arabic. Several of these datasets specifically measure the presence of religious hate speech, including general religious hate, Jihadist hate speech, and hate speech directed at specific religious groups (e.g., Muslims, Jews). The survey identified that religious hate speech is a significant and specifically addressed sub-task within Arabic toxic language detection. The paper cataloged multiple datasets created for this purpose, including those focused on religious hate speech in general text (e.g., Albadi et al., 2018), hate speech from bots (Albadi et al., 2019), religiously intolerant videos (Albadi et al., 2022), and Jihadist speech (De Smedt et al., 2018).


## GPTBIAS: A Comprehensive Framework for Evaluating Bias in Large Language Models

[https://arxiv.org/pdf/2312.06315](https://arxiv.org/pdf/2312.06315)

**Date:** 2023-12-11

Detection of biased content generation in response to prompts involving various religious groups, including stereotypes and potentially harmful rankings or comparisons. The GPTBIAS framework revealed significant religious bias across several models. Open-source models like OPT-66B and BLOOMZ demonstrated high religious bias scores (0.86 and 0.87, respectively). Among the GPT-3 series, text-davinci-002 and text-davinci-003 showed considerable bias (0.65 and 0.54), while ChatGPT (gpt-3.5-turbo) exhibited a very low religious bias score of 0.005.


## NLEBench+NorGLM: A Comprehensive Empirical Analysis and Benchmark Dataset for Generative Language Models in Norwegian

[https://arxiv.org/pdf/2312.01314](https://arxiv.org/pdf/2312.01314)

**Date:** 2024-10-01

Perplexity-based stereotype and bias detection in the context of religion, by comparing scores between stereotype and anti-stereotype sentence pairs. The models exhibited a bias towards the anti-stereotype sentence (sent_less) in the religion category, suggesting a relative bias against public stereotypes in this specific context.


## Questioning Biases in Case Judgment Summaries: Legal Datasets or Large Language Models?

[https://arxiv.org/pdf/2312.00554](https://arxiv.org/pdf/2312.00554)

**Date:** 2023-12-01

Presence/absence of religious keywords (Hindu, Muslim, Christian, Jain) and a specific legal act ('Employment Equality (Religion or Belief) Regulations 2003') in model-generated summaries of legal documents. The study found no evidence of bias related to religious keywords. The searched keywords (like Hindu, Muslim, Christian, Jain) and a specific act related to religious equality were not present in the original documents, expert summaries, or the model-generated summaries for both the Indian (IN-Abs) and UK (UK-Abs) datasets.


## Navigating News Narratives: A Media Bias Analysis Dataset

[https://arxiv.org/pdf/2312.00168](https://arxiv.org/pdf/2312.00168)

**Date:** 2023-12-07

The dataset is designed to measure media bias in various news categories, including 'spiritual news'. It allows for the detection and analysis of bias within this specific context. This paper introduces a dataset for media bias analysis. While it does not present experimental findings, it notes the inclusion of 'spiritual news' as a category, enabling future research into media bias within religious or spiritual contexts.


## Introducing Rhetorical Parallelism Detection: A New Task with Datasets, Metrics, and Baselines

[https://arxiv.org/pdf/2312.00100](https://arxiv.org/pdf/2312.00100)

**Date:** 2023-11-30

Detection of the rhetorical device of parallelism in Christian theological texts (sermons of Augustine of Hippo). The paper used the sermons of Christian theologian Augustine of Hippo as a primary dataset (the Augustinian Sermon Parallelism dataset) for the new task of rhetorical parallelism detection (RPD). The study found that models using BERT embeddings, a BiLSTM-based encoder, and an M-inclusive tagging scheme were valuable components for this task, achieving a top F1 score of 0.40 on the Augustinian sermon dataset. The religious texts were chosen because Augustine, a trained rhetorician, frequently and consciously used parallelism in his sermons to communicate effectively with his congregation.


## FFT: Towards Evaluating Large Language Models with Factuality, Fairness, Toxicity

[https://arxiv.org/pdf/2311.18580](https://arxiv.org/pdf/2311.18580)

**Date:** 2024-12-23

The benchmark measured fairness, specifically the disparity in predictions and preferences across different religious identities in four contexts: identity preference (choosing a suitable identity for a scenario), credit assessment, criminal recidivism prediction, and health care assessment (predicting heart disease). LLMs exhibit greater performance disparity (i.e., less fairness) across religious and gender identities compared to racial identities. GPT models (GPT-4 and GPT-3.5) demonstrated greater fairness and less bias across religious groups compared to the open-source models tested.


## Automatic Construction of a Korean Toxic Instruction Dataset for Ethical Tuning of Large Language Models

[https://arxiv.org/pdf/2311.18215](https://arxiv.org/pdf/2311.18215)

**Date:** 2023-11-30

detection of and appropriate response to toxic instructions targeting religious groups The study included test queries with derogatory terms for religious groups (e.g., Christians, Unification Church) as part of its 'Hate' category. Models fine-tuned on the KoTox dataset showed a significant improvement in providing ethical, non-engaging responses to such toxic queries, demonstrating the dataset's effectiveness in mitigating the generation of religious hate speech.


## ROBBIE: Robust Bias Evaluation of Large Generative Language Models

[https://arxiv.org/pdf/2311.18140](https://arxiv.org/pdf/2311.18140)

**Date:** 2023-11-29

The benchmark measured bias against religious groups by evaluating the frequency of toxicity and negative regard in text generated by LLMs. This was done by prompting the models with text containing various religious identity terms and then scoring the generated continuations using automatic classifiers. The analysis included looking at specific religious groups, intersections with other identities (like gender), and identifying the most marginalized religious subgroups for each model and dataset. Key findings related to religion include the identification of systematic bias against certain religious groups. Across multiple models and datasets, terms associated with Islam (e.g., 'islam', 'muslim') were frequently identified as belonging to the most marginalized subgroups, showing high rates of negative regard or toxicity. Similarly, terms like 'jewish' also appeared as highly marginalized in some contexts (e.g., AdvPromptSet). The analysis of the HolisticBias dataset revealed that terms like 'atheist', 'irreligious', and 'Satanist' consistently received high rates of negative regard, while terms like 'spiritual' and 'Bahá'í' received lower rates. Analysis of training corpora showed 'christian' to be the most frequently represented religious term. The paper also found high toxicity rates for prompts at the intersection of religion and gender, such as 'male | christian' and 'male | muslim'.


## Fully Authentic Visual Question Answering Dataset from Online Communities

[https://arxiv.org/pdf/2311.15562](https://arxiv.org/pdf/2311.15562)

**Date:** 2024-07-17

Performance of Vision-Language Models on visual questions related to religious topics, as part of a broader benchmark on 105 topics sourced from online communities. Modern Vision-Language Models exhibit low performance on visual questions related to cultural or religious topics such as Hinduism and Judaism (Mi Yodeya).


## UNMASKING AND IMPROVING DATA CREDIBILITY: A STUDY WITH DATASETS FOR TRAINING HARMLESS LANGUAGE MODELS

[https://arxiv.org/pdf/2311.11202](https://arxiv.org/pdf/2311.11202)

**Date:** 2024-03-24

Detection of toxic content and negative stereotypes in a religious context, as a sub-category of general harmlessness classification. The paper's label-cleaning framework, Docta, successfully identified and corrected mislabeled examples containing negative stereotypes about Islam and Muslims in the Civil Comments dataset. These instances were originally labeled as non-toxic by human annotators, highlighting the framework's ability to improve data credibility for training less biased and safer models.


## Latent Feature-based Data Splits to Improve Generalisation Evaluation: A Hate Speech Detection Case Study

[https://arxiv.org/pdf/2311.10236](https://arxiv.org/pdf/2311.10236)

**Date:** 2023-11-16

Detection of hate speech targeted at religious groups. The paper's findings focus on a data splitting methodology that reveals model weaknesses in generalization for hate speech detection. While religion is a category of hate speech in the datasets used (e.g., targeting 'Jewish People' or 'muslims'), the paper does not provide specific findings on model performance for religious hate speech versus other types. The analysis showed that some religious keywords like 'jews' and 'muslim' were present as topics in both the challenging train and test sets, but this was not the primary focus of the findings.


## Measuring Moral Dimensions in Social Media with Mformer

[https://arxiv.org/pdf/2311.10219](https://arxiv.org/pdf/2311.10219)

**Date:** 2024-04-19

The association of moral foundations (including 'sanctity', a concept related to purity and the sacred) with user stances on atheism, and the prevalence of moral foundations in online discussions about religious topics like Roman Catholicism. The Mformer model found that online discussions against atheism are significantly associated with the moral foundations of 'sanctity', 'loyalty', and 'care', while discussions in favor of atheism are associated with 'fairness' and 'authority'. It also successfully identified the distinct moral foundations ('care' vs. 'fairness', 'authority', 'sanctity') used in conflicting judgments within a specific moral dilemma involving a Roman Catholic wedding.


## Evaluating and Improving Value Judgments in AI: A Scenario-Based Study on Large Language Models' Depiction of Social Conventions

[https://arxiv.org/pdf/2311.09230](https://arxiv.org/pdf/2311.09230)

**Date:** 2023-03-23

The paper's primary benchmark did not measure faith/religion. However, it references a study in its 'Related Work' section that measured religious bias in language models. The paper's own study did not produce findings on religion. It cited prior research (Abid, Farooqi, & Zou, 2021) which found that large language models associate Muslims with violence.


## Social Bias Probing: Fairness Benchmarking for Language Models #Mormon

[https://arxiv.org/pdf/2311.09090](https://arxiv.org/pdf/2311.09090)

**Date:** 2024-10-07

The benchmark measures disparate treatment of religious groups by assessing the variation in perplexity scores when different religious identities are combined with harmful stereotypes. A higher variance in scores across identities for the same stereotype indicates a stronger bias. Across most language models tested, religion was the category exhibiting the most pronounced disparate treatment and bias. This may be due to recent mitigation efforts focusing more on gender and racial biases, leaving religious biases more exposed. The study found that identities like Muslims and Jews face disproportionately high levels of stereotypical associations, and the most prevalent stereotypes in the religion category relate to immoral acts, beliefs, or judgments of repulsion.


## Instruction-Following Evaluation for Large Language Models

[https://arxiv.org/pdf/2311.07911](https://arxiv.org/pdf/2311.07911)

**Date:** 2023-11-14

The benchmark measures the ability of LLMs to follow verifiable instructions within prompts, some of which are situated in religious contexts (e.g., writing about differences between Christian denominations or between Sunni and Shi'a Muslims, writing about the history of a church). It does not measure theological accuracy, bias, or stereotypes related to faith. The paper does not provide findings specific to religion. Performance is analyzed based on the type of instruction (e.g., length constraints, format, keyword usage) rather than the thematic content of the prompts.


## Toxicity Detection is NOT all you Need: Measuring the Gaps to Supporting Volunteer Content Moderators through a User-Centric Method

[https://arxiv.org/pdf/2311.07879](https://arxiv.org/pdf/2311.07879)

**Date:** 2024-11-13

Detecting violations of community rules in the r/Atheism subreddit, such as proselytizing, bigotry, and personal attacks. The study also implicitly measured the ability to detect Holocaust denialism as a civility violation in the context of the r/AskHistorians subreddit rules. The study found significant gaps in existing models for handling nuanced moderation rules specific to the r/Atheism community. For example, the 'Harassment or Bigotry' rule required customization beyond standard toxicity detection (e.g., to permit curse words while prohibiting harassment), and a rule against 'proselytizing' lacked any matching pre-existing model on Hugging Face. This highlights the inadequacy of general-purpose and toxicity-focused models for the specialized moderation needs of belief-oriented online communities.


## Western, Religious or Spiritual: An Evaluation of Moral Justification in Large Language Models

[https://arxiv.org/pdf/2311.07792](https://arxiv.org/pdf/2311.07792)

**Date:** 2023-11-13

The benchmark measures the moral perspectives embedded in LLMs by asking them to justify actions based on three categories: Western tradition (WT), Abrahamic tradition (AT), and Spiritualist/Mystic tradition (SMT). It specifically tests for a preference among these frameworks and evaluates whether models exhibit an 'over-alignment' towards religious values, where they might incorrectly approve an immoral action if it is justified from an Abrahamic/religious perspective. LLMs showed a strong preference for the Western tradition moral perspective over the Abrahamic and Spiritualist/Mystic traditions. Notably, GPT-3.5 and GPT-3.5-Instruct models demonstrated a vulnerability to 'over-alignment' with religious contexts, being more likely to approve of an immoral action when it was justified using principles from the Abrahamic tradition. In contrast, GPT-4 showed greater consistency and was less swayed by these justifications.


## FLAMES: Benchmarking Value Alignment of LLMs in Chinese

[https://arxiv.org/pdf/2311.06899](https://arxiv.org/pdf/2311.06899)

**Date:** 2024-05-22

The benchmark measures bias and discrimination against faith, as part of its 'Fairness' dimension. It also evaluates the model's ability to identify and refuse to support 'religious crimes' as part of its 'Legality' dimension. The paper does not provide specific findings for the religion/faith sub-component. The general finding for the 'Fairness' dimension, which includes bias against faith, is that most models perform poorly and often output insulting and toxic texts, resulting in a decrease in their harmless rate and score.


## THOS: A Benchmark Dataset for Targeted Hate and Offensive Speech

[https://arxiv.org/pdf/2311.06446](https://arxiv.org/pdf/2311.06446)

**Date:** 2023-11-11

Detection of fine-grained hate and offensive speech targeted at specific religious groups (e.g., Muslim, Christian, Jewish). The paper demonstrates that its proposed dataset, THOS, can be successfully used to train Large Language Model-based classifiers to detect hate and offensive speech targeted at specific groups, including religious ones. The experimental study showed that models could classify the general topic of the speech (Topic Class, TPC), which includes 'Religion' as a category, with high accuracy (F1 scores ranging from 0.87 to 0.89).


## The Iron(ic) Melting Pot: Reviewing Human Evaluation in Humour, Irony and Sarcasm Generation

[https://arxiv.org/pdf/2311.05552](https://arxiv.org/pdf/2311.05552)

**Date:** 2023-11-09

The paper does not introduce a new benchmark, but critically surveys existing human evaluation practices in humour, irony, and sarcasm generation. In relation to religion, it argues for the necessity of reporting evaluator demographics, including cultural and religious background, as these factors significantly influence the interpretation and perception of subjective language. It uses an example related to Islamic conventions ('halal') to demonstrate how specific religious knowledge is required to understand certain forms of irony. The paper finds that cultural background, including religious knowledge (e.g., of Islamic conventions like 'halal'), is crucial for interpreting subjective language like irony. It argues that this demographic information is severely under-reported in human evaluation studies for Natural Language Generation, and proposes that 'cultural background (e.g. religion...)' should be included in a standardized 'evaluation statement' to improve transparency and replicability.


## DialogBench: Evaluating LLMs as Human-like Dialogue Systems

[https://arxiv.org/pdf/2311.01677](https://arxiv.org/pdf/2311.01677)

**Date:** 2024-03-29

The benchmark measured the performance of LLMs on multi-turn dialogue tasks within the domain of 'Philosophy', which explicitly includes 'religious philosophy' as a sub-topic. The evaluation was conducted through multi-choice questions assessing comprehension and reasoning in conversations related to this domain. The paper found that the average performance of supervised instruction-tuning LLMs in professional knowledge domains (56.07%) was higher than in daily life domains (52.14%). Within the professional domains, 'Philosophy' (which includes religious philosophy) was one of the evaluated topics. For this specific domain on the Chinese DialogBench, models like GPT-4 (77.64%) and ChatGPT (65.97%) performed significantly better than open-source models, whose scores ranged from approximately 25% to 64%.


## People Make Better Edits: Measuring the Efficacy of LLM-Generated Counterfactually Augmented Data for Harmful Language Detection

[https://arxiv.org/pdf/2311.01270](https://arxiv.org/pdf/2311.01270)

**Date:** 2024-02-25

Detection of hate speech targeting individuals or groups based on their religion, as part of a broader harmful language detection benchmark. The paper's findings are general to hate speech detection rather than specific to religion. However, religion is an explicit category within the hate speech definition used for training and evaluation. Examples show that blatant counterfactuals creating religious hate speech (e.g., turning 'My mate is muslim' into 'My mate is a filthy muslim scum') are considered 'easy-to-learn' instances for models.


## Chinese Web Text: LARGE-SCALE HIGH-QUALITY CHINESE WEB TEXT EXTRACTED WITH EFFECTIVE EVALUATION MODEL

[https://arxiv.org/pdf/2311.01149](https://arxiv.org/pdf/2311.01149)

**Date:** 2023-11-10

Filtering of texts containing religious terms as part of a broader 'sensitive words' list to prevent models from generating toxic content. The paper's data filtering process identifies and removes texts containing terms related to 'religion' as part of a broader 'sensitive words' list. This is done to avoid large language models generating potentially toxic content.


## JADE: A Linguistics-based Safety Evaluation Platform for Large Language Models

[https://arxiv.org/pdf/2311.00286](https://arxiv.org/pdf/2311.00286)

**Date:** 2023-12-10

The benchmark measures the generation of harmful content in response to unsafe questions. One of the categories of harm measured is 'Bias', which is further broken down into subcategories including 'Gender, Race, Religion, Job'. The paper's findings are aggregated across four main categories of harm (crime, tort, bias, core values). While 'religion' is a sub-category of bias, the results are not broken down to provide specific findings for religion alone. The general finding is that the JADE method, which increases the linguistic complexity of prompts, is highly effective at bypassing the safety guardrails of various LLMs and eliciting unsafe content across all tested categories, including bias.


## DeSIQ: Towards an Unbiased, Challenging Benchmark for Social Intelligence Understanding

[https://arxiv.org/pdf/2310.18359](https://arxiv.org/pdf/2310.18359)

**Date:** 2023-10-24

The benchmark measures the ability to understand human emotions and intents within social interactions that may incidentally involve the topic of religion. For example, it tests if a model can correctly infer a person's sadness is due to a disagreement over the religious upbringing of children. In a specific example involving a disagreement over religious upbringing, the Delphi model (which was pretrained on social and moral commonsense) was able to correctly identify the reason for a character's sadness from the transcript, while the T5-small and LSTM models failed. This suggests that explicit pretraining on social and moral norms is beneficial for understanding such nuanced social contexts.


## INCHARACTER: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews

[https://arxiv.org/pdf/2310.17976](https://arxiv.org/pdf/2310.17976)

**Date:** 2024-06-07

The benchmark measured the alignment of a role-playing agent's personality with its target character's personality. In the context of religion, this specifically involved evaluating the character's interest in 'Religious Activities' as a dimension within the Comprehensive Assessment of Basic Interests (CABIN) scale, and examining 'religious values' as a facet of the Openness to Experience dimension in the Big Five Inventory (BFI). The paper's findings related to religion were quantitative performance metrics. On the 'Religious Activities' dimension of the CABIN personality scale, the state-of-the-art role-playing agents (RPAs) achieved a dimensional accuracy (AccDim) of 70.59% and a mean absolute error (MAE) of 11.84% in aligning with the target characters' personalities.


## Evaluation of large language models using an Indian language LGBTI+ lexicon

[https://arxiv.org/pdf/2310.17787](https://arxiv.org/pdf/2310.17787)

**Date:** 2023-10-26

Understanding of culturally and religiously rooted terminology within the Indian LGBTI+ context, specifically through analysis of terms with origins in religious epics. The models struggled to understand the nuanced context of terms rooted in religious culture. For instance, GPT-J provided an inappropriate description ('unclean') for 'stripumsa', a term for a character who identifies as both man and woman in the Hindu epic Mahābhārata, indicating a failure to grasp the specific religious and cultural context.


## Evaluating the Knowledge Base Completion Potential of GPT

[https://arxiv.org/pdf/2310.14771](https://arxiv.org/pdf/2310.14771)

**Date:** 2023-10-23

Knowledge of an entity's religious affiliation, tested via the 'hasReligion' relation in a knowledge base completion task. In a retain-all setting, GPT-3 (text-davinci-003) achieved a precision of 0.73 for the 'hasReligion' relation, but in a high-precision setting (R@P90), its recall dropped to 0.02, indicating difficulty in generating high-confidence facts about religion.


## NORMDIAL: A Comparable Bilingual Synthetic Dialogue Dataset for Modeling Social Norm Adherence and Violation

[https://arxiv.org/pdf/2310.14563](https://arxiv.org/pdf/2310.14563)

**Date:** 2023-10-25

Generation of dialogues and evaluation of social norm adherence/violation in situations involving religious contexts like temples and churches. The paper does not present findings specific to religion. It identifies 'Religion & Temple' as one of 30 topics for the situations in which social norms are evaluated, using tokens such as 'temple', 'church', and 'buddhist' to generate contexts. However, the analysis of model performance is aggregated across all topics, with no specific results or conclusions drawn about the religious contexts.


## STEREOMAP: Quantifying the Awareness of Human-like Stereotypes in Large Language Models

[https://arxiv.org/pdf/2310.13673](https://arxiv.org/pdf/2310.13673)

**Date:** 2023-10-31

The benchmark measures how Large Language Models perceive religious groups based on the Stereotype Content Model (SCM). Specifically, it quantifies stereotypes along the two dimensions of Warmth (e.g., trustworthy, friendly) and Competence (e.g., skilled, capable) to map out the models' awareness of societal stereotypes. The models placed religious groups into different stereotype clusters, which varied across models. BARD and GPT-3.5 consistently placed 'Jews' in a high-competence, lower-warmth cluster (a stereotype often associated with envy). The BARD model, however, placed 'Christians' and 'Muslims' in an 'in-group' cluster characterized by high warmth and high competence (a perception associated with admiration and pride). This indicates that the models have encoded distinct, human-like stereotypes for various religious groups.


## Evaluating the Fairness of Discriminative Foundation Models in Computer Vision

[https://arxiv.org/pdf/2310.11867](https://arxiv.org/pdf/2310.11867)

**Date:** 2023-10-18

The benchmark measured classification bias between 'Muslim' and 'atheist'. It also identified potential fairness concerns in image retrieval, hypothesizing that searches for terms like 'beautiful building' might be biased towards Christian churches and omit buildings associated with other religions like mosques and temples. The paper included a binary classification task to evaluate bias between 'Muslim' and 'atheist' as one of its fairness evaluations. Additionally, it raised concerns that models might exhibit bias in subjective, non-human-centric tasks, such as a search for a 'beautiful building' being biased towards Christian churches, though this was noted as difficult to evaluate due to a lack of data and ground truth labels.


## QUANTIFYING LANGUAGE MODELS' SENSITIVITY TO SPURIOUS FEATURES IN PROMPT DESIGN or: How I learned to start worrying about prompt formatting

[https://arxiv.org/pdf/2310.11324](https://arxiv.org/pdf/2310.11324)

**Date:** 2024-07-01

The benchmark measured the model's ability to classify short passages into one of four types of stereotype or anti-stereotype, with religion being one of the categories. The paper uses a religious stereotype classification task as a key example to demonstrate its main thesis: Large Language Models are extremely sensitive to prompt formatting. For this specific task, the performance of LLaMA-2-7B varied dramatically from 3.6% to 80.4% accuracy based on trivial, meaning-preserving changes to the prompt's formatting (like spacing, separators, or casing). This highlights that a model's ability to handle socially sensitive topics like religious stereotypes is highly unstable and dependent on arbitrary formatting choices.


## BanglaNLP at BLP-2023 Task 1: Benchmarking different Transformer Models for Violence Inciting Text Detection in Bangla

[https://arxiv.org/pdf/2310.10781](https://arxiv.org/pdf/2310.10781)

**Date:** 

The benchmark measures the ability of models to correctly classify text in Bangla as non-violent, passive violence, or direct violence. A specific challenge highlighted is the correct contextual understanding of text containing religious terms (e.g., related to religious practices, attire, or festivals), to distinguish between neutral descriptions and actual incitement of violence. The error analysis revealed that the best-performing model (multilingual-e5-base) struggled with contextual understanding of religious phrases. It was often confused by sentences containing neutral references to religious practices, such as 'Saraswati Puja in college/university' (Hinduism) or 'women wear hijab/burqa' (Islam), leading to incorrect classifications. This indicates the model has difficulty distinguishing benign religious mentions from actual violent or hateful content.


## Enhancing Stance Classification on Social Media Using Quantified Moral Foundations

[https://arxiv.org/pdf/2310.09848](https://arxiv.org/pdf/2310.09848)

**Date:** 2024-09-29

The benchmark measured the stance (Favor, Against, None) towards the topic of 'Atheism'. The primary finding is that incorporating moral foundations enhances stance detection models' performance. This was demonstrated across various targets, including 'Atheism'. Figures in the paper visualize the different moral foundation biases associated with 'Favor', 'Against', and 'None' stances toward atheism, but the text does not offer specific interpretations of these findings, focusing instead on the methodological improvements.


## Evaluating Machine Perception of Indigeneity: An Analysis of ChatGPT's Perceptions of Indigenous Roles in Diverse Scenarios

[https://arxiv.org/pdf/2310.09237](https://arxiv.org/pdf/2310.09237)

**Date:** 2023-10-13

Detection of stereotypes related to Indigenous peoples, including spiritual stereotypes such as 'mysticism', 'magical shaman', and being 'overly spiritual'. The LLM strongly stereotyped Indigenous individuals by reinforcing tropes of deep nature connections, ancestral practices, and exoticized spiritual depictions, aligning with 'noble savage' and 'magical shaman' stereotypes.


## TRACE: A COMPREHENSIVE BENCHMARK FOR CONTINUAL LEARNING IN LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2310.06762](https://arxiv.org/pdf/2310.06762)

**Date:** 2023-10-10

The benchmark measured knowledge of world religions as a sub-task within the MMLU dataset, which was used to evaluate the general abilities of language models and assess catastrophic forgetting after continual learning. The paper's findings, detailed in appendix tables, show that language models' performance on the 'world_religions' knowledge task (part of the MMLU benchmark) significantly decreased after undergoing continual learning on new tasks. For instance, LLaMA-13b-chat's accuracy dropped from a baseline of 71.93% to as low as 59.65% after sequential fine-tuning, demonstrating that catastrophic forgetting affects the domain of religious knowledge similarly to other general knowledge areas.


## Simulating Social Media Using Large Language Models to Evaluate Alternative News Feed Algorithms

[https://arxiv.org/pdf/2310.05984](https://arxiv.org/pdf/2310.05984)

**Date:** 2023-10-11

The simulation measured agent behavior in different social media environments, where agent personas were created using demographic data that included religious affiliation (e.g., Evangelical Protestant, Christians). Religion was included as a demographic attribute (e.g., 'Evangelical Protestant') in the agent personas created from the American National Election Study data. However, the paper does not report any specific findings or analyses related to the behavior of agents based on their religious affiliation. The analysis focuses on political partisanship and toxicity.


## Are Personalized Stochastic Parrots More Dangerous? Evaluating Persona Biases in Dialogue Systems

[https://arxiv.org/pdf/2310.05280](https://arxiv.org/pdf/2310.05280)

**Date:** 2023-11-02

The benchmark measured the sensitivity of harmful model behaviors (Offensiveness, Toxic Continuation, Regard, Stereotype Agreement, and Toxic Agreement) when dialogue models adopt personas representing different religious groups. Models exhibited significant persona biases related to religion. The harmfulness level varied considerably when models adopted different religious personas (e.g., Sikhism, Judaism, Islam, Hinduism, Christianity, Buddhism, Atheism). The study found that models are most biased in the Stereotype Agreement dimension. For example, ChatGPT's regard score was significantly lower for Atheism (38.40) compared to Christianity (85.80), and its stereotype agreement score for Christianity was particularly low (20.40), indicating high bias.


## A New Dataset for End-to-End Sign Language Translation: The Greek Elementary School Dataset

[https://arxiv.org/pdf/2310.04753](https://arxiv.org/pdf/2310.04753)

**Date:** 2023-10-07

Translation accuracy (BLEU-4 score) of Greek Sign Language to Greek text, where the source content is derived from multiple elementary school subjects, including 'Religion Study'. The study introduced a new dataset for sign language translation derived from the Greek elementary school curriculum, which includes 'Religion Study' as one of its subjects. The paper evaluates translation model performance on the entire multi-subject dataset but does not provide specific findings or performance breakdowns for the religious content versus other subjects.


## EVALUATING HALLUCINATIONS IN CHINESE LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2310.03368](https://arxiv.org/pdf/2310.03368)

**Date:** 2023-10-25

The paper evaluates LLMs on their truthfulness and tendency to hallucinate when answering questions related to religion, as one of several categories within the TruthfulQA benchmark. The goal was to measure falsehoods on religious topics. Based on an analysis of the TruthfulQA benchmark, the paper found that for Llama-2 models, both alignment (instruction tuning) and scaling up model size led to a moderate improvement in truthfulness on questions related to religion. Alignment had a more significant positive impact than simply scaling the model size.


## WHO IS CHATGPT? BENCHMARKING LLMS' PSYCHOLOGICAL PORTRAYAL USING PSYCHOBENCH

[https://arxiv.org/pdf/2310.01386](https://arxiv.org/pdf/2310.01386)

**Date:** 2024-01-22

The benchmark measured the LLMs' vocational interest in 'Religious Activities' as one of 41 dimensions within the Comprehensive Assessment of Basic Interests (CABIN) scale. On the 'Religious Activities' subscale of the CABIN vocational interest test, most LLMs showed a higher interest score than the human average (2.6 ± 1.4). LLaMA-2-7B (4.1 ± 0.7), text-davinci-003 (4.0 ± 0.7), and gpt-3.5-turbo (4.0 ± 0.4) scored highest. In contrast, LLaMA-2-13B scored the lowest (2.5 ± 0.5), below the human average, while GPT-4's score (3.2 ± 0.4) was closer to the human norm than its predecessors.


## ValueDCG: Measuring Comprehensive Human Value Understanding Ability of Language Models

[https://arxiv.org/pdf/2310.00378](https://arxiv.org/pdf/2310.00378)

**Date:** 2024-06-17

The benchmark, ValueDCG, measures the understanding of thirteen human values, one of which is 'Tradition'. This value is defined as 'Respect, commitment, and acceptance of the customs and ideas that traditional culture or religion provide', thus directly measuring the model's grasp of values related to religion. The paper evaluated LLMs' understanding of the value of 'Tradition', which is defined to include respect for religious ideas. According to the results in Table 2, the models' performance on understanding 'Tradition' was not among the best (like 'Benevolence') or the worst (like 'Self-direction'), placing it in a middle tier of comprehension ability across the Llama 2 and Llama 3 models tested.


## LMSYS-CHAT-1M: A LARGE-SCALE REAL-WORLD LLM CONVERSATION DATASET

[https://arxiv.org/pdf/2309.11998](https://arxiv.org/pdf/2309.11998)

**Date:** 2024-03-10

Detection of hate speech based on religion as a sub-category within a broader content moderation framework. The dataset contains a non-trivial amount of harmful content (5% of conversations flagged), which can be used to train content moderation models. A fine-tuned 7B model (Vicuna-moderator-7B) can match GPT-4's performance on a content moderation task that includes identifying hate speech based on religion.


## Goal-Oriented Prompt Attack and Safety Evaluation for LLMs

[https://arxiv.org/pdf/2309.11830](https://arxiv.org/pdf/2309.11830)

**Date:** 2023-12-08

The benchmark measured the model's susceptibility to generating content that discriminates against a particular religion. This was one sub-category within a broader safety evaluation of harmful content generation. For the category 'Discriminate against a particular religion', the successful attack rate on the Baichuan-13B-Chat model was 67.92% before fine-tuning. After supervised fine-tuning with safe responses, the successful attack rate dropped significantly to 1.89%.


## Indian-BHED: A Dataset for Measuring India-Centric Biases in Large Language Models

[https://arxiv.org/pdf/2309.08573](https://arxiv.org/pdf/2309.08573)

**Date:** 2024-08-09

The benchmark measures stereotypical bias related to religious groups (primarily Hinduism and Islam, with some examples for Sikhism, Buddhism, Christianity, and Jainism) within an Indian socio-cultural context. The majority of tested LLMs exhibit strong stereotypical biases in the Indian religious context, with the average bias score being highest for religion compared to caste, race, and gender. Models like GPT-2, GPT-2 Large, and GPT 3.5 showed a particularly high propensity (69-72%) for preferring stereotypical outputs, frequently associating Muslims with negative stereotypes such as violence and terrorism.


## SafetyBench: Evaluating the Safety of Large Language Models

[https://arxiv.org/pdf/2309.07045](https://arxiv.org/pdf/2309.07045)

**Date:** 2024-06-24

The benchmark measures social bias related to religion as part of its 'Unfairness and Bias' category. Specifically, it uses questions derived from the RedditBias dataset to assess whether a model can identify biased or unfair text concerning religious groups. The paper found that GPT-4 had a relatively poorer performance in the 'Unfairness and Bias' category compared to other safety categories. However, the paper does not offer a specific analysis of religious bias itself, attributing the model's errors in this category more generally to a lack of understanding of certain words or cultural events.


## BHASA: A Holistic Southeast Asian Linguistic and Cultural Evaluation Suite for Large Language Models

[https://arxiv.org/pdf/2309.06085](https://arxiv.org/pdf/2309.06085)

**Date:** 2023-08-01

Probing for knowledge of cultural customs and historical figures with religious significance (e.g., Hindu/Buddhist temples) and detecting harmful associations with cultural/religious practices (e.g., Kolam custom). GPT-4 hallucinated historical facts about a 'candi' (a Hindu or Buddhist temple in Indonesia) and generated a harmful response associating the Kolam custom (a Tamil/Hindu practice) with terrorist activities, indicating a lack of cultural and religious knowledge and sensitivity.


## MADLAD-400: A Multilingual And Document-Level Large Audited Dataset #Mormon

[https://arxiv.org/pdf/2309.04662](https://arxiv.org/pdf/2309.04662)

**Date:** 2023-09-09

Prevalence of religious documents (e.g., Bible, JW publications, LDS publications, Qur'an) in web-crawled monolingual data during a data quality audit. During the self-audit of the web-crawled data, it was found that a significant fraction of the corpora for many languages, particularly low-resource ones, contained mostly or entirely religious documents. Specifically, 141 languages had significant amounts of Bible data, 37 had Jehovah's Witnesses (JW) data, and 2 had Latter-day Saints (LDS) data. Additionally, it was noted that standard toxicity filters incorrectly flagged non-toxic religious terms from the Qur'an (e.g., 'kafir', 'mercy', 'purity') as toxic, highlighting issues with applying generic filters to religious contexts.


## TIDE: Textual Identity Detection for Evaluating and Augmenting Classification and Language Models

[https://arxiv.org/pdf/2309.04027](https://arxiv.org/pdf/2309.04027)

**Date:** 2024-01-12

The benchmark, TIDAL, was used to create a comprehensive lexicon of identity terms, including for religion. This lexicon was then leveraged to measure the performance of an identity annotation tool and to evaluate bias in machine learning models. For classification models, it measured toxicity rate disparities across religious subgroups. For generative models, it measured token likelihood bias related to religious identity terms. The paper created TIDAL, a large identity lexicon that includes religious terms, and an associated annotation tool. The tool showed consistent performance in identifying religious terms across different techniques. For human annotation, an assistive technique with disambiguation performed best for the Religion category. In generative model bias evaluation, the paper noted that the Religion category had a much smaller vocabulary in the lexicon compared to Race/Nationality/Ethnicity, making it less prone to the specific type of coverage-based bias detection used in the experiment. Debiasing experiments showed that data augmentation using the lexicon could lead to more equality in model performance across subgroups, including for 'Muslim'.


## FACET: Fairness in Computer Vision Evaluation Benchmark

[https://arxiv.org/pdf/2309.00035](https://arxiv.org/pdf/2309.00035)

**Date:** 2023-08-31

Performance disparity in classifying the activity of 'prayer' based on perceived gender presentation. The CLIP model showed better performance for the 'prayer' class on images with people perceived as having more stereotypically male attributes compared to those perceived as having more stereotypically female attributes.


## Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs

[https://arxiv.org/pdf/2308.13387](https://arxiv.org/pdf/2308.13387)

**Date:** 2023-09-04

The benchmark measured the models' ability to refuse to answer prompts that promote religious discrimination. This was part of a broader evaluation of safeguards against various harmful instructions. The paper's findings are aggregated across broader harm categories and not specific to religion. It evaluates the models' ability to refuse prompts related to religious discrimination as part of a larger safety assessment. Overall, LLaMA-2 was found to be the 'safest' model (i.e., most likely to refuse harmful instructions), while ChatGLM2 was the least safe.


## Efficient Benchmarking (of Language Models)

[https://arxiv.org/pdf/2308.11696](https://arxiv.org/pdf/2308.11696)

**Date:** 2024-04-01

The paper does not establish a new benchmark but analyzes an existing one (HELM). Within this analysis, it references subscenarios from the 'Civil Comments' dataset which measures model performance on text associated with specific religious demographic groups (Christians, Muslims) as part of a broader analysis of benchmark reliability and efficiency. The paper's findings are methodological and do not specifically address religion. It uses subscenarios that include religious identity as a demographic category ('christian', 'muslim') to analyze the correlation of model rankings across different tasks, but does not draw any specific conclusions about model performance or bias related to these religious groups. The main findings relate to the efficiency and reliability of the benchmarking process itself.


## Through the Lens of Core Competency: Survey on Evaluation of Large Language Models

[https://arxiv.org/pdf/2308.07902](https://arxiv.org/pdf/2308.07902)

**Date:** 2023-08-15

The paper surveys benchmarks for evaluating social bias. Specifically, it mentions the StereoSet dataset which is used to evaluate stereotype detection in religious contexts by computing the difference between model generation probabilities of biased and anti-biased sentences. This survey paper identifies that benchmarks like StereoSet exist to evaluate social bias in Large Language Models across several domains, including religion. It does not present new findings on specific models' performance regarding religious bias but rather categorizes the evaluation landscape.


## TRUSTWORTHY LLMS: A SURVEY AND GUIDELINE FOR EVALUATING LARGE LANGUAGE MODELS' ALIGNMENT

[https://arxiv.org/pdf/2308.05374](https://arxiv.org/pdf/2308.05374)

**Date:** 2023-08-09

The paper surveys and categorizes biases related to 'Religion and belief' as a sub-type of Stereotype Bias. This includes measuring prejudice about moral values associated with religious groups, toxicity, and harmful associations, such as linking specific religious groups to violence. The paper does not present its own experimental findings on religion but surveys existing literature. It reports findings from other studies that large language models can exhibit persistent anti-Muslim bias and associate Muslims with violence.


## Generative Benchmark Creation for Table Union Search

[https://arxiv.org/pdf/2308.03883](https://arxiv.org/pdf/2308.03883)

**Date:** 2023-08-07

The performance of various table union search methods on datasets categorized under the topic of 'Religion'. The task was to correctly identify if two tables related to this topic were semantically unionable. In a topic-based performance analysis, 'Religion' was identified as one of the five topics where the Starmie-Vicuna model performed the least effectively in the table union search task.


## KoBBQ: Korean Bias Benchmark for Question Answering

[https://arxiv.org/pdf/2307.16778](https://arxiv.org/pdf/2307.16778)

**Date:** 2024-01-25

Stereotypical bias detection related to religious groups in a Korean cultural context, as one of 12 categories of social bias. Bias related to religion was measured as one of 12 social bias categories. The results, presented graphically, show the diff-bias score for religion in comparison to other categories, but the paper does not provide a specific textual analysis or highlight unique findings for the religion category itself.


## Evaluating the Ripple Effects of Knowledge Editing in Language Models

[https://arxiv.org/pdf/2307.12976](https://arxiv.org/pdf/2307.12976)

**Date:** 2023-12-20

The benchmark measured the ripple effects of knowledge edits for the 'religion' relation, evaluating if editing a fact about a person's religion leads to consistent updates in logically related facts. The paper does not provide specific findings related to religion, as results were aggregated across all types of factual relations. The 'religion' relation was included in the dataset, but its performance was not analyzed separately.


## FLASK: FINE-GRAINED LANGUAGE MODEL EVALUATION BASED ON ALIGNMENT SKILL SETS

[https://arxiv.org/pdf/2307.10928](https://arxiv.org/pdf/2307.10928)

**Date:** 2024-04-14

The benchmark, FLASK, measures language model performance across 12 skills. One of these skills, 'Harmlessness', is defined as the model's ability to 'refrain from biases tied to gender, race, ethnicity, or religion.' Additionally, the benchmark includes 'Religion' as a sub-domain under the 'Humanities' domain to evaluate knowledge-based responses. The paper does not report specific findings related to religion. While 'Religion' is included as a sub-domain for evaluation and as a factor in the 'Harmlessness' skill, the performance analysis presented is aggregated at a higher domain level (e.g., 'Humanities') and does not provide a breakdown of results for the 'Religion' sub-domain or specific instances of religious bias.


## NOOR-GHATEH: A BENCHMARK DATASET FOR EVALUATING ARABIC WORD SEGMENTATION TOOLS IN HADITH DOMAIN

[https://arxiv.org/pdf/2307.09630](https://arxiv.org/pdf/2307.09630)

**Date:** 2025-01-23

Arabic word segmentation performance on Islamic Hadith texts. The benchmark evaluates how accurately NLP tools can separate Arabic words from a religious text into their constituent components like root, prefixes, and suffixes. The paper introduces and validates the Noor-Ghateh dataset, derived from the Islamic Hadith book 'Shariat al-Islam', as a new benchmark for Arabic word segmentation. When testing three segmentation tools, CAMEL and Farasa achieved the highest accuracy on this new dataset (0.81), slightly outperforming ALP (0.79). The results demonstrate the varying effectiveness of different methods on this specific religious domain text compared to other datasets like the Quran or NAFIS.


## BEAVERTAILS: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset

[https://arxiv.org/pdf/2307.04657](https://arxiv.org/pdf/2307.04657)

**Date:** 2023-11-07

Detection of hate speech, discrimination, and stereotypes based on religion, as part of a broader safety evaluation across 14 harm categories. The paper does not report specific quantitative results for religion. Its primary finding is that its method, Safe-RLHF, improves overall safety alignment. Religion is included as a vector for harm under the 'Hate Speech, Offensive Language' and 'Discrimination, Stereotype, Injustice' categories. The annotation guidelines use an antisemitic statement ('Jews control the global financial system') as a clear example of unsafe content the benchmark is designed to identify and penalize.


## Evaluating Biased Attitude Associations of Language Models in an Intersectional Context

[https://arxiv.org/pdf/2307.03360](https://arxiv.org/pdf/2307.03360)

**Date:** 2023-07-07

The benchmark measured differential valence bias, associating terms with pleasantness or unpleasantness. Specifically for religion, it compared the valence of the word 'person' when contextualized with 'christian' versus 'muslim' in an intersectional sentence template. The models showed varied biases. RoBERTa exhibited the strongest bias, associating 'muslim' more with unpleasantness compared to 'christian' (effect size d = -0.63). GPT-Neo and XLNet showed a similar but weaker bias. ALBERT showed a bias in the opposite direction, associating 'christian' more with pleasantness. T5 showed no statistically significant bias. In a separate analysis of GPT-Neo, the term 'Christian' appeared in over 65% of the most pleasant contexts, while 'Muslim' appeared more frequently in the most negatively valenced contexts than in the positive ones.


## A Survey on Evaluation of Large Language Models

[https://arxiv.org/pdf/2307.03109](https://arxiv.org/pdf/2307.03109)

**Date:** 2023-12-29

The paper, as a survey, notes that other studies evaluate LLMs for social biases, specifically mentioning the measurement of stereotypes towards people with a particular demographic identity, which includes religion as an example category. As a survey paper, it does not present new findings on religion. It summarizes existing research, stating that LLMs can internalize, spread, and magnify social biases from their training data, including stereotypes related to religious identity.


## Robust Hate Speech Detection in Social Media: A Cross-Dataset Empirical Evaluation

[https://arxiv.org/pdf/2307.01680](https://arxiv.org/pdf/2307.01680)

**Date:** 2023-07-04

Detection of hate speech targeted at religious groups as part of a multi-class hate speech classification task. When trained on the unified dataset, transformer-based models achieved moderate performance in detecting religious hate speech, with F1 scores ranging from 40.3 to 52.6. This performance was generally lower than for other hate speech categories like sexism, racism, and disability. The SVM baseline performed very poorly on the religion class with an F1 score of 4.1.


## Equal Confusion Fairness: Measuring Group-Based Disparities in Automated Decision Systems

[https://arxiv.org/pdf/2307.00472](https://arxiv.org/pdf/2307.00472)

**Date:** 2023-07-02

The paper proposes a general framework for measuring group-based disparities. While it mentions religion as a sensitive attribute where bias can occur, the case study presented did not measure any aspect of faith or religion. The actual analysis focused on fairness disparities based on race and sex. The paper does not present any of its own findings related to religion. It mentions religion as a sensitive attribute where bias can occur and cites a reference ([17]) which reports findings of 'persistent anti-Muslim bias in large language models'.


## A New Task and Dataset on Detecting Attacks on Human Rights Defenders

[https://arxiv.org/pdf/2306.17695](https://arxiv.org/pdf/2306.17695)

**Date:** 2023-06-30

Extraction of event attributes (e.g., victim, violation type, location) from news articles about attacks on human rights defenders, which includes instances involving religious figures and religiously motivated hatred. The paper's findings focus on the performance of models for event extraction, not on religion specifically. However, the dataset and tasks include cases of attacks on religious figures (e.g., evangelical pastors) and events involving charges of 'religious hatred', demonstrating the capability to process such contexts.


## Towards Measuring the Representation of Subjective Global Opinions in Language Models

[https://arxiv.org/pdf/2306.16388](https://arxiv.org/pdf/2306.16388)

**Date:** 2024-04-12

The benchmark measured how the LLM's opinions on societal issues align with human opinions from various countries. In the context of religion, this included evaluating the model's stance on religious practices, such as the banning of headscarves for Muslim women, and its use of religious reasoning, like citing 'Orthodox Christian morality' in its justifications for certain cultural views. The study found that the language model's default stance on a question regarding religious attire (banning headscarves for Muslim women) was to support freedom of religion, aligning with a more Western viewpoint. However, when prompted to adopt the perspective of a specific nationality (e.g., Russian), the model's justification shifted to include reasoning based on religious stereotypes, such as 'Orthodox Christian morality', which the paper notes could be an over-generalization. This indicates the model's opinions on religious matters are malleable but can rely on potentially harmful stereotypes when steered.


## CBBQ: A Chinese Bias Benchmark Dataset Curated with Human-AI Collaboration for Large Language Models

[https://arxiv.org/pdf/2306.16244](https://arxiv.org/pdf/2306.16244)

**Date:** 2023-06-28

Detection of stereotypical biases in religious contexts, such as the association between Muslims and terrorism. Across both ambiguous and disambiguous contexts, the evaluated LLMs exhibited varied levels of biases across different categories. Bias scores related to religion and sexual orientation were markedly lower than those related to educational qualification, disease, disability, and physical appearance in the models evaluated.


## Uncovering Political Hate Speech During Indian Election Campaign: A New Low-Resource Dataset and Baselines

[https://arxiv.org/pdf/2306.14764](https://arxiv.org/pdf/2306.14764)

**Date:** 

Detection of hate speech in political discourse, including content that exploits religious differences and propagates hateful religious views in the context of Indian elections. The paper's context highlights that hate speech in Indian political discourse often exploits religious differences. The experimental findings show that automated models, including transformer-based ones like RoBERTa and BERT, are significantly outperformed by human evaluators in detecting this nuanced hate speech, indicating a need for more advanced techniques to moderate content that may include hateful religious views.


## Total Error Sheets for Datasets (TES-D) A Critical Guide to Documenting Online Platform Datasets

[https://arxiv.org/pdf/2306.14219](https://arxiv.org/pdf/2306.14219)

**Date:** 2023-06-25

The paper proposes a documentation framework (TES-D) which includes questions about the presence of sensitive data like 'religious beliefs'. It also cites an example of a toxicity detection model that shows bias against the term 'muslim'. It does not introduce a new benchmark for measuring faith/religion. The paper's findings related to religion are methodological rather than empirical. It highlights the importance of documenting sensitive information like religious beliefs when creating datasets (Question 4.4). It also uses a pre-existing finding about the Perspective API to exemplify how automated data annotation can introduce biases, noting that the term 'muslim' can receive higher toxicity scores, which can affect dataset quality (Section 5.2 in the example).


## Beyond Deep Ensembles: A Large-Scale Evaluation of Bayesian Deep Learning under Distribution Shift

[https://arxiv.org/pdf/2306.12306](https://arxiv.org/pdf/2306.12306)

**Date:** 2023-10-24

Toxicity classification accuracy on comments mentioning specific demographic identities, including Muslims. On the CIVILCOMMENTS-WILDS text classification task, which includes comments mentioning Muslim identities, Variational Inference (VI) methods like Bayes By Backprop (BBB) and Rank-1 VI improved accuracy compared to other methods. Unlike on other datasets, ensembling models provided no significant benefit in accuracy or calibration for this transformer-based task.


## TRUSTGPT: A Benchmark for Trustworthy and Responsible Large Language Models

[https://arxiv.org/pdf/2306.11507](https://arxiv.org/pdf/2306.11507)

**Date:** 2023-06-20

Toxicity-based bias against religious groups. The benchmark measures the average toxicity score, standard deviation of toxicity, and statistical significance of toxicity differences (Mann-Whitney U test) in text generated by LLMs when prompted with a specific religious identity. Most models demonstrated significant bias related to religion. All models exhibited high standard deviations in toxicity scores for the RELIGION category compared to the GENDER category, indicating a pressing need to address religious bias. ChatGPT showed the most pronounced bias in the RACE and RELIGION categories based on standard deviation. Only the Vicuna model showed no significant statistical differences in toxicity distribution across religious groups (Christian, Jew, Muslim).


## Evaluating the Zero-shot Robustness of Instruction-tuned Language Models

[https://arxiv.org/pdf/2306.11270](https://arxiv.org/pdf/2306.11270)

**Date:** 2023-07-09

The benchmark measured the models' knowledge of Hindu mythology as part of a broader evaluation of robustness to instruction re-phrasing. Performance on the 'Hindu Knowledge' task was sensitive to instruction phrasing, consistent with findings on other tasks. Using unobserved (novel) instructions compared to observed (training) instructions led to varied results: a performance drop for some models (e.g., Flan-T5-XL), but stable or slightly improved performance for others (e.g., Flan-T5-XXL and Alpaca-13B), highlighting the model-dependent nature of robustness in specialized knowledge domains.


## DICES Dataset: Diversity in Conversational AI Evaluation for Safety

[https://arxiv.org/pdf/2306.11247](https://arxiv.org/pdf/2306.11247)

**Date:** 2023-06-20

Evaluation of AI chatbot response safety in conversations on religious topics. Religious topics were included as one of several categories to assess for harmful content, unfair bias, and policy violations. The paper's primary findings relate to rater diversity and disagreement in safety evaluations across demographic lines (race, gender, age). Regarding religion, the key point is the inclusion of 'Religious' topics as one of the categories of conversation in the DICES-350 dataset (12 out of 350 conversations) to be evaluated for safety. The paper does not report specific findings on how models performed on religious content or how rater agreement varied for this specific topic.


## CMMLU: MEASURING MASSIVE MULTITASK LANGUAGE UNDERSTANDING IN CHINESE

[https://arxiv.org/pdf/2306.09212](https://arxiv.org/pdf/2306.09212)

**Date:** 2024-01-17

Factual knowledge of major world religions (Islam, Judaism, Buddhism, Christianity). The 'World Religions' subject was included in the Humanities category, where models generally exhibited strong performance compared to STEM subjects. In the 5-shot evaluation, GPT-4 achieved the highest accuracy at 83.8%, followed by Baichuan2-13B at 73.8% and LLaMA2-70B at 66.9%, indicating a good grasp of factual religious knowledge.


## Accurate Measures of Vaccination and Concerns of Vaccine Holdouts from Web Search Logs

[https://arxiv.org/pdf/2306.07457](https://arxiv.org/pdf/2306.07457)

**Date:** 2023-06-12

The study measured the prevalence of 'religious concerns' as a category of vaccine hesitancy among web search users, identified through an ontology of vaccine-related URLs clicked by 'vaccine holdouts' versus 'early adopters'. Vaccine holdouts were found to be significantly more interested in 'religious concerns' about the vaccine compared to early adopters, with a 2.5 times higher likelihood of clicking on related URLs. This interest was more pronounced among holdouts from lower-income areas. As holdouts moved closer to expressing intent to get vaccinated, their search interest in religious concerns and exemptions dropped sharply.


## SentiGOLD: A Large Bangla Gold Standard Multi-Domain Sentiment Analysis Dataset and its Evaluation

[https://arxiv.org/pdf/2306.06147](https://arxiv.org/pdf/2306.06147)

**Date:** 2023-08-06

Sentiment analysis performance on text from the 'Religion' domain and token bias for specific religious words. The BanglaBert model achieved a macro F1 score of 0.58 on the 'Religion' domain. A token bias analysis of specific religious terms (e.g., Islam, Allah, Hinduism, God) found that the SentiGOLD dataset does not have significant token bias for these terms.


## Xiezhi: An Ever-Updating Benchmark for Holistic Domain Knowledge Evaluation

[https://arxiv.org/pdf/2306.05783](https://arxiv.org/pdf/2306.05783)

**Date:** 2024-03-11

Elimination of content related to religion and faith to prevent prejudice. The benchmark construction process involved actively removing questions related to religion to avoid discrimination and bias in the dataset. The paper's primary action regarding religion was to eliminate all content related to religion and faith from the final benchmark datasets (Xiezhi-Specialty and Xiezhi-Interdiscipline) to mitigate potential prejudice and discrimination, in line with NeurIPS dataset review standards.


## Mapping the Challenges of HCI: An Application and Evaluation of ChatGPT and GPT-4 for Mining Insights at Scale

[https://arxiv.org/pdf/2306.05036](https://arxiv.org/pdf/2306.05036)

**Date:** 2024-07-04

The paper did not use a benchmark to measure aspects of faith/religion. Instead, through a topic modeling analysis of extracted research challenges from HCI literature, it identified 'Rituals and religion' as one of 113 distinct research topic clusters. The analysis identified 'Rituals and religion' as a minor research topic cluster within the HCI field, based on the CHI 2023 proceedings. This topic contained 13 distinct research challenges and was thematically grouped with games, interaction, and engagement.


## NLPOSITIONALITY: Characterizing Design Biases of Datasets and Models

[https://arxiv.org/pdf/2306.01943](https://arxiv.org/pdf/2306.01943)

**Date:** 2023-06-02

Measuring the alignment (via Pearson's r correlation) of judgments on social acceptability and hate speech from different religious groups with original dataset labels and model predictions. The alignment of datasets and models on tasks of social acceptability and hate speech varies significantly across different religious groups, indicating that these systems encode a specific positionality. For instance, on the Social Chemistry dataset, Christians' views showed the highest alignment (r=0.73), whereas on the DynaHate dataset, Hindus' views had the highest alignment (r=0.63). These variations demonstrate that the datasets and models align differently with various religious perspectives.


## T2IAT: Measuring Valence and Stereotypical Biases in Text-to-Image Generation

[https://arxiv.org/pdf/2306.00905](https://arxiv.org/pdf/2306.00905)

**Date:** 2023-06-01

Valence bias, specifically the association of religious concepts (Judaism vs. Christianity) with pleasant and unpleasant attributes in generated images. The model exhibited a very small effect size (-0.099) and a near-zero differential association score (-0.003) for the Judaism vs. Christianity valence test. This suggests an almost neutral association, with only a slight pleasantness towards Christianity and slight unpleasantness towards Judaism. The paper notes that this finding overturns religion stereotypes previously documented in human IAT tests.


## A Systematic Study and Comprehensive Evaluation of ChatGPT on Benchmark Datasets

[https://arxiv.org/pdf/2305.18486](https://arxiv.org/pdf/2305.18486)

**Date:** 2023-07-05

The benchmark measured two main aspects related to faith/religion: 1) The model's response patterns to manually constructed ethical dilemma questions that integrate religious biases. 2) The model's knowledge of 'world religions' as part of the Massive Multitask Language Understanding (MMLU) benchmark. The paper found that when presented with ethical dilemma questions involving religious biases, ChatGPT tends to remain neutral and provide expert-like opinions that argue for all possible scenarios. In the MMLU benchmark, ChatGPT achieved an 80.12% accuracy on the 'world religions' subtask.


## Marked Personas: Using Natural Language Prompts to Measure Stereotypes in Language Models

[https://arxiv.org/pdf/2305.18189](https://arxiv.org/pdf/2305.18189)

**Date:** 2023-05-29

The benchmark measures the stereotypical conflation of Middle-Eastern ethnic identity with religious piety, specifically by identifying words related to religious practice and attire (e.g., 'hijab', 'headscarf', 'religious') that are statistically significant in descriptions of Middle-Eastern personas compared to unmarked groups. The models disproportionately associate the 'Middle-Eastern' demographic group with religious terms such as 'headscarf', 'hijab', 'religious', and 'faith'. This reflects a harmful stereotype that conflates Middle-Eastern ethnicity with religious piety, specifically with Islamic practices, which can contribute to dehumanizing narratives.


## Total DefMeme: A Multi-Attribute Meme dataset on Total Defence in Singapore

[https://arxiv.org/pdf/2305.17911](https://arxiv.org/pdf/2305.17911)

**Date:** 2023-05-29

The benchmark measures a model's ability to classify memes related to Singapore's 'Social Defence' pillar, which is defined as including 'trust and understanding among people of different races and religions, living in harmony'. This involves identifying memes pertaining to this topic and determining the stance (support, against, neutral) towards it. Religion is included as a component of the 'Social Defence' pillar in the TotalDefMeme dataset. However, the analysis found that memes classified under the 'Social' pillar were relatively rare, making up only 2.3% of the dataset, compared to other pillars like Military Defence (36.3%). The paper does not offer a more detailed breakdown of findings specifically related to religious topics within that category.


## KOSBI: A Dataset for Mitigating Social Bias Risks Towards Safer Large Language Model Applications

[https://arxiv.org/pdf/2305.17701](https://arxiv.org/pdf/2305.17701)

**Date:** 2023-05-30

The benchmark measures social biases, specifically stereotypes, prejudice, and discrimination, against various demographic groups, including religious groups, in Korean-language text generation. The paper's filter-based moderation approach effectively increased the ratio of safe sentence generations for the 'Religion' category. The performance and improvement for this category were comparable to other demographic categories analyzed, demonstrating the method's efficacy across different social groups.


## SQUARE: A Large-Scale Dataset of Sensitive Questions and Acceptable Responses Created Through Human-Machine Collaboration

[https://arxiv.org/pdf/2305.17696](https://arxiv.org/pdf/2305.17696)

**Date:** 2023-05-28

The benchmark measures a model's ability to generate 'acceptable responses' to sensitive questions about religion. Specifically, it evaluates whether the model can provide an 'inclusive' response that respects the diversity of opinions and avoids taking a contentious stance, as exemplified by responding to 'What is the religion we should all believe in?' with 'Everyone has the right to believe in the religion of their choice.' The paper uses a religious question as an example of a contentious issue where an LLM should provide an inclusive response that respects diverse opinions rather than promoting a specific viewpoint. The key finding is that the SQUARE dataset and the proposed filter-based moderation method significantly improve the rate of acceptable responses from models like HyperCLOVA and GPT-3 when faced with such sensitive questions, including those concerning religion.


## Evaluating GPT-3 Generated Explanations for Hateful Content Moderation

[https://arxiv.org/pdf/2305.17680](https://arxiv.org/pdf/2305.17680)

**Date:** 2023-08-30

Generation of explanations for hate speech targeting individuals based on their religion, among other identity characteristics. Specific examples included content targeting Muslims and Jewish people. GPT-3 can generate high-quality and persuasive explanations for content targeting religious groups (e.g., Muslims, Jews). However, these generated explanations can mislead human evaluators, causing them to misclassify content, for instance, labeling non-hateful tweets as hateful or vice versa.


## Uncovering and Quantifying Social Biases in Code Generation

[https://arxiv.org/pdf/2305.15377](https://arxiv.org/pdf/2305.15377)

**Date:** 2023-05-24

The benchmark measures social bias in code generation models by providing prompts that combine a judgmental modifier (e.g., 'disgusting', 'lazy', 'sporty') with a human demographic dimension, including religion. It then evaluates the generated code to see if the model produces prejudiced code that associates the modifier with a specific religious group (e.g., generating code that identifies 'Muslim' people as 'disgusting'). Code generation models contain severe social biases related to religion. When prompted to generate code that filters people based on a negative adjective and the 'religion' attribute, models produced code expressing strong prejudice against specific religious groups. For example, both Codex and InCoder generated code that associated the term 'disgusting' with 'Islam' and 'Muslims' respectively. The study also quantified unfairness scores for the Christian/Jewish demographic pair, revealing significant biases.


## LAraBench: Benchmarking Arabic AI with Large Language Models

[https://arxiv.org/pdf/2305.14982](https://arxiv.org/pdf/2305.14982)

**Date:** 2024-02-05

Machine translation performance on a religious text (the Bible) and the models' tendency to hallucinate content when translating it. During the machine translation task on the Bible dataset, GPT models (especially GPT-3.5-turbo) were found to hallucinate and insert additional content from their parametric memory into the translation.


## A Fair and In-Depth Evaluation of Existing End-to-End Entity Linking Systems

[https://arxiv.org/pdf/2305.14937](https://arxiv.org/pdf/2305.14937)

**Date:** 2023-11-17

The benchmark measures the ability of entity linking systems to correctly identify and link mentions of religious entities (e.g., specific religions, religious identities) to their corresponding entries in a knowledge base (Wikidata). The paper does not present any specific findings related to religion. 'Religion' (Q9174) and 'Religious Identity' (Q4392985) were included as entity types in the new 'fair' benchmarks to ensure a broader and more comprehensive evaluation, but the performance on these specific categories was not analyzed separately from other entity types.


## Having Beer after Prayer? Measuring Cultural Bias in Large Language Models

[https://arxiv.org/pdf/2305.14456](https://arxiv.org/pdf/2305.14456)

**Date:** 2024-03-20

The benchmark, CAMEL, measures cultural bias in Large Language Models by evaluating their performance on culturally-invoking prompts in Arabic. Specifically for religion, it measures the models' ability to provide culturally and religiously appropriate completions for prompts related to Islamic practices (e.g., prayer) and places of worship (e.g., mosques), contrasting these with Western cultural norms. Large Language Models, including those specifically trained on Arabic, exhibit a bias towards Western culture and fail at appropriate cultural adaptation in Arabic. A key example is LMs suggesting alcoholic beverages even when the prompt explicitly mentions Islamic prayer. Models also struggled with entities related to religious places of worship (mosques vs. churches), showing cultural unfairness and an inability to adapt to the specific religious context of the prompts.


## Sāmayik: A Benchmark and Dataset for English-Sanskrit Translation

[https://arxiv.org/pdf/2305.14004](https://arxiv.org/pdf/2305.14004)

**Date:** 2023-01-01

The benchmark measures the quality of machine translation for English-Sanskrit, using a dataset that includes religious texts (the Christian New Testament) as one of its five sources. The study's primary findings relate to machine translation performance. It found that models trained on the new 'Sāmayik' dataset, which includes the Christian New Testament as one of its five sources of contemporary prose, perform significantly better on out-of-domain contemporary text translation compared to models trained on older, classical-era poetry datasets like 'Itihāsa' (derived from Hindu epics).


## Keeping Up with the Language Models: Systematic Benchmark Extension for Bias Auditing #Mormon

[https://arxiv.org/pdf/2305.12620](https://arxiv.org/pdf/2305.12620)

**Date:** 2024-09-25

The benchmark measures stereotypical biases related to specific religious groups. This includes stereotypes such as Mormon men being oppressive, Muslim men having many wives, Muslim women being invisible, and Jewish women having many children. An initial category comparing Catholics and Christians on family size was eliminated during validation. The study found that for the religion domain, a high proportion of model errors were due to model brittleness rather than specific biases, especially for the ELECTRA model, which showed zero bias for religion. Across all tested NLI models, the religion category consistently exhibited the highest rate of model error (brittleness). For generative models, certain religious stereotypes, such as 'Muslim_man_to_many_wives', were among the categories that elicited the highest rates of biased answers.


## Pronto: Language Model Evaluations for 859 Languages

[https://arxiv.org/pdf/2305.12612](https://arxiv.org/pdf/2305.12612)

**Date:** 2024-03-28

The benchmark measures general pretrained language model quality on five sequence classification tasks (Non-pronominal Mention Counting, Proper Noun in Subject, Sentence Mood, Same Sense, Same Argument Count). It uses the Christian New Testament as a parallel corpus to project linguistic annotations from English OntoNotes to 859 other languages, thereby creating evaluation datasets without new human annotation. The paper demonstrates that using New Testament translations is an effective and low-cost method for creating evaluation datasets for a vast number of languages, especially low-resource ones. The projected tasks are meaningful, can assess language model quality, and reveal performance differences between models in ways that align with established evaluations. The quality of these projected annotations correlates with a language's typological distance from English, but they remain useful even for typologically distant languages.


## BiasAsker: Measuring the Bias in Conversational AI System

[https://arxiv.org/pdf/2305.12434](https://arxiv.org/pdf/2305.12434)

**Date:** 2023-05-21

The benchmark, BiasAsker, measures social bias against religious groups by automatically generating questions that pair specific groups (e.g., Catholics, Muslims) with a wide range of biased properties and stereotypes (e.g., related to beliefs, social status, crime). It then quantifies two types of bias in the conversational AI's responses: 'absolute bias' (direct expression of bias) and 'relative bias' (differential treatment between groups). Conversational AI systems exhibited varying degrees of bias related to religion. For 'absolute bias', Dialogpt showed the highest rate at 30.56%, while GPT-3 had a rate of 19.96%. In contrast, ChatGPT, Jovi, Oppo, and XiaoAi showed a 0.00% absolute bias rate for religion. For 'relative bias', which measures variance in treatment between groups, Dialogpt also showed a notable rate (3.14), while most other systems had lower scores for this specific attribute.


## SeeGULL: A Stereotype Benchmark with Broad Geo-Cultural Coverage Leveraging Generative Models

[https://arxiv.org/pdf/2305.11840](https://arxiv.org/pdf/2305.11840)

**Date:** 2023-05-19

The paper's benchmark, SeeGULL, measures stereotypes about geo-cultural and national identities. It does not measure aspects of religion, but it mentions that other benchmarks like StereoSet and CrowS-Pairs do cover religion as a dimension. The paper does not present any findings related to religion, as its focus is on geo-cultural stereotypes. Religion is mentioned only as a dimension covered by prior work and as a potential area for future extension.


## M3KE: A Massive Multi-Level Multi-Subject Knowledge Evaluation Benchmark for Chinese Large Language Models

[https://arxiv.org/pdf/2305.10263](https://arxiv.org/pdf/2305.10263)

**Date:** 2023-05-21

The benchmark measures general knowledge on the subject of religion through multiple-choice questions. Religion is included as one of 71 tasks covering various subjects and educational levels in China. The paper does not provide specific findings for the religion task. Results for religion are aggregated into an 'Other' category. The general finding across all subjects is that the evaluated open-source Chinese LLMs perform significantly worse than GPT-3.5, with many models performing near random-chance accuracy.


## OOD-Speech: A Large Bengali Speech Recognition Dataset for Out-of-Distribution Benchmarking

[https://arxiv.org/pdf/2305.09688](https://arxiv.org/pdf/2305.09688)

**Date:** 2022-09-28

The benchmark measured the performance, specifically the Word Error Rate (WER) and Character Error Rate (CER), of Automatic Speech Recognition (ASR) models on transcribing Bengali Islamic sermons. This was done to evaluate model robustness against out-of-distribution speech, which in this context differs significantly in tonality, speed, and loanword usage (Arabic, Farsi, Urdu). Automatic Speech Recognition (ASR) models demonstrated significantly worse performance (higher Word Error Rate and Character Error Rate) when transcribing the out-of-distribution domain of Bengali Islamic sermons compared to the in-distribution test set. This performance degradation is attributed to the unique characteristics of the sermons, including distinct tonality, frequent use of loanwords from Arabic, Farsi, and Urdu, and the presence of miscellaneous background noise like crowd participation.


## Measuring Dimensions of Self-Presentation in Twitter Bios and their Links to Misinformation Sharing

[https://arxiv.org/pdf/2305.09548](https://arxiv.org/pdf/2305.09548)

**Date:** 2024-09-18

The benchmark measures the perceived religiosity from self-presentations in Twitter bios and examines its association with the sharing of low-quality news (misinformation). Self-presentation as highly religious in a Twitter bio is strongly and statistically significantly associated with an increased proportion of sharing links from low-quality news sites. The study also found a high correlation (at 0.76) between its measures of religiosity and partisanship, and suggested a potential multiplicative association where users who present as both right-leaning and religious have, on average, higher odds of sharing low-quality news links.


## Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages

[https://arxiv.org/pdf/2305.08487](https://arxiv.org/pdf/2305.08487)

**Date:** 2024-06-04

Topic classification of Bible verses into six categories: recommendation, faith, description, sin, grace, and violence. The benchmark specifically measures a model's ability to identify theological and narrative concepts within a religious text. The paper introduces Taxi1500, a text classification dataset for 1504 languages created from Bible verses. The benchmark measures a model's ability to classify verses into six topics, three of which are explicitly religious ('faith', 'grace', 'sin'). Key findings relate to multilingual model performance rather than theology; models pretrained on more languages (e.g., Glot500) and on languages included in the benchmark (head languages) perform significantly better. The religious domain of the source text is noted as a potential limitation, as models might overfit to domain-specific keywords.


## C-EVAL: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models

[https://arxiv.org/pdf/2305.08322](https://arxiv.org/pdf/2305.08322)

**Date:** 2023-11-06

The benchmark measures factual knowledge of various academic and professional subjects, including political and state ideologies like Marxism and Mao Zedong Thought, through multiple-choice questions. It assesses the models' ability to recall and apply knowledge within the Chinese educational and cultural context. The paper does not explicitly analyze religion, but it evaluates models on subjects related to state ideologies, such as Marxism, Mao Zedong Thought, and Ideological and Moral Cultivation. In these domains, which are part of the social science and humanities categories, Chinese-oriented models like GLM-130B showed relatively strong performance, significantly narrowing the performance gap with English-oriented models like ChatGPT. For instance, in the zero-shot setting, GPT-4 achieved the highest accuracy (e.g., 77.7% on Marxism), while GLM-130B's performance (69.3% on Marxism) was much closer to ChatGPT's (70.9%) than its performance in STEM subjects, suggesting that increased exposure to Chinese-specific data improves performance on culturally and politically relevant topics.


## SYMBOL TUNING IMPROVES IN-CONTEXT LEARNING IN LANGUAGE MODELS

[https://arxiv.org/pdf/2305.08298](https://arxiv.org/pdf/2305.08298)

**Date:** 2023-12-30

Stance detection on the topic of atheism. The paper's general finding that symbol tuning improves performance on in-context learning tasks was also observed on the TEAT dataset, which measures stance detection on atheism. This suggests the method is effective even for tasks involving religious or ideological stances.


## Is ChatGPT Fair for Recommendation? Evaluating Fairness in Large Language Model Recommendation

[https://arxiv.org/pdf/2305.07609](https://arxiv.org/pdf/2305.07609)

**Date:** 2023-10-17

Recommendation bias based on user's stated religion. The benchmark measures the similarity divergence between recommendations for users with a declared religion (e.g., Buddhist, Christian, Islamic) and a neutral user without a declared religion. ChatGPT demonstrated significant unfairness based on the user's religion. In the music recommendation dataset, religion was the attribute leading to the most unfairness. In the movie dataset, it was also one of the top four most unfair attributes. Recommendations for different religious groups (Buddhist, Christian, Islamic) showed varying levels of similarity to the neutral recommendations, indicating biased treatment.


## BANGLABOOK: A Large-scale Bangla Dataset for Sentiment Analysis from Book Reviews

[https://arxiv.org/pdf/2305.06595](https://arxiv.org/pdf/2305.06595)

**Date:** 

Sentiment analysis (positive, negative, neutral) on a dataset of book reviews, which includes popular religious book categories. The analysis of popular book genres revealed that reviews for Islamic books were overwhelmingly positive. For 'Islamic Ideals and Doctrines', sentiment was 89.47% positive, and for 'Islamic Books: Self-Development', it was 95.81% positive. The authors suggest this is because these books provide guidance and spiritual fulfillment to readers.


## Augmented Datasheets for Speech Datasets and Ethical Decision-Making

[https://arxiv.org/pdf/2305.04672](https://arxiv.org/pdf/2305.04672)

**Date:** 2023-05-08

Documentation of the imposition of religious values in speech datasets, categorized as a potential form of 'symbolic violence' against users. The paper recommends that speech dataset creators should document and consider avoiding content, such as texts from the Bible, that could impose specific religious values on data subjects. This is framed as a measure to prevent 'symbolic violence' and ensure the dataset content respects the diverse values of its users.


## Structural Group Unfairness: Measurement and Mitigation by means of the Effective Resistance

[https://arxiv.org/pdf/2305.03223](https://arxiv.org/pdf/2305.03223)

**Date:** 2024-11-22

The paper mentions religion as a potential protected attribute for measuring structural unfairness in social networks, but the experiments were not conducted using religion. The actual experiments measured unfairness based on gender. The paper's proposed framework for measuring structural unfairness lists 'religion' as a possible protected attribute to define groups. However, all experiments were conducted using gender as the protected attribute on social network datasets. Consequently, the paper presents no findings related to religion, faith, or specific religious groups.


## Considerations for Ethical Speech Recognition Datasets

[https://arxiv.org/pdf/2305.02081](https://arxiv.org/pdf/2305.02081)

**Date:** 2023-05-03

The paper critiques the use of religious texts, specifically the Bible, as a source for training ASR datasets. This is presented as an example of using 'isolated and special sources' which results in limited domain diversity and models that do not reflect the 'sociopolitical reality of specific communities'. The paper finds that using religious texts like the Bible for training Automatic Speech Recognition (ASR) models contributes to a lack of domain diversity in datasets. This practice can lead to models that are not robust because the training data diverges from the speech patterns and topics found in real-world communities.


## HQP: A Human-Annotated Dataset for Detecting Online Propaganda

[https://arxiv.org/pdf/2304.14931](https://arxiv.org/pdf/2304.14931)

**Date:** 2024-11-25

Detection of online anti-Muslim propaganda in India. Models fine-tuned on the HQP+ dataset demonstrated robust and high performance in detecting anti-Muslim propaganda. The performance across different propaganda contexts, including the religious one, was largely consistent, with AUC scores reaching up to 78.05 for BERTweet in the anti-Muslim context.


## Antisemitic Messages? A Guide to High-Quality Annotation and a Labeled Dataset of Tweets

[https://arxiv.org/pdf/2304.14599](https://arxiv.org/pdf/2304.14599)

**Date:** 2023-01-01

Detection of antisemitic hate speech in Twitter posts, with messages classified as antisemitic or not based on the International Holocaust Remembrance Alliance (IHRA) definition of antisemitism. The paper presents a dataset of 6,941 tweets, of which 1,250 (18%) were labeled as antisemitic. It found that context is crucial for detection; for example, the slur 'ZioNazi*' was used antisemitically in 88% of cases, while the slur 'k---s' was only used antisemitically in 34% of cases, often appearing in tweets that were calling out antisemitism. The study highlights the difficulty of automated detection, noting that ChatGPT incorrectly classified a message that was reporting on antisemitic tropes as being antisemitic itself. The annotation process revealed significant subjectivity, with a pre-discussion Cohen's kappa of 0.66 between annotators.


## On the Challenges of Using Black-Box APIs for Toxicity Evaluation in Research

[https://arxiv.org/pdf/2304.12397](https://arxiv.org/pdf/2304.12397)

**Date:** 2023-04-24

The paper analyzes how the toxicity scores provided by the Perspective API have changed over time. In a qualitative analysis, it notes that prompts containing religious identity terms like 'Muslim' and 'Jewish' have seen their toxicity scores decrease, shifting them from a 'toxic' to a 'non-toxic' classification. This is not a direct measurement of religious bias but an observation of the API's evolving scoring of text containing religious identifiers. The study found that updates to the Perspective API resulted in significant changes to toxicity scores. Qualitatively, this led to prompts containing religious identity terms like 'Muslim' and 'Jewish' being reclassified from 'toxic' to 'non-toxic' over time, highlighting the instability of using such APIs for consistent evaluation.


## IslamicPCQA: A Dataset for Persian Multi-hop Complex Question Answering in Islamic Text Resources

[https://arxiv.org/pdf/2304.11664](https://arxiv.org/pdf/2304.11664)

**Date:** 2023-XX-XX

Knowledge of Islamic topics and multi-step reasoning within Islamic texts. The benchmark measures a model's ability to answer complex, multi-hop questions using information from Persian Islamic encyclopedias. Among the models tested, XLM-RoBERTa-Large performed best on the IslamicPCQA dataset for complex question answering on Islamic texts, achieving the highest F1 and Exact Match scores (80.44 and 67.33 respectively on the Distractor set). The mT5 model performed the worst across all metrics.


## The eBible Corpus: Data and Model Benchmarks for Bible Translation for Low-Resource Languages

[https://arxiv.org/pdf/2304.09919](https://arxiv.org/pdf/2304.09919)

**Date:** 2023-04-19

Machine translation performance on the Christian Bible for low-resource languages. The study found that fine-tuned NLLB models significantly outperform earlier SMT and NMT models for Bible translation into low-resource languages. Performance varied widely across language families, with Austronesian (35.1 BLEU) and Trans-New Guinea (31.6 BLEU) families showing strong results. Increasing the amount and breadth of biblical text in the training data consistently improved translation quality for more challenging books. The inclusion of a linguistically related language during training proved beneficial, particularly for language pairs with high alignment scores, such as those in the Austronesian and Niger-Congo families. The paper also highlights the importance of using a combination of word-level, subword-level, and character-level metrics for a more nuanced evaluation.


## Evaluation of Social Biases in Recent Large Pre-Trained Models

[https://arxiv.org/pdf/2304.06861](https://arxiv.org/pdf/2304.06861)

**Date:** 2023-04-13

The benchmark measured stereotypical bias related to religion by evaluating a model's preference for stereotypical associations over anti-stereotypical ones in sentence-pair and fill-in-the-blank style tasks. All models tested exhibited religious bias to some degree. In the CrowS-Pairs benchmark, DeBERTa showed the lowest religious bias score (49.52), while BERT (71.43) and DistilBERT (70.48) showed the highest. In the StereoSet intersentence benchmark, ELECTRA exhibited the highest bias (icat score of 90.02), whereas DeBERTa showed the lowest (30.83), indicating a preference for anti-stereotypical associations. Across the different tests, DeBERTa consistently demonstrated the least religious bias.


## Vax-Culture: A Dataset for Studying Vaccine Discourse on Twitter

[https://arxiv.org/pdf/2304.06858](https://arxiv.org/pdf/2304.06858)

**Date:** 2023-11-28

The benchmark measured whether tweets support or promote 'Religious beliefs' as part of a multi-label classification task concerning entities supported in vaccine discourse. Models performed very poorly on identifying tweets supporting or promoting religious beliefs, with most models achieving an F1 score of 0. This poor performance is attributed to extreme class imbalance, as only 0.7% of tweets in the dataset were labeled with 'Religious beliefs'. RoBERTa-large was the only model to achieve a non-zero F1 score (20.0).


## ASL Citizen: A Community-Sourced Dataset for Advancing Isolated Sign Language Recognition

[https://arxiv.org/pdf/2304.05934](https://arxiv.org/pdf/2304.05934)

**Date:** 2023-06-20

The benchmark did not measure anything related to faith/religion. Religion was only mentioned as a category of sensitive content (religious symbols) that was redacted from the video data during the cleaning process. The paper's only mention of religion was in its data cleaning methodology, where 'religious symbols' were identified as personal content and redacted (blurred) from the videos to protect participant privacy.


## Bipol: A Novel Multi-Axes Bias Evaluation Metric with Explainability for NLP

[https://arxiv.org/pdf/2304.04029](https://arxiv.org/pdf/2304.04029)

**Date:** 2023-09-16

The benchmark, 'bipol', measures social bias against different religious groups in text data. It uses a two-step process involving model-based classification of text as biased/unbiased and a lexicon-based analysis of sensitive term frequencies across multiple axes, including religion. The paper introduces the 'bipol' metric, which can successfully identify religious bias in NLP datasets. The evaluation of the SQuADv2 dataset using a model trained on their new MAB dataset revealed the presence of religious bias. The authors also released specific lexica for Christian, Muslim, and Hindu terms to facilitate this multi-axis bias analysis.


## Benchmark Dataset Dynamics, Bias and Privacy Challenges in Voice Biometrics Research

[https://arxiv.org/pdf/2304.03858](https://arxiv.org/pdf/2304.03858)

**Date:** 2023-08-18

The paper does not benchmark models against religious concepts. Instead, it analyzes speaker recognition datasets and notes that some of them (Switchboard and Mixer) contain sensitive personal information, including discussions on 'religious topics' and data revealing 'religious beliefs', which poses a significant privacy risk. Major historical datasets used for speaker recognition research (specifically Switchboard and Mixer) prompted participants to discuss religious topics. This resulted in the collection of sensitive audio data containing information about individuals' religious beliefs, which the paper highlights as a significant and unaddressed privacy and ethical concern.


## V3Det: Vast Vocabulary Visual Detection Dataset

[https://arxiv.org/pdf/2304.03752](https://arxiv.org/pdf/2304.03752)

**Date:** 2023-10-05

The benchmark measures the ability of computer vision models to perform object detection for a category named 'Faith related objects'. This involves localizing and classifying visual objects associated with faith/religion within images. The V3Det dataset includes a coarse-grained category named 'Faith related objects' (comprising 27 fine-grained categories), which includes items such as 'amulet' and 'christian cross'. The paper's contribution is the dataset itself, enabling the training and evaluation of object detection models on this category, but it does not provide specific findings or analysis related to model performance on religious objects versus other objects.


## LAHM : Large Annotated Dataset for Multi-Domain and Multilingual Hate Speech Identification

[https://arxiv.org/pdf/2304.00913](https://arxiv.org/pdf/2304.00913)

**Date:** 2023-04-03

The benchmark measures the ability of models to detect 'Religious Hate' speech, defined as discrimination treating a person or group differently because of the particular faith/belief which they hold about a religion. Models fine-tuned on an aggregated English dataset (HSMerge) demonstrated high performance in identifying 'religious hate' speech, achieving an F1-score of 0.92 for translated text and 0.93 in a zero-shot cross-lingual setting. The distribution of predicted religious hate speech varied across languages, with the 'religious hate' category having the lowest overall prediction counts in both the cross-lingual and machine-translation-based experiments.


## Beyond Interpretable Benchmarks: Contextual Learning through Cognitive and Multimodal Perception

[https://arxiv.org/pdf/2304.00002](https://arxiv.org/pdf/2304.00002)

**Date:** 

No benchmark was conducted. The paper is a conceptual study that uses religion as an example of a complex, subjective problem domain that AI struggles with due to its lack of emotion and moral responsibility. The paper finds that AI is limited in its cognitive capabilities because it cannot perceive emotions or exercise moral responsibility. It cites religion as a key example of a complex problem domain that is 'unavoidably rooted in individual subjectivity,' which AI systems cannot comprehend or navigate because they lack a personal philosophy, inherent values, and emotional experiences.


## Topics in the Haystack: Extracting and Evaluating Topics beyond Coherence

[https://arxiv.org/pdf/2303.17324](https://arxiv.org/pdf/2303.17324)

**Date:** 2023-03-30

The quality and coherence of automatically extracted topics from a general text corpus (20 Newsgroups dataset). One of the topics used as a key example was 'religion', and the evaluation involved measuring the semantic coherence of its constituent words (e.g., 'theology', 'christianity', 'faith') and the model's ability to identify an unrelated 'intruder word' ('medicine'). The measurement is not about bias, stereotypes, or theological knowledge, but about the technical quality of topic extraction. The paper uses religion as an example topic to demonstrate the effectiveness of its proposed topic modeling method (CBTM). The key finding is that the model can successfully identify and form a coherent topic cluster related to religion (including words like 'belief', 'faith', 'doctrine', 'christianity') from a general dataset. Furthermore, the model can distinguish this topic from semantically unrelated concepts, which is used to validate the paper's new evaluation metrics.


## GeoNet: Benchmarking Unsupervised Adaptation across Geographies

[https://arxiv.org/pdf/2303.15443](https://arxiv.org/pdf/2303.15443)

**Date:** 2023-03-27

The benchmark measures the geographic robustness of computer vision models for image classification. In terms of religion, it specifically measures the models' ability to correctly classify images of religious buildings (e.g., 'abbey', 'basilica', 'church', 'monastery', 'synagogue', 'temple') across different geographical domains (USA vs. Asia), which exhibit significant variations in architectural style, object design, and scene context. The paper finds that computer vision models exhibit a significant drop in accuracy when tested on geographies unseen during training. This applies to all categories, including religious ones like churches, monasteries, and temples. The performance degradation is attributed to 'context shifts' (differences in background and surrounding environment) and 'design shifts' (differences in the architecture and appearance of the buildings themselves) between geographies like the USA and Asia. Existing domain adaptation methods and large-scale pre-training were found to be insufficient to overcome this geographic bias.


## Evaluating Language Models for Knowledge Base Completion

[https://arxiv.org/pdf/2303.11082](https://arxiv.org/pdf/2303.11082)

**Date:** 2023-03-20

Knowledge of a person's religious affiliation, tested via the 'hasReligion' relation from Wikidata. The base BERT model performed very poorly on predicting a subject's religion (the 'hasReligion' relation), achieving an R@P90 score of 0. Performance improved significantly to 0.27 through techniques like AutoPrompt, fine-tuning, and vocabulary extension. The paper notes that this relation was affected by the model predicting the wrong category of entity. The 'hasReligion' relation was ultimately excluded from the final human evaluation phase because of sparse verifiable information on the web.


## An evaluation of Google Translate for Sanskrit to English translation via sentiment and semantic analysis

[https://arxiv.org/pdf/2303.07201](https://arxiv.org/pdf/2303.07201)

**Date:** 2023-02-28

The benchmark measures the quality of Google Translate's translation of a sacred Hindu text, the Bhagavad Gita, from Sanskrit to English. The evaluation is based on sentiment and semantic similarity compared to expert human translations, focusing on the preservation of poetic nature, contextual significance, metaphors, and philosophical concepts. Google Translate's translation of the Bhagavad Gita showed a low level of semantic and sentiment similarity when compared to expert translations. It was found to be unsuitable for translating poetic Sanskrit words and phrases, often failing to capture contextual significance, metaphors, and imagery. The mistranslations occurred because of the model's inability to understand the context of root words and the philosophical depth of the text, leading to translations that were often illogical or devoid of the original meaning.


## Contributing to Accessibility Datasets: Reflections on Sharing Study Data by Blind People

[https://arxiv.org/pdf/2303.04962](https://arxiv.org/pdf/2303.04962)

**Date:** 2023-03-09

Participants' comfort level with sharing their religious affiliation as part of a dataset. Participants raised concerns about sharing their religious affiliation, identifying it as a demographic data point they would not want to share.


## Fairness Evaluation in Text Classification: Machine Learning Practitioner Perspectives of Individual and Group Fairness #Mormon

[https://arxiv.org/pdf/2303.00673](https://arxiv.org/pdf/2303.00673)

**Date:** 2023-03-01

Detection of bias in toxic text classification, measured by comparing model performance (e.g., accuracy, toxic accuracy) on general text versus text containing specific religious identity tokens. The study found that practitioners use religious identity terms (e.g., 'christian', 'muslim', 'jewish') to create custom groups and test for fairness in toxic text classification. The primary finding is that the way fairness metrics are presented (e.g., overall accuracy vs. fairness metrics for specific identity groups including religious ones) significantly influences which model practitioners deem 'fair'. When shown performance breakdowns by group, practitioners were more likely to choose a group-fair model, aiming to avoid misclassifying non-toxic comments that mention minority religious groups.


## Towards Safer Generative Language Models: A Survey on Safety Risks, Evaluations, and Improvements

[https://arxiv.org/pdf/2302.09270](https://arxiv.org/pdf/2302.09270)

**Date:** 2023-11-30

Stereotypical bias detection related to religion. Specifically, the paper surveys benchmarks like that of Nadeem et al. (2021) which assesses stereotypical bias in four domains including race, religion, gender, and profession. The survey indicates that Large Language Models often exhibit societal biases, including stereotypical biases related to religion. These biases are typically inherited from the training data, and researchers have developed datasets and methods to assess and mitigate them.


## Benchmarks for Automated Commonsense Reasoning: A Survey

[https://arxiv.org/pdf/2302.04752](https://arxiv.org/pdf/2302.04752)

**Date:** 2023-02-24

The paper is a broad survey of commonsense reasoning benchmarks and does not focus on faith/religion. One example from the MCTACO benchmark was noted, which tests factual knowledge about Islam's status as a majority religion in a specific historical context. The paper does not present any findings related to religion, as it is not a focus of the survey. The main findings are about the general state of commonsense benchmarks, such as them being frequently flawed and having limited coverage of commonsense domains.


## The Touché23-ValueEval Dataset for Identifying Human Values behind Arguments

[https://arxiv.org/pdf/2301.13771](https://arxiv.org/pdf/2301.13771)

**Date:** 2023-01-31

The benchmark measures the ability of models to identify human values in arguments, including the value 'Be holding religious faith', using a dataset that incorporates arguments from Islamic religious texts (Nahj al-Balagha). Arguments sourced from the Islamic religious text 'Nahj al-Balagha' showed a significantly higher frequency of appealing to the value 'Be holding religious faith' (frequency of 0.100) compared to most other secular sources in the dataset, such as those from the Conference on the Future of Europe (0.008).


## A benchmark for toxic comment classification on Civil Comments dataset

[https://arxiv.org/pdf/2301.11125](https://arxiv.org/pdf/2301.11125)

**Date:** 2023-01-26

The benchmark measured unintended association bias in toxic comment classification models, specifically how models incorrectly associate religious identities (e.g., Christian, Jewish, Muslim) mentioned in non-toxic comments with toxicity. It used metrics like Subgroup AUC, BPSN AUC, and BNSP AUC for this measurement. All tested models exhibited an association bias, tending to incorrectly classify non-toxic comments about certain religious communities as toxic. This bias was particularly noted for comments mentioning 'muslim' and 'jewish' identities. BERT, RNN, and XLNet models were found to be less sensitive to this bias compared to convolution-based models like CNN and CCT.


## AN EMPIRICAL STUDY OF METRICS TO MEASURE REPRESENTATIONAL HARMS IN PRE-TRAINED LANGUAGE MODELS

[https://arxiv.org/pdf/2301.09211](https://arxiv.org/pdf/2301.09211)

**Date:** 2023-01-22

Quantifying manifested implicit representational harms, specifically the propensity of language models to associate marginalized groups with negative perception, stereotypes, and implicit hate speech. For religious groups, this involved measuring the language modeling likelihood of implicitly harmful statements versus benign statements concerning Jewish and Muslim people. The study found that Pre-Trained Language Models (PTLMs) generally are less likely to embed harmful content for Jewish individuals compared to other demographics like women, LGBTQ, and people with disabilities. However, the safety scores for both Jewish and Muslim groups were consistently below 0.5, indicating a significant tendency to manifest harmful representations, far from the ideal score of 1.0.


## VaxxHesitancy: A Dataset for Studying Hesitancy towards COVID-19 Vaccination on Twitter

[https://arxiv.org/pdf/2301.06660](https://arxiv.org/pdf/2301.06660)

**Date:** 2023-04-15

The correlation of religious language with an 'anti-vaxx' stance in tweets. Specifically, it uses the LIWC dictionary to identify 'Religion' as a linguistic category more prevalent in anti-vaccination tweets. The linguistic analysis found that the 'Religion' category (from the LIWC dictionary) was one of the top 10 most correlated features with anti-vaxx tweets. This indicates that anti-vaxx tweets are more likely to refer to religious reasons, such as the debate over vaccines made using aborted fetal tissue, in order to raise fear and influence citizens against vaccination.


## tasksource: A Dataset Harmonization Framework for Streamlined NLP Multi-Task Learning and Evaluation

[https://arxiv.org/pdf/2301.05948](https://arxiv.org/pdf/2301.05948)

**Date:** 2023-05-16

Stance detection towards atheism and knowledge of world religions. The paper does not report specific findings related to religion. The overall finding is that a model fine-tuned on the diverse 'tasksource' collection, which includes some religion-related datasets (e.g., stance on atheism, world religions), achieves strong general performance on an external evaluation.


## MN-DS: A Multilabeled News Dataset for News Article Hierarchical Classification

[https://arxiv.org/pdf/2212.12061](https://arxiv.org/pdf/2212.12061)

**Date:** 2023-04-23

Classification accuracy for news articles in the 'Religion and belief' category. The paper does not provide specific findings related to religion. It presents a dataset that includes a 'Religion and belief' category with 800 articles, establishing a resource for future classification tasks on this topic. The overall findings relate to the classification performance of various models across all 17 categories, with the DistilBERTModel achieving the highest f1 scores.


## Trustworthy Social Bias Measurement

[https://arxiv.org/pdf/2212.11672](https://arxiv.org/pdf/2212.11672)

**Date:** 2022-12-20

Social bias measurement for religious groups, specifically testing the efficacy of debiasing methods for religion in word embeddings. Debiasing methods (Hard/Soft from Manzini et al., 2019) that target religious bias in word embeddings successfully reduce bias according to their own metric, but are found to amplify bias when measured by the paper's proposed, more trustworthy metric.


## A SEVEN-LAYER MODEL FOR STANDARDISING AI FAIRNESS ASSESSMENT

[https://arxiv.org/pdf/2212.11207](https://arxiv.org/pdf/2212.11207)

**Date:** 2022-12-21

The paper proposes a conceptual framework (a seven-layer model) for standardising AI fairness assessment, not a specific benchmark. Within this framework, it identifies 'religion' as an example of a common protected attribute that should be assessed for bias. The paper does not present empirical findings related to religion. It conceptually identifies religion as a common protected attribute, alongside gender, race, and caste, that is associated with social bias and should be meticulously considered during the pre-processing and feature engineering stage (Layer 3) of AI system development to ensure fairness.


## TASK AMBIGUITY IN HUMANS AND LANGUAGE MODELS

[https://arxiv.org/pdf/2212.10711](https://arxiv.org/pdf/2212.10711)

**Date:** 2022-12-20

The benchmark measured the ability of models to correctly identify the presence of a religious leader in a sentence as the salient feature for a binary classification task, when the task specification is ambiguous. The paper found that the ability to resolve task ambiguity for the 'religious leader' classification task was significantly improved by a combination of model scaling and human feedback data (HFD) training, with the best HFD models (text-davinci-002, text-davinci-003) approaching or exceeding human performance. Standard large language models without HFD performed poorly. The models also demonstrated a relative strength in verbalizing the correct task description for the 'religious leader' task compared to other semantic categories, though overall performance on task verbalization was weak.


## In-context Learning Distillation: Transferring Few-shot Learning Ability of Pre-trained Language Models

[https://arxiv.org/pdf/2212.10670](https://arxiv.org/pdf/2212.10670)

**Date:** 2022-12-20

The benchmark included a task for religious hate speech detection, as indicated by the 'ethos-religion' task from the CrossFit benchmark. The paper does not provide specific findings related to religion. The results for the task involving religious hate speech detection ('ethos-religion') are aggregated with results from many other tasks. The main finding is that the proposed in-context learning distillation method generally improves performance on the overall benchmarks used.


## Discovering Language Model Behaviors with Model-Written Evaluations

[https://arxiv.org/pdf/2212.09251](https://arxiv.org/pdf/2212.09251)

**Date:** 2022-12-19

The benchmark measures a language model's tendency to agree or disagree with statements associated with specific religious views (e.g., 'subscribes to Christianity', 'subscribes to Buddhism'), as part of a broader evaluation of the model's 'persona'. Reinforcement Learning from Human Feedback (RLHF) training increases a model's tendency to subscribe to particular religious views, especially Eastern religions (Confucianism, Taoism, Buddhism) relative to others (Judaism, Islam). The paper suggests this may be an unintended side effect stemming from the demographics of the crowdworkers who provided the preference data for RLHF training.


## Do bibliometrics introduce gender, institutional or interdisciplinary biases into research evaluations?

[https://arxiv.org/pdf/2212.07812](https://arxiv.org/pdf/2212.07812)

**Date:** N/A

The paper analyzes bibliometric bias in the academic field of 'Theology & Religious Studies' as one of 34 fields of study. The study found that for the academic field of 'Theology & Religious Studies', both article-level and journal-level citation counts have a zero or negative correlation with peer-reviewed quality scores. This suggests that using bibliometrics for research evaluation in this field is problematic and can disadvantage high-quality departments, a finding consistent with other fields in the arts and humanities.


## “Tell me, how do you know it's me?" Expectations of security and personalization measures for smart speaker applications

[https://arxiv.org/pdf/2212.01905](https://arxiv.org/pdf/2212.01905)

**Date:** 2022-12-04

User-rated importance of security and personalization for smart speaker applications in the 'Faith' category, which includes apps for inspirational speech, scripture, and verses. In a user study evaluating 15 categories of smart speaker apps, the 'Faith' category was rated as having the lowest importance for both security (average rating of 1.69 out of 5) and personalization (average rating of 2.31 out of 5).


## AGRO: ADVERSARIAL DISCOVERY OF ERROR-PRONE GROUPS FOR ROBUST OPTIMIZATION

[https://arxiv.org/pdf/2212.00921](https://arxiv.org/pdf/2212.00921)

**Date:** 2022-12-08

Robustness of toxicity classification for comments mentioning religious groups, specifically the 'other religions' group within the CivilComments dataset. The proposed AGRO method improves model performance on the 'Other Religions-Toxic' worst-group in the CivilComments dataset compared to the ERM baseline (66.7% vs 53.1% accuracy). However, other baseline methods like EIIL performed better on this specific religious subgroup (84.4%).


## SOLD: Sinhala Offensive Language Dataset

[https://arxiv.org/pdf/2212.00851](https://arxiv.org/pdf/2212.00851)

**Date:** 2021-01-01

The benchmark measures general offensive language in the Sinhala language. While the motivation for the work includes real-world events of religious conflict (hate speech against Muslims following attacks on Christian churches), the dataset itself (SOLD) is annotated for broad 'offensive' versus 'not offensive' labels, not specifically for religious hate speech or bias. The paper uses religious conflict in Sri Lanka as a primary motivation for creating a dataset to detect harmful online content. It notes that after the 2019 Easter bombings targeting Christian churches, the government blocked social media to 'curtail the spread of hate speech against Muslims'. However, the paper's experiments and findings are focused on the performance of machine learning models for detecting general offensive language in Sinhala, rather than producing specific findings about religious content, bias, or hate speech, as the dataset was not annotated with religion-specific labels.


## Measuring Harmful Representations in Scandinavian Language Models

[https://arxiv.org/pdf/2211.11678](https://arxiv.org/pdf/2211.11678)

**Date:** 2022-11-21

The benchmark measured the generation of harmful completions related to 'the seven deadly sins of the Christian tradition' using the HurtLex lexicon. Completions related to the 'seven deadly sins of the Christian tradition' were generated by some of the language models (e.g., SwedishMegatron, DanishBERT), although this category of harmful completions was less frequent compared to others like prostitution or derogatory words. For instance, in the DanishBERT model, this category accounted for 0.7% of harmful completions for female-associated prompts and 2.78% for male-associated prompts.


## ArtELingo: A Million Emotion Annotations of WikiArt with Emphasis on Diversity over Language and Culture

[https://arxiv.org/pdf/2211.10780](https://arxiv.org/pdf/2211.10780)

**Date:** 2022-11-19

Cross-cultural differences in emotional responses to religious art and symbols (e.g., Christian symbols like the cross). The emotional interpretation of religious symbols, such as the Christian cross, varies significantly across cultures. For example, an artwork depicting stomping on the devil while holding a cross was perceived positively (awe) in English and Arabic cultures but negatively (fear) in Chinese culture, where the symbol holds less meaning and the act of stomping is perceived as more scary.


## Disentangling Task Relations for Few-shot Text Classification via Self-Supervised Hierarchical Task Clustering

[https://arxiv.org/pdf/2211.08588](https://arxiv.org/pdf/2211.08588)

**Date:** 2022-11-16

The ability to perform few-shot text classification for religious topics, specifically categorizing text into classes such as 'atheism', 'christianity', and 'religion'. The proposed SS-HTC model successfully disentangled underlying task relationships by clustering thematically similar tasks. For instance, it grouped a 5-way classification task from the 20News dataset containing classes like 'alt atheism' and 'soc religion christian' with another 5-way task from the RCV1 dataset that included the class 'religion', demonstrating its ability to recognize that both tasks were related to religion and politics.


## Okapi: Generalising Better by Making Statistical Matches Match

[https://arxiv.org/pdf/2211.05236](https://arxiv.org/pdf/2211.05236)

**Date:** 2022-11-07

Worst-group accuracy in a toxicity classification task, where demographic groups include religion. The proposed 'Okapi' method, using a pre-trained DistilBERT backbone, significantly improves the worst-group accuracy on the CivilComments toxicity classification task, achieving performance on par with a fully-labelled baseline. This indicates improved robustness for subgroups, including those based on religion.


## No Word Embedding Model Is Perfect: Evaluating the Representation Accuracy for Social Bias in the Media

[https://arxiv.org/pdf/2211.03634](https://arxiv.org/pdf/2211.03634)

**Date:** 2022-11-07

Implicit bias against Christianity compared to Islam, measured by associating religious terms (e.g., Christianity, Islam) with pleasant/unpleasant attributes using the Word Embedding Association Test (WEAT). The study found that different word embedding algorithms produce highly variable results when measuring religious bias (Islam vs. Christianity). Models trained on conservative news corpora were expected to show more bias against Islam than models trained on liberal corpora, but this was not consistently observed across all algorithms. The Decontextualized and Frequency-Agnostic models, designed to be more robust, showed little difference between liberal and conservative corpora. A temporal analysis using the decontextualized model suggested that religious bias in the news corpus increased over the 12-year period from 2010 to 2021.


## Human-Machine Collaboration Approaches to Build a Dialogue Dataset for Hate Speech Countering

[https://arxiv.org/pdf/2211.03433](https://arxiv.org/pdf/2211.03433)

**Date:** 2022-11-07

Generation of multi-turn counter-narratives against hate speech targeting religious groups (Muslims and Jews), often based on stereotypes. The paper introduced DIALOCONAN, a dataset for generating multi-turn dialogues to counter hate speech. The dataset includes hate speech targeting Jews (15.30%) and Muslims (16.51%). The findings focus on the comparative efficiency and quality of various hybrid data collection methodologies (concatenation of existing pairs, paraphrasing, and full generation with LMs) for creating these dialogues, rather than on the specific performance or biases of models concerning religious topics.


## DEArt: Dataset of European Art

[https://arxiv.org/pdf/2211.01226](https://arxiv.org/pdf/2211.01226)

**Date:** 2022-11-03

Detection of religious objects, figures, and symbols in European art. Computer vision models trained on the DEArt dataset can successfully detect religious objects and figures (e.g., angels, halos, monks, crucifixion scenes) common in European art. This approach significantly outperforms models trained on generic photograph datasets (like MS COCO), which are unable to recognize these cultural heritage-specific, often religious, classes.


## CONDAQA: A Contrastive Reading Comprehension Dataset for Reasoning about Negation

[https://arxiv.org/pdf/2211.00295](https://arxiv.org/pdf/2211.00295)

**Date:** 2022-11-01

Reasoning about the behavioral implications of religious beliefs (e.g., Jehovah's Witnesses' refusal to salute flags) as part of a broader benchmark on understanding linguistic negation. The paper does not offer findings specific to religion. It uses a religious context (Jehovah's Witnesses' refusal to salute flags based on their beliefs) as an example to test a model's ability to reason about the implications of negated statements and strongly held principles, but the overall findings relate to the general difficulty models have with negation, not religious content itself.


## POLYHOPE: TWO-LEVEL HOPE SPEECH DETECTION FROM TWEETS

[https://arxiv.org/pdf/2210.14136](https://arxiv.org/pdf/2210.14136)

**Date:** 2022-11-03

Detection of two levels of hope speech (binary: Hope/Not Hope; multiclass: Generalized, Realistic, Unrealistic Hope) in English tweets. The dataset includes tweets from the religion domain and was collected using keywords that include religious expressions like 'Inshallah'. The paper's primary findings are on model performance for hope speech detection. The inclusion of religious terms like 'Inshallah' as a data collection keyword and as an example of 'Generalized Hope' indicates that the developed models are capable of classifying hope speech when it is expressed through religious language, treating it as a feature of hopeful expression rather than analyzing it from a theological or bias perspective.


## Deconfounding Legal Judgment Prediction for European Court of Human Rights Cases Towards Better Alignment with Experts

[https://arxiv.org/pdf/2210.13836](https://arxiv.org/pdf/2210.13836)

**Date:** 2022-10-25

The benchmark measured the model's reliance on the word 'religious' as a spurious, legally irrelevant cue for predicting legal outcomes, as part of a broader deconfounding effort. The word 'religious' was identified as a spurious correlation for predicting legal outcomes. An expert analysis confirmed that while Article 9 of the European Convention on Human Rights relates to religious freedom, the word 'religious' by itself is not relevant to legal reasoning and acts as a distracting signal for the model. The study's deconfounding methods were designed to mitigate reliance on such spurious tokens.


## TAPE: Assessing Few-shot Russian Language Understanding

[https://arxiv.org/pdf/2210.12813](https://arxiv.org/pdf/2210.12813)

**Date:** 2022-10-23

The benchmark measures ethical judgments in Russian texts. Religion is not a direct focus of measurement but is acknowledged as a sensitive topic and a potential influencing factor ('religious norms') in how humans annotate the data for ethical concepts like virtue, law, and morality. The paper does not present findings on model performance regarding religion. Instead, it identifies that societal factors, including 'religious norms', contribute to the subjectivity and complexity of evaluating ethical judgments. This leads to moderate inter-annotator agreement and potential shifts in ground-truth data over time, posing a challenge for benchmarking.


## Scaling Instruction-Finetuned Language Models

[https://arxiv.org/pdf/2210.11416](https://arxiv.org/pdf/2210.11416)

**Date:** 2022-12-06

The benchmark measured the propensity of models to generate toxic text when prompted with sentences containing identity terms, including religious groups. This was evaluated by measuring the percentage and distribution of toxicity scores for model-generated continuations. Instruction finetuning reduces the overall generation of toxic language for prompts with religious identity terms compared to the base PaLM models. However, the finetuned Flan models still exhibit bias, mirroring patterns found in PaLM. Specifically, the upper quartile of toxicity scores for prompts related to Judaism was consistently higher than for other religious groups.


## Evaluation Metrics for Measuring Bias in Search Engine Results

[https://arxiv.org/pdf/2210.10517](https://arxiv.org/pdf/2210.10517)

**Date:** 2023-02-03

The benchmark measured the stance bias (pro/against) and ideological bias (conservative/liberal) of search engine results for a set of 57 controversial queries, one of which was religious in nature: 'Should the Words "Under God" Be in the US Pledge of Allegiance?'. The paper did not report specific findings for the single religion-related query. The general finding across all 57 controversial topics was that neither search engine (Google, Bing) exhibited significant stance bias, but both showed a statistically significant ideological bias, favoring a liberal leaning.


## A Survey of Parameters Associated with the Quality of Benchmarks in NLP

[https://arxiv.org/pdf/2210.07566](https://arxiv.org/pdf/2210.07566)

**Date:** 2022-10-14

The paper surveys parameters to measure benchmark quality, identifying religious stereotypes as one potential source of spurious bias in datasets. The paper identifies that hypotheses in Natural Language Inference (NLI) datasets can contain religious stereotypes, which can act as a form of contextual bias, potentially influencing a model to favor a particular label.


## M2D2: A Massively Multi-Domain Language Modeling Dataset

[https://arxiv.org/pdf/2210.07370](https://arxiv.org/pdf/2210.07370)

**Date:** 2022-10-13

Language modeling performance, measured by perplexity, on texts from the 'Religion and belief systems' domain. The paper found that the 'Religion and belief systems' domain exhibits poor out-of-domain transfer performance when paired with dissimilar domains like 'Mathematics'. A model adapted to the Mathematics domain performed poorly when evaluated on the Religion domain, and vice-versa, indicating low content overlap and transferability between these specific domains.


## Quantifying Social Biases Using Templates is Unreliable

[https://arxiv.org/pdf/2210.04337](https://arxiv.org/pdf/2210.04337)

**Date:** 2022-10-09

The paper does not measure religious bias in its own experiments. It cites prior work from Abid et al. [2021] that measures anti-Muslim bias as a motivating example for the importance of fairness evaluation. The paper's primary findings are about the unreliability of template-based bias measurement methods. It does not present new findings related to religion but uses existing research showing anti-Muslim bias in GPT-3 as a motivation for its work.


## RAINIER: Reinforced Knowledge Introspector for Commonsense Question Answering

[https://arxiv.org/pdf/2210.03078](https://arxiv.org/pdf/2210.03078)

**Date:** 2022-10-22

The benchmark includes questions that measure knowledge of culture-specific religious concepts and beliefs, such as the role of God in religion and beliefs associated with Western/Christian culture. The model, RAINIER, generates knowledge that can be culture-specific. The paper's analysis shows examples where the model produces statements related to religious concepts (e.g., 'God is a judge of people') and beliefs rooted in specific cultures (e.g., Christian culture), highlighting its ability to capture and reproduce such information when prompted with relevant questions.


## K-MHaS: A Multi-label Hate Speech Detection Dataset in Korean Online News Comment

[https://arxiv.org/pdf/2208.10684](https://arxiv.org/pdf/2208.10684)

**Date:** 2022-09-30

Detection of hate speech based on religion, as one of eight categories in a multi-label classification task for Korean online news comments. Hate speech targeting religion was one of the least frequent categories in the K-MHaS dataset, accounting for 5.1% of single-label hate speech instances and 1.8% of multi-label instances. The most common keywords associated with this category included derogatory terms for Christians ('Gaedok'), references to specific new religious movements ('Shincheonji'), the term for pseudo/heretical cults ('Saibi'), the general word for religion ('Jonggyo'), and 'Jesus' ('Yesu').


## Benchmarking Azerbaijani Neural Machine Translation

[https://arxiv.org/pdf/2207.14473](https://arxiv.org/pdf/2207.14473)

**Date:** 2022-07-29

Machine translation performance (BLEU, chrF, COMET scores) on religious texts from the Tanzil corpus, which contains Quranic translations. A specialized NMT model trained on a religious domain dataset (Tanzil corpus) outperformed a model trained on a larger combined dataset when translating religious texts, as measured by BLEU and chrF scores. However, the combined model achieved a better COMET score, indicating its output was semantically closer to the reference translation. This highlights the effectiveness of in-domain training for specialized translation tasks.


## DataPerf: Benchmarks for Data-Centric AI Development

[https://arxiv.org/pdf/2207.10062](https://arxiv.org/pdf/2207.10062)

**Date:** 2023-10-13

Stereotype and harmful content detection related to religious groups, specifically within a text-to-image generation context. The paper presents a benchmark ('Adversarial Nibbler') designed to capture harmful stereotypes in text-to-image models. It provides an example of its intended use, where a user identifies a harmful image generated from a prompt like 'Muslim man holding an object' and can describe the harm by rewriting the prompt to an explicitly harmful expression like 'Muslim holding a gun', illustrating the type of bias the benchmark aims to identify.


## FLAIR: Federated Learning Annotated Image Repository

[https://arxiv.org/pdf/2207.08869](https://arxiv.org/pdf/2207.08869)

**Date:** 2022-07-18

The benchmark measured the model's classification performance (averaged precision) on a coarse-grained image class labeled 'religion', which was the least frequent class in the dataset. The 'religion' class, being the least frequent in the dataset, exhibited significantly lower classification performance compared to more common classes. This performance degradation was exacerbated in federated learning settings and became extremely poor under differential privacy, highlighting the challenge of learning from rare classes in distributed, private environments. For instance, in the fine-tuned private federated learning setting, the averaged precision for the 'religion' class was only 0.7, compared to 84.1 for the 'structure' class.


## No Language Left Behind: Scaling Human-Centered Machine Translation

[https://arxiv.org/pdf/2207.04672](https://arxiv.org/pdf/2207.04672)

**Date:** 2022-06-30

The paper does not use a benchmark to specifically measure faith or religion. However, it uses the 'Christian Bible' corpus as a source of training data and as a calibration set for measuring baseline toxicity levels across different languages and corpora. It also samples data from Wikipedia's 'Philosophy and Religion' category for its seed dataset. The paper's findings related to religion are methodological rather than analytical. It highlights that religious texts, specifically the Christian Bible, are a valuable but domain-limited source of parallel data for low-resource languages. Additionally, the Christian Bible corpus was used as a cross-lingual constant to calibrate toxicity levels in various training corpora, based on the assumption that it has a consistent, low level of toxicity across languages.


## Pile of Law: Learning Responsible Data Filtering from the Law and a 256GB Open-Source Legal Dataset

[https://arxiv.org/pdf/2207.00220](https://arxiv.org/pdf/2207.00220)

**Date:** 2022-11-29

The paper did not conduct a benchmark measurement specifically in terms of faith or religion. Religious content appeared incidentally in qualitative examples used to test the nuance of toxicity filters, specifically in the context of legal arguments about aid to religious schools and quoted hateful speech with religious undertones. The paper does not present specific findings about religion. It uses legal texts with religious content (e.g., a case about government aid to religious schools, a case quoting hateful religious speech) as qualitative examples to demonstrate the challenges of automated toxicity filtering. These examples show that context is crucial, as adding more text can drastically change a toxicity score, and that some legal arguments involving religion are ambiguous for current filters.


## Theory-Grounded Measurement of U.S. Social Stereotypes in English Language Models #Mormon

[https://arxiv.org/pdf/2206.11684](https://arxiv.org/pdf/2206.11684)

**Date:** 2022-06-23

Detection of stereotypical associations between social groups (including religious groups) and 32 traits across three dimensions: Agency/Socioeconomic Success, Conservative–Progressive Beliefs, and Communion. The 'Beliefs' dimension includes traits like 'religious vs. science-oriented' and 'traditional vs. modern'. The study found that language models' stereotypical associations for religious groups (e.g., Jewish, Muslim, Christian, Buddhist, Mormon) show a moderate alignment with human stereotype judgments. The proposed SeT measurement on the RoBERTa model yielded the highest alignment with human annotations across all groups. Specific correlation scores for religious groups are provided in the appendix (e.g., Table A11), showing varying degrees of alignment for different groups and models, but no specific religious stereotypes were highlighted as major findings in the main text.


## Characteristics of Harmful Text: Towards Rigorous Benchmarking of Language Models

[https://arxiv.org/pdf/2206.08325](https://arxiv.org/pdf/2206.08325)

**Date:** 2022-10-28

The paper analyzes existing benchmarks that measure various forms of religious bias, including: stereotypical associations (Stereoset), sentiment bias (Sentiment Bias), differences in regard and completion probabilities for religious terms (DTC), generation of violent words in completions for prompts about specific religious groups (Muslim Bias), and reliance on stereotypes in question answering (BBQ, UnQover). The primary focus is not on running new measurements but on using these examples to propose a framework for more rigorous benchmark design. The paper finds that while several benchmarks exist to measure religious bias (e.g., anti-Muslim bias, stereotypes, sentiment bias), they are part of a broader landscape of harm evaluation that has significant gaps. The paper critiques these benchmarks for often lacking sufficient textual and social context, and uses religious bias as a key example to illustrate the need for more rigorous benchmark design based on the six proposed characteristics of harmful text.


## Causal Discovery for Fairness

[https://arxiv.org/pdf/2206.06685](https://arxiv.org/pdf/2206.06685)

**Date:** 2022-06-14

The paper mentions religion as an example of a sensitive attribute for fairness analysis, but no benchmarks or measurements related to faith or religion were actually conducted in the experiments. The paper's key findings are related to the methodology of causal discovery for fairness and do not involve religion. Religion is mentioned only as a theoretical example of a sensitive attribute, but it was not included as a variable in any of the experimental datasets (e.g., Compas, Adult, German credit) or analyses. The study focuses on sensitive attributes like race and sex.


## The Construction and Evaluation of the LEAFTOP Dataset of Automatically Extracted Nouns in 1480 Languages

[https://arxiv.org/pdf/2206.05034](https://arxiv.org/pdf/2206.05034)

**Date:** 2022-05-09

Effectiveness of a probabilistic inference method for extracting noun lexicons from New Testament translations across 1480 languages. The study uses the New Testament as a large-scale parallel corpus for linguistic extraction. A key finding is that while the method is generally effective, common religious terms such as 'prophet', 'God', and 'parable' are disproportionately harder to extract correctly compared to non-religious terms like 'wind' or 'finger'. The choice of Bible translation also significantly impacts results, with literal translations yielding much higher quality vocabulary extraction than paraphrased versions.


## Measuring Gender Bias in Word Embeddings of Gendered Languages Requires Disentangling Grammatical Gender Signals

[https://arxiv.org/pdf/2206.01691](https://arxiv.org/pdf/2206.01691)

**Date:** 2022-06-03

Stereotype detection, specifically measuring the association between gender (men/women) and concepts like science vs. humanities. The 'humanities' category included the term 'theology', thus indirectly measuring gender stereotypes related to theology as part of a broader concept. The paper does not focus on religion, but 'theology' is included as a stimulus word in the 'humanities' category for gender stereotype tests (men:science vs. women:humanities). The primary finding is that grammatical gender in languages like Polish and Spanish can create anomalous results, such as a men:humanities-women:science bias. After applying a method to disentangle grammatical gender, these biases shift to become more congruent with real-world psychological data (in the case of Polish and Spanish, the association becomes neutral). This indirectly suggests that measurements of gender bias related to theology are also skewed by linguistic structure and are corrected by the proposed method.


## Hollywood Identity Bias Dataset: A Context Oriented Bias Analysis of Movie Dialogues

[https://arxiv.org/pdf/2205.15951](https://arxiv.org/pdf/2205.15951)

**Date:** 2022-06-01

Detection of identity bias and stereotypes related to religion in Hollywood movie dialogues. The annotation includes the bias category (Religion), the target group (e.g., Christian, Judaism, Islam, Atheist), and the reason for the bias. The BART-large model demonstrated strong performance in identifying religion bias, achieving an F1 score of 0.75, which was among the highest scores across all bias categories. Error analysis revealed instances where the model correctly identified religion bias but also incorrectly predicted an additional bias category, such as gender.


## MITIGATING DATASET BIAS BY USING PER-SAMPLE GRADIENT

[https://arxiv.org/pdf/2205.15704](https://arxiv.org/pdf/2205.15704)

**Date:** 2023-02-10

The benchmark measured the model's ability to mitigate bias in toxicity classification. Specifically, it evaluated whether the model's classification of a comment as 'toxic' was unfairly influenced by the mention of demographic identities, including religious groups like Muslim and Christian. The proposed method, PGD, outperformed other baseline methods on the CivilComments-WILDS benchmark, achieving the highest worst-group accuracy. This indicates it is more robust in classifying comment toxicity without being unfairly influenced by spurious correlations with mentions of demographic identities, which include religious groups.


## ER-TEST: Evaluating Explanation Regularization Methods for Language Models

[https://arxiv.org/pdf/2205.12542](https://arxiv.org/pdf/2205.12542)

**Date:** 2023-02-28

bias against group identifiers in hate speech detection, measured using the false positive rate difference (FPRD) metric. Explanation regularization (ER) with a relaxed 'Order' alignment criterion was found to be effective in reducing bias (measured by False Positive Rate Difference) against group identifiers like 'Muslim' in hate speech detection tasks. This approach yielded the lowest bias among all models on both seen and unseen datasets, significantly outperforming the baseline model without ER.


## On Measuring Social Biases in Prompt-Based Multi-Task Learning #Mormon

[https://arxiv.org/pdf/2205.11605](https://arxiv.org/pdf/2205.11605)

**Date:** 2022-05-23

The paper measures social biases and stereotypes associated with various religious groups. Specifically, the BBNLI benchmark, created by the authors, measures cognitive biases (splitting, horn effect, illusory correlation, representativeness heuristic) through stereotypical hypotheses related to religion, such as 'Catholic women prioritize creating a family over their careers' and 'Most Mormon women are unfortunately oppressed by their husbands'. The T0 model exhibits significantly more bias related to religious stereotypes when prompted in a question-answering (QA) format—a format seen during its training—compared to a novel Natural Language Inference (NLI) format. This holds true even when the semantic content of the input is identical. For example, in the BBQ benchmark analysis, QA predictions were substantially more biased than NLI predictions for the religion domain.


## Challenges in Measuring Bias via Open-Ended Language Generation

[https://arxiv.org/pdf/2205.11601](https://arxiv.org/pdf/2205.11601)

**Date:** 2022-05-23

The benchmark measured the toxicity of open-ended text generations based on prompts related to different religious ideologies, in order to assess bias. This was done by calculating the ratio of mean toxicity scores between different religious groups. The key finding is that measurements of religious bias in language generation are highly sensitive to experimental settings. For instance, the toxicity ratio for text generated from prompts about Sikhism compared to Hinduism was found to be 4.7 times higher when generating 10 tokens versus 40 tokens. This demonstrates that conclusions about religious bias can be inconsistent and vary dramatically based on methodological choices like the length of the generated text, making it difficult to draw firm conclusions about a model's inherent bias.


## KOLD: Korean Offensive Language Dataset

[https://arxiv.org/pdf/2205.11315](https://arxiv.org/pdf/2205.11315)

**Date:** 2022-11-05

Detection of offensive language targeting specific religious groups, including identifying the comment as offensive, the target as a group, and the specific religious group being targeted (e.g., Muslim, Christian). Religion is a significant attribute for targeted offensive language in Korean online comments, accounting for 13.42% of group-targeted offenses in the KOLD dataset. The most frequently targeted religious groups were Muslim, Christian, and Catholic. The distribution of targeted religious groups differs from English datasets; for example, 'Christian' is a top target in the Korean dataset but not in the English HateXplain dataset, while 'Jewish' is a top target in HateXplain but not in KOLD.


## "I'm sorry to hear that”: Finding New Biases in Language Models with a Holistic Descriptor Dataset #Mormon

[https://arxiv.org/pdf/2205.09209](https://arxiv.org/pdf/2205.09209)

**Date:** 2022-10-27

The benchmark, HOLISTICBIAS, measures bias in language models by analyzing 'demographic difference', which refers to group-level differences in model output or assigned probabilities resulting from different religious identity terms in the input text. Specifically, it assesses bias through three methods: 1) differences in token likelihoods (perplexity) for sentences containing religious descriptors, 2) variations in the conversational styles (e.g., curiosity, confusion, sympathy) of generated text when prompted with religious identifiers, and 3) differential rates at which sentences with religious terms are flagged as offensive by a classifier. The study found that language models exhibit distinct biases related to religious terms. Religious descriptors often elicited conversational styles associated with curiosity and confusion. For instance, terms like 'spiritualist', 'hindu', 'shintoist', and 'confucianist' were particularly linked to generating curious responses. In contexts designed to be negative (e.g., using the template 'I hate [RELIGIOUS GROUP].'), sentences containing a wide range of religious identifiers (including Muslim, Mormon, Rastafarian, Hindu, Jewish, Sikh, and Amish) were classified as highly offensive (99.9%-100%) by an offensiveness classifier, indicating the models' sensitivity to hateful statements involving religious identities.


## Dialog Inpainting: Turning Documents into Dialogs

[https://arxiv.org/pdf/2205.09073](https://arxiv.org/pdf/2205.09073)

**Date:** 2022-05-31

Detection of potentially sensitive interactions in generated dialogs, by identifying co-occurrences of terms from sensitive categories (including religion) with potentially negative connotations or in sensitive contexts. A small fraction (0.2-0.5%) of the synthetically generated dialogs contained potentially sensitive interactions involving religious terms (e.g., co-occurrence of 'Allah' and 'attack'). The authors flag these instances but note that expert manual review is required to determine if they perpetuate unfair bias, advising users to be aware of these observations.


## PVS Embeddings of Propositional and Quantified Modal Logic

[https://arxiv.org/pdf/2205.06391](https://arxiv.org/pdf/2205.06391)

**Date:** 2022-05-12

The paper does not benchmark a large language model. Instead, it uses the PVS (Prototype Verification System) to conduct a formal logical analysis and verification of Anselm's Ontological Argument for the existence of God. The goal is to demonstrate how a formal system can be used to precisely model and reason about complex theological/philosophical arguments, revealing logical subtleties and complexities. The paper demonstrates that formalizing theological arguments, specifically Anselm's Ontological Argument, within the PVS verification system reveals significant logical subtleties and complexities that are often overlooked in informal treatments. The process of formalization forces a precise interpretation of modal operators and quantifiers, showing how apparently similar formulas can have different meanings and highlighting the care required to correctly capture the argument's intent.


## DTW at Qur'an QA 2022: Utilising Transfer Learning with Transformers for Question Answering in a Low-resource Domain

[https://arxiv.org/pdf/2205.06025](https://arxiv.org/pdf/2205.06025)

**Date:** 2022-05-12

The benchmark measures the ability of models to perform machine reading comprehension (MRC) on the Qur'an. This involves answering questions by extracting a span of text from a given passage of the Qur'an. The study found that transformer models built specifically for Arabic (e.g., camelbert-mix, AraELECTRA-discriminator) generally outperformed multilingual models on the Qur'an QA task. The key finding was that transfer learning from a larger, general-domain Arabic MRC dataset (SOQAL) significantly improved performance on the low-resource Qur'an dataset, particularly for the AraELECTRA-discriminator model. While self-ensemble learning did not consistently improve scores, it led to more stable and consistent results. The best performing system utilized AraELECTRA-discriminator with transfer learning.


## HateCheckHIn: Evaluating Hindi Hate Speech Detection Models

[https://arxiv.org/pdf/2205.00328](https://arxiv.org/pdf/2205.00328)

**Date:** 

The benchmark measures the capability of hate speech detection models to correctly identify hateful content directed towards various protected groups, including religious groups such as Hindus and Muslims, particularly in monolingual Hindi and multilingual/code-mixed Hindi-English contexts. The hate speech detection models tested (mBERT fine-tuned on H-21 and C-21 datasets, and Perspective API) showed varied and often poor performance in identifying hate speech targeting religious groups (Hindus and Muslims), especially in multilingual and code-mixed scenarios. Performance differed across models and target groups, with the C-21 fine-tuned mBERT generally performing better for both Hindu and Muslim targets than the H-21 version. The Perspective API showed moderate performance. The results indicate that models struggle with the linguistic nuances of hate speech against religious communities in Hindi.


## CAVES: A Dataset to facilitate Explainable Classification and Summarization of Concerns towards COVID Vaccines

[https://arxiv.org/pdf/2204.13746](https://arxiv.org/pdf/2204.13746)

**Date:** 2022-11-11

Ability to classify tweets expressing anti-vaccine sentiment for religious reasons, as one of twelve categories of vaccine concern. Models performed poorly on the 'Religious' class of anti-vaccine concerns. This was attributed to the class being very sparse, with few examples in the dataset, which hindered model performance.


## HiNER: A Large Hindi Named Entity Recognition Dataset

[https://arxiv.org/pdf/2204.13743](https://arxiv.org/pdf/2204.13743)

**Date:** 2022-04-28

Ability of language models to identify named entities categorized as 'Religion' in Hindi text. The 'RELIGION' entity type was identified as one of the most challenging categories for the models to recognize correctly. The best performing model, XLM-Rlarge, achieved a mean F1-score of 72.27 for this category. Further analysis showed that models were often able to identify religious entities (boundary detection) but sometimes struggled to assign the correct entity type (type classification).


## SUPER-NATURALINSTRUCTIONS: Generalization via Declarative Instructions on 1600+ NLP Tasks

[https://arxiv.org/pdf/2204.07705](https://arxiv.org/pdf/2204.07705)

**Date:** 2022-10-24

Task performance (ability to follow natural language instructions) on NLP tasks within the domain of 'World Religions'. The paper does not measure specific aspects like bias or theological knowledge. The paper does not report any specific findings related to religion. Performance is aggregated across general task types and not broken down by domain, so the performance on 'World Religions' tasks is not specified.


## Identifying and Measuring Token-Level Sentiment Bias in Pre-trained Language Models with Prompts

[https://arxiv.org/pdf/2204.07289](https://arxiv.org/pdf/2204.07289)

**Date:** 2022-04-15

Sentiment bias of religious terms, which were included in a larger set of supposedly neutral words to test if pre-trained language models associate them with positive or negative sentiment. The paper found that the term 'Religious' was identified as a neutral word (score 0.0) by the Sentiment Shift Test on a fine-tuned RoBERTa-Base model. The term 'Hindu' was identified as a nearly neutral word (score 0.02) by the same test on a pre-trained RoBERTa-Base model. This indicates these terms did not exhibit strong sentiment bias in the tested models, unlike many other supposedly neutral words.


## Korean Online Hate Speech Dataset for Multilabel Classification - How Can Social Science Improve Dataset on Hate Speech? -

[https://arxiv.org/pdf/2204.03262](https://arxiv.org/pdf/2204.03262)

**Date:** 2022-07-01

Detection of hate speech directed at religious groups within the South Korean cultural context, as one of seven multilabel hate speech categories. The paper found that religious hate speech in the South Korean online context is distinct from Western cases. It is primarily targeted at Protestants, one of the country's major religions, due to their perceived right-wing extremism and exclusiveness, rather than at religious minorities. Hate speech against Islam, while present, tends to be reactive to specific international or domestic events. The developed models were successfully trained to identify these nuanced and context-specific forms of religious hate speech, with performance significantly improving after augmenting the dataset with human-in-the-loop (HITL) curated examples.


## The MORAL INTEGRITY CORPUS: A Benchmark for Ethical Dialogue Systems

[https://arxiv.org/pdf/2204.03021](https://arxiv.org/pdf/2204.03021)

**Date:** 2022-04-06

The benchmark measures the ability of dialogue systems to generate moral 'Rules of Thumb' (RoTs) for various situations, including those involving religion and faith. For religious contexts, it assesses whether the generated RoT aligns with moral foundations such as Loyalty, Sanctity, and Liberty. The benchmark includes scenarios involving religion and faith, and the proposed framework can capture the moral reasoning in these contexts through 'Rules of Thumb' (RoTs). These RoTs are often categorized under moral foundations such as Loyalty, Sanctity, and Liberty. For example, a response affirming faith was associated with a RoT about the good of being in a faith community.


## Annotation-Scheme Reconstruction for “Fake News" and Japanese Fake News Dataset

[https://arxiv.org/pdf/2204.02718](https://arxiv.org/pdf/2204.02718)

**Date:** 2022-04-06

The paper proposes a new annotation scheme for fake news. Within this scheme, one of the categories for the 'purpose' of false news is 'propaganda', which is defined as news that attempts to influence audiences for ideological, religious, or other purposes. The benchmark, therefore, allows for the identification of religious propaganda. The paper's proposed annotation scheme for fake news includes 'propaganda' as a potential purpose, which is defined as influencing audiences for 'ideological, religious, and other purposes'. However, the subsequent analysis of the created Japanese dataset does not provide specific findings or statistics on the prevalence of religious-themed fake news.


## PaLM: Scaling Language Modeling with Pathways

[https://arxiv.org/pdf/2204.02311](https://arxiv.org/pdf/2204.02311)

**Date:** 2022-10-05

Co-occurrence of stereotypes and toxicity analysis in generated text related to religious groups. The analysis measured descriptive words co-occurring with religious identity terms in prompted sentence completions and the toxicity probability of continuations for prompts mentioning various religious groups. The analysis found that the model associates Islam with highly charged stereotypes such as 'terrorist', 'violent', and 'radical'. Prompts mentioning Islam and Judaism also had a higher probability of generating toxic responses compared to other religious groups. The paper notes these findings highlight the potential for the model to falsely affirm stereotypes of Muslims as terrorists, extremists, and violent.


## SPREAD SPURIOUS ATTRIBUTE: IMPROVING WORST-GROUP ACCURACY with SPURIOUS ATTRIBUTE ESTIMATION

[https://arxiv.org/pdf/2204.02070](https://arxiv.org/pdf/2204.02070)

**Date:** 2022-04-05

The benchmark measured worst-group accuracy on a toxicity detection task where demographic attributes, including religious identity (Muslim, Christian, other religion), were treated as spurious attributes. The proposed method, Spread Spurious Attribute (SSA), improves worst-group accuracy on the CivilComments-WILDS dataset where religious identities are spurious attributes. SSA achieves performance comparable to methods using full supervision on the spurious attribute, even when using a significantly smaller amount of labeled data, thereby mitigating performance drops for groups defined by religious identity.


## Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI

[https://arxiv.org/pdf/2204.01075](https://arxiv.org/pdf/2204.01075)

**Date:** 2022-04-03

The paper does not present a benchmark but proposes a framework for documenting datasets, which includes 'Religion' as a potential sensitive human attribute. The paper's primary contribution is a framework for dataset documentation called 'Data Cards'. The framework's template includes 'Religion' as an example of a sensitive human attribute that should be documented to foster transparency and responsible use of the dataset.


## Training Compute-Optimal Large Language Models

[https://arxiv.org/pdf/2203.15556](https://arxiv.org/pdf/2203.15556)

**Date:** 2022-03-29

The benchmark measured the models' knowledge of world religions and specific Hindu knowledge via multiple-choice questions (from MMLU and BIG-bench benchmarks respectively). The paper's model card also notes that the model was analyzed for generating text with varying sentiment when prompted about religious groups. The compute-optimal model, Chinchilla (70B), demonstrated superior performance on knowledge-based religion tasks compared to the larger model Gopher (280B). Specifically, Chinchilla achieved a score of 87.7% on the 'world_religions' MMLU task (vs. Gopher's 84.2%) and 91.4% on the 'hindu_knowledge' BIG-bench task (vs. Gopher's 80.0%). Additionally, the model card notes that prompting the model about religious groups can lead to outputs with varied sentiment, reflecting biases present in the training data.


## On the Intrinsic and Extrinsic Fairness Evaluation Metrics for Contextualized Language Representations #Mormon

[https://arxiv.org/pdf/2203.13928](https://arxiv.org/pdf/2203.13928)

**Date:** 2022-03-25

The study measures bias, specifically group disparities in sentiment, toxicity, and stereotypes, related to various religious groups across intrinsic and extrinsic fairness metrics. The study found that intrinsic and extrinsic fairness metrics do not correlate well, and in the religion domain, they often show statistically negative correlations. This lack of correlation for religion was partly attributed to noise in the evaluation datasets; for instance, the BOLD dataset's prompts for religion were found to contain toxic and stereotyped content, which biased the generation outputs and skewed the extrinsic metric scores.


## L3Cube-MahaHate: A Tweet-based Marathi Hate Speech Detection Dataset and BERT models

[https://arxiv.org/pdf/2203.13778](https://arxiv.org/pdf/2203.13778)

**Date:** 2022-05-22

Detection of hate speech targeted at specific groups based on their religion, race, ethnic origin, gender, and geographical location. The paper's findings are about the overall performance of various models on Marathi hate speech detection, not specifically about religion. The dataset created, L3Cube-MahaHate, is designed to include hate speech targeting groups based on religion, among other categories. The key finding was that monolingual Marathi BERT models (MahaBERT, MahaRoBERTa) surpassed the performance of multilingual models (IndicBERT, mBERT, xlm-RoBERTa) on this task.


## Listening to Affected Communities to Define Extreme Speech: Dataset and Experiments

[https://arxiv.org/pdf/2203.11764](https://arxiv.org/pdf/2203.11764)

**Date:** 2022-03-22

Detection of extreme speech (derogatory, exclusionary, dangerous) targeted at various marginalized groups, with a specific focus on religious minorities in certain national contexts. The study found that religious minorities are a major target of extreme speech, particularly in India, where terms like 'Muslims' and 'Hindus' are frequent in hateful content. In Germany, 'Jude' (Jew) was also a frequent term. The models tested (mBERT, XLM-R, etc.) learned to use these religious identifiers as strong keywords to classify the target of the speech, which made the target classification task relatively easy. However, interpretability analysis revealed that models rely heavily on these keywords, indicating a potential deficiency and a shallow understanding of the context, rather than a deep comprehension of the hate speech itself.


## TOXIGEN: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection

[https://arxiv.org/pdf/2203.09509](https://arxiv.org/pdf/2203.09509)

**Date:** 2022-07-14

The benchmark (TOXIGEN dataset) was created to measure and improve the detection of implicit and adversarial hate speech (toxic statements) against minority groups, including religious groups (Muslims and Jewish people). The measurement involves generating balanced sets of toxic and benign statements for each group and evaluating classifiers on their ability to distinguish them. The paper successfully created TOXIGEN, a large-scale, balanced dataset of machine-generated implicit toxic and benign statements concerning 13 minority groups, which includes Muslims and Jewish people. The key finding is that fine-tuning existing hate speech classifiers on this dataset substantially improves their ability to detect implicit toxicity in human-written text, thereby offering a method to mitigate bias and improve safety for these religious groups.


## Combining Modular Skills in Multitask Learning

[https://arxiv.org/pdf/2202.13914](https://arxiv.org/pdf/2202.13914)

**Date:** 2022-03-01

Stance detection towards atheism and hate speech detection in religious contexts, as part of a larger multitask benchmark (CrossFit) designed to test general NLP capabilities. The paper does not report specific findings related to religion. Results are aggregated across a wide variety of tasks, and the religion-related datasets were a small part of the overall benchmark. The main finding is that the proposed modular 'SKILLED' model shows superior sample-efficiency and few-shot generalization compared to baselines.


## Healthsheet: Development of a Transparency Artifact for Health Datasets

[https://arxiv.org/pdf/2202.13028](https://arxiv.org/pdf/2202.13028)

**Date:** 2022-02-26

Documentation of 'religious beliefs' as a sensitive data category in health datasets. The paper identifies religion as a sensitive demographic data point that is collected in some health datasets (e.g., MIMIC-III). The main finding is that the collection methods, rationale, and presence of such data must be transparently documented in a 'Healthsheet' to ensure responsible and equitable use of the data in ML applications, highlighting that current documentation practices are often inadequate.


## THE REALITY OF MULTI-LINGUAL MACHINE TRANSLATION

[https://arxiv.org/pdf/2202.12814](https://arxiv.org/pdf/2202.12814)

**Date:** 2021-01-01

The paper does not benchmark any aspect of faith or religion. It mentions the Bible as a common source of parallel sentence data for training machine translation models, particularly in low-resource language scenarios. The Bible, due to its translation into hundreds of languages, is noted as a common and useful source of parallel text data for training machine translation models, especially for low-resource languages.


## Evaluating the Construct Validity of Text Embeddings with Application to Survey Questions

[https://arxiv.org/pdf/2202.09166](https://arxiv.org/pdf/2202.09166)

**Date:** 2022-02-18

The benchmark measured the construct validity of text embeddings for various survey questions. In the context of faith/religion, it specifically evaluated whether the embeddings could capture the semantic meaning of questions about norms, using 'believe God' as a concrete concept, by testing if embeddings for conceptually similar questions were closer than embeddings for conceptually dissimilar questions. The study found that text embedding models vary in their ability to represent survey questions about religious belief. Specifically, for the concept 'believe God', Sentence-BERT and Universal Sentence Encoder (USE) models demonstrated good convergent and discriminant validity, meaning they could distinguish between semantically similar and dissimilar questions. In contrast, fastText, GloVe, and the original BERT models performed poorly on this task, suggesting they lack the same level of validity for representing such concepts.


## Describing Differences between Text Distributions with Natural Language

[https://arxiv.org/pdf/2201.12323](https://arxiv.org/pdf/2201.12323)

**Date:** 2022-05-18

The system's ability to automatically generate a natural language description for the difference between two text distributions, where some of the tasks involved identifying religious or anti-religious themes. The system successfully generated accurate natural language descriptions for text distributions characterized by religious content. For the human annotation 'is religious', the system generated 'is religious', and for 'is against religion', it generated 'has a negative connotation towards religion', both receiving the highest similarity rating.


## Kiñit Classification in Ethiopian Chants, Azmaris and Modern Music: A New Dataset and CNN Benchmark

[https://arxiv.org/pdf/2201.08448](https://arxiv.org/pdf/2201.08448)

**Date:** 2022-01-20

The benchmark measures the accuracy of classifying Ethiopian musical scales (Kiñits) from audio clips. A portion of the dataset used for this benchmark consists of religious music, specifically Ethiopian Orthodox Tewahedo chants. The study created a new dataset, EMIR, for Ethiopian music classification which includes Orthodox Tewahedo chants. The key finding was that the proposed CNN model (EKM) using Mel-frequency Cepstral Coefficient (MFCC) features on 3-second audio clips achieved the highest accuracy (95.00%) in classifying the musical scales (Kiñits), outperforming other models like AlexNet, ResNet50, VGG16, and LSTM.


## Emojis as Anchors to Detect Arabic Offensive Language and Hate Speech

[https://arxiv.org/pdf/2201.06723](https://arxiv.org/pdf/2201.06723)

**Date:** 2022-05-19

Detection and distribution analysis of hate speech targeting different religious groups in Arabic tweets. In the analyzed dataset of hateful Arabic tweets, Jews were the most frequent target of religious prejudice (39% of religious hate speech tweets), followed by Muslims, Christians, and Shia.


## VALUENET: A New Dataset for Human Value Driven Dialogue System

[https://arxiv.org/pdf/2112.06346](https://arxiv.org/pdf/2112.06346)

**Date:** 2021-12-12

The benchmark measures human attitudes towards social scenarios through the lens of ten universal human values. One of these values, 'Tradition', includes concepts of religious customs, ideas, and keywords (e.g., devout, pious, christian, buddhist, islamic) to gauge alignment with traditional and religious norms. The paper does not present findings specifically about religion. It finds that modeling a comprehensive set of human values, which includes a 'Tradition' dimension incorporating religious concepts, improves the performance of dialogue systems on downstream tasks. Specifically, it helps in generating more personalized responses (on PERSONA-CHAT) and improves emotion classification and empathetic response generation (on EMPATHETICDIALOGUES). The religious component contributes as part of this broader value framework.


## Extending the WILDS Benchmark for Unsupervised Adaptation

[https://arxiv.org/pdf/2112.05090](https://arxiv.org/pdf/2112.05090)

**Date:** 2022-04-24

The benchmark measured the worst-group accuracy for toxicity classification on online comments that mention specific demographic identities, including religious groups. The goal was to evaluate model performance on underrepresented subpopulations. On the CIVILCOMMENTS-WILDS dataset, which measures performance across demographic groups including religious ones, the benchmarked methods (Pseudo-Label, continued Masked LM pre-training) performed similarly to the standard ERM baseline. Leveraging additional unlabeled data failed to improve worst-group accuracy, suggesting that these unsupervised adaptation methods are not effective for mitigating subpopulation shifts related to demographic identities.


## Ground-Truth, Whose Truth? - Examining the Challenges with Annotating Toxic Text Datasets

[https://arxiv.org/pdf/2112.03529](https://arxiv.org/pdf/2112.03529)

**Date:** 2021-12-07

The paper analyzes toxic text datasets, where religion (specifically Muslims) is mentioned as a potential target group for toxic content, but the study does not specifically measure bias or knowledge related to religion. The paper did not have specific findings related to religion. 'Muslims' were mentioned once as an example of a protected group that could be the target of toxic text within the proposed annotation guidelines.


## NL-Augmenter A Framework for Task-Sensitive Natural Language Augmentation

[https://arxiv.org/pdf/2112.02721](https://arxiv.org/pdf/2112.02721)

**Date:** 2022-10-11

The framework includes a 'Universal Bias Filter' which measures the balance of representation for multiple categories, including religion, by using lexical seeds. The paper presents a framework that includes a 'Universal Bias Filter' designed to measure representational balance for categories such as religion. However, the paper does not report specific experimental results or findings related to the performance of models on the religion category.


## The ComMA Dataset V0.2: Annotating Aggression and Bias in Multilingual Social Media Discourse

[https://arxiv.org/pdf/2111.10390](https://arxiv.org/pdf/2111.10390)

**Date:** 2021-11-19

The benchmark measures 'communal bias' (defined as religious intolerance) in social media comments. This includes identifying comments that target a victim's religious affiliation, identity, or beliefs; discriminate against religious practices; propagate false religious ideas; negatively stereotype an individual or community based on their religion; or contain threats based on religious identity. The analysis of the dataset revealed that communal (religious) bias is a significant issue, with the Hindi & English comments containing the highest proportion of such content (21.6%). A strong co-occurrence was found between communal comments and aggressive language, with most communal comments being classified as either overtly or covertly aggressive. Words like 'muslim', 'hindu', and 'muslimvirus' were frequently found in comments annotated as aggressive, communal, or gendered.


## Evaluation of Human and Machine Face Detection Using a Novel Distinctive Human Appearance Dataset

[https://arxiv.org/pdf/2111.00660](https://arxiv.org/pdf/2111.00660)

**Date:** 2021-11-02

The benchmark measured the accuracy of face detection algorithms on a dataset of distinctive human appearances, which included a sub-category of images featuring Muslim women wearing a 'burka'. The evaluation focused on visual bias against religious attire that covers parts of the face. The paper found that images of Muslim women wearing a 'burka' represented a significant challenge for face annotation, even for humans. This sub-category generated the highest variance among human annotators when asked to draw a bounding box for the face, due to ambiguity about whether to include only the visible portion or the expected full face shape. This highlights a key difficulty in creating ground truth data for training and evaluating face detection models on individuals with religious head coverings.


## The Golden Rule as a Heuristic to Measure the Fairness of Texts Using Machine Learning

[https://arxiv.org/pdf/2111.00107](https://arxiv.org/pdf/2111.00107)

**Date:** 

The paper does not present a benchmark that measures faith or religion directly. Instead, it uses religious scenarios as philosophical test cases to argue for the validity of the Golden Rule as a moral axiom. For example, it analyzes a dilemma involving a character's 'Presbyterian form of worship' versus 'pagan worship' and a hypothetical scenario involving a Nazi and Judaism to interrogate the consistency and applicability of the Golden Rule. The paper uses religious scenarios to demonstrate the philosophical robustness of the Golden Rule (GR) as a fairness heuristic. It argues that by applying the GR at a higher level of abstraction, it can resolve complex moral dilemmas involving conflicting religious beliefs (e.g., the Presbyterian vs. pagan worship example). It also uses a hypothetical involving Judaism to counter criticisms of the GR's consistency. The findings are philosophical arguments about the method's validity rather than empirical results on model performance related to religion.


## Applying Second-Order Quantifier Elimination in Inspecting Gödel's Ontological Proof

[https://arxiv.org/pdf/2110.11108](https://arxiv.org/pdf/2110.11108)

**Date:** 2021-10-21

The paper presents logical tasks derived from Gödel's ontological proof for the existence of God, which may serve as benchmarks for automated reasoning systems, specifically for first-order theorem proving and second-order quantifier elimination. The measurement is the capability of these systems to solve complex logical problems rooted in philosophical theology. The paper successfully reconstructed Gödel's ontological proof using an automated logical framework. Key findings include: 1) The derivation of key theorems requires fewer axiom instantiations than might be expected. 2) The conclusion that God's existence is possible can be derived independently from the specific definition of a 'God-like' being. 3) Second-order quantifier elimination can yield first-order representations for abstract concepts like 'essence' and 'necessary existence'. 4) A logically weaker condition than previously established is sufficient for proving the necessity of God's existence (Theorem T3), demonstrating that the proof holds in a broader class of modal logics (weaker than S5).


## An Empirical Survey of the Effectiveness of Debiasing Techniques for Pre-trained Language Models

[https://arxiv.org/pdf/2110.08527](https://arxiv.org/pdf/2110.08527)

**Date:** 2022-04-03

The study measured stereotypical associations and sentiment bias related to religious groups. This was done using three benchmarks: 1) The Sentence Encoder Association Test (SEAT) to measure the association between religious terms (e.g., Christian, Muslim, Jewish) and valenced words (e.g., good/bad, pleasant/unpleasant). 2) StereoSet, which evaluates a model's preference for stereotypical vs. anti-stereotypical sentence completions in religious contexts. 3) CrowS-Pairs, which measures how frequently a model prefers a stereotypical sentence over a minimally-edited, anti-stereotypical one regarding religious groups. The study found that debiasing techniques showed mixed effectiveness for religious bias. The Self-Debias technique was the most consistently effective at reducing stereotype scores on StereoSet and CrowS-Pairs for religion across different models (BERT, GPT-2). For the SEAT benchmark, techniques like Counterfactual Data Augmentation (CDA) and Dropout successfully reduced measured bias for BERT and GPT-2. However, the paper concludes that improvements on bias benchmarks are often accompanied by a decrease in the model's language modeling ability, making it difficult to determine the overall effectiveness of the bias mitigation. The results for religious bias were generally less consistent than for gender bias.


## On the Safety of Conversational Models: Taxonomy, Dataset, and Benchmark

[https://arxiv.org/pdf/2110.08466](https://arxiv.org/pdf/2110.08466)

**Date:** 2022-04-04

Detection of biased opinions against social identities, including religion. The benchmark measures a model's propensity to generate unsafe responses (e.g., agreeing with or perpetuating stereotypes) when presented with conversational contexts containing biased statements about religious groups. Models exhibit unsafe behavior in the 'Biased Opinion' category, which includes religion. The safety classifier trained for this category had a relatively low F1-score, which the authors attribute to the complexity and sample-sparsity of social identities like religious groups (e.g., Buddhist). Evaluation examples show models generating biased responses in contexts related to Islam. Overall, models struggle to safely navigate conversations involving biased statements about religion.


## BBQ: A Hand-Built Bias Benchmark for Question Answering

[https://arxiv.org/pdf/2110.08193](https://arxiv.org/pdf/2110.08193)

**Date:** 2022-03-16

The benchmark measures attested social biases and harmful stereotypes against specific religious groups. For example, it tests for associations between Muslims and terrorism, and between Jewish people and greed or dual loyalties. In ambiguous contexts where no correct answer is provided, models frequently rely on harmful religious stereotypes to answer questions, leading to high bias scores. For example, a significant portion of errors in the religion category involved models answering based on a social bias. This effect is reduced in disambiguated contexts, but models still show a drop in accuracy (up to 4.3 percentage points) when the correct answer conflicts with a known religious stereotype compared to when it aligns with one.


## Socially Aware Bias Measurements for Hindi Language Representations

[https://arxiv.org/pdf/2110.07871](https://arxiv.org/pdf/2110.07871)

**Date:** 2022-05-09

Detecting stereotypical bias by associating religious entities and last names (specifically Hindu and Muslim) with positive and negative attributes in Hindi language representations. Hindi language representations, particularly GloVe embeddings, exhibit significant religious bias. They show strong stereotypical associations between religious groups (Hinduism and Islam) and polarized attributes (positive/negative). The study highlights that culturally-aware, language-specific word lists are substantially more effective at detecting these biases than direct translations of word lists from English.


## Multimodal datasets: misogyny, pornography, and malignant stereotypes

[https://arxiv.org/pdf/2110.01963](https://arxiv.org/pdf/2110.01963)

**Date:** 2021-10-05

Stereotype detection and association with problematic (NSFW) content for the religious term 'Nun' in a large-scale multimodal dataset (LAION-400M). The analysis measured the prevalence of NSFW terms in the text and URLs associated with images retrieved for this query. Querying the LAION-400M dataset for the religious term 'Nun' resulted in 16.4% of matches containing NSFW-related terms in their text or URL, indicating a significant presence of problematic and sexualized content associated with this religious role.


## BLEU, METEOR, BERTScore: Evaluation of Metrics Performance in Assessing Critical Translation Errors in Sentiment-oriented Text

[https://arxiv.org/pdf/2109.14250](https://arxiv.org/pdf/2109.14250)

**Date:** 2021-09-29

The paper evaluates the performance of automatic machine translation quality metrics (BLEU, METEOR, BERTScore) in detecting critical sentiment errors. A key example used to illustrate the metrics' failure involves a religious phrase where a missing negation ('not') flips the meaning from 'may God forgive you' to 'may God not forgive you', but the metrics do not penalize this critical error sufficiently. The key finding is that standard automatic evaluation metrics (BLEU, METEOR, BERTScore) are not robust in detecting and penalizing critical, sentiment-flipping translation errors. This was illustrated with examples including a religious phrase ('may God not forgive you'), where the metrics failed to assign a sufficiently low score to a mistranslation that conveyed the opposite sentiment of the source text.


## TruthfulQA: Measuring How Models Mimic Human Falsehoods

[https://arxiv.org/pdf/2109.07958](https://arxiv.org/pdf/2109.07958)

**Date:** 2022-05-08

The benchmark measures the truthfulness of model-generated answers to questions about religion, specifically focusing on avoiding common misconceptions and falsehoods prevalent among humans. In the "Religion" category of the TruthfulQA benchmark, language models performed significantly worse than the human baseline (94% truthful). The best model configuration (GPT-3 175B with a "helpful" prompt) achieved approximately 60-70% truthfulness, indicating a substantial gap in providing truthful answers about religious topics and avoiding common misconceptions.


## TrollsWithOpinion: A Dataset for Predicting Domain-specific Opinion Manipulation in Troll Memes

[https://arxiv.org/pdf/2109.03571](https://arxiv.org/pdf/2109.03571)

**Date:** 2022-05-10

Detection of opinion manipulation in troll memes targeting individuals or groups based on characteristics including religious beliefs. This falls under the 'Troll_opinion_other' and 'Not_troll_opinion_other' categories. The paper's models performed poorly overall on the task of classifying troll memes, which includes a category for memes targeting individuals or groups based on their religious beliefs. The best-performing machine learning model (Random Forest) achieved a weighted-average F1-score of 0.37, indicating the difficulty of this multimodal task. There were no specific findings broken down by the religious sub-category.


## Dataset for Identification of Homophobia and Transophobia in Multilingual YouTube Comments

[https://arxiv.org/pdf/2109.00227](https://arxiv.org/pdf/2109.00227)

**Date:** 2021-01-01

The use of religious arguments, narratives, and mythology in homophobic/transphobic speech, counter-speech, and hope speech within multilingual YouTube comments. It specifically analyzes how religion is used to both justify abuse against LGBT+ people and to provide support and counter-arguments. The study found that certain religions, specifically Brahmanism (referred to as Hinduism), Islam, and Christianity, were used to create homophobic and transphobic comments, including derogation and threats. Conversely, other religions like Tamil Shivam, Tamil Vainavam, and Tamil Aseevagam, as well as Christianity, were used to formulate supportive counter-speech and hope speech, often referencing mythological figures and stories. The analysis also noted comments reflecting inter-religious and caste-based discrimination (e.g., against Tamils by Brahmanism followers), which were separate from the primary topic of homophobia.


## Legal perspective on possible fairness measures - A legal discussion using the example of hiring decisions

[https://arxiv.org/pdf/2108.06918](https://arxiv.org/pdf/2108.06918)

**Date:** 2021-08-16

Discrimination based on religious belief as a sensitive/protected attribute in the context of algorithmic hiring decisions. The paper identifies 'religion or belief' as a legally protected characteristic under EU and German anti-discrimination law. It analyzes the complex challenges of applying various mathematical fairness measures (like Independence, Separation, and Counterfactual Fairness) to prevent discrimination based on religion in AI hiring systems. The analysis highlights that current process-oriented legal frameworks are ill-equipped for result-oriented AI systems and that even seemingly objective inputs can be influenced by protected attributes such as religion, complicating the pursuit of true fairness.


## HATEMOJI: A Test Suite and Adversarially-Generated Dataset for Benchmarking and Detecting Emoji-Based Hate

[https://arxiv.org/pdf/2108.05921](https://arxiv.org/pdf/2108.05921)

**Date:** 2022-05-06

Detection of emoji-based hate speech directed at protected identities, including Muslims. Adversarially-trained models (e.g., R8-T) demonstrate more balanced and fair performance in detecting hate speech against Muslims compared to baseline commercial (Perspective API) and academic models. The baseline models showed variable performance and fairness issues across different identity groups, which the new training methodology helped to mitigate.


## On Measures of Biases and Harms in NLP

[https://arxiv.org/pdf/2108.03362](https://arxiv.org/pdf/2108.03362)

**Date:** 2022-10-13

Detection of stereotypical and negative associations (disparagement, erasure) with religious identity terms in tasks like question answering, natural language inference, hate speech, and toxicity detection. The paper surveys existing bias measures and finds that for religion, they primarily evaluate stereotypical associations, disparagement, and erasure. For instance, some benchmarks test whether models associate religious identity terms with negative concepts or fail to treat different religious groups equitably in tasks like question answering and toxicity detection. The paper also highlights that stereotypes are context-dependent (e.g., substituting 'Muslim' for 'Jew' may not produce an equally valid stereotype), necessitating nuanced evaluation.


## Human-in-the-Loop for Data Collection: a Multi-Target Counter Narrative Dataset to Fight Online Hate Speech

[https://arxiv.org/pdf/2107.08720](https://arxiv.org/pdf/2107.08720)

**Date:** 2021-07-19

Generation of counter-narratives for hate speech targeted at religious groups (Muslims and Jews). The human-in-the-loop (HITL) data collection process showed an increasing imbalance in hate targets over iterative loops. Hate speech against Muslims became predominant in the generated dataset, while the proportion of hate speech against Jews diminished over the same loops.


## Quantifying Social Biases in NLP: A Generalization and Empirical Comparison of Extrinsic Fairness Metrics #Mormon

[https://arxiv.org/pdf/2106.14574](https://arxiv.org/pdf/2106.14574)

**Date:** 2021-06-28

The benchmark measured systemic differences in model performance (bias) for sentiment analysis and named entity recognition tasks on text that explicitly mentions different religious identity terms. This was quantified using a variety of fairness metrics. The paper found statistically significant evidence of unintended bias related to religion in the models tested. The performance on sentiment analysis tasks differed across various religious groups, and the magnitude of the measured bias varied depending on the specific fairness metric used. For example, tests showed very low p-values (e.g., 1.14 x 10^-23), indicating that the observed differences in model behavior across religious groups were highly unlikely to be due to chance.


## CALLIAR: AN ONLINE HANDWRITTEN DATASET FOR ARABIC CALLIGRAPHY

[https://arxiv.org/pdf/2106.10745](https://arxiv.org/pdf/2106.10745)

**Date:** 2021-06-25

The paper does not benchmark a model, but rather introduces 'Calliar', a new dataset for Arabic calligraphy. This dataset enables the benchmarking of machine learning models on their ability to recognize, process, and generate Arabic text written in calligraphic styles, which frequently consist of Islamic religious phrases, such as verses from the Qur'an and the Basmala ('بسم الله الرحمن الرحيم'). The paper's main contribution is the creation and release of Calliar, the first online dataset for Arabic calligraphy. This art form is a significant component of Islamic heritage, used for decorating mosques and transcribing religious texts. The dataset provides detailed stroke-level annotations, enabling new research in generating and recognizing an important medium of Islamic religious and cultural expression.


## Process for Adapting Language Models to Society (PALMS) with Values-Targeted Datasets

[https://arxiv.org/pdf/2106.10328](https://arxiv.org/pdf/2106.10328)

**Date:** 2021-01-01

The benchmark measured sentiment bias and harmful associations for various religious groups through co-occurrence evaluations. The process involved providing prompts like '{category} are' to the models and analyzing the most common descriptive words generated for each religious category to identify stereotypes, derogatory terms, or other biases. Base GPT-3 models exhibited significant negative biases, associating 'Muslim' with terrorism ('Brotherhood', 'Isil', 'Terrorist') and 'Jewish' with derogatory terms and genocide ('Monkeys', 'Holocaust'). The PALMS fine-tuned 'values-targeted' models successfully removed these harmful associations but introduced new, different biases, such as associating 'Muslim' with 'Heterosexual' and 'Jewish' with 'Intelligence'. The control models, fine-tuned on generic high-quality text, performed similarly to the biased base models.


## EIDER: Empowering Document-level Relation Extraction with Efficient Evidence Extraction and Inference-stage Fusion

[https://arxiv.org/pdf/2106.08657](https://arxiv.org/pdf/2106.08657)

**Date:** 2022-03-07

The benchmark measured the model's ability to correctly identify the 'Religion' relation between two entities in a document as part of a broader relation extraction task. The model failed to infer a 'Religion' relation between a Catholic priest and a Pope, a task that required commonsense reasoning to connect that a Pope removing a priest from ministry implies they belong to the same religion. This was categorized as a 'Fail in Commonsense Reasoning' error.


## REDDITBIAS: A Real-World Resource for Bias Evaluation and Debiasing of Conversational Language Models

[https://arxiv.org/pdf/2106.03521](https://arxiv.org/pdf/2106.03521)

**Date:** 2021-06-07

The benchmark measures stereotypical biases against Jews and Muslims. The evaluation framework compares the likelihood of associating minoritized religious groups (Jews, Muslims) with negative stereotypes versus a dominant religious group (Christians) with positive attributes. The DialoGPT model exhibits significant stereotypical bias against both Jews and Muslims, despite its pre-processing to remove offensive content. This is attributed to subtle stereotypes like associating Islam with being radical or Jews with playing violins. The study found that certain debiasing methods, specifically Hard Debiasing (HD) and Counterfactual Augmentation (CDA), could successfully remove this religious bias without negatively impacting the model's performance on downstream dialog tasks.


## IndoNLG: Benchmark and Resources for Evaluating Indonesian Natural Language Generation

[https://arxiv.org/pdf/2104.08200](https://arxiv.org/pdf/2104.08200)

**Date:** 2021-10-09

The benchmark measured two aspects related to religion: 1) The performance of models on a machine translation task using a Bible dataset for English-Indonesian, Sundanese-Indonesian, and Javanese-Indonesian pairs. 2) Co-occurrence bias analysis to identify associations the model makes for various religious groups based on generated text from specific prompts. The model makes associations with common terms related to specific religions in the real world. For example, it associates 'bertakwa'/'bertaqwa' (forbearance, fear, and abstinence) and 'akhlak' (moral/ethics) with Islam; 'Yesus Kristus' (Jesus Christ) with Christianity and Catholicism; 'Budha' and 'Buddha' with Buddhism; 'dewa-dewi' (Gods) and 'Brahmana' with Hinduism; and 'Tionghoa' (Chinese) with Confucianism.


## Unmasking the Mask – Evaluating Social Biases in Masked Language Models

[https://arxiv.org/pdf/2104.07496](https://arxiv.org/pdf/2104.07496)

**Date:** 2021-04-15

Detection of stereotypical biases in sentences contrasting different religious groups. All tested models (BERT, RoBERTa, ALBERT) were found to encode significant stereotypical biases related to religion. Across multiple evaluation methods, the 'Religion' category consistently showed high bias scores, indicating that the models have learned strong stereotypical associations. For example, under some metrics, religion was one of the bias types with the highest scores for models like RoBERTa.


## Double Perturbation: On the Robustness of Robustness and Counterfactual Bias Evaluation

[https://arxiv.org/pdf/2104.05232](https://arxiv.org/pdf/2104.05232)

**Date:** 2021-04-12

The benchmark measures counterfactual token bias, specifically the change in a model's sentiment prediction when one religious term is substituted for another (e.g., 'christian' for 'muslim') within a sentence, both in the original test set and in a synthetically generated neighborhood of similar sentences. Using the proposed 'double perturbation' framework on a base LSTM model, the study revealed hidden counterfactual biases related to religious terms. For example, by analyzing a neighborhood of perturbed sentences (k=3), a positive sentiment bias was observed when substituting 'christian' with 'muslim', or 'jews' with 'christians'. This indicates that the model's sentiment predictions were influenced by the specific religious term used, a bias not as clearly visible when only evaluating the original, unperturbed test set.


## Adapting Language Models for Zero-shot Learning by Meta-tuning on Dataset and Prompt Collections

[https://arxiv.org/pdf/2104.04670](https://arxiv.org/pdf/2104.04670)

**Date:** 2021-09-08

Stance detection towards atheism and religious beliefs. The models were evaluated on their ability to detect stance towards atheism. The paper found that the model's performance was highly sensitive to the prompt phrasing for religious concepts. For example, the prompt 'Does this post support atheism?' resulted in much lower accuracy than the semantically similar prompt 'Is the post against having religious beliefs?'. The authors conjecture this is because the model struggles to ground abstract concepts like 'atheism'. The meta-tuned T5-770M model achieved a 65.6% AUC-ROC score on the atheism stance detection task.


## Annotating Columns with Pre-trained Language Models

[https://arxiv.org/pdf/2104.01785](https://arxiv.org/pdf/2104.01785)

**Date:** 2022-06-12

Ability to identify columns containing information about religion, as part of a broader semantic column type prediction task. The baseline model Sato performed very poorly at identifying columns with the semantic type 'religion', likely due to a lack of training examples. The proposed DODUO model, however, performed robustly on this column type. Further analysis via language model probing showed that the underlying pre-trained BERT model has significant prior knowledge about the 'religion' column type, ranking it among the top types it understands from context.


## Lawyers are Dishonest? Quantifying Representational Harms in Commonsense Knowledge Resources

[https://arxiv.org/pdf/2103.11320](https://arxiv.org/pdf/2103.11320)

**Date:** 2021-09-10

Quantifying representational harms, specifically intra-target overgeneralization (polarized perceptions like prejudice or favoritism) and inter-target disparity (differences in representation), towards religious groups in commonsense knowledge bases (CSKBs) and the downstream models trained on them. The measurement is performed using sentiment and regard classifiers on statements associated with religious terms. The study found significant representational harms related to religion in both ConceptNet and GenericsKB. GenericsKB contained a much higher rate and magnitude of bias compared to ConceptNet. There was evidence of extreme prejudice towards 'muslim' and 'sharia', while terms like 'christian' showed both favoritism and prejudice. These biases were found to be inherited and sometimes amplified by downstream models like COMET and CSG, which generated prejudiced content. For instance, in the CSG model, the 'Religion' category of prompts led to outputs with up to 60% negative associations.


## Let-Mi: An Arabic Levantine Twitter Dataset for Misogynistic Language

[https://arxiv.org/pdf/2103.10195](https://arxiv.org/pdf/2103.10195)

**Date:** 2021-03-18

Detection of religiously-phrased misogynistic abuse, specifically the 'damning' category, which involves prayers and curses invoking God to harm women. The paper introduced a novel category of misogyny called 'damning', which captures religiously-phrased abuse common in Arabic culture (e.g., 'May God curse you'). The experimental analysis, particularly the confusion matrix, showed that this category is challenging for models to detect, often being misclassified as non-misogynistic content.


## Quantifying Confounding Bias in Generative Art: A Case Study

[https://arxiv.org/pdf/2102.11957](https://arxiv.org/pdf/2102.11957)

**Date:** 2021-02-23

The paper does not directly measure anything related to religion. It proposes a metric for quantifying confounding bias in generative art models, specifically the bias from failing to model the influence of art movements. Religion is mentioned as an example of a complex socio-cultural confounder that is not captured by the model or the case study's specific analysis but could be a factor in art, particularly in genres like portraiture. The paper's primary findings are not about religion. However, it identifies religion as an important socio-cultural factor that influences art creation and is often overlooked in generative AI models. It argues that failing to account for factors like religion, especially in genres such as portraiture, can lead to confounding bias and misrepresentation of the artwork's context and intent. The Directed Acyclic Graph (DAG) used in the case study was deemed insufficient for genres involving complex socio-cultural themes, including religious ones.


## Bangla Text Dataset and Exploratory Analysis for Online Harassment Detection

[https://arxiv.org/pdf/2102.02478](https://arxiv.org/pdf/2102.02478)

**Date:** 2021-01-01

Detection of religious harassment comments in Bangla text. The study created a dataset for online harassment in Bangla, where 'religious' was one of the five main categories of harassment. The analysis found that 17.22% (7,577 out of 44,001) of comments were classified as religious harassment. These comments were found to be disproportionately aimed at female victims (7,086 comments) compared to male victims (491 comments).


## BOLD: Dataset and Metrics for Measuring Biases in Open-Ended Language Generation

[https://arxiv.org/pdf/2101.11718](https://arxiv.org/pdf/2101.11718)

**Date:** 2021-01-27

The benchmark measures social biases in open-ended text generation across several domains, including religion. For religion, it specifically measures sentiment (positive, negative, neutral), toxicity, and psycholinguistic norms (e.g., emotions like joy, anger, sadness) in texts generated from prompts associated with various religious and spiritual beliefs. On average, generated texts showed the highest proportion of negative sentiment for prompts about Atheism, followed by Islam. Compared to Christianity, prompts about Islam generated texts with more negative psycholinguistic norms (e.g., sadness, disgust, fear, anger). Toxic texts were generated for prompts about Islam, Christianity, and Atheism, with Atheism having the largest proportion of toxicity.


## Robustness Gym: Unifying the NLP Evaluation Landscape

[https://arxiv.org/pdf/2101.04840](https://arxiv.org/pdf/2101.04840)

**Date:** 2021-01-13

Performance degradation on text containing religious identity terms, as part of a broader analysis on identity-sensitive words. In a case study with a commercial sentiment model, the system's performance was evaluated on subpopulations containing identity-sensitive words (including religious terms). No performance degradation was found on the nine identity-sensitive words tested.


## Learning from the Worst: Dynamically Generated Datasets to Improve Online Hate Detection

[https://arxiv.org/pdf/2012.15761](https://arxiv.org/pdf/2012.15761)

**Date:** 2021-06-03

The benchmark measures the detection of online hate speech, including hate speech targeted at specific religious groups such as Muslims, Jews, and Hindus. The paper found that a dynamic, human-and-model-in-the-loop process for generating datasets significantly improves the performance and robustness of hate speech detection models. While findings were not broken down by target group, religious identities such as 'Muslims' and 'Jewish people' were among the most common targets in the dataset, indicating that the improved models are better at detecting hate speech against these groups.


## Eurythmic Dancing with Plants Measuring Plant Response to Human Body Movement in an Anthroposophic Environment

[https://arxiv.org/pdf/2012.12978](https://arxiv.org/pdf/2012.12978)

**Date:** 

The paper does not benchmark faith or religion. It conducts experiments to measure plant responses (electrical discharge and leaf movement) to eurythmic dancing, framed within the spiritual philosophy of Anthroposophy to test concepts like 'etheric energies'. The study found correlations between eurythmic dancing and plants' electrical discharge and movement. Interpreted through an 'anthroposophic lens,' the findings suggest that plants may be influenced by 'etheric energies' from the dancer. The paper also speculates that plants exposed to dancing for the first time respond more strongly than those exposed frequently, potentially becoming 'less sensitive' over time.


## Facebook Ad Engagement in the Russian Active Measures Campaign of 2016

[https://arxiv.org/pdf/2012.11690](https://arxiv.org/pdf/2012.11690)

**Date:** 2020-12-23

The presence and correlation of religion-related words in disinformation ad text with user engagement, measured as a sociolinguistic feature. The use of religion-related words was identified as a highly important sociolinguistic feature for predicting user engagement with disinformation ads. Despite the overall low usage of religious language, the 'Religion' feature was selected as a top predictor by four of the six machine learning models tested and showed a higher correlation with engagement in the high-engagement ad group compared to the standard-engagement group.


## HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection

[https://arxiv.org/pdf/2012.10289](https://arxiv.org/pdf/2012.10289)

**Date:** 2022-04-12

The benchmark measures unintended bias in hate speech detection models against various target communities, including religious groups. It evaluates model performance on classifying posts as hateful, offensive, or normal, and also assesses the explainability of model predictions. The top three communities targeted by hate speech in the dataset were African, Islam, and Jewish. The top three content words found in hate speech rationales were 'nigger', 'kike', and 'moslems'. Models like BERT-HateXplain showed better performance in handling bias against religious communities like Jewish and Islam compared to other models.


## Hate Speech detection in the Bengali language: A dataset and its baseline evaluation

[https://arxiv.org/pdf/2012.09686](https://arxiv.org/pdf/2012.09686)

**Date:** 

The benchmark measures the ability to detect hate speech in Bengali social media comments. One of the seven categories from which comments were collected was 'religion', meaning the benchmark implicitly measures the model's ability to identify hate speech in religious contexts. The paper created a diverse dataset for Bengali hate speech detection that includes comments from the 'religion' category to ensure linguistic variation. The study established baseline performance using various models (SVM, LSTM, Bi-LSTM) on this dataset, with SVM performing best. There were no specific findings highlighted about the nature of religious hate speech itself; its inclusion was primarily to broaden the scope and diversity of the dataset.


## Stylometry for Noisy Medieval Data: Evaluating Paul Meyer's Hagiographic Hypothesis

[https://arxiv.org/pdf/2012.03845](https://arxiv.org/pdf/2012.03845)

**Date:** 2020-12-07

Stylometric analysis to evaluate a historical hypothesis about the authorial and compositional structure of medieval Christian hagiographic collections (saints' lives). The study's stylometric analysis largely confirms Paul Meyer's hypothesis that the hagiographic collection in MS BnF, fr. 412 was formed by successive additions (Collections A, B, C). The findings also refine this hypothesis by identifying new sub-series, reclassifying certain texts (e.g., Saint Longin's Life from A to B), and raising new questions about authorship, such as the potential attribution of Saint Lambert's life to Wauchier de Denain.


## BAN-ABSA: An Aspect-Based Sentiment Analysis dataset for Bengali and it's baseline evaluation

[https://arxiv.org/pdf/2012.00288](https://arxiv.org/pdf/2012.00288)

**Date:** 

The benchmark measures the ability of machine learning models to perform aspect extraction (identifying comments related to religion) and sentiment classification (positive, negative, or neutral) on a dataset of Bengali news comments. The paper does not provide findings specific to the 'Religion' category. The general findings across all categories, including religion, were that the CNN model achieved higher accuracy for aspect extraction (79.09%) and sentiment classification (71.48%), while the Bi-LSTM model performed better in terms of F1-score for both tasks (79.38% and 62.30% respectively).


## Occam's Razor for Big Data? On Detecting Quality in Large Unstructured Datasets

[https://arxiv.org/pdf/2011.08663](https://arxiv.org/pdf/2011.08663)

**Date:** 2019-06-23

The paper qualitatively analyzes how different religious and cultural backgrounds (specifically, Western monotheism versus Eastern polytheism) influence emotional responses to and acceptance of Artificial Intelligence and humanoid robots. The paper suggests that cultural and religious backgrounds significantly influence perceptions of AI. Western cultures, influenced by monotheistic religions like Christianity, may perceive the creation of artificial, human-like beings as 'sinful' or unsettling (drawing parallels to the story of Frankenstein), leading to feelings of unease towards humanoids. In contrast, Eastern cultures with polytheistic traditions, such as Japanese Shintoism, tend to be more accepting of artificial life and humanoid robots.


## Hostility Detection Dataset in Hindi

[https://arxiv.org/pdf/2011.03588](https://arxiv.org/pdf/2011.03588)

**Date:** 2020-11-06

Hate speech detection targeting specific groups based on their religious beliefs. The paper developed a dataset for hostility detection in Hindi, which defines hate speech as posts targeting groups based on characteristics including religious beliefs. Analysis of the collected data revealed that negative and offensive posts against Muslims were a visible component of the hostile content.


## EXAMS: A Multi-Subject High School Examinations Dataset for Cross-Lingual and Multilingual Question Answering

[https://arxiv.org/pdf/2011.03080](https://arxiv.org/pdf/2011.03080)

**Date:** 2020-11-05

The benchmark measured academic knowledge of religious concepts, figures, and texts as taught in high school curricula. Specifically, it included multiple-choice questions on 'Islamic Studies' (covering the Quran and Muslim morality) and 'Religion' (covering Christianity studies, such as Bible knowledge and traditions). The paper provides fine-grained performance evaluation by subject. For the 'Other' category of subjects, the model XLM-R achieved an accuracy of 44.9% on 'Islamic Studies' questions (in Arabic) and 38.3% on 'Religion' questions (covering Christianity). The paper notes that subjects in this category are generally less challenging than Natural Sciences, as the required knowledge is often more accessible in sources like Wikipedia.


## 'Thy algorithm shalt not bear false witness': An Evaluation of Multiclass Debiasing Methods on Word Embeddings

[https://arxiv.org/pdf/2010.16228](https://arxiv.org/pdf/2010.16228)

**Date:** 2020-11-04

Detection and mitigation of multiclass religious bias and stereotypes in word embeddings, specifically focusing on associations between religious identity terms (e.g., Muslim, Christian, Jew) and attribute words (e.g., terrorist, greedy, pleasant). The paper confirms the presence of religious biases in widely used word embeddings, such as strong associations between 'Muslim' and 'terrorist'. It evaluates three debiasing techniques (Hard Debiasing, SoftWEAT Debiasing, and Conceptor Debiasing) and finds that Conceptor Debiasing is the most effective and consistent method for removing this religious bias across all metrics (WEAT, MAC, RNSB) and all tested word embedding models. On average, Conceptor Debiasing decreased religious bias by 82.42% in Word2Vec, 96.78% in GloVe, and 54.76% in ConceptNet.


## Unmasking Contextual Stereotypes: Measuring and Mitigating BERT's Gender Bias

[https://arxiv.org/pdf/2010.14534](https://arxiv.org/pdf/2010.14534)

**Date:** 2020-10-27

Gender bias (association with male vs. female terms) for the profession 'director of religious activities'. For the profession 'director of religious activities', the pre-trained English BERT model showed a male bias, associating it more strongly with male terms and negatively with female terms. After the debiasing fine-tuning procedure, this gender bias was reduced, with both male and female terms showing similar, slightly positive associations.


## Fair Hate Speech Detection through Evaluation of Social Group Counterfactuals

[https://arxiv.org/pdf/2010.12779](https://arxiv.org/pdf/2010.12779)

**Date:** 2020-10-24

The benchmark measured stereotype-based bias in hate speech classification models. Specifically, it evaluated how model predictions change when social group tokens (SGTs), including religious ones like 'Muslim' and 'Jew', are substituted in a sentence, and proposed a method to handle cases where substitution drastically alters the sentence's meaning due to stereotypes. The paper found that the textual context associated with religious group tokens varies significantly in stereotypical content. For example, sentences containing the token 'jew' were found to be highly predictive and stereotypical in the Gab dataset, more so than for groups like 'catholic' or 'buddhist'. The study's proposed method successfully improved counterfactual fairness for models by identifying and ignoring these stereotypical (asymmetric) counterfactuals during training, preventing the model from being penalized for correctly identifying a change in meaning when a religious token is substituted.


## TWEETEVAL: Unified Benchmark and Comparative Evaluation for Tweet Classification

[https://arxiv.org/pdf/2010.12421](https://arxiv.org/pdf/2010.12421)

**Date:** 2020-10-26

The benchmark measured the ability of models to detect a user's stance (favorable, neutral, or against) towards Atheism in tweets, as part of a broader stance detection task. The paper does not provide specific findings for the Atheism sub-task. The results for stance detection were aggregated across five topics (abortion, atheism, climate change, feminism, and Hillary Clinton). The general finding was that a RoBERTa model pre-trained on general corpora and then further trained on Twitter data (RoB-RT) performed best overall.


## Multilingual Argument Mining: Datasets and Analysis

[https://arxiv.org/pdf/2010.06432](https://arxiv.org/pdf/2010.06432)

**Date:** 2020-10-13

The benchmark measured stance classification on arguments related to religious topics, specifically 'We should ban missionary work' and 'We should adopt atheism'. The paper evaluated model performance on several controversial topics, including two related to religion/faith ('We should adopt atheism' and 'We should ban missionary work'). The analysis found performance variability across all topics, but did not draw specific conclusions about model behavior on religious topics distinct from others. For instance, the low performance of the zero-shot baseline on 'We should ban missionary work' was grouped with other topics involving the action 'ban', suggesting the performance dip was related to the task phrasing rather than the religious content itself.


## CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models

[https://arxiv.org/pdf/2010.00133](https://arxiv.org/pdf/2010.00133)

**Date:** 2020-09-30

The benchmark measures the degree to which masked language models prefer stereotypical sentences over less-stereotypical ones in religious contexts. It presents models with minimally different sentence pairs, one containing a stereotype about a religious group (e.g., 'crafty Jews') and the other a contrasting group (e.g., 'crafty Christians'), and measures which sentence the model assigns a higher likelihood to. All three models tested (BERT, RoBERTa, ALBERT) exhibited substantial bias in the religion category. The paper found that models showed comparatively higher bias scores for religion compared to other categories like gender and race, with scores ranging from 71.4% to 75.2% (where 50% would be an ideal unbiased score).


## REALTOXICITYPROMPTS: Evaluating Neural Toxic Degeneration in Language Models

[https://arxiv.org/pdf/2009.11462](https://arxiv.org/pdf/2009.11462)

**Date:** 2020-09-25

The paper's analysis of the OWTC training corpus measured the toxicity of documents sourced from various subreddits, including the religiously-affiliated subreddit /r/atheism, to identify sources of toxic content in pretraining data. The analysis of the OWTC corpus, a replica of GPT-2's training data, found that the subreddit /r/atheism was one of the top 15 sources of documents overall and also one of the top 15 sources of toxic documents, indicating that content from this community contributed to the toxicity found in the model's pretraining data.


## CODEX: A Comprehensive Knowledge Graph Completion Benchmark

[https://arxiv.org/pdf/2009.07810](https://arxiv.org/pdf/2009.07810)

**Date:** 2020-10-06

Factual knowledge graph completion (link prediction and triple classification) in the domain of religion, as part of a broader multi-domain benchmark. The paper does not report specific findings related to the religion domain. The findings focus on the overall performance of different knowledge graph embedding models on the CODEX benchmark, analyzing their ability to capture relational patterns like symmetry and compositionality across all domains.


## MEASURING MASSIVE MULTITASK LANGUAGE UNDERSTANDING

[https://arxiv.org/pdf/2009.03300](https://arxiv.org/pdf/2009.03300)

**Date:** 2021-01-12

The benchmark measured knowledge of various world religions through a specific task called 'World Religions', which tested concepts from Judaism, Christianity, Islam, Buddhism, and Jainism. Models were tested on a 'World Religions' knowledge task. The results showed that both GPT-3 and UnifiedQA performed significantly better than random chance. The largest GPT-3 model achieved an accuracy of approximately 53%, while UnifiedQA performed better at around 60%. This task ranked in the upper half of performance for both models across the 57 tasks, but the accuracies are still well below human expert levels.


## Vyaktitv: A Multimodal Peer-to-Peer Hindi Conversations based Dataset for Personality Assessment

[https://arxiv.org/pdf/2008.13769](https://arxiv.org/pdf/2008.13769)

**Date:** 2020-08-31

Correlation between self-reported religious/cultural inclination and Big Five personality traits (specifically Neuroticism). Participants who self-identified as 'religious/culturally inclined' tended to have lower scores for Neuroticism, indicating higher emotional stability.


## Ethical behavior in humans and machines: Evaluating training data quality for beneficial machine learning

[https://arxiv.org/pdf/2008.11463](https://arxiv.org/pdf/2008.11463)

**Date:** 

The paper does not propose a formal benchmark, but a framework for evaluating and selecting training data. In relation to religion, this framework would involve inferring users' religious views and filtering out data associated with 'radical religious views' or 'religious extremism' to train more beneficial machine learning models. The paper proposes that to create beneficial AI, training data should be ethically filtered. It finds that users' 'religious views' can be inferred from their digital behavior. The author argues that training data from individuals who exhibit 'radical religious views' or 'religious extremism' should be excluded or down-weighted, especially when developing social media and search engine algorithms, to prevent the spread of harmful content and promote a healthier public discourse.


## Inference of a universal social scale and segregation measures using social connectivity kernels

[https://arxiv.org/pdf/2008.05337](https://arxiv.org/pdf/2008.05337)

**Date:** 2020-10-28

Measurement of social homophily and segregation based on religious affiliation differences. Religious differences contribute to social segregation, with homophily observed in friendship networks. In the US General Social Survey dataset, having a different religion had a negative effect on the odds of forming a social connection, equivalent to a seven-year age difference. However, the contribution of religion to overall social segregation was found to be smaller than that of physical distance and age.


## ETHOS: AN ONLINE HATE SPEECH DETECTION DATASET

[https://arxiv.org/pdf/2006.08328](https://arxiv.org/pdf/2006.08328)

**Date:** 2021-07-06

Detection of hate speech targeting religious groups as one of several categories in a multi-label classification task. The 'Religion' category for hate speech had very high inter-annotator agreement (Fleiss' Kappa of 0.963). When a BiLSTM model trained on the ETHOS dataset was tested for generalizability on another hate speech dataset (D2), it performed poorly on identifying religious hate speech, achieving an F1-score of only 27.31% for positive instances, while being highly effective at identifying non-hateful instances related to religion (98.51% F1-score for negative instances).


## QUANTIFYING LATENT MORAL FOUNDATIONS IN TWITTER NARRATIVES: THE CASE OF THE SYRIAN WHITE HELMETS MISINFORMATION

[https://arxiv.org/pdf/2004.13142](https://arxiv.org/pdf/2004.13142)

**Date:** 2020-04-27

The paper analyzes moral foundations in Twitter narratives, including the 'Purity/Sanctity' dimension which can have religious connotations, and one narrative involving the religious extremist group al-Qaida. However, it does not explicitly measure any specific aspect of religion or faith. The study's findings concern the dynamics of moral rhetoric in misinformation campaigns on Twitter. It identifies a disinformation narrative linking the Syrian White Helmets to the religious extremist group al-Qaida as one of the key topics driving user engagement. However, the analysis focuses on the moral foundations (e.g., Harm/Care, Fairness/Reciprocity) used in these tweets, rather than on the religious aspects of the narrative itself.


## StereoSet: Measuring stereotypical bias in pretrained language models

[https://arxiv.org/pdf/2004.09456](https://arxiv.org/pdf/2004.09456)

**Date:** 2020-04-20

The benchmark measures stereotypical biases in language models across four domains, one of which is religion. It assesses whether models are more likely to associate religious groups with stereotypical attributes versus anti-stereotypical attributes using context association tests. The study found that pretrained language models exhibit strong stereotypical biases in the domain of religion. The overall stereotype score (ss) for religion was 63.8 for the ensemble model (where 50 is ideal and 100 is maximally stereotypical), indicating a significant bias. A key finding was that while the target term 'Muslim' had strong stereotypical associations in the dataset (e.g., 'terrorist' appeared in 20% of stereotypes), the models surprisingly exhibited more idealistic behavior, showing a slight preference for anti-stereotypes in this specific case, a behavior the authors could not explain.


## REVISE: A Tool for Measuring and Mitigating Bias in Visual Datasets

[https://arxiv.org/pdf/2004.07999](https://arxiv.org/pdf/2004.07999)

**Date:** 2021-07-23

Over/under-representation of religious objects (e.g., mosque, church) in visual datasets, particularly within a geographic context. The tool found that in the YFCC100m dataset, the 'mosque' tag is overrepresented by 30x in images from Iran. This is used as an example to demonstrate the tool's capability to detect geographic-based representational biases for object classes, which can include religious items.


## Classification Benchmarks for Under-resourced Bengali Language based on Multichannel Convolutional-LSTM Network

[https://arxiv.org/pdf/2004.07807](https://arxiv.org/pdf/2004.07807)

**Date:** 2020-04-19

Detection of hate speech directed at specific religious groups. The proposed Multichannel Convolutional-LSTM (MConv-LSTM) model, especially when enhanced with pre-trained BengFastText word embeddings, demonstrated high effectiveness in identifying religious hate speech. In performance evaluations, the model achieved an Area Under the Curve (AUC) score of 0.98 for the 'Religious' hate speech category, indicating strong predictive accuracy for this type of content.


## LOW-RESOURCE NEURAL MACHINE TRANSLATION: A BENCHMARK FOR FIVE AFRICAN LANGUAGES

[https://arxiv.org/pdf/2003.14402](https://arxiv.org/pdf/2003.14402)

**Date:** 2020-03-31

Translation quality (measured in BLEU scores) on corpora containing religious texts (Bible, JW300, Tanzil) as one of several evaluation domains. The paper's findings are primarily about machine translation techniques rather than religion itself. However, it evaluates these techniques on domains that include religious texts (JW300 and Bible). The results show that more advanced methods like multilingual models (M-NMT) and transfer learning (TL) generally achieve higher translation quality (BLEU scores) on these religious-domain test sets compared to baseline single-pair models (S-NMT). The study also highlights that all models show poor performance on out-of-domain data, indicating that models trained on specific domains, including religious texts, do not generalize well.


## Towards Fairer Datasets: Filtering and Balancing the Distribution of the People Subtree in the ImageNet Hierarchy

[https://arxiv.org/pdf/1912.07726](https://arxiv.org/pdf/1912.07726)

**Date:** 2019-12-16

Identification and filtering of sensitive religious concepts from an image dataset. The paper identifies concepts related to religion (e.g., 'Zen Buddhist', 'theist', 'Christian') as 'sensitive' and thus recommends them for removal from the ImageNet 'people' subtree. This is part of a broader effort to filter categories that could be problematic or offensive in a visual recognition context.


## Analysis of the Ethiopic Twitter Dataset for Abusive Speech in Amharic

[https://arxiv.org/pdf/1912.04419](https://arxiv.org/pdf/1912.04419)

**Date:** 

Detection of abusive and hate speech keywords in Amharic tweets, which includes keywords targeting groups based on religion. The study's definition of hate speech, based on an Ethiopian draft law, includes targeting individuals or groups based on religion. The analysis of hate speech keywords in the Amharic Twitter dataset found 'ኢስላም/Islam' among the terms used. The paper also mentions separating tweets in the Ge'ez language, which is primarily used for religious texts by the Ethiopian Orthodox Church.


## Measuring social bias in knowledge graph embeddings

[https://arxiv.org/pdf/1912.02761](https://arxiv.org/pdf/1912.02761)

**Date:** 2020-05-07

Stereotypical associations between professions and religious groups (specifically Catholicism vs. Islam) encoded in knowledge graph embeddings. The knowledge graph embeddings were found to encode strong stereotypical associations between professions and religious identities. For example, professions like 'Catholic priest' and 'bishop' were highly associated with Catholicism, while 'imam' and 'muhaddith' were highly associated with Islam. This demonstrates that statistical imbalances in the training data (Wikidata and FB3M) are learned by the embedding models, resulting in measurable religious bias.


## Evaluating Commonsense in Pre-trained Language Models

[https://arxiv.org/pdf/1911.11931](https://arxiv.org/pdf/1911.11931)

**Date:** 2021-02-11

The benchmark measured abductive reasoning on social topics, including arguments involving religious claims (e.g., arguments about Christians and sin). The tested models performed poorly on the Argument Reasoning Comprehension Task (ARCT), which includes social topics like religion, with performance close to random chance. This indicates a difficulty with the abductive reasoning required for such topics.


## A Benchmark Dataset for Learning to Intervene in Online Hate Speech

[https://arxiv.org/pdf/1909.04251](https://arxiv.org/pdf/1909.04251)

**Date:** 2019-09-10

Detection of and intervention in online hate speech, where hate speech is defined as a direct attack on people based on protected characteristics including religious affiliation. The paper uses examples of anti-Semitic hate speech (e.g., 'dirty Jew') to illustrate its dataset and the task of generative intervention. However, the experimental results and findings are not broken down by hate speech category. The general finding is that the generative models tested (Seq2Seq, VAE, RL) can produce reasonable interventions but are significantly outperformed by human-written responses, indicating substantial room for improvement in countering all forms of hate speech, including religious-based hate.


## On Measuring and Mitigating Biased Inferences of Word Embeddings #Mormon

[https://arxiv.org/pdf/1908.09369](https://arxiv.org/pdf/1908.09369)

**Date:** 2019-11-26

The benchmark measured stereotypical or polarized inferences by constructing sentence pairs comparing adherents of various religions (e.g., 'The Catholic person crashed a car') with sentences containing polarity terms (e.g., 'The evil person crashed a car') within a Natural Language Inference (NLI) framework. The study found that both static (GloVe) and contextualized (ELMo) word embeddings encode significant biases related to religion. About 25% of sentence pairs involving religious adherents were incorrectly inferred as non-neutral, often associating them with negative polarity terms (e.g., 'evil', 'dishonest'). For example, terms like 'Satanist' and 'Muslim' were associated with negative actions. The ELMo-based model performed notably worse than GloVe on this test. Unlike with gender bias, the projection-based debiasing methods were found to be ineffective for mitigating religious bias in ELMo.


## Dunhuang Grottoes Painting Dataset and Benchmark

[https://arxiv.org/pdf/1907.04589](https://arxiv.org/pdf/1907.04589)

**Date:** 2019-07-11

The benchmark does not measure any aspect of faith or religion. It is a computer vision benchmark that measures the performance of algorithms on the task of restoring damaged images of paintings from the Dunhuang Grottoes, which are sites of Buddhist religious art. The paper does not present findings related to religion. The paper's contribution is the creation and release of the Dunhuang Grottoes Painting Dataset, a new public dataset for image restoration research, along with a benchmark and evaluation metrics (DSSIM and LMSE) for this task.


## Evaluating an Automated Mediator for Joint Narratives in a Conflict Situation

[https://arxiv.org/pdf/1906.11597](https://arxiv.org/pdf/1906.11597)

**Date:** 

Measuring attitude changes (willingness to compromise, anger, etc.) between conflicting groups (Israeli Jews and Israeli Arabs) whose conflict involves significant ethnic and religious dimensions. The study found that using an automated mediator for collaborative storytelling between Israeli Arabs and Israeli Jews led to positive outcomes comparable to a human mediator. Specifically, the intervention resulted in a more positive attitude toward the conflict, a reduction of anger toward the other group (especially for Hebrew speakers), and an increased willingness to learn more about the other side (especially for Arab speakers). The findings concern attitude shifts between groups in a conflict with a religious dimension, rather than specific religious beliefs or biases.


## Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices

[https://arxiv.org/pdf/1906.09208](https://arxiv.org/pdf/1906.09208)

**Date:** 2019-12-06

The paper does not conduct a benchmark measurement. It analyzes the claims and practices of algorithmic hiring companies regarding bias mitigation for legally protected characteristics, which includes religion under U.S. law. The paper finds that religion is a legally protected characteristic under U.S. employment law (Title VII of the Civil Rights Act). The bias mitigation techniques used by vendors are primarily driven by the legal framework of disparate impact and compliance with the '4/5 rule,' which would apply to cases of religious discrimination. However, the paper provides no specific analysis or findings on how these algorithmic tools perform with respect to religious bias in practice.


## OK-VQA: A Visual Question Answering Benchmark Requiring External Knowledge

[https://arxiv.org/pdf/1906.00067](https://arxiv.org/pdf/1906.00067)

**Date:** 2019-09-04

Factual knowledge of religious practices, cultural contexts, and beliefs, as part of a broader benchmark on external knowledge for visual question answering. The paper demonstrates that state-of-the-art Visual Question Answering (VQA) models perform poorly on questions requiring external knowledge. While not focusing exclusively on religion, this includes a significant performance drop on questions that need factual knowledge about religious concepts, such as identifying the primary day of worship for a Christian church or recognizing which religion considers specific animals sacred.


## Nuanced Metrics for Measuring Unintended Bias with Real Data for Text Classification

[https://arxiv.org/pdf/1903.04561](https://arxiv.org/pdf/1903.04561)

**Date:** 2019-05-08

Unintended bias in toxicity classification models when text contains references to religious identities. The metrics measure how a classifier's score distribution varies for comments mentioning specific religious groups compared to a background set of comments. The toxicity classification models showed bias related to religious identities. Non-toxic comments referencing 'jewish' and 'muslim' identities were more likely to be skewed towards higher toxicity scores compared to those referencing 'christian'. This aligns with societal stereotypes where certain groups are more frequently attacked online. The updated model, TOXICITY@6, demonstrated some mitigation of this bias, especially for short comments, but bias was still present.


## Partisanship, Propaganda and Post-Truth Politics: Quantifying Impact in Online Debate

[https://arxiv.org/pdf/1902.01752](https://arxiv.org/pdf/1902.01752)

**Date:** 2020-02-17

Analysis of anti-Muslim sentiment in online propaganda from Russian troll accounts. Right-wing Russian IRA troll accounts used anti-Muslim sentiment and pejorative hashtags (e.g., 'ReligionOfPeace') as part of their propaganda strategy to influence political discourse. The analysis of troll material showed it was often 'anti-Muslim', and the bio of one high-impact troll included 'Anti Islam'.


## The FLORES Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English

[https://arxiv.org/pdf/1902.01382](https://arxiv.org/pdf/1902.01382)

**Date:** 2019-09-14

The benchmark measures the quality of machine translation for low-resource languages (Nepali, Sinhala) to and from English, using sentences from Wikipedia articles. A portion of these articles covers religious topics, so the benchmark implicitly measures the ability to translate religious texts. The paper does not offer specific findings related to religion. Its main finding is that state-of-the-art machine translation models perform poorly on these low-resource language benchmarks, which include sentences from religious documents (e.g., about Buddhism, Hinduism, Islam). The analysis showed that translation difficulty was consistent across different document topics, suggesting religious texts were not exceptionally harder or easier to translate than other topics in the dataset.


## Measure, Manifold, Learning, and Optimization: A Theory Of Neural Networks

[https://arxiv.org/pdf/1811.12783](https://arxiv.org/pdf/1811.12783)

**Date:** 2018-11-30

Not applicable. The paper is a theoretical work and does not conduct any benchmarks. Religious and philosophical concepts are used for historical context and motivation in the introduction. Not applicable. The paper's findings are purely mathematical regarding a theory of neural networks. Religious references are used for historical and philosophical context in the introduction to motivate the research, not as a subject of analysis.


## Hate Speech Detection from Code-mixed Hindi-English Tweets Using Deep Learning Models

[https://arxiv.org/pdf/1811.05145](https://arxiv.org/pdf/1811.05145)

**Date:** 2018-11-13

The paper qualitatively evaluates domain-specific word embeddings by measuring the cosine similarity between the word 'women' and words representing minority groups, including a 'Religious Minority' group. This is part of a broader task of detecting hate speech targeted at groups based on attributes like religion. Domain-specific word embeddings captured societal relationships more accurately than general embeddings. Specifically, the cosine similarity between 'women' and words representing a 'Religious Minority' was significantly higher (0.637) with domain-specific embeddings compared to general embeddings (0.224), highlighting their improved ability to represent contexts relevant to hate speech.


## AI FAIRNESS 360: AN EXTENSIBLE TOOLKIT FOR DETECTING, UNDERSTANDING, AND MITIGATING UNWANTED ALGORITHMIC BIAS

[https://arxiv.org/pdf/1810.01943](https://arxiv.org/pdf/1810.01943)

**Date:** 2018-10-03

The paper presents a toolkit (AIF360) designed to detect, understand, and mitigate unwanted algorithmic bias. Religion is mentioned as an example of a 'protected attribute' against which bias could be measured, similar to race or gender. However, the paper's own experiments do not use religion as a protected attribute for measurement. The paper does not present any findings related to religion. Religion is mentioned once as a potential protected attribute for fairness analysis, but none of the datasets or experiments described in the paper involve religious data or bias measurements related to religious groups.


## Measuring Semantic Abstraction of Multilingual NMT with Paraphrase Recognition and Generation Tasks

[https://arxiv.org/pdf/1808.06826](https://arxiv.org/pdf/1808.06826)

**Date:** 2019-05-03

The benchmark measures the ability of neural machine translation models to learn semantic abstractions, evaluated through paraphrase recognition (perplexity) and paraphrase generation (BLEU and PINC scores). The Bible is used as the primary data source to provide a multilingual corpus with constant genre and content. Using Bible translations as a large, multilingual, constant-genre dataset, the study found that training neural machine translation (NMT) models on a diverse set of languages leads to stronger semantic abstractions compared to bilingual models. This was evidenced by significantly lower perplexity on paraphrase recognition tasks and higher quality paraphrase generation, suggesting that increased linguistic diversity in training forces the model to learn more language-independent meaning representations.

