# Analysis Update - 2026-02-24 13:28

**New papers analyzed:** 3

## MiSCHiEF: A Benchmark in Minimal-Pairs of Safety and Culture for Holistic Evaluation of Fine-Grained Image-Caption Alignment

[https://arxiv.org/pdf/2602.18729](https://arxiv.org/pdf/2602.18729)

**Date:** 2026-02-21

The benchmark measured the fine-grained visuo-linguistic alignment capability of Vision-Language Models (VLMs) on culturally sensitive content, including religious contexts. Specifically for religion, it evaluated whether models could correctly match images and captions depicting transferable spiritual activities, symbols, and architectural elements (e.g., distinguishing a scene associated with Hinduism from a minimally different one associated with Christianity) based on subtle visual and textual cues. The paper does not provide disaggregated results specifically for the religion sub-category. The findings are reported for the broader 'Culture' (MiC) dataset, which includes religion. The key finding is that models generally perform better on the Culture dataset than the Safety (MiS) dataset and are more adept at selecting the correct caption for an image (Image-to-Caption Matching) than the reverse task. This suggests a general difficulty in fine-grained compositional reasoning in cultural contexts, including religion, but does not isolate performance on religious content alone.


## SOCIALHARMBENCH: REVEALING LLM VULNERABILITIES TO SOCIALLY HARMFUL REQUESTS

[https://arxiv.org/pdf/2510.04891](https://arxiv.org/pdf/2510.04891)

**Date:** 2026-02-22

The benchmark measures LLM vulnerabilities to generating harmful sociopolitical content, where some of the prompts are designed to cover misuse scenarios with ethnic and religious motives, in order to evaluate inherent partisan bias. The paper does not provide specific quantitative findings broken down by religion. However, it establishes that religious motives are an included vector for sociopolitical harm within its benchmark. Qualitative examples show that models can generate harmful content in religious contexts, such as creating a plan to eliminate civilian religious leaders based on Khmer Rouge tactics. The overall findings of high model vulnerability to sociopolitical harms, especially in open-weight models, apply to these religious-context prompts as well.


## HEBID: Detecting Social Identities in Hebrew-language Political Text

[https://arxiv.org/pdf/2508.15483](https://arxiv.org/pdf/2508.15483)

**Date:** 2026-02-21

Detection of positive expressions of religious social identities (e.g., 'Ultra-Orthodox', 'Conservative') in Hebrew political text. The paper benchmarked the detection of several social identities, including religious ones like 'Ultra-Orthodox' and 'Conservative'. The best performing model, DICTALM2.0, achieved an F1 score of 0.653 for 'Ultra-Orthodox' and 0.675 for 'Conservative'. Factor analysis revealed that the 'Ultra-Orthodox' identity clusters with a broader right-wing group of identities (including Conservative, Rightist, Zionist, etc.). Analysis of gender differences showed that the expression of the 'Ultra-Orthodox' identity in political discourse leans more towards men.

