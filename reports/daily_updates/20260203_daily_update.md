# Analysis Update - 2026-02-03 19:39

**New papers analyzed:** 8

## Sinhala Physical Common Sense Reasoning Dataset for Global PIQA

[https://arxiv.org/pdf/2602.02207](https://arxiv.org/pdf/2602.02207)

**Date:** 2026-02-02

The benchmark measures physical common sense reasoning knowledge, with a specific domain dedicated to questions situated within the cultural context of Sinhala Buddhism. The dataset contains a specific domain for 'Buddhism' to test common sense reasoning within that cultural context. It was found that while GPT-5 generally outperformed SinBERT, SinBERT achieved a higher accuracy (83.33% vs 50.00%) on question-answer pairs in the Buddhism domain. The paper's authors also acknowledge that the dataset has an inherent bias towards Sinhala Buddhist culture, as both data creators belong to this group.


## WildGraphBench: Benchmarking GraphRAG with Wild-Source Corpora

[https://arxiv.org/pdf/2602.02053](https://arxiv.org/pdf/2602.02053)

**Date:** 2026-02-02

The benchmark measured the factual retrieval, aggregation, and summarization capabilities of GraphRAG systems using Wikipedia articles and their cited web sources from the 'Religion' domain. In the 'Religion' domain, several systems (NaiveRAG, Microsoft GraphRAG(global), LightRAG(hybrid)) achieved perfect 100% accuracy on multi-fact questions, a significant outlier compared to other topics. For single-fact questions, HippoRAG2 performed best with 68.06% accuracy. All methods struggled with summarization tasks, where NaiveRAG achieved the highest F1 score (6.83), reinforcing the finding that flat RAG baselines can have better factual coverage for broad summary questions.


## SEA-Guard: Culturally Grounded Multilingual Safeguard for Southeast Asia

[https://arxiv.org/pdf/2602.01618](https://arxiv.org/pdf/2602.01618)

**Date:** 2026-02-02

Detection of harmful, stereotypical, or culturally insensitive content related to religious topics, such as generalizations about religious groups (e.g., assuming all Indonesians are Muslim) and religious food prohibitions. Existing safeguard models perform poorly on culturally and religiously sensitive topics specific to Southeast Asia, failing to block prompts that make harmful generalizations (e.g., assuming all Indonesians are Muslim). The proposed SEA-Guard model, trained on culturally grounded data including religious contexts, significantly outperforms these existing models in identifying regionally sensitive content while maintaining strong general safety performance.


## Wiki Live Challenge: Challenging Deep Research Agents with Expert-Level Wikipedia Articles

[https://arxiv.org/pdf/2602.01590](https://arxiv.org/pdf/2602.01590)

**Date:** 2026-02-02

Performance in generating factual, comprehensive, and neutral Wikipedia-style articles on topics related to 'Philosophy and religion'. Deep Research Agents performed best on the 'Philosophy and religion' category compared to 14 other domains. This category had the highest average win rate (56.2%) across all tested systems, indicating these topics were relatively less difficult for the agents to generate high-quality articles about compared to categories like 'History' and 'Mathematics'.


## How Implicit Bias Accumulates and Propagates in LLM Long-term Memory

[https://arxiv.org/pdf/2602.01558](https://arxiv.org/pdf/2602.01558)

**Date:** 2026-02-02

The benchmark measured implicit bias against religious individuals, specifically framing religious observance as an operational burden compared to the flexibility of secular individuals. This was tested in scenarios like workplace scheduling. The study found that implicit biases related to religion, when injected into long-term memory, accumulate and propagate to other unrelated social domains. For example, injecting bias against religious observance could increase bias in domains like race or nationality. The proposed mitigation strategy, Dynamic Memory Tagging (DMT), was shown to effectively reduce this cross-domain propagation, for instance, preventing Religion bias from affecting Age-related decisions.


## PersistBench: When Should Long-Term Memories Be Forgotten by LLMs?

[https://arxiv.org/pdf/2602.01146](https://arxiv.org/pdf/2602.01146)

**Date:** 2026-02-01

Inappropriate injection of stored religious user beliefs into unrelated conversational contexts, a failure mode termed 'Belief and Identity Injection'. The benchmark found that LLMs are highly susceptible to inappropriately injecting stored user beliefs, including religious beliefs (e.g., a user's Christian views on morality and music), into unrelated tasks. This is categorized as a 'Belief and Identity Injection' failure, where the model prioritizes the user's stored ideology over objective task requirements.


## Fair-GPTQ: Bias-Aware Quantization for Large Language Models

[https://arxiv.org/pdf/2509.15206](https://arxiv.org/pdf/2509.15206)

**Date:** 2026-02-02

The benchmarks measured stereotype likelihood and generative question-answering bias in contexts involving religion, as part of a broader evaluation of social biases across protected groups. The proposed method, Fair-GPTQ, successfully reduces stereotypical bias related to religion in generative question-answering tasks. In evaluations using the BBQ benchmark, Fair-GPTQ showed a significant reduction in bias scores for the 'Religion' category compared to the baseline GPTQ model.


## Improving the Distributional Alignment of LLMs using Supervision #Mormon

[https://arxiv.org/pdf/2507.00439](https://arxiv.org/pdf/2507.00439)

**Date:** 2026-02-02

The benchmark measures the distributional alignment of Large Language Model opinions with those of different religious groups on a variety of subjective survey questions from the WGM, OQA, and WVS datasets. The study found that supervised calibration generally improves the opinion alignment of LLMs with various religious groups. The degree of alignment, both before and after calibration, varies across different religious groups, datasets, and LLMs. For instance, on the OQA dataset, groups like Jewish, Muslim, and Orthodox showed relatively high pre-calibration alignment with some models. On the WVS dataset, alignment scores for Hindu respondents were particularly high after calibration (e.g., 86.0 for 'V' and 93.4 for 'Vc' with OLMo-2-7B-I). The paper demonstrates that its methods can improve consistency but does not delve into the reasons for the performance differences between religious groups.

