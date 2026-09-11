# Analysis Update - 2026-09-11 06:47

**New papers analyzed:** 2

## MUtE: A Dual Framework for Concept Erasure and Counterfactual Interventions

[https://arxiv.org/pdf/2609.11253](https://arxiv.org/pdf/2609.11253)

**Date:** 2024-09-10

The paper evaluated the ability of its MUtE (Maximum Utility-preserving Erasure) framework to erase 'religion' as a sensitive concept from continuous textual representations (GPT-4 embeddings). Specifically, it measured how well the methodology could eliminate the predictability of specific religious affiliations from the embeddings (using probing classifiers) while simultaneously preserving the embeddings' utility for a downstream binary toxicity classification task. The paper found that the MUtE framework successfully reduced the ability of probing classifiers to detect religious categories within GPT-4 embeddings of online comments, dropping the probe accuracy near to the chance-level baseline. At the same time, it maintained high downstream utility, effectively preserving the embeddings' structural integrity for toxicity classification better than established baseline erasure methods.


## Reference-Based Bias Detection in LLMs via Relative Representations of Hidden States

[https://arxiv.org/pdf/2609.10060](https://arxiv.org/pdf/2609.10060)

**Date:** 2024-09-09

The paper measures representational bias shifts (ΔB) in the hidden-state representations of LLMs and compares these shifts against output-level biases, such as harmfulness rates and stereotype agreement, across 9 consolidated social group topics, one of which is 'Religion'. Religious groups were evaluated as part of a broader set of demographic topics. The paper demonstrated that changes in output-level biases (such as increased harmfulness or toxicity toward Muslims, Jews, or Buddhists after harmful fine-tuning) strongly correlate with shifts in the model's internal hidden-state representations (ΔB) for those specific groups, validating the efficacy of representational bias shift as a metric for tracking induced bias.

