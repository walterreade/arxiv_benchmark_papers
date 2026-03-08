# Analysis Update - 2026-02-23 10:44

**New papers analyzed:** 2

## VIRAASAT: Traversing Novel Paths for Indian Cultural Reasoning

[https://arxiv.org/pdf/2602.18429](https://arxiv.org/pdf/2602.18429)

**Date:** 2026-02-20

The benchmark measures multi-hop reasoning and factual knowledge about various facets of Indian culture, with religion being one of the 13 attributes. This includes knowledge of religious festivals (e.g., Ramman festival, Baha Parab), sacred sites (e.g., Har ki Pauri ghat), and related cultural artifacts. The paper's findings are general across all cultural categories, including religion, as no religion-specific analysis was presented. The key findings are that large language models exhibit poor zero-shot performance in multi-hop reasoning about long-tail cultural entities. Standard supervised fine-tuning on Chain-of-Thought (CoT) traces improves performance moderately. However, the proposed Symbolic Chain-of-Manipulation (SCoM) framework, which trains models on structured, graph-grounded reasoning traces, yields substantial improvements, boosting end-to-end accuracy by over 20% compared to CoT baselines.


## Neurosymbolic Language Reasoning as Satisfiability Modulo Theory

[https://arxiv.org/pdf/2602.18095](https://arxiv.org/pdf/2602.18095)

**Date:** 2026-02-20

The benchmark measured the ability of large language models to perform compositional and combinatorial reasoning when applying a multi-clause content moderation policy related to religious content. This was part of a broader set of policies designed to test reasoning on documents with mixed textual and logical structures. The paper found that even frontier LLMs exhibit significant 'reasoning gaps' when handling tasks with complex logical structures. For the religious content moderation task, the proposed neurosymbolic framework, Logitext, consistently outperformed end-to-end LLM prompting in both text instance generation and text coverage generation, demonstrating improved accuracy and coverage by explicitly handling the policy's logical structure.

