# Analysis Update - 2026-04-01 14:11

**New papers analyzed:** 3

## Emergent Social Intelligence Risks in Generative Multi-Agent Systems

[https://arxiv.org/pdf/2603.27771](https://arxiv.org/pdf/2603.27771)

**Date:** 2026-03-29

The paper evaluated the ability of multi-agent systems to negotiate, compromise, and converge on shared plans when agents are assigned divergent cultural and religious norms. Specifically, it measured whether agents could resolve conflicts when one agent (representing a South Asian religious community) rigidly demanded sacred time for prayer, meditation, and pure-vegetarian dietary restrictions against the secular preferences of other agents. The study found that without an explicit arbitrator, multi-agent systems often fail to converge and experience persistent deadlock when faced with deep-seated religious and cultural norm conflicts (e.g., an agent refusing to compromise on an 'inviolable sacred time' for prayer). However, introducing a mediation-enabled arbitrator agent successfully introduced coordination anchors that guided the agents toward a stable, compromised resolution while respecting the religious constraints.


## Routing Sensitivity Without Controllability: A Diagnostic Study of Fairness in MoE Language Models

[https://arxiv.org/pdf/2603.27141](https://arxiv.org/pdf/2603.27141)

**Date:** 2026-03-28

The paper measures sociodemographic bias and stereotyping (across nine axes, including religion) by evaluating routing sensitivity and distributions in Mixture-of-Experts (MoE) language models. It tests whether altering inference-time routing can reduce bias on standard fairness benchmarks without degrading model utility. The models exhibited universal routing sensitivity to demographic variations, including religion. However, the study found that this sensitivity does not reliably equate to controllability. In most models, routing-level interventions to reduce demographic bias were either unachievable, incurred a severe utility cost, or failed to transfer to the decoded text generation entirely.


## ParsCN: A Persian Dataset for Counter-Narrative Generation to Combat Online Hate Speech

[https://arxiv.org/pdf/2603.27011](https://arxiv.org/pdf/2603.27011)

**Date:** 2026-03-27

The paper measures the ability of various Large Language Models to generate high-quality, culturally appropriate, and safe counter-narratives to online hate speech in Persian. This includes evaluating responses to a specific subset of hate speech targeting 'Religious' groups (such as statements targeting Islam or the Jewish religion). The models are assessed on relevance, effectiveness, fluency, tone appropriateness, semantic similarity, and toxicity. The paper curated the ParsCN dataset, containing 1,100 hate speech-counter-narrative pairs. The dataset features a dedicated 'Religious' target group comprising 200 pairs. Interestingly, the average counter-narrative addressing religious hate speech had the longest word count (32.04 words) of all categories. While the study did not isolate model performance solely on the religious subset, general findings showed that human-written counter-narratives scored highest in quality, with GPT-4o and Claude closely matching human performance in relevance and tone. Baseline models like mBART and PersianMind struggled significantly with fluency, cultural nuance, and safety (toxicity) when generating counter-narratives.

