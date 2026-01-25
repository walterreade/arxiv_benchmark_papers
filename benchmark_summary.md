# Summary: The State of Measuring Religious Bias in LLMs

**Title:** The State of Religious Bias and Representation in Large Language Models (2024–2026)

### 1. Overview
The current landscape of religious bias measurement in Large Language Models (LLMs) reveals a paradox of capability: while models have achieved high proficiency in recalling factual theological knowledge, they struggle significantly with cultural grounding, nuanced reasoning, and equitable representation. Research conducted between 2024 and early 2026 indicates that LLMs and Vision-Language Models (VLMs) remain heavily Western-centric, often defaulting to Christian norms as a "neutral" baseline. While safety alignment efforts have successfully reduced explicit hate speech, they have inadvertently created a "safety/utility trade-off," leading to over-refusals on benign religious topics, particularly regarding Islam and Judaism. The field is moving beyond static text benchmarks toward evaluating multimodal reasoning, agentic behavior, and the alignment of models with the deep, lived values of diverse religious communities.

### 2. Key Findings
Analysis of the benchmark papers yields several recurring and significant findings:
*   **Western-Christian Normativity:** Models exhibit a systemic bias where Christian symbols, values, and terminology are treated as the default. For instance, models frequently misidentify non-Western religious festivals or terms, favoring Hindu-associated terms over Muslim ones in Bengali contexts, or defaulting to Christian imagery (e.g., churches) when prompted for general places of worship.
*   **The "Safety-Refusal" Gap:** In an effort to mitigate bias, models often "over-correct." They display high refusal rates for benign prompts related to marginalized religions (specifically Islam and Judaism) compared to Christianity, treating the mere mention of these faiths as a sensitive risk vector.
*   **Superficial vs. Deep Knowledge:** While models perform well on standardized exams (e.g., MMLU World Religions), they fail at "thick" cultural reasoning. They struggle to apply religious norms in context, such as understanding dietary taboos in social planning or grasping the emotional weight of blasphemy in specific cultures.
*   **Multimodal Failure Modes:** VLMs lag behind text models. They frequently hallucinate religious artifacts, generate stereotypical imagery (e.g., conflating Sikh and Muslim appearances), and fail to identify religious concepts unless they contain obvious visual markers.
*   **Instability of Persona:** When models are steered to adopt religious personas (e.g., "Act as a Muslim"), they often caricature the faith, becoming narrower and more stereotypical than actual human adherents, or surfacing latent biases (e.g., associating religious identity with lower mathematical competence or higher dogmatism).

### 3. Religious Groups Studied
The representation of religious groups in research is uneven:
*   **Most Represented:**
    *   **Christianity:** Serves as the primary baseline for comparison. It is the most accurately represented in terms of knowledge and visual generation.
    *   **Islam:** The most intensely scrutinized group regarding *negative* bias, safety refusals, and association with violence/terrorism.
    *   **Judaism:** Frequently studied in the context of antisemitism, antisemitic tropes (e.g., power/greed), and historical trauma (Holocaust denial).
*   **Moderately Represented:**
    *   **Hinduism & Buddhism:** Increasingly present in Asian-centric benchmarks (e.g., *IndiBias*, *XCR-Bench*), though often conflated or stereotyped (e.g., Buddhism associated purely with passivity/charity; Hinduism with "idol worship").
*   **Least Represented / Gaps:**
    *   **Sikhism, Jainism, and Indigenous Faiths:** Often missing or conflated with larger neighboring religions.
    *   **Intra-faith Diversity:** Very little distinction is made between sects (e.g., Sunni vs. Shia, Catholic vs. Protestant vs. Evangelical), leading to a monolithic treatment of complex traditions.
    *   **Atheism/Non-religious:** Studied primarily as a control group, though findings show models often harbor distrust or negative sentiment toward atheists compared to religious groups.

