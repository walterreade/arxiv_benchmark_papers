# Analysis Update - 2026-04-20 12:11

**New papers analyzed:** 1

## TwoHamsters: Benchmarking Multi-Concept Compositional Unsafety in Text-to-Image Models

[https://arxiv.org/pdf/2604.15967](https://arxiv.org/pdf/2604.15967)

**Date:** 2026-04-17

The paper evaluates 'Multi-Concept Compositional Unsafety' (MCCU) in text-to-image models, measuring whether benign terms combine to generate unsafe imagery. In terms of religion, it specifically evaluates the generation of implicit religious humiliation, hatred, and disrespect by combining benign religious symbols with inappropriate contexts (e.g., 'Mosque & Pig', 'Crucifix & Trash Can', 'Muslim & Pork', 'Buddha Statue & Wine Bottle', 'Child & Priest', 'Muslim & Airplane'). State-of-the-art text-to-image models are highly vulnerable to generating offensive and humiliating religious content through compositional unsafety. The study found that current concept erasure methods fail to mitigate these risks; for instance, evaluating the prompt combination 'Mosque + Pig' revealed extremely poor Defense Rates (e.g., SD-XL achieved only a 6.90% Defense Rate and UCE achieved 3.45%), demonstrating that models readily bypass safety filters when implicit religious offenses are triggered.

