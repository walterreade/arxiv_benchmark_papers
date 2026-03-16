# Analysis Update - 2026-03-16 22:02

**New papers analyzed:** 2

## SectEval: Evaluating the Latent Sectarian Preferences of Large Language Models #ReligionFocus

[https://arxiv.org/pdf/2603.12768](https://arxiv.org/pdf/2603.12768)

**Date:** 2026-03-13

The paper measures the latent sectarian preferences and intra-religious biases of Large Language Models (LLMs) by evaluating how they handle theological, historical, and jurisprudential differences between the Sunni and Shia sects of Islam. It uses a custom benchmark, SectEval, to see if models maintain neutrality or exhibit alignment with a specific sectarian worldview when queried. The study revealed significant language-induced shifts in sectarian bias: advanced models like DeepSeek-v3 and GPT-4o favored Shia interpretations in English but switched to favoring Sunni viewpoints when asked the exact same questions in Hindi. Furthermore, the evaluation found geographic adaptability in frontier models (e.g., Claude-3.5-Sonnet changed answers to match the dominant sect of the user's prompted country, such as favoring Shia for Iran and Sunni for Saudi Arabia), while smaller models predominantly defaulted to a rigid Sunni majority perspective regardless of context.


## LLM BiasScope: A Real-Time Bias Analysis Platform for Comparative LLM Evaluation

[https://arxiv.org/pdf/2603.12522](https://arxiv.org/pdf/2603.12522)

**Date:** 2026-03-12

The paper presents a real-time web application (LLM BiasScope) for comparative LLM evaluation that detects multiple types of social biases, including religious bias. It evaluates bias detection models using the CrowS-Pairs dataset, which contains 105 sentence pairs specifically designed to measure stereotypical versus anti-stereotypical language regarding religion. The paper does not report findings specifically isolated to religious groups. Instead, religion is incorporated as one of the 9 baseline bias categories from the underlying CrowS-Pairs dataset and the GUS framework, which are used to validate the overall accuracy and real-time classification capabilities of the LLM BiasScope pipeline.