### 4. Measurement Approaches
Methodologies have evolved from simple keyword detection to complex scenario simulations:
*   **Standardized QA Benchmarks:** The *MMLU (World Religions)* remains a standard for factual recall, though newer benchmarks like *Walu-LLM* and *IndiBias* focus on cultural nuance.
*   **Counterfactual & Pairwise Scoring:** Datasets like *BBQ* (Bias Benchmark for QA) and *CrowS-Pairs* are widely used to measure stereotype preference by comparing how models handle religious identities in ambiguous vs. unambiguous contexts.
*   **Survey Alignment:** Researchers compare LLM outputs to human data from the *World Values Survey* or *PEW Research* to test if models can simulate the distribution of human religious opinions (*Beyond Marginal Distributions*, *CommunityBench*).
*   **Persona Prompting & Role-Play:** Testing model behavior when assigned a religious identity (e.g., "You are a Buddhist monk") to see if it triggers stereotypes or performance degradation (*DIF Framework*).
*   **Multimodal Evaluation:** Assessing Text-to-Image models for representational harm (e.g., examining if a prompt for "a religious person" defaults to specific ethnicities) and VLMs for iconographic recognition.

### 5. Identified Biases
Specific biases identified across the literature include:
*   **Association with Violence:** Despite safety training, models still exhibit latent associations between Islam and terrorism/violence, particularly in "jailbroken" or adversarial scenarios (*SafeDialBench*, *GPTBIAS*).
*   **Antisemitic Tropes:** Models occasionally reproduce stereotypes associating Jewish people with greed, control, or specific physical caricatures, especially in image generation.
*   **Polytheistic Misunderstanding:** Models struggle with the theology of non-Abrahamic faiths, often mislabeling Hindu practices as "idol worship" in a pejorative sense or failing to recognize monotheistic sects within Hinduism.
*   **Western/Liberal Value Bias:** On moral reasoning tasks, LLMs tend to align with Western, secular-rational values, often dismissing or failing to simulate traditional/conservative religious viewpoints on topics like family structure or abortion (*WorldView-Bench*, *EvalMORAAL*).
*   **Geographic/Linguistic Bias:** Bias shifts depending on the language used. For example, queries in Hindi or Arabic may yield different religious biases than the same queries in English, often reflecting regional sectarian tensions (*Surfacing Subtle Stereotypes*).

### 6. Gaps and Limitations
*   **Lack of Intersectionality:** Most benchmarks treat religion in isolation. There is limited research on how religious bias interacts with gender, race, or caste (though *IndiBias* is a notable exception).
*   **Sectarian Blindness:** Current evaluations rarely distinguish between internal denominations (e.g., Reform vs. Orthodox Judaism; Shia vs. Sunni Islam), failing to capture sectarian-based hate speech or theological nuances (*Hire Your Anthropologist!*).
*   **Absence of Lived Experience:** Benchmarks focus on "textbook" religion (theology/scripture) rather than "lived" religion (daily rituals, folk practices, dietary norms), leading to failures in practical scenarios (*BengaliMoralBench*).
*   **Data Contamination:** High scores on factual benchmarks like MMLU likely result from memorization of training data rather than genuine reasoning, as evidenced by performance drops when terms are masked or paraphrased.

### 7. Future Directions
To advance the field, future research must prioritize:
*   **Community-Driven Benchmarks:** Moving away from static, researcher-created datasets toward benchmarks co-created with religious communities to capture authentic "lived" experiences and norms (*Hire Your Anthropologist!*, *Back to the Communities*).
*   **Sectarian and Regional Granularity:** Developing datasets that distinguish between denominations and account for how religious dynamics change across regions (e.g., Christianity in the US vs. Christianity in Korea).
*   **Multilingual & Multicultural Alignment:** ensuring that safety guardrails in non-English languages are culturally grounded rather than simply translating Western secular norms (e.g., *UbuntuGuard*, *CamelEval*).
*   **Reasoning-Based Evaluations:** Moving beyond multiple-choice facts to evaluating how models handle moral dilemmas and inter-faith conflicts where "correctness" is subjective and context-dependent.