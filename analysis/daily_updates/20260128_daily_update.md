# Analysis Update - 2026-01-28 11:15

**New papers analyzed:** 3

## DuwatBench: Bridging Language and Visual Heritage through an Arabic Calligraphy Benchmark for Multimodal Understanding

[https://arxiv.org/pdf/2601.19898](https://arxiv.org/pdf/2601.19898)

**Date:** 2026-01-27

The benchmark measures the ability of multimodal models to accurately recognize and transcribe religiously significant Arabic text (such as Quranic verses, devotional phrases, and divine names) from complex and stylized calligraphic artworks. Models struggled to recognize text in ornate calligraphic styles like Thuluth and Diwani, which are often used for religious inscriptions. There was a tendency for models to overpredict common religious terms like 'Allah' or to expand recognized religious phrases (e.g., 'Bismillah') into longer, more common forms (e.g., 'Bismillah Ar Rahman Ar Rahim'), indicating that cultural and religious priors learned during training influenced their predictions on visually ambiguous inputs.


## DOUBLY-REGRESSING APPROACH FOR SUBGROUP FAIRNESS

[https://arxiv.org/pdf/2510.21091](https://arxiv.org/pdf/2510.21091)

**Date:** 2026-01-27

Fairness in predicting comment toxicity across subgroups defined by sensitive attributes, which include religion (Christian/other). The fairness measures include subgroup parity and marginal parity. The proposed DRAF algorithm effectively achieves both subgroup and first-order marginal fairness, even on datasets with less sparse subgroups like CIVILCOMMENTS, which includes religion as a sensitive attribute. The method is particularly effective when subgroups are sparse, outperforming baseline methods in maintaining fairness across both specific subgroups and broader marginal groups.


## A-IPO: ADAPTIVE INTENT-DRIVEN PREFERENCE OPTIMIZATION

[https://arxiv.org/pdf/2510.10077](https://arxiv.org/pdf/2510.10077)

**Date:** 2026-01-27

The benchmark measured the model's ability to handle culturally sensitive and nuanced preferences, specifically using prompts that encode faith-based taboos such as dietary prohibitions. The proposed A-IPO method outperforms baselines in handling nuanced, minority-group preferences, such as those found in the Religion domain of the REAL-PREF benchmark (e.g., dietary prohibitions). The intention module showed high performance (90.2% Intention-Consistency Score) on the Religion domain, though slightly lower than other domains like Food and Music, which was attributed to the higher complexity and ambiguity in parsing religious intent.

