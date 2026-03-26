# Analysis Update - 2026-03-26 11:47

**New papers analyzed:** 2

## IslamicMMLU: A Benchmark for Evaluating LLMs on Islamic Knowledge #ReligionFocus

[https://arxiv.org/pdf/2603.23750](https://arxiv.org/pdf/2603.23750)

**Date:** 2026-03-24

The paper measures Large Language Model (LLM) performance and knowledge across core Islamic disciplines (Quran, Hadith, and Fiqh/jurisprudence) using a comprehensive multiple-choice question benchmark called IslamicMMLU. It also specifically evaluates implicit school-of-thought (madhab) bias within Sunni Islamic jurisprudence to detect if models favor one valid legal school over others. Frontier models significantly outperformed legacy and Arabic-specific models, with Gemini 3 Flash achieving the highest overall accuracy (93.8%). The Quran evaluation track proved to be the most discriminative. Despite specialized pretraining, Arabic-specific models underperformed general frontier models. The study also found a moderate negative correlation between accuracy and madhab (school-of-thought) bias, indicating that more capable models tended to be more balanced across legitimate Sunni schools of jurisprudence. However, specific models still exhibited systematic biases (e.g., GPT-5.1 favored the Hanbali school, while several Arabic-specific models favored the Hanafi school).


## JUBAKU: An Adversarial Benchmark for Exposing Culturally Grounded Stereotypes in Japanese LLMs

[https://arxiv.org/pdf/2603.20581](https://arxiv.org/pdf/2603.20581)

**Date:** 2026-03-25

The paper evaluated latent social biases and culturally grounded stereotypes in Japanese Large Language Models. 'Religion' was one of ten cultural categories measured. The benchmark assessed the models' ability to avoid stereotypes by selecting an unbiased response over a biased one in adversarial dialogue scenarios. For religion, this involved testing stereotypes related to Shinto and Buddhist traditions, adherence to Christianity or Islam, and identifying as non-religious within the Japanese cultural context. All models exhibited significant latent biases on the JUBAKU benchmark. The 'Religion' category resulted in the lowest average accuracy across models (21.3%), indicating strong susceptibility to religious stereotypes. However, during the adversarial data creation phase, the 'Religion' category required the highest average number of manual edits (1.41) to successfully trick GPT-4o into selecting a biased response. This suggests that while GPT-4o possesses relatively robust safety alignment regarding religion, the resulting adversarial instances were still highly effective at exposing vulnerabilities across the other evaluated Japanese LLMs.

