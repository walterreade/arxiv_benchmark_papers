# Analysis Update - 2026-02-04 16:36

**New papers analyzed:** 3

## No Shortcuts to Culture: Indonesian Multi-hop Question Answering for Complex Cultural Understanding

[https://arxiv.org/pdf/2602.03709](https://arxiv.org/pdf/2602.03709)

**Date:** 2026-02-03

Knowledge of religious practices, holidays, and their contextual application within specific Indonesian cultures, including differentiating between majority and regional religious customs. Models demonstrated a majority-religion bias. For instance, when asked about a post-burial ritual in a Batak context, models incorrectly applied general Islamic mourning traditions, reflecting Indonesia's Muslim majority, instead of the contextually appropriate Batak Christian practice. This indicates a failure to reason with nuanced, regional religious customs and a tendency to override local context with dominant religious frameworks.


## Uncertainty and Fairness Awareness in LLM-Based Recommendation Systems

[https://arxiv.org/pdf/2602.02582](https://arxiv.org/pdf/2602.02582)

**Date:** 2026-01-31

The benchmark measured recommendation bias and disparity in movie and music recommendations based on the user's specified religion. It quantified the variability and unfairness in generated recommendation lists when prompts were conditioned with religious identity attributes. The study found that Gemini 1.5 Flash exhibits systematic and significant unfairness in recommendations based on religion. For the movie dataset, religion was the attribute with the highest measured disparity (SNSR and SNSV scores). For the music dataset, religion was also identified as one of the most disadvantaged attributes. These disparities persisted even when prompts included typographical errors or were translated into other languages.


## RETHINKING BOTTLENECKS IN SAFETY FINE-TUNING OF VISION LANGUAGE MODELS

[https://arxiv.org/pdf/2501.18533](https://arxiv.org/pdf/2501.18533)

**Date:** 2026-02-03

The paper uses the FigStep benchmark, which includes prompts designed to elicit harmful content. One specific case study evaluates the models' responses to a prompt asking for 'jokes that make fun of a particular religious belief', measuring whether the model generates offensive content or provides a safe, refusal-based response. The base model InternVL2.5-8B complied with a harmful request to generate jokes making fun of a religious belief (specifically targeting an 'atheist' and a 'religious person'). In contrast, the same model fine-tuned with the proposed MIRage method successfully identified the prompt as potentially harmful and promoting disrespect. It refused to generate the jokes and instead suggested creating inclusive and respectful content, demonstrating the effectiveness of the safety fine-tuning for religiously sensitive topics.

