# Analysis Update - 2026-10-22 10:04

**New papers analyzed:** 3

## Effects of Model Scale and Quantization on Social Bias and Abstention in Question Answering

[https://arxiv.org/pdf/2610.29657](https://arxiv.org/pdf/2610.29657)

**Date:** 2026-10-21

The paper measures social stereotype bias, including biases related to religion, by evaluating how model scale and quantization affect a model's tendency to produce biased responses versus appropriately abstaining (or over-abstaining) when answering ambiguous and disambiguated multiple-choice questions. Religion was evaluated as one of the 11 social bias categories in the BBQ benchmark. The study found that model compression/quantization affects bias and abstention behaviors across all categories, including religion. When the models were forced to choose an answer by removing the 'Unknown' option, previously hidden biases—or anti-biased tendencies—surfaced across multiple categories, including religion. This indicates that a low bias score in religious contexts can sometimes reflect a model's tendency to abstain rather than an inherently fair judgment.


## Melange: A Synthetic Visual Bias Benchmark for Multi-modal Large Language Models

[https://arxiv.org/pdf/2610.29537](https://arxiv.org/pdf/2610.29537)

**Date:** 2026-10-21

The paper evaluated social bias and stereotype alignment in Multimodal Large Language Models (MLLMs) across seven demographic categories, including religion. Specifically, it measured the extent to which models rely on human stereotypes when answering ambiguous visual question answering (VQA) prompts featuring generated images of characters from different religious backgrounds. The paper found that the models evaluated showed the highest fairness (FaiR scores) on the religion and race categories compared to other demographic categories. Additionally, a perception control probe revealed that even though religious affiliation is theoretically visually indeterminate, models achieved 84.8% accuracy in identifying religion from the synthetic images because the image generator (Flux) encoded visible religious markers such as clothing or headwear.


## BEYOND MODEL WEIGHTS: SAMPLING-DEPENDENT FAIRNESS IN DIFFUSION LANGUAGE MODELS

[https://arxiv.org/pdf/2610.27584](https://arxiv.org/pdf/2610.27584)

**Date:** 2024-10-20

The paper measures representational social bias, including bias regarding religion, by evaluating whether models favor stereotype-aligned answers in ambiguous versus disambiguated contexts. It investigates how bias scores are affected not just by model weights, but by sampling configurations (e.g., block length, tokens per step, remasking strategy) in Diffusion Language Models (DLMs). Religion was evaluated as one of 11 social categories from the Open-BBQ benchmark. The base models exhibited moderate social bias in the Religion category in ambiguous contexts (e.g., an ambiguous bias score of 0.157 for LLaDA-8B and 0.167 for LLaDA-1.5). However, bias in these models was mostly concentrated in other categories like Age, Physical Appearance, SES, and Disability Status. Applying debiasing techniques (Supervised Fine-Tuning and On-Policy Self-Distillation) successfully reduced the bias scores across categories, including Religion, though the measured magnitude of these biases remained highly sensitive to the generation sampling configurations.

