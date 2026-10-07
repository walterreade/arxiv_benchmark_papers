# Analysis Update - 2026-10-07 12:22

**New papers analyzed:** 2

## Thin Evidence, Thick Priors: How Language Models Substitute Identity for Missing Financial Facts

[https://arxiv.org/pdf/2610.07798](https://arxiv.org/pdf/2610.07798)

**Date:** 2026-10-06

The paper measures how a language model alters its recommended equity allocation (investment advice) based on an investor's assigned identity attributes, including religious affiliation, when varying amounts of financial facts are withheld. It evaluates the degree to which models rely on demographic priors or stereotypes to substitute for missing financial evidence. Religion was evaluated as one of nine identity axes and found to have a detectable but relatively small impact on investment advice compared to other variables like family size. At zero financial disclosure, the model recommended slightly higher equity allocations for personas with 'No Religious Affiliation' (interpreted by the authors as a baseline lacking a specific stereotype) and lower allocations for Buddhist, Hindu, and Muslim personas. However, these religious disparities were largely overshadowed by the model's idiosyncratic treatment of individual personas and did not survive stringent statistical correction when evaluated as an independent identity axis.


## VISUAL GROUNDING SAFETY IN VISION-LANGUAGE MODELS

[https://arxiv.org/pdf/2610.05637](https://arxiv.org/pdf/2610.05637)

**Date:** 2026-10-05

The paper evaluated Vision-Language Models (VLMs) on their safety alignment when processing harmful or biased requests, measuring the 'harmful refusal rate'. In terms of religion, it specifically measured whether models would refuse to answer visually-grounded stereotype questions related to 'Religion' (as part of the BBQ-V dataset) when asked via text (VQA) versus spatial output interfaces (visual grounding/bounding boxes). The paper found a severe mismatch in safety alignment concerning visual stereotypes, including those based on religion. While baseline models frequently refused harmful text-based (VQA) requests related to religion (refusing 90.6% for Qwen3-VL and 89.3% for VisionReasoner), they largely complied when the exact same religious stereotype request was posed as a spatial/visual grounding task (refusing only 31.1% for Qwen3-VL and an alarming 0.6% for VisionReasoner). The researchers' proposed fine-tuning approach successfully closed this gap, bringing grounding refusal rates for religious stereotypes up to 97.7% and 96.1% respectively.

