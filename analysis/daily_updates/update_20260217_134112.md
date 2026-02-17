# Analysis Update - 2026-02-17 13:41

**New papers analyzed:** 7

## Counterfactual Fairness Evaluation of LLM-Based Contact Center Agent Quality Assurance System

[https://arxiv.org/pdf/2602.14970](https://arxiv.org/pdf/2602.14970)

**Date:** 2026-02-16

The benchmark measured evaluative bias in a Quality Assurance (QA) setting against contact center agents with religiously identifiable names (e.g., 'Daniel' for Christian vs. 'Imran' for Muslim) and against agents who use benign religious expressions (e.g., 'Inshallah', 'God bless'). The goal was to determine if these religious cues unfairly altered the LLM's performance judgments. Models showed minimal bias when only agent names were substituted based on religion (6.25% Counterfactual Flip Rate). However, fairness significantly worsened when benign religious linguistic cues (e.g., 'Inshallah') were added, increasing the flip rate to 9.24% and the Mean Absolute Score Difference for confidence to 10.35. This indicates that while models have some surface-level robustness, implicit biases against religious expressions remain entrenched.


## Concept Influence: Leveraging Interpretability to Improve Performance and Efficiency in Training Data Attribution

[https://arxiv.org/pdf/2602.14869](https://arxiv.org/pdf/2602.14869)

**Date:** 2026-02-16

Generation of biased, extremist, and conspiratorial content against Muslims, used as an example of 'emergent misalignment'. The evaluation focuses on whether data attribution methods can identify and filter training data that causes this behavior. The paper demonstrates that its proposed data attribution methods, such as Concept Influence, can effectively identify training data points that lead to misaligned behaviors like generating extremist and biased content about Muslims. By filtering out these influential data points, the model's tendency to produce such harmful content (measured as an 'evil' trait score) is significantly reduced.


## The Global Representativeness Index: A Total Variation Distance Framework for Measuring Demographic Fidelity in Survey Research

[https://arxiv.org/pdf/2602.14835](https://arxiv.org/pdf/2602.14835)

**Date:** 2026-02-16

The benchmark measures the distributional fidelity of a survey sample's religious affiliation composition against global population benchmarks from the Pew Global Religious Landscape. This is evaluated as a cross-classification with country (Country × Religion) to assess how well the joint distribution in a sample matches the target population. The paper finds that survey representativeness for the 'Country × Religion' dimension (mean GRI score of ~0.50 for the Global Dialogues survey) is significantly better than for the more granular 'Country × Gender × Age' dimension (mean GRI ~0.34). This is attributed to three structural factors: religion has fewer demographic strata (1,607 vs. 2,699), the major religious groups have large population proportions, and there is a strong geographic correlation (sampling many countries naturally captures a degree of religious diversity). However, the paper also notes a limitation: the religious benchmark data is from 2010 and may overstate religious affiliation due to secularization.


## ForesightSafety Bench: A Frontier Risk Evaluation and Governance Framework towards Safe AI

[https://arxiv.org/pdf/2602.14135](https://arxiv.org/pdf/2602.14135)

**Date:** 2026-02-15

The benchmark includes a dimension for 'Extremist & Cult' content, categorized under 'Fake & Misleading Information'. It aims to test whether a model generates or reinforces propaganda from extremists or cults. The paper does not present specific findings for the 'Extremist & Cult' risk dimension. The analysis focuses on higher-level safety pillars (e.g., Fundamental Safety, AI4Science, Risky Agentic Autonomy), and no detailed results related to religion, faith, or cults are discussed.


## Empty Shelves or Lost Keys? Recall Is the Bottleneck for Parametric Factuality

[https://arxiv.org/pdf/2602.14080](https://arxiv.org/pdf/2602.14080)

**Date:** 2026-02-15

The benchmark (WikiProfile) measures factual knowledge encoding and recall across nine categories of facts derived from Wikipedia. One of these categories is 'Philosophy & Religion', which covers belief systems, ethics, religions, and mythological narratives. The paper's findings are general to the mechanisms of factual recall in LLMs and do not offer specific insights related to the 'Philosophy & Religion' category. This category was included as part of the overall dataset to ensure broad topic coverage, but was not singled out for separate analysis.


## ADAB: Arabic Dataset for Automated Politeness Benchmarking - A Large-Scale Resource for Computational Sociopragmatics

[https://arxiv.org/pdf/2602.13870](https://arxiv.org/pdf/2602.13870)

**Date:** 

The benchmark measures the ability of models to correctly interpret the sociopragmatic function of religious expressions in Arabic, such as 'Subhan'Allah', for politeness classification. It also involved a data cleaning process that removed texts with strong religious sectarian content or unacceptable criticism of religious beliefs to focus on politeness rather than ideology. Models frequently misclassify texts containing religious expressions (e.g., 'Subhan'Allah') because their politeness value is highly context-dependent. This ambiguity, where a religious phrase can signal either politeness or impoliteness, poses a significant challenge, leading to errors where models default to a 'Neutral' classification. The dataset construction also explicitly filtered out strong sectarian religious content to avoid conflating ideology with politeness.


## Bridging the Multilingual Safety Divide: Efficient, Culturally-Aware Alignment for Global South Languages

[https://arxiv.org/pdf/2602.13867](https://arxiv.org/pdf/2602.13867)

**Date:** 2026-02-14

Detection of culturally harmful content, including biased generalizations, dismissive portrayals, and one-sided framings, with religion being one of the 11 societal domains evaluated. Large Language Models, even those deemed 'safe' by standard toxicity metrics, can produce culturally insensitive or harmful outputs related to societal domains including religion. These failures manifest as biased generalizations, dismissive portrayals of local customs, and one-sided framings. Culturally aware alignment, using preference data from local annotators, was shown to effectively reduce these harms without degrading performance on other tasks.

