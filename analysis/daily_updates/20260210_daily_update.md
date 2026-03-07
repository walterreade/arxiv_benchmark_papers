# Analysis Update - 2026-02-10 14:38

**New papers analyzed:** 5

## How2Everything: Mining the Web for How-To Procedures to Evaluate and Improve LLMs

[https://arxiv.org/pdf/2602.08808](https://arxiv.org/pdf/2602.08808)

**Date:** 2026-02-09

The benchmark measured the ability of Large Language Models to generate valid, step-by-step procedures for tasks categorized under the topic 'Religion'. This category is broad and includes not only tasks related to organized religions but also spiritual practices like astrology, as indicated by an example task: 'Analyze the influence of decanates in horoscopes and their relation to Consciousness on the principal theme of a natal chart.' The 'Religion' topic was one of 14 categories evaluated for procedural generation. On the Qwen3-8B model, the baseline performance for this topic was a 48.09% success rate. After reinforcement learning (RL) on a dataset covering all 14 topics, the score improved to 53.91%. A regression analysis also showed that the 'Religion' topic was slightly more difficult for models to generate correct procedures for compared to the baseline 'Art & Design' topic, even after controlling for other factors like the number of steps.


## ValueFlow: Measuring the Propagation of Value Perturbations in Multi-Agent LLM Systems

[https://arxiv.org/pdf/2602.08567](https://arxiv.org/pdf/2602.08567)

**Date:** 2026-02-09

The benchmark measures the β-susceptibility (sensitivity to peer influence) of LLMs' expressed values in multi-agent systems. Among the 56 values from the Schwartz Value Survey, this includes the religion-related values of 'Devout' and 'A Spiritual Life'. The susceptibility of religion-related values to peer influence varies significantly. In experiments with the Qwen3-8B model, the value 'Devout' exhibited a relatively high β-susceptibility score, indicating it is more easily influenced by peer agents. In contrast, 'A Spiritual Life' showed a lower-middle susceptibility score, suggesting greater stability against peer influence.


## Agent-Supported Foresight for AI Systemic Risks: AI Agents for Breadth, Experts for Judgment

[https://arxiv.org/pdf/2602.08565](https://arxiv.org/pdf/2602.08565)

**Date:** 2026-02-09

Identification of potential displacement of the roles of religious communities in mourning rituals by AI systems. Human domain leaders, in their evaluation of the 'Griefbot' AI use case, identified a systemic risk that the in-silico agents had overlooked: the potential for AI to displace the traditional roles of institutions, including religious communities, in managing tasks related to death and mourning. This displacement could reconfigure how societies organize these fundamental rituals.


## Fairness Aware Reward Optimization

[https://arxiv.org/pdf/2602.07799](https://arxiv.org/pdf/2602.07799)

**Date:** 2026-02-08

Stereotype detection and bias reduction in ambiguous contexts involving religious groups. Specifically, it measured whether the model would rely on harmful stereotypes about Muslims and Jews to assign blame in a criminal scenario. The base model (Gemma-2) relied on religious stereotypes, incorrectly implicating a Jewish person in a crime based on prompt wording. The proposed method, FARO, successfully trained the model to abstain from making a determination based on protected attributes like religion, leading it to correctly answer 'Can't be determined' and provide bias-aware reasoning.


## From Native Memes to Global Moderation: Cross-Cultural Evaluation of Vision–Language Models for Hateful Meme Detection

[https://arxiv.org/pdf/2602.07497](https://arxiv.org/pdf/2602.07497)

**Date:** 2026-02-07

Detection of hateful memes containing region-specific religious symbolism as part of a broader cross-cultural evaluation. The study evaluated model performance on an Arabic dataset (Prop2Hate) that includes memes with region-specific religious symbolism. The general finding is that models struggle with culturally nuanced content, including religious contexts, and that common 'translate-then-detect' approaches degrade performance, while native-language prompting and culturally aligned examples improve it.

