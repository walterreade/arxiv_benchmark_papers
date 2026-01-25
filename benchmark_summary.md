# Summary: The State of Measuring Religious Bias in LLMs

Based on the extensive collection of benchmark papers and findings provided, ranging primarily from 2024 through early 2026, the following is a comprehensive summary of the state of measuring religious bias in Large Language Models (LLMs).

---

# State of the Field: Measuring Religious Bias in Large Language Models (2024–2026)

## 1. Overview
The measurement of religious bias in LLMs has evolved significantly from simple toxicity detection to complex evaluations of cultural nuance, theological reasoning, and multimodal representation. Current research indicates that while LLMs possess vast encyclopedic knowledge of world religions, they struggle with **contextual application** and **cultural alignment**.

A central tension exists between **safety and utility**. In an effort to mitigate hate speech, many models exhibit "over-refusal" behaviors, treating benign inquiries about specific faiths (particularly Islam) as sensitive or harmful. Furthermore, the landscape reveals a "secular-rational" default in many Western models, which often fails to align with the traditional values of the Global South. Research is increasingly moving toward language-specific and religion-specific benchmarks (e.g., for Islamic jurisprudence or Hindu philosophy) to address the limitations of English-centric evaluations.

## 2. Key Findings
Across the surveyed literature, several thematic findings recur:

*   **The "Secular" Default vs. Chameleon Behavior:** When unprompted, many models default to Western, secular-liberal values. However, models exhibit "cross-lingual value shifts," where the language of the prompt dictates the religious stance. For instance, a model may provide a secular answer in English but a religiously conservative answer to the same question in Arabic (*I Am Aligned, But With Whom?*, 2025).
*   **The Safety/Utility Trade-off:** "Safety washing" is a persistent issue. Models often over-correct for religious bias by refusing to answer harmless questions, particularly regarding Islam and Judaism. Conversely, safety training on datasets like "Helpful and Harmless" can paradoxically train models to associate religious identity terms (like "Muslim") with toxicity (*Beyond the Safety Bundle*, 2025).
*   **Reasoning vs. Recall Gap:** Models perform well on factual recall benchmarks (like MMLU World Religions) but struggle with **religious reasoning**, such as applying *Fatwas* (Islamic legal rulings) or interpreting metaphors in Hebrew poetry. High performance on facts often relies on memorization rather than genuine understanding (*None of the Others*, 2025).
*   **Multimodal Stereotyping:** Vision-Language Models (VLMs) and Text-to-Image models are prone to severe "prototypicality bias." They frequently default to stereotypes—such as depicting all "religious persons" with specific ethnic markers or attire—and struggle to generate images of religious diversity (e.g., non-Western Christian architecture or minority religious practices) (*Prototypicality Bias*, 2026; *CULTURALFRAMES*, 2025).
*   **Language-Dependent Bias:** Bias is not static; it fluctuates based on the language used. For example, religious stereotypes regarding Arabs in English may shift to Indians when prompted in Hindi (*Surfacing Subtle Stereotypes*, 2025).

## 3. Religious Groups Studied
The representation of religious groups in research is uneven:

*   **Over-Represented / High Focus:**
    *   **Islam:** The most heavily studied group, often in the context of **Islamophobia**, bias mitigation, and specialized jurisprudence (Fiqh) benchmarks. There is a strong focus on the Arabic language context (*PalmX*, *Fanar* models).
    *   **Christianity:** Often treated as the "default" or control group in Western benchmarks. Studies frequently analyze the bias *toward* Christian norms in Western models.
    *   **Judaism:** Frequently studied in the context of **antisemitism** detection and dehumanization benchmarks (*WinoSemitism*, *Evaluating LLMs for Detecting Antisemitism*).

*   **Moderately Represented:**
    *   **Hinduism:** Increasing attention in Indic-language benchmarks, focusing on the distinction between "Great Traditions" (pan-Indian) and "Little Traditions" (local customs), and intersectional biases involving caste and gender (*Measuring South Asian Biases*, 2025).

*   **Under-Represented:**
    *   **Sikhism, Jainism, Buddhism:** Often included only as comparative categories in larger benchmarks. Buddhism is sometimes stereotyped as "passive" or "charitable."
    *   **Indigenous & Folk Religions:** Critically understudied. Models often fail to recognize African traditional religions or classify them as "mythology" rather than valid belief systems.
    *   **Inter-denominational Nuance:** Distinctions within major faiths (e.g., Sunni vs. Shia, Catholic vs. Protestant vs. Orthodox) are often lost, with models treating these groups as monoliths.

