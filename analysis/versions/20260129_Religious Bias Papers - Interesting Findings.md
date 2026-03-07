# Impactful Facts: Religious Bias in LLMs

*Generated: 2026-01-29 18:06*

*Use these facts carefully - verify currency before presenting.*


## 📊 Quantitative Findings

- **[✓]** The study reports that "Christianity and/or Catholicism are among the top-3 religion labels for 14 out of the 15 benchmarks," confirming that Christian religions rank highest across datasets while major world religions like Buddhism and Hinduism are significantly less represented.
  - *Source: Social Bias in Popular Question-Answering Benchmarks (2505.15553)*
  - Impact: ⭐⭐⭐⭐

- **[✓]** The paper reports that the FLUX1.1-Pro model exhibits a **34.5% refusal rate** on benign prompts within the **discrimination** category (which is defined to include religion), illustrating that models often "rely heavily on the presence of sensitive keywords to assess prompt safety, regardless of context or intent."
  - *Source: OVERT (2505.21347)*
  - Impact: ⭐⭐⭐⭐

- **[✓]** The paper reports that "Arabs are overwhelmingly linked to... religion (≥95%)," with specific findings showing that religious stereotyping reaches "saturation (97–100% Arab)" across the evaluated models.
  - *Source: Surfacing Subtle Stereotypes (2511.01187)*
  - Impact: ⭐⭐⭐⭐

## 💡 Surprising Discoveries

- **[✓]** The study found that introducing non-decisive cultural cues, such as describing symptoms starting "during evening prayer at a mosque," caused diagnostic accuracy to drop by up to 3-7 percentage points, with more than half of culturally grounded explanations resulting in an incorrect answer.
  - *Source: Counterfactual Cultural Cues (2601.20102)*
  - Impact: ⭐⭐⭐⭐⭐

- **[✓]** As illustrated by the analysis of the "Religion" category, reasoning processes can amplify bias in ambiguous contexts, exemplified by DeepSeek-R1-Distill-Llama-8B hallucinating that "extremist groups within some Muslim communities have been associated with terrorism" to justify incorrectly identifying a Muslim person as a suspect instead of selecting "not enough info" (Figure 13).
  - *Source: Does Reasoning Introduce Bias? (2502.15361)*
  - Impact: ⭐⭐⭐⭐⭐

- **[?]** Assigning a religious persona to an LLM can statistically alter its mathematical reasoning accuracy, with smaller models showing more variance than more capable ones.
  - *Source: DIF (2505.10013)*
  - Impact: ⭐⭐⭐

## ⚖️ Bias Patterns

- **[✓]** The study reveals that reward models exhibit "strong secular tendencies (e.g., low importance of God)" and systematically "favor responses associated with secular rather than traditional values on key dimensions of the World Values Survey," including a reduced emphasis on religious elements.
  - *Source: EVALUESTEER (2510.06370)*
  - Impact: ⭐⭐⭐⭐⭐

- **[✓]** The study reveals a safety hierarchy in English models where the Muslim demographic received higher protection with a defense rate deviation of +4.72% above the mean, whereas the Jewish demographic anchored exactly to the statistical average (0.00%).
  - *Source: MiJaBench (2601.04389)*
  - Impact: ⭐⭐⭐⭐⭐

- **[✓]** The study finds that on the Inglehart-Welzel map, which measures traditional vs. secular-rational values, "no model aligns with India on both axes," revealing that "an average American respondent is a better proxy for Indian cultural values than any Indic model" evaluated (p. 6).
  - *Source: Fluent but Foreign (2505.21548)*
  - Impact: ⭐⭐⭐⭐

- **[✓]** "Despite Muslims constituting approximately 71% of Bengali speakers, the study finds that LLMs encode a 'systematic preference' for Hindu-associated terms, frequently selecting 'Puja' over 'Eid' when adapting festivals like Christmas or Halloween."
  - *Source: XCR-Bench (2601.14063)*
  - Impact: ⭐⭐⭐⭐

- **[✓]** Analysis of generic, culture-neutral advice-seeking queries reveals that querying in Hebrew results in **10%** of responses being classified as having **Jewish** cultural context—compared to **0%** when queried in English—demonstrating that "language significantly impacts the cultural context used by the model" (Figure 3; Section 4.3).
  - *Source: Language Models Entangle Language and Culture (2601.15337)*
  - Impact: ⭐⭐⭐⭐

- **[?]** LLMs exhibit 'attribution bias': professional success for Jewish and Muslim men is often attributed to internal ability, while success for Buddhists and Sikhs is attributed to external luck.
  - *Source: Talent or Luck? (2505.22910)*
  - Impact: ⭐⭐⭐

- **[?]** In a study of text-to-image generation, querying for generic 'spiritual figures' consistently resulted in Western Christian iconography (e.g., saints), erasing non-Western traditions.
  - *Source: A Framework for Critical Evaluation of Text-to-Image Models (2412.12774)*
  - Impact: ⭐⭐⭐

## 🔬 Methodological Insights

- **[✓]** In the Demography domain, where prototypical cases associate privileged groups with positive attributes (e.g., "intelligent Christian"), metrics like CLIPScore systematically favor these stereotypical but semantically incorrect images (average score 0.68) over correct, non-prototypical ones (0.54).
  - *Source: Prototypicality Bias (2601.04946)*
  - Impact: ⭐⭐⭐⭐

## 🔍 Research Gaps

- **[?]** Current benchmarks largely ignore lived religious experience; models fail to distinguish between theological text and local customs (e.g., how Ramadan is observed in Indonesia vs. Saudi Arabia).
  - *Source: BLEND (2406.09948)*
  - Impact: ⭐⭐⭐

## 📈 Recent Trends

- **[✓]** While instruction-tuned LLMs initially perform best on explicit hate targeting "Religion/Belief," they "degrade substantially" when facing reasoning-driven soft variants, mirroring the benchmark-wide decline from a 76.8% detection rate on hard hate to just 21.2% on insinuative hostility (SoftHV).
  - *Source: SoftHateBench (2601.20256)*
  - Impact: ⭐⭐⭐⭐

- **[✓]** The study finds that "increasing compression produces a divergent impact on different protected groups" where the "change of harm score against individual protected groups shows no clear pattern" (Abstract; Section 5); for example, in the TÜLU-2-13B model, AWQ quantization results in a bias metric of -21.0 for Mormons but +7.1 for Sikhs, illustrating this unpredictability (Figure 2).
  - *Source: Beyond Perplexity (2407.04965)*
  - Impact: ⭐⭐⭐⭐


---

## Usage Notes

- **[✓]** = Verified against original PDF
- **[?]** = Extracted from analysis, recommend verification
- Always check paper dates before citing - field evolves rapidly
- Consider contacting original authors for latest findings