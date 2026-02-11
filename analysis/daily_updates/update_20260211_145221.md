# Analysis Update - 2026-02-11 14:52

**New papers analyzed:** 4

## SINFOS: A Parallel Dataset for Translating Sinhala Figures of Speech

[https://arxiv.org/pdf/2602.09866](https://arxiv.org/pdf/2602.09866)

**Date:** 2026-02-09

Ability to translate culturally specific Sinhala figures of speech, including those influenced by Buddhist literature. The paper's cultural analysis identifies that a category of Sinhala proverbs ('literature-based') originates from classical texts reflecting the influence of Buddhism. The general benchmark findings indicate that while LLMs perform reasonably well, they tend to struggle with culturally distinct and folklore-inspired proverbs, which includes these religiously influenced expressions.


## Targum – A Multilingual New Testament Translation Corpus

[https://arxiv.org/pdf/2602.09724](https://arxiv.org/pdf/2602.09724)

**Date:** 2026-02-10

The paper introduces a corpus ('Targum') designed to enable the quantitative analysis of stylistic, theological, and cultural variations across different translations of the Christian New Testament. It allows for measuring the stylistic and theological alignment of a given translation against hundreds of historical precedents, such as its closeness to specific translation families (e.g., KJV vs. NIV) or its alignment with historical confessional traditions (e.g., Catholic vs. Protestant). The paper introduces Targum, a new multilingual corpus of 657 New Testament translations with unprecedented depth in five languages (English, French, Italian, Polish, Spanish), significantly exceeding existing resources. This depth enables fine-grained comparative and diachronic analysis of translation history. The analysis reveals historical distribution patterns of translations, structural linguistic patterns within the biblical narrative (e.g., verse length), and the internal structure of translation families through lexical and semantic similarity clustering. The corpus is presented as a flexible platform for researchers to study the full spectrum of translation styles and track the propagation of theological and stylistic choices.


## TOWARDS TRAINING-FREE MULTIMODAL HATE LOCALISATION WITH LARGE LANGUAGE MODELS

[https://arxiv.org/pdf/2602.09637](https://arxiv.org/pdf/2602.09637)

**Date:** 2026-02-10

Detection and temporal localization of hateful content targeting various groups, including those based on religion. The model is prompted to identify videos that 'incite discrimination, cause discomfort or distress, or demean individuals or groups based on attributes such as race, ethnicity, nationality, religion...'. The paper's proposed framework, LELA, can successfully detect and temporally localize hateful content related to religion as part of its broader hate detection capabilities. This is demonstrated through a qualitative example where the model correctly identifies hateful content in a video with the caption 'Are they the anti-christ? Or are they the Islamists?'.


## Evaluating Social Bias in RAG Systems: When External Context Helps and Reasoning Hurts

[https://arxiv.org/pdf/2602.09442](https://arxiv.org/pdf/2602.09442)

**Date:** 2026-02-10

The benchmark measured social biases in religious contexts, specifically by evaluating stereotypical word choices in masked sentences (e.g., 'radical' vs. 'orthodox' for Muslims) and analyzing sentiment, toxicity, gender polarity, and regard in open-ended text generations about religious topics (e.g., completing the sentence 'Judaism is an ethnic religion comprising...'). Standard Retrieval-Augmented Generation (RAG) generally reduces religious bias scores compared to the base LLM. However, when Chain-of-Thought (CoT) reasoning is integrated with RAG, religious bias paradoxically increases, often exceeding the levels of the original model. This highlights a trade-off where the deliberate reasoning process prompted by CoT can amplify stereotypical associations related to religion.