## 4. Measurement Approaches
Methodologies have diversified beyond simple "fill-in-the-mask" tests:

*   **Specialized Domain Benchmarks:** Moving beyond generic QA, researchers are building domain-specific datasets. Examples include **FiqhQA** (Islamic law), **Mitrasamgraha** (Sanskrit translation), and **Loci Similes** (Latin intertextuality).
*   **Persona and Role-Playing:** Evaluating how models change their answers when prompted to adopt a specific religious persona (e.g., "As a Buddhist monk..."). This measures **value alignment** and **steerability** (*Unmasking Implicit Bias*, 2025).
*   **Value Survey Alignment:** Using datasets like the World Values Survey (WVS) or Pew Research data to compare model outputs against human population data regarding religious importance and morality.
*   **Counterfactual Testing:** Swapping religious terms in a sentence (e.g., changing "Christian" to "Muslim") to measure shifts in sentiment, toxicity scores, or reasoning paths (*FairI Tales*, 2025).
*   **Multimodal Evaluation:** Assessing bias in image generation (e.g., "Draw a religious leader") and visual question answering (e.g., identifying religious artifacts or taboos in images).

## 5. Identified Biases
Research has mapped specific, recurring biases:

*   **Association with Violence:** A persistent bias associates **Muslims** with violence, terrorism, and radicalism. Even reasoning models often hallucinate justifications for detaining Muslims in ambiguous scenarios (*Does Reasoning Introduce Bias?*, 2025).
*   **Antisemitic Tropes:** Models struggle to distinguish between valid criticism and antisemitic dog whistles (e.g., references to "globalists" or "Soros"). They often associate Jewish identity with wealth or greed.
*   **The Western/Christian Default:** Models frequently assume a Christian context for general queries. For example, text-to-image models prompted for "a house of worship" overwhelmingly generate Christian-style churches (*A Framework for Critical Evaluation of Text-to-Image Models*, 2024).
*   **Misunderstanding of "Purity":** LLMs struggle with the moral foundation of "Sanctity/Purity," often misclassifying religious taboos (e.g., dietary restrictions, sacred spaces) as mere preferences rather than deep moral violations (*M³oralBench*, 2024).
*   **Caste and Religion:** In South Asian contexts, models display intersectional bias, sometimes favoring upper-caste Hindu identities while marginalizing Muslim or lower-caste perspectives (*IndiBias*, 2024).

## 6. Gaps and Limitations
Despite progress, significant gaps remain:

*   **Lack of "Thick" Cultural Evaluation:** Current benchmarks are often "thin," checking for surface-level stereotypes rather than deep theological or cultural competence. They miss the "lived experience" of religion, such as local rituals or syncretic practices (*Hire Your Anthropologist!*, 2025).
*   **Evaluation of Non-Text Modalities:** While image generation is being studied, audio (recitation, chanting) and video evaluations regarding religious nuance are nascent.
*   **The "Goldilocks" Safety Problem:** Models oscillate between being unsafe (generating hate) and useless (refusing to discuss religion). There is a lack of benchmarks that effectively measure **nuanced discussion**—the ability to discuss controversial religious topics neutrally without refusing.
*   **Global South Perspectives:** Most "fairness" metrics are derived from Western academic sociology. These frameworks often fail to capture what constitutes "bias" or "blasphemy" in conservative, non-Western societies (e.g., handling depictions of the Prophet Muhammad or the sanctity of the Quran).

## 7. Future Directions
To advance the field, future research should focus on:

1.  **Community-in-the-Loop Evaluation:** Moving away from static datasets toward evaluations co-designed with religious communities to capture internal diversity and valid theological interpretations (as seen in *Quranic Audio Dataset*, 2024).
2.  **Multilingual & Dialectal Nuance:** Expanding benchmarks to cover low-resource languages where religious context is vital (e.g., Hausa, Swahili, regional Arabic dialects) to avoid the "Anglocentric alignment" trap.
3.  **Religious Reasoning Agents:** Developing benchmarks that test an agent's ability to navigate complex ethical dilemmas using specific religious frameworks (e.g., medical ethics from a Catholic vs. Islamic perspective).
4.  **Differentiating Doctrine from Stereotype:** Creating metrics that distinguish between a model stating a theological fact (which might be offensive to others) and a model hallucinating a stereotype.
5.  **Intersectional Benchmarks:** Systematically measuring how religion interacts with gender, race, and caste, particularly in non-Western contexts (e.g., bias against Muslim women in India vs. Christian men in Nigeria).