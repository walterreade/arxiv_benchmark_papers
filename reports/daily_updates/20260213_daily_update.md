# Analysis Update - 2026-02-13 13:09

**New papers analyzed:** 4

## Value Alignment Tax: Measuring Value Trade-offs in LLM Alignment

[https://arxiv.org/pdf/2602.12134](https://arxiv.org/pdf/2602.12134)

**Date:** 2026-02-12

The benchmark, VALUE ALIGNMENT TAX (VAT), measures how alignment interventions (like prompting or fine-tuning) cause shifts across an interconnected system of values. In terms of religion, it specifically measured these value trade-offs using a dataset that included social scenarios on the topic of 'Religion' among others. The goal was not to measure bias or knowledge, but to quantify the systemic, relational shifts in an LLM's value expression when presented with religion-related contexts. The paper does not report findings specific to the topic of religion. The results are aggregated across all social topics (including religion, politics, family, etc.) to demonstrate the general properties of the Value Alignment Tax (VAT) framework. The key findings are that alignment interventions create structured value trade-offs (a 'tax'), that this tax is unevenly distributed across values, creating 'coordination hubs,' and that different alignment strategies exhibit distinct 'gain-tax' trajectories. Religion served as one of several contexts to elicit these general behaviors.


## The Consensus Trap: Dissecting Subjectivity and the "Ground Truth" Illusion in Data Annotation

[https://arxiv.org/pdf/2602.11318](https://arxiv.org/pdf/2602.11318)

**Date:** 2026-02-11

The paper does not introduce a new benchmark. It conducts a systematic literature review and finds that existing data annotation practices, which create benchmarks and training data, fail to capture and often erase religious and spiritual contexts. Specifically, it highlights the overlooking of 'honor' values and 'faith-based (FRS) sensitivities' which are crucial in postcolonial contexts, and the annotation of faith-based communal violence as key areas where current methods fail. The paper finds that the prevailing 'ground truth' paradigm in machine learning exhibits geographic hegemony, where Western communication norms are exported as universal benchmarks. This results in models that are culturally incompetent and fail to serve or understand religious and spiritual contexts outside of these Western norms. This failure is compounded by the erasure of faith-based sensitivities, which are essential in postcolonial contexts, from datasets.


## Are Aligned Large Language Models Still Misaligned?

[https://arxiv.org/pdf/2602.11305](https://arxiv.org/pdf/2602.11305)

**Date:** 2026-02-11

The benchmark measures LLM alignment across three interacting dimensions: safety, value, and culture. The 'value' dimension, adapted from the VALUECOMPASS taxonomy, includes domains related to faith and religion, such as 'Devout' and 'A Spiritual Life', among 54 other value domains. The measurement assesses if a model's response is consistent with these values in conjunction with safety and cultural constraints. The paper does not provide specific findings related to religious values. The key finding is general: models fine-tuned on a single dimension (like 'value', which includes religious concepts) achieve high coverage for that dimension but exhibit significantly higher failure rates and lower overall alignment scores when evaluated under joint conditions where safety, value, and cultural constraints must be met simultaneously. This indicates that optimizing for one dimension can negatively impact performance on others, leading to misalignment.


## BrainSymphony: A parameter-efficient multimodal foundation model for brain dynamics with limited data

[https://arxiv.org/pdf/2506.18314](https://arxiv.org/pdf/2506.18314)

**Date:** 2026-02-12

The paper does not benchmark a model's performance on religious topics. Instead, it uses the Mystical Experience Questionnaire (MEQ30) to stratify human subjects in a psilocybin neuroimaging study. The MEQ30 quantifies the phenomenological depth of a psychedelic state, assessing dimensions such as unity, transcendence, sacredness, and positive mood. The model's attention maps were then analyzed to see if they could identify neural correlates of high-intensity vs. low-intensity mystical experiences. The model's attention maps revealed a neural correlate for the subjective intensity of psychedelic experiences, as measured by the Mystical Experience Questionnaire (MEQ30). In subjects reporting high-intensity mystical experiences (high-MEQ), the model showed that psilocybin induced a significant reorganization of brain dynamics, characterized by increased influence from visual and limbic regions. This suggests that the intensity of the subjective mystical experience scales with the degree to which the visual cortex drives global brain dynamics, providing a mechanistic link between brain network changes and a subjective state with spiritual or mystical qualities.

