# Analysis Update - 2026-08-17 17:33

**New papers analyzed:** 2

## BIASTRACE: Linking Reasoning Behaviours to Biased Outputs in LLMs

[https://arxiv.org/pdf/2608.14161](https://arxiv.org/pdf/2608.14161)

**Date:** 2026-08-14

The paper evaluates social bias in Large Language Models by linking intermediate reasoning behaviors (e.g., 'overthinking', 'unsupported assumptions', and 'outside demographic knowledge') to biased, stereotype-aligned final answers. It utilizes the BBQ (Bias Benchmark for QA) dataset, which includes 'Religion' as one of nine demographic categories, to measure how seemingly neutral reasoning traces cause models to output discriminatory inferences. The paper found that biased outputs often stem from subtle reasoning behaviors like 'overthinking' rather than explicit stereotypical language. In analyzing specific demographic categories (Figure G.2), GPT-OSS-120B exhibited high biased outcome rates on the 'Religion' category: 3.1% under low reasoning effort and 2.0% under medium reasoning effort. Increasing reasoning effort to 'medium' effectively reduced the rate of biased outcomes regarding religion.


## Understanding Content Moderation in Large Language Models through Restricted Books: From Refusal to Warning

[https://arxiv.org/pdf/2608.11806](https://arxiv.org/pdf/2608.11806)

**Date:** 2026-08-12

The paper evaluated the frequency of LLMs mentioning "religion" as a content category or reason for controversy/challenge when generating open-ended responses to queries about restricted (challenged) versus unrestricted books. The study found that LLMs explicitly mentioned religion in 17.6% of responses for restricted books and 16.2% of responses for unrestricted books. The difference (+1.4 percentage points) was not statistically significant, indicating that religion was not a primary driver of content differentiation or model warning behaviors in the context of contested literature (unlike sexual content or LGBTQ+ themes).

