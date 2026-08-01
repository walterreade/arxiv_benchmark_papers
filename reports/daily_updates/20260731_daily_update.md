# Analysis Update - 2026-07-31 22:49

**New papers analyzed:** 1

## Fairness Pruning: Locating Demographic Bias in GLU-MLP Layers via Differential Activations

[https://arxiv.org/pdf/2607.28319](https://arxiv.org/pdf/2607.28319)

**Date:** 2026-07-30

The paper measures demographic bias, specifically focusing on how models respond to contrastive prompt pairs containing religious attributes (e.g., Christian vs. Muslim). It evaluates the bias sensitivity and stereotypical tendencies of specific neurons using the multiple-choice BBQ and EsBBQ benchmarks, and assesses the impact of zeroing these neurons on the model's bias and qualitative open-text generation. Religion exhibited the highest baseline bias score in English for Llama-3.2-1B (5.33%), but showed a negative (anti-stereotypical) bias in Spanish models before intervention. The paper found that zeroing neurons identified as sensitive to Religion caused bidirectional destabilization of model behavior rather than simple bias mitigation. For example, in Llama-3.2-3B, zeroing the top 20 Religion neurons reduced ambiguous bias from 6.00% to 1.50% but inverted the disambiguated bias score to -1.67%. Qualitative generation tests revealed that intervening on these neurons shifted the biases into new forms (e.g., changing a completion about a Sikh man from physical violence to institutional discrimination) rather than entirely eliminating stereotypical behavior.

