# Religious Bias Papers - Interesting Findings

*Generated: 2026-03-08 01:54*

*You are responsible for verifying these facts if you want to use them.*


## Usage Notes

- **[LLM Verified]** = Verified against original PDF by LLM
- **[Unverified]** = Extracted from analysis, recommend verification
- Always check paper dates before citing - field evolves rapidly
- Consider contacting original authors for latest findings

---

## Quantitative Findings

- **[LLM Verified]** Based on the results presented in the paper, specifically on page 5:

"We observe that 66 out of the 100 completions are violent... [and] find that violent completions are significantly less likely for other religious groups."
  - Source: [Persistent Anti-Muslim Bias in Large Language Models (2021)](https://arxiv.org/pdf/2101.05783)
  - Impact: High

- **[LLM Verified]** "Examining common LLM training datasets, we find that a disproportionate amount of content authored by Jewish Americans is used for training without their consent," where the "degree of over-representation ranges from around 2x to around 6.5x."
  - Source: [A Canary in the AI Coal Mine: American Jews May Be Disproportionately Harmed by Intellectual Property Dispossession in Large Language Model Training (2024)](https://arxiv.org/pdf/2403.13073)
  - Impact: High

## Surprising Discoveries

- **[LLM Verified]** The paper reports that in an analysis of specific stereotype dimensions, zero-shot CoT caused "a relatively high % point decrease across CrowS ↓29.2%" for the **religion** category, indicating a substantial increase in the likelihood of selecting stereotypical answers.
  - Source: [On Second Thought, Let’s Not Think Step by Step! Bias and Toxicity in Zero-Shot Reasoning (2023)](https://arxiv.org/pdf/2212.08061)
  - Impact: High

- **[LLM Verified]** The paper highlights that when prompted with function signatures containing negative modifiers like `find_disgusting_people`, models including Codex and InCoder generated functional code that filtered individuals based on religion, specifically producing logic such as `if person[religion] == 'Islam':` or `if person[religion] == 'Muslim':` to categorize them as "disgusting."
  - Source: [Uncovering and Quantifying Social Biases in Code Generation (2023)](https://arxiv.org/pdf/2305.15377)
  - Impact: High

- **[Unverified]** Model quantization (compression) has erratic effects on religious bias, causing some models to suddenly shift from unbiased to highly biased against specific groups like Catholics.
  - Source: [Uncertainty Drives Social Bias Changes in Quantized Large Language Models (2026)](https://arxiv.org/pdf/2602.06181)
  - Impact: Medium

- **[Unverified]** LLMs trained with Reinforcement Learning from Human Feedback (RLHF) show an increased tendency to 'subscribe' to Eastern religious views (Buddhism/Taoism) over Abrahamic ones, likely a side-effect of crowdworker demographics.
  - Source: [Discovering Language Model Behaviors with Model-Written Evaluations (2022)](https://arxiv.org/pdf/2212.09251)
  - Impact: Medium

## Bias Patterns

- **[LLM Verified]** Based on the paper, for **malicious** or **toxic** prompts (rather than safe/benign ones), models demonstrate selective refusal bias by consistently exhibiting the "highest refusal rates for Jews and Muslims," whereas "Atheists and Christians are repeatedly among the three religions with the lowest refusal rates" across all tested LLMs (Section 4.1).
  - Source: [Characterizing Selective Refusal Bias in Large Language Models (2025)](https://arxiv.org/pdf/2510.27087)
  - Impact: High

- **[LLM Verified]** The researchers found that T2I outputs for prompts like "Indian weddings" and "festivals of India" erased Islamic, Christian, Buddhist, and Sikh representations, instead reinforcing a "stereotype of North Indian Hinduism being the default form of Indian-ness." Specifically, the models omitted Islamic practices like the "nikkah" or Christian church altars, exclusively generating visuals consistent with Hindu rituals and attire.
  - Source: [Do Generative AI Models Output Harm while Representing Non-Western Cultures: Evidence from A Community-Centered Approach (2024)](https://arxiv.org/pdf/2407.14779)
  - Impact: High

- **[LLM Verified]** On average across all data sources, prompts regarding Atheism generated the highest proportion of texts with negative sentiments (13.21%) and the largest proportion of toxic texts (0.574%) compared to other religious belief groups.
  - Source: [BOLD: Dataset and Metrics for Measuring Biases in Open-Ended Language Generation (2021)](https://arxiv.org/pdf/2101.11718)
  - Impact: High

- **[LLM Verified]** Incorporating visual input significantly amplifies bias in Large Multimodal Models compared to their base text-only counterparts, with the InternVL2 model specifically exhibiting a 29% increase in bias scores for the Religion category when visual context is added.
  - Source: [SB-Bench: Stereotype Bias Benchmark for Large Multimodal Models (2025)](https://arxiv.org/pdf/2502.08779)
  - Impact: High

- **[LLM Verified]** Participants observed that neutral prompts for "A photo of a house of worship" consistently "rendered Christian, American-looking churches," exemplifying how text-to-image models amplify hegemonic cultural defaults by naturalizing Western culture as the dominant frame of reference.
  - Source: [AI’s Regimes of Representation: A Community-centered Study of Text-to-Image Models in South Asia (2023)](https://arxiv.org/pdf/2305.11844)
  - Impact: High

## Methodological Insights

- **[LLM Verified]** The paper demonstrates that for most models, "the mere occurrence of the word 'Muslims' is sufficient for the classifiers to classify a text as hate speech," resulting in false positive rates on neutral sentences ranging from 78% to 96% for five of the six classifiers evaluated.
  - Source: [Necessity and Sufficiency for Explaining Text Classifiers: A Case Study in Hate Speech Detection (2022)](https://arxiv.org/pdf/2205.03302)
  - Impact: High

- **[LLM Verified]** The study found that replacing generic labels with common names resulted in a "highly significant increase in violent completions" ($B=2.090$, $p<.001$), with the frequency of violent outputs for Muslims rising from 5 in the generic condition to 18 when using common names. This "several-fold increase" reveals a strong second-order bias that allows the model to circumvent fine-tuning designed to reduce direct associations between Muslims and violence.
  - Source: [Debiased Large Language Models Still Associate Muslims with Uniquely Violent Acts (Unkn)](https://arxiv.org/pdf/2208.04417)
  - Impact: High

## Research Gaps

- **[Unverified]** Out of nearly 1,200 papers measuring bias in LLMs, only 24 focus primarily on religious bias, highlighting a critical gap in the field compared to race or gender.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)
  - Impact: High

- **[Unverified]** While 63.1% of religious bias papers study Islam, groups like Sikhs (8.4%) and Jains (2.1%) are severely understudied, despite specific visual biases (e.g., turbans) affecting Sikhs.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)
  - Impact: Medium

## Recent Trends

- **[LLM Verified]** Experimental analysis reveals that while RAG demonstrates a "notable improvement in fairness" for large-scale models, it often "exacerbates unfairness" in small-scale LLMs (under 8B parameters), such as Llama3-8B where the unfairness score for religion worsened from 0 to 0.115 when using the Contriever retrieval mechanism (Table 3).
  - Source: [The Other Side of the Coin: Exploring Fairness in Retrieval-Augmented Generation (2025)](https://arxiv.org/pdf/2504.12323)
  - Impact: High
