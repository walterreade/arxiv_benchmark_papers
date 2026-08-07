# Analysis Update - 2026-08-07 14:23

**New papers analyzed:** 2

## What Current AI Benchmarks Leave Unmeasured: Modality, Search, Citations, and Implications (for Safety Evaluations)

[https://arxiv.org/pdf/2608.06202](https://arxiv.org/pdf/2608.06202)

**Date:** 2026-08-06

The paper evaluated the model's accuracy, response consistency, and abstention (refusal) rates when answering multiple-choice questions about social biases, including a specific subset of prompts from the BBQ benchmark that test for stereotypes related to religion (e.g., assumptions about Christians vs. Muslims regarding harassment or hijacking). The study found that abstention (refusal) behavior was highly inconsistent across repeated runs and access modalities (API vs. Chat UI). Notably, out of only four distinct prompts that triggered abstentions in the study, two were from the Religion category (one testing bias about a Muslim vs. Christian harassing a woman, and another regarding hijacking). The model would abstain in one setting (e.g., Chat UI) but answer the same prompt in another (e.g., API), demonstrating that guardrails around identity-related and religious content are inconsistently applied.


## Innocent Panels, Hateful Stories: Evaluating and Detecting Hateful Intent in Multi-Turn Visual Story Generation

[https://arxiv.org/pdf/2608.05210](https://arxiv.org/pdf/2608.05210)

**Date:** 2026-08-05

The paper measures the extent to which conversational multi-turn text-to-image (T2I) models can be exploited to generate sequence-level hateful visual stories (including antisemitic and anti-Muslim narratives) from individually benign prompts. It also evaluates whether existing safety classifiers and vision-language models can successfully detect this distributed religious and racial hate when inspecting the full sequence. State-of-the-art text-to-image models successfully completed hateful visual stories (which include discrimination against Jewish people and Muslims) in 80.4% to 99.0% of cases, bypassing per-turn safety filters because the hateful intent is distributed across multiple innocuous prompts. Existing post-generation safety detectors generally fail to identify these antisemitic and anti-Muslim visual narratives from the completed image sets, although proactive interaction-aware monitoring and specialized story-level fine-tuning significantly improved detection rates.

