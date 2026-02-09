# Analysis Update - 2026-02-09 14:24

**New papers analyzed:** 1

## Uncertainty Drives Social Bias Changes in Quantized Large Language Models

[https://arxiv.org/pdf/2602.06181](https://arxiv.org/pdf/2602.06181)

**Date:** 2026-02-05

The benchmark measured social bias (stereotyping, toxicity, disparate outcomes) related to religious groups and figures. For instance, the IAT dataset measured stereotypical word associations with religious figures (e.g., 'jesus', 'muhammad'), while datasets like BBQ, BiasLens, and CEB evaluated model behavior on prompts involving a 'religion' social axis. Quantization has an unpredictable and asymmetric impact on model bias related to religion. The paper found that for certain models and datasets (e.g., LLaMA 3.2 3B on BBQ), bias against the 'catholic' group significantly increased post-quantization. Conversely, in other instances, quantization caused a model to shift from a biased statement about a religious group ('Sunni kids are just troublemakers') to an unbiased one. These findings demonstrate that compression can fundamentally and erratically alter how models handle religious topics, with effects varying by model, quantization method, and specific context.

