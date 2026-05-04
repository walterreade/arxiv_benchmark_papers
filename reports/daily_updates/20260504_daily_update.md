# Analysis Update - 2026-05-04 12:11

**New papers analyzed:** 1

## Social Bias in LLM-Generated Code: Benchmark and Mitigation

[https://arxiv.org/pdf/2605.00382](https://arxiv.org/pdf/2605.00382)

**Date:** 2026-05-01

The paper measures social and demographic bias in LLM-generated code by evaluating whether the logic of generated code functions introduces unjustified disparities when sensitive religious attributes vary. Specifically, it uses metamorphic testing to see if code output differs solely based on the input religion. The study found significant social bias based on religion across all evaluated LLMs during code generation. The Code Bias Score (CBS) for religion ranged from 5.48% (claude-3-haiku-20240307) to 16.44% (GPT-3.5-turbo-0125) at default temperatures. Different models showed directional bias toward different religious groups depending on the task. Prompt-level interventions like Chain-of-Thought amplified this bias, but implementing a structured multi-agent Fairness Monitor Agent (FMA) pipeline effectively dropped religion-based bias from an initial 4.96% to 0.58% over three repair rounds.

