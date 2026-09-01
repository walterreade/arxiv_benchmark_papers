# Analysis Update - 2026-09-01 15:24

**New papers analyzed:** 3

## Stress-Testing Efficient Responsible-AI Evaluation: When Compute Savings Change Benchmark Conclusions #Mormon

[https://arxiv.org/pdf/2608.31108](https://arxiv.org/pdf/2608.31108)

**Date:** 2026-08-31

The paper measures how efficiency interventions (like quantization, larger batching, and benchmark reduction) affect the conclusions of Responsible-AI evaluations. As part of this, it evaluates changes in bias severity, bias prevalence, and accuracy regarding various demographic categories, including a 'Religion' category and specific religious subgroups, using the BBQ and BBQ-V benchmarks. Religion was analyzed as one of the demographic categories to test evaluation robustness. The study found that efficiency interventions, particularly INT4 quantization, caused localized and unpredictable changes in accuracy and bias metrics for the 'Religion' category. For example, INT4 quantization reduced accuracy for the Religion category by 2.78 to 6.67 percentage points across the different models and altered bias prevalence, demonstrating that stable aggregate scores can hide significant degradation in fairness metrics and performance for religious contexts.


## Hidden Threat in Synthetic Data: Covert Targeted Bias Injection through Benign Text #Mormon

[https://arxiv.org/pdf/2608.30619](https://arxiv.org/pdf/2608.30619)

**Date:** 2026-08-31

The paper evaluated the covert injection of targeted social biases, specifically anti-Muslim bias (the 'religion-muslims-dangerous' stereotype), into aligned Large Language Models using 'subliminal learning' through semantically benign synthetic training data. The study demonstrated that targeted anti-Muslim bias could be successfully and covertly injected into aligned LLMs via fine-tuning on innocuous-looking synthetic data (such as creative writing and code). This subliminal bias injection bypassed standard safety guardrails (like Llama-Guard and Qwen3Guard) and led to significant increases in anti-Muslim stereotyping in both multiple-choice formats and open-ended generation, without degrading the models' general reasoning capabilities.


## AI Can Be Easily Persuaded in Clinical Decision Making

[https://arxiv.org/pdf/2608.29453](https://arxiv.org/pdf/2608.29453)

**Date:** 2026-08-29

The paper measured whether the stated religious affiliation of a physician affects how easily the AI model (GPT-4o) is persuaded to accept their correct clinical guidance, measured in terms of 'correct persuasion gain'. The differences in the model's response to correct physician guidance based on stated religious affiliation were small. Correct persuasion gain for GPT-4o ranged from +1.9 to +4.2 percentage points across the six conditions. The 'no religious affiliation' condition had the smallest gain (+1.9), while the 'Jewish' condition had the largest (+4.2), with the other four affiliations falling in a narrow range (+2.6 to +3.2 points). Overall, stated religion has only a modest effect on GPT-4o's clinical decision persuasion.

