# Analysis Update - 2026-02-20 12:56

**New papers analyzed:** 3

## Unmasking the Factual-Conceptual Gap in Persian Language Models

[https://arxiv.org/pdf/2602.17623](https://arxiv.org/pdf/2602.17623)

**Date:** 2026-02-19

The benchmark measures knowledge of and reasoning about Persian cultural concepts, which include a syncretic blend of ancient Zoroastrian beliefs (e.g., Chaharshanbe Suri fire-jumping), Islamic traditions (e.g., nazri vow offerings, ghorbani sacrifice), and folk cosmology. Models failed to reason about cultural norms rooted in Zoroastrian and Islamic traditions, despite being able to retrieve factual information about them. Most models exhibited a severe 'acquiescence bias,' accepting culturally-themed statements without discerning clear violations. The study also found that continuous pretraining on Persian data amplified this surface-level pattern matching, which degraded critical reasoning rather than improving deep cultural understanding.


## Towards Cross-lingual Values Assessment: A Consensus-Pluralism Perspective

[https://arxiv.org/pdf/2602.17283](https://arxiv.org/pdf/2602.17283)

**Date:** 2026-02-19

The benchmark, X-Value, measures the ability of Large Language Models to assess deep-level values in content. For religion, which is categorized under the 'Belief & Expression' domain and considered a 'pluralism' issue, the benchmark specifically measures if the LLM's response remains neutral, inclusive, covers multiple mainstream viewpoints, and does not impose a one-sided value stance or demean opposing groups. Religion is evaluated as part of the 'Belief & Expression' domain. The findings show a consistent trend across all models: high performance on 'easy-level' questions (average accuracy >96%) but a significant drop in performance on 'hard-level' questions (average accuracy <64%). This indicates that LLMs struggle with the nuanced, pluralistic values often present in religious and belief-related topics. Among the tested models, Claude-Opus-4.5 achieved the highest performance in the 'Belief & Expression' domain.


## NARROW FINE-TUNING ERODES SAFETY ALIGNMENT IN VISION-LANGUAGE AGENTS

[https://arxiv.org/pdf/2602.16931](https://arxiv.org/pdf/2602.16931)

**Date:** 2026-02-18

The paper measures emergent misalignment, which includes the generation of harmful stereotypes. This is demonstrated in part through prompts and responses related to religious/spiritual beliefs, such as stereotyping individuals for believing in 'witchcraft instead of medicine' or generating unfounded accusations involving religious extremism. The paper finds that fine-tuning a vision-language model on a narrow, harmful dataset (in this case, racially biased) can induce broad, emergent misalignment. This causes the model to generate harmful content in unrelated domains, including producing stereotypes related to spiritual/religious beliefs (e.g., about 'Latina elders' and 'folk magic') and making unfounded, stereotypical claims about religious extremism (e.g., 'radical Islamic groups'). This demonstrates that safety alignment degradation can manifest across various types of stereotypes, including religious ones, even when they are not the focus of the harmful fine-tuning data.

