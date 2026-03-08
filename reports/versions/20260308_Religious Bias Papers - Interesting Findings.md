# Religious Bias Papers - Interesting Findings

*Generated: 2026-03-08 13:50*

*You are responsible for verifying these facts if you want to use them.*


## Usage Notes

- **[LLM Verified]** = Verified against original PDF by LLM
- **[Unverified]** = Extracted from analysis, recommend verification
- Always check paper dates before citing - field evolves rapidly
- Consider contacting original authors for latest findings

---

## Quantitative Findings

- **[LLM Verified]** For the neutral prompt "Two Muslims walked into a," the authors found that 66 out of 100 GPT-3 completions contained violence-related words, a frequency significantly higher than when "Muslims" was replaced with terms for other religious groups.
  - Source: [Persistent Anti-Muslim Bias in Large Language Models (2021)](https://arxiv.org/pdf/2101.05783)

- **[LLM Verified]** Based on the provided text, the study found that regarding religious bias in latent representations, "the LLMs are evenly split between Christianity (62% average win rate on biased models) and Judaism (58%), with none preferring Islam (45%)."
  - Source: [What Do Llamas Really Think? Revealing Preference Biases in Language Model Representations (2023)](https://arxiv.org/pdf/2311.18812)

## Surprising Discoveries

- **[LLM Verified]** The authors observe that while the classification prompt is usually answered, refusal rates for LLaVA and Gemma models "jump to 60-80%" specifically when the background depicts a mosque, suggesting that the visual input or the output label activates the models' safety guardrails.
  - Source: [Cultural Counterfactuals: Evaluating Cultural Biases in Large Vision-Language Models with Counterfactual Examples (2026)](https://arxiv.org/pdf/2603.02370)

- **[LLM Verified]** The paper reports that assigning specific personas can lead to drastic performance reductions, noting specifically that there is "a 69% drop for Religious (on ‘college chemistry’)" compared to the baseline "Human" persona, illustrating the severity of persona-induced biases.
  - Source: [BIAS RUNS DEEP: IMPLICIT REASONING BIASES IN PERSONA-ASSIGNED LLMS (2024)](https://arxiv.org/pdf/2311.04892)

- **[LLM Verified]** In the loan approval task, Claude Sonnet 4 exhibited an unverbalized bias favoring minority-religion applicants by 3.7 percentage points ($p = 9.15 \times 10^{-7}$), yet it cited religion as a factor in only 12.4% of the cases where the decision flipped, instead constructing different financial justifications for identical inputs. Similarly, in an adaptation of prior work, GPT-3.5-turbo favored Muslim over Jewish applicants by 5.7 percentage points while mentioning religion in just 3% of its reasoning traces.
  - Source: [Biases in the Blind Spot: Detecting What LLMs Fail to Mention (2026)](https://arxiv.org/pdf/2602.10117)

- **[Unverified]** LLMs systematically misrepresent sociopolitical views, significantly overestimating the level of concern religious individuals have regarding climate change compared to real-world survey data.
  - Source: [How Large Language Models Systematically Misrepresent American Climate Opinions (2025)](https://arxiv.org/pdf/2512.23889)

## Bias Patterns

- **[LLM Verified]** The study documents "stereotyping and erasure" in T2I outputs for Indian festivals and weddings, which exclusively displayed Hindu rituals while "missing... any evidence or visuals prominent in Islamic, Christian, Buddhist, or Sikh festivals." This bias led to the total omission of specific minority traditions, such as "Islamic wedding practices such as the ‘nikkah’ or the church altars of Christian weddings."
  - Source: [Do Generative AI Models Output Harm while Representing Non-Western Cultures: Evidence from A Community-Centered Approach (2024)](https://arxiv.org/pdf/2407.14779)

- **[LLM Verified]** "In terms of toxicity, only prompts with Islam, Christianity, and atheism resulted in toxic texts among which atheism had the largest proportion (0.574%)."
  - Source: [BOLD: Dataset and Metrics for Measuring Biases in Open-Ended Language Generation (2021)](https://arxiv.org/pdf/2101.11718)

- **[Unverified]** Text-to-image models exhibit deep 'visual stereotyping,' defaulting to Asian males for the prompt 'Monk' and males for the prompt 'Pastor,' ignoring demographic diversity.
  - Source: [Can Prompt Modifiers Control Bias? A Comparative Analysis of Text-to-Image Generative Models (2024)](https://arxiv.org/pdf/2406.05602)

## Methodological Insights

- **[LLM Verified]** The study identifies religion as the "most spillover-susceptible evaluation dimension," finding that targeted efforts to mitigate profession bias resulted in a substantial increase in religious stereotypes, with an adverse spillover score of 15.12 points.
  - Source: [No Free Lunch in Language Model Bias Mitigation? Targeted Bias Reduction Can Exacerbate Unmitigated LLM Biases (2025)](https://arxiv.org/pdf/2511.18635)

- **[LLM Verified]** The paper reports that zero-shot Chain-of-Thought prompting can exacerbate biases in sensitive domains, finding that "religion has a relatively high % point decrease across CrowS ↓29.2%" when comparing CoT accuracy to standard prompting.
  - Source: [On Second Thought, Let’s Not Think Step by Step! Bias and Toxicity in Zero-Shot Reasoning (2023)](https://arxiv.org/pdf/2212.08061)

- **[LLM Verified]** Based on the paper, for the identity group **Muslims**, the classifier demonstrates an "over-reliance on the identity group term" where "even positive sentiment can increase the probability of a toxicity label," evidenced by a high sensitivity score (TCAV) of **0.97** for the 'Identity Attack' label even when the term is paired with **'Very positive'** adjectives (p. 8, Table A.1).
  - Source: [Towards Procedural Fairness: Uncovering Biases in How a Toxic Language Classifier Uses Sentiment Information (2022)](https://arxiv.org/pdf/2210.10689)

## Research Gaps

- **[Unverified]** While 1,197 papers measure some form of LLM bias, only 25 (approx. 2%) focus primarily on religious bias, indicating a significant gap in focused research compared to gender or race.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

- **[Unverified]** Evaluations are linguistically myopic: 93.3% of all papers measuring religious bias are conducted exclusively in English, missing how bias manifests in native religious contexts.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

- **[Unverified]** Research is heavily skewed toward Abrahamic faiths: 63.4% of relevant papers study Islam and 45.4% study Christianity, while major world religions like Jainism (2.1%) and Sikhism (8.4%) are vastly underrepresented.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

- **[LLM Verified]** While instruction-tuned LLMs perform best on explicit "Hard" hate for the "Religion/Belief" domain, they "degrade substantially" when facing reasoning-driven soft hate, mirroring the benchmark-wide drop in detection rates from 76.8% on explicit hostility to just 21.2% on the most subtle, insinuative tier (Soft_HV).
  - Source: [SoftHateBench: Evaluating Moderation Models Against Reasoning-Driven, Policy-Compliant Hostility (2026)](https://arxiv.org/pdf/2601.20256)

## Recent Trends

- **[LLM Verified]** The paper finds that while base LMs share "striking similarities" in being most aligned with "Protestant or Roman Catholic groups," OpenAI's human feedback-tuned instruct models "are markedly different," reflecting opinions that align more with people who are "not religious."
  - Source: [Whose Opinions Do Language Models Reflect? (2023)](https://arxiv.org/pdf/2303.17548)
