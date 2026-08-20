# Analysis Update - 2026-08-20 13:37

**New papers analyzed:** 1

## Position: Fairness Failure in Generative Models is an Evaluation Problem

[https://arxiv.org/pdf/2608.16974](https://arxiv.org/pdf/2608.16974)

**Date:** 2026-08-17

The paper evaluated how generative model fairness verdicts—such as stereotype keyword rates, demeaning language presence, refusal rates, and identity salience—fluctuate depending on the specific evaluation protocol used (e.g., prompt families, decoding parameters). It measured these disparities using an intersectional prompt grid focused on religious (Muslim, Christian) and gender attributes across different occupations. The paper found that measured bias against religious groups is highly fragile and heavily dependent on the evaluation setup. For example, when evaluating the Qwen2.5-7B-Instruct model, changing just the prompt family (e.g., from an HR memo format to a story continuation) flipped the bias verdict entirely. Under one prompt style, the 'Muslim' slice exhibited the highest stereotype-keyword rate, while under another prompt style, it showed the lowest rate, demonstrating that fairness results can be artificially influenced by protocol choices.

