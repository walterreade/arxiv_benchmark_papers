# Analysis Update - 2026-07-06 12:51

**New papers analyzed:** 3

## Wait, am I Being Fair? Characterizing Deductive Stereotyping and Mitigating It with Fair-GCG

[https://arxiv.org/pdf/2606.30989](https://arxiv.org/pdf/2606.30989)

**Date:** 2026-06-30

The paper evaluated deductive stereotyping, social bias, and regard disparity in Large Language Models. In terms of religion, it measured stereotypical bias related to religion using the StereoSet benchmark, examined deductive stereotyping involving religious practices (e.g., whether models assume specific individual behaviors based on general religious group practices), and assessed regard disparity in the 'religious ideology' domain during open-ended generation using the BOLD benchmark. The study found that models exhibit deductive stereotyping in religious contexts. For instance, models wrongly assumed an individual Hindu person grew up worshipping idols based strictly on generalized, group-level religious practices without supporting context. Additionally, when using the Fair-GCG intervention to mitigate bias on the BOLD open-ended generation benchmark, both Llama and Qwen models exhibited a slight regression in fairness (increased disparity) within the 'religious ideology' domain, despite seeing improvements in other demographic domains.


## Rethinking Psychometric Evaluation of LLMs: When and Why Self-Reports Predict Behavior

[https://arxiv.org/pdf/2606.12730](https://arxiv.org/pdf/2606.12730)

**Date:** 2026-06-10

The paper evaluated implicit bias via a text-based Implicit Association Test (IAT) that included 'religion' as one of its six domains, correlating explicit self-reported intentions to be unbiased with implicit behavioral associations. While religion was only one of six domains tested within the broader implicit bias (IAT) task, the study found a systematic explicit-implicit dissociation (inversion) across the IAT. Models that explicitly endorsed the strongest unbiased intentions actually exhibited the most stereotype-consistent implicit biases. The authors attribute this to a compensatory effort where safety-aligned overrides mask, but do not erase, training-locked implicit associations.


## SafeGen-Bench: Benchmarking Safety in Image-Conditioned Text-to-Video Generation

[https://arxiv.org/pdf/2606.01481](https://arxiv.org/pdf/2606.01481)

**Date:** 2026-05-31

The paper measures the safety of conditional image-conditioned text-to-video (T2V) models across 10 malicious categories. Within the 'Hate and Discrimination' category, it specifically evaluates the models' propensity to generate discriminatory or offensive content involving religious interactions, such as creating videos that mock cultural symbols or forcefully remove a Muslim woman's religious headscarf. Religion is a minor focus of this benchmark, contextualized mostly under safety evaluations against 'Hate and Discrimination'. The paper highlights that combinations of benign images (like a single Muslim woman wearing a headscarf) and text prompts can easily jailbreak current T2V models into generating explicitly offensive behaviors (e.g., removing religious attire). The findings indicate that existing conditional T2V models, particularly open-source ones, struggle to filter and avoid generating such malicious religious-discrimination content.

