# Analysis Update - 2026-04-24 12:20

**New papers analyzed:** 7

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

