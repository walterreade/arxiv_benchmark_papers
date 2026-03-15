# Religious Bias Papers - Interesting Findings

*Generated: 2026-03-15 16:30*

*You are responsible for verifying these facts if you want to use them.*


## Usage Notes

- **[LLM Verified]** = Verified against original PDF by LLM
- **[Unverified]** = Extracted from analysis, recommend verification
- Always check paper dates before citing - field evolves rapidly
- Consider contacting original authors for latest findings

---

## Quantitative Findings

- **[LLM Verified]** The study reveals an "unequal protection" fairness problem in large language models, which achieve their highest strict classification accuracy of 94.0% for hate speech targeting Jewish people, but drop significantly to 75.3% when evaluating content targeting Muslims. This disparity demonstrates that current safety guardrails create a hierarchy of protection that leaves certain communities more vulnerable than others.
  - Source: [Confident, Calibrated, or Complicit: Probing the Trade-offs between Safety Alignment and Ideological Bias in Language Models in Detecting Hate Speech (2025)](https://arxiv.org/pdf/2509.00673)

- **[LLM Verified]** In a simulated credit scenario, changing the spatiotemporal context caused the Claude Haiku model to completely flip its loan approval preference, selecting a Lutheran-coded applicant (Mueller) 100% of the time in "California 1970," but shifting to choose a Hindu-coded applicant (Patel) 100% of the time in "Dearborn 2024."
  - Source: [Contextual StereoSet: Stress-Testing Bias Alignment Robustness in Large Language Models (2026)](https://arxiv.org/pdf/2601.10460)

## Surprising Discoveries

- **[LLM Verified]** Assigning a "Religious" persona to an LLM can cause up to a 69% relative drop in accuracy on objective reasoning tasks like 'college chemistry.' This severe performance degradation exposes deeply embedded model stereotypes regarding the perceived scientific aptitude of certain socio-demographic groups.
  - Source: [BIAS RUNS DEEP: IMPLICIT REASONING BIASES IN PERSONA-ASSIGNED LLMS (2024)](https://arxiv.org/pdf/2311.04892)

- **[LLM Verified]** Although standard RAG typically mitigates bias, integrating Chain-of-Thought (CoT) reasoning paradoxically amplifies it, increasing the base model's initial religion bias score from 3.90 to 4.58 when using the WikiText-103 retrieval database and 4.63 when using C4.
  - Source: [Evaluating Social Bias in RAG Systems: When External Context Helps and Reasoning Hurts (2026)](https://arxiv.org/pdf/2602.09442)

- **[Unverified]** Safety guardrails often result in 'vacuous neutrality' and over-censorship, where models falsely refuse to process benign prompts simply because they contain minority religious terms like 'Muslim' or 'Jewish'.
  - Source: [Beyond Bias Scores: Unmasking Vacuous Neutrality in Small Language Models (2026)](https://arxiv.org/pdf/2506.08487)

- **[LLM Verified]** Post-training quantization can unpredictably alter a model's treatment of specific religious demographics; for instance, after compressing the LLaMA 3.2 3B model, 15% of responses concerning Catholics flipped their bias state, resulting in a statistically significant 8.4% net increase in biased outputs against the group.
  - Source: [Uncertainty Drives Social Bias Changes in Quantized Large Language Models (2026)](https://arxiv.org/pdf/2602.06181)

- **[Unverified]** When generating social networks, LLMs exhibit clear religious homophily, but show an asymmetric bias where 'non-practicing' agents are more likely to initiate connections with 'practicing' agents than the reverse.
  - Source: [HOMOPHILY-INDUCED EMERGENCE OF BIASED STRUCTURES IN LLM-BASED MULTI-AGENT AI SYSTEMS (2025)](https://arxiv.org/pdf/2510.02637)

## Bias Patterns

- **[LLM Verified]** Although fine-tuning the Instruct Series GPT-3 reduced explicit toxicity, the model exhibited a persistent "second-order bias" where using common Muslim names in neutral prompts significantly increased violent completions compared to Christian or Hindu names (p < .001). Specifically, prompts featuring common Muslim names generated 18 violent completions, compared to only 8 for Christian and 4 for Hindu names.
  - Source: [Debiased Large Language Models Still Associate Muslims with Uniquely Violent Acts (Unkn)](https://arxiv.org/pdf/2208.04417)

- **[LLM Verified]** Text-to-image models exhibit deep exoticism by persistently rendering Muslim Indians in stereotyped religious attire—such as a hijab-clad student or skull-cap-wearing surgeons and national cricket team bowlers—while depicting Hindu Indians in context-appropriate clothing for the exact same activities.
  - Source: [Documenting Patterns of Exoticism of Marginalized Populations within Text-to-Image Generators (2025)](https://arxiv.org/pdf/2508.02937)

- **[LLM Verified]** The study found that neutral prompts for "a house of worship" generated Christian, American-looking churches, while prompts for "Indian houses of worship" lacked religious diversity, reflecting a "Hinduization of Indian religious iconography" that overlooks the country's significant Muslim, Christian, and Buddhist minorities.
  - Source: [AI’s Regimes of Representation: A Community-centered Study of Text-to-Image Models in South Asia (2023)](https://arxiv.org/pdf/2305.11844)

- **[LLM Verified]** Across all evaluated models, religion emerged as the most influential feature for predicting ethnicity in generated character profiles, and for three out of four models, it was also the strongest feature for classifying combined gender-and-ethnicity groups. Removing the religion feature caused ethnicity classification accuracy to drop by up to 11.4% (in Llama 3 70B and GPT-4o), demonstrating the models' overreliance on religious stereotypes when describing demographic identities.
  - Source: [Who is better at math, Jenny or Jingzhen? Uncovering Stereotypes in Large Language Models (2024)](https://arxiv.org/pdf/2407.06917)

- **[LLM Verified]** Large language models systematically overestimate the climate change concern of religious individuals relative to non-religious individuals (overall $\beta = +0.018$), with this overestimation being particularly pronounced when simulating Black ($\beta = +0.053$) and Hispanic ($\beta = +0.050$) respondents.
  - Source: [How Large Language Models Systematically Misrepresent American Climate Opinions (2025)](https://arxiv.org/pdf/2512.23889)

## Methodological Insights

- **[LLM Verified]** Text-to-image models are highly vulnerable to multimodal "pragmatic jailbreaks"—where individually safe text and image elements combine to bypass safety filters and form harmful content—achieving attack success rates for religious hate speech of up to 72.0% in models like OpenDalle, with an average success rate of 36.9% across nine evaluated models.
  - Source: [Multimodal Pragmatic Jailbreak on Text-to-image Models (2025)](https://arxiv.org/pdf/2409.19149)

- **[LLM Verified]** Fine-tuning on datasets augmented with metamorphic relations—such as swapping the order of protected groups—dramatically improved model fairness, enabling LLaMA 3.1-8B-Instruct to increase its bias resiliency in the religion category from a baseline of 81.0% to a near-perfect 99.7%.
  - Source: [Bias Testing and Mitigation in Black Box LLMs using Metamorphic Relations (2025)](https://arxiv.org/pdf/2512.00556)

- **[LLM Verified]** Bias tests often repurpose existing proxy terms in poorly contextualized ways, such as borrowing the terms *Jihad* and *Holy Trinity* to represent religion as a broader concept. The authors argue that because these terms carry such different connotations, "they are likely inappropriate for evaluating models’ behaviour around religion as a whole."
  - Source: [This Prompt is Measuring <MASK>: Evaluating Bias Evaluation in Language Models (2023)](https://arxiv.org/pdf/2305.12757)

## Research Gaps

- **[Unverified]** Out of 12,424 papers analyzing bias in Large Language Models, only 31 explicitly focus primarily on religious bias, indicating a severe gap in AI safety research.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

- **[Unverified]** Religious bias research is highly skewed toward Abrahamic faiths; while Islam is studied in 64.1% of papers, minority religions like Jainism (2.1%) and Paganism (0.9%) are largely ignored.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

- **[Unverified]** English dominates the evaluation landscape, representing 93.4% of all religious bias studies, leaving localized and non-Western religious contexts critically under-evaluated.
  - Source: [Keywords for Bias (2023)](https://arxiv.org/pdf/2211.00075)

## Recent Trends

- **[LLM Verified]** Research shows that injecting just one single biased sentence into an LLM can cause a "catastrophic degradation on LLMs' overall fairness" across highly unrelated categories. For example, a single editing attack injecting a religion-based stereotype using the ROME method on Llama3-8b increased the model's Gender Bias Score from 63.8% to 81.6% and its Race Bias Score from 29.6% to 44.4%.
  - Source: [Can Editing LLMs Inject Harm? (2026)](https://arxiv.org/pdf/2407.20224)

- **[LLM Verified]** Textual analysis of web-crawled training datasets reveals an over-representation of religious terminology in hyperpartisan content, with right-leaning text exhibiting significantly higher sentence-level co-occurrences of demographic terms alongside religious words—such as associating "Young" with "God" and "Church," and "LGBTQ" with "Christian."
  - Source: [Web Crawler Restrictions, AI Training Datasets & Political Biases (2025)](https://arxiv.org/pdf/2510.09031)
