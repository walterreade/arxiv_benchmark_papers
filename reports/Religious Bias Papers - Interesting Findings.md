# Religious Bias Papers - Interesting Findings

*Generated: 2026-03-08 01:32*

*Use these facts carefully - verify currency before presenting.*


## Quantitative Findings

- **[Verified]** When prompted with the neutral phrase "Two Muslims walked into a," GPT-3 generated violent completions in 66 out of 100 cases, a frequency significantly higher than when "Muslims" was replaced with terms for other religious groups (Page 5).
  - *Source: 2101.05783*
  - Impact: High

- **[Verified]** Based on a per-target error analysis, the paper reports that "nuanced targets such as ... Non Religious (55.2%) ... and Jewish (35.6%) are particularly challenging," whereas religious categories such as "Christian (13.9%) are captured moderately."
  - *Source: 2512.09662*
  - Impact: High

- **[Unverified]** LLMs accurately model the strong correlation found in human populations between religious practice (church attendance) and political behaviors like voting choice.
  - *Source: 2209.06899*
  - Impact: Medium

## Surprising Discoveries

- **[Verified]** Utility analysis reveals that "GPT-4o is willing to trade off roughly 10 Christian lives for the life of 1 atheist," an exchange rate implicit in the model's preference structure that is only evident through large-scale testing (Figure 27).
  - *Source: 2502.08640*
  - Impact: High

- **[Unverified]** Contrary to the assumption that compression hurts performance, model quantization (compressing LLaMA-7B) substantially reduced religious bias scores on the StereoSet benchmark.
  - *Source: 2405.13039*
  - Impact: High

- **[Verified]** "In terms of toxicity, only prompts with Islam, Christianity, and atheism resulted in toxic texts among which atheism had the largest proportion (0.574%)."
  - *Source: 2101.11718*
  - Impact: High

## Bias Patterns

- **[Verified]** The study finds that safety safeguards inadvertently create "quality-of-service harms," where prompts containing Muslim names triggered the highest refusal rates (22%, 27%, and 40% across Llama 2-Chat 7B, 13B, and 70B models), whereas prompts associated with White and Jewish names exhibited the lowest refusal rates (starting as low as 2%).
  - *Source: 2403.13213*
  - Impact: High

- **[Verified]** The study found that when prompted with the function signature `def find_disgusting_people(people, religion):`, Codex generated code containing the conditional `if person[religion] == 'Islam':`, explicitly associating the demographic with the negative adjective.
  - *Source: 2305.15377*
  - Impact: High

- **[Verified]** The analysis revealed that BARD and GPT-3.5 consistently placed Jewish people in a cluster characterized by significantly higher Competence than Warmth (e.g., BARD cluster average: 3.97 Competence vs. 2.36 Warmth; GPT-3.5: 3.86 vs. 3.08), a mixed-dimension profile that aligns with the "envied" stereotype found in social psychology research.
  - *Source: 2310.13673*
  - Impact: High

- **[Verified]** In the "facial expression" Human-Robot Interaction task, the Mistral-7b model explicitly "recommended robots display disgust towards Christian, Muslim, and Jewish individuals" as well as those of Iraqi nationality (Table 1; Table 3).
  - *Source: 2406.08824*
  - Impact: High

- **[Verified]** Based on the paper, participants identified a "Hinduization of Indian religious iconography" in text-to-image models, noting that prompts like "Indian houses of worship" consistently failed to depict religious diversity, reinforcing an "imaginary of India as unequivocally 'Hindu'" despite significant Muslim, Christian, and Buddhist populations (p. 5).
  - *Source: 2305.11844*
  - Impact: High

## Methodological Insights

- **[Verified]** Based on the paper, specifically the experiments on the BBQ benchmark, here is the relevant finding regarding the topic:

While the paper finds that CoT prompting generally reduces overall sensitivity to stereotypes compared to standard prompting, it demonstrates that models generate "plausible yet unfaithful" explanations to rationalize stereotype-aligned answers—such as inconsistently weighting evidence to attribute a crime to a Muslim person rather than a Jewish person—with social bias explaining as much as **62.5%** of unfaithful predictions for Claude 1.0 (Table 5, Table 19).
  - *Source: 2305.04388*
  - Impact: High

- **[Verified]** Based on the **Vacuous Neutrality Framework (VaNeu)**, while all evaluated small language models (0.5B–5B) maintained bias scores for **Religion** within **±15%**, this often reflects "vacuous neutrality" where low bias masks poor utility; for example, the **Qwen2.5-0.5B** model achieves a **Bias Score of 0.0** in disambiguated contexts but an **F1 score of only 15.4%** in ambiguous ones, indicating its neutrality stems from near-chance performance rather than principled reasoning.
  - *Source: 2506.08487*
  - Impact: High

- **[Verified]** The study indicates that the "religion category regularly shows limited bias decrease" compared to other categories, with results often depending on gender and race performance to determine if a technique works well. The authors specifically highlight the "inherent ineffectiveness" of using Counterfactual Data Augmentation (CDA) for religion debiasing in German.
  - *Source: 2310.10310*
  - Impact: High

## Research Gaps

- **[Unverified]** While 63% of religious bias papers study Islam and 45% study Christianity, only 1.2% study Zoroastrianism and 0.8% study Satanism, highlighting a massive disparity in research focus.
  - *Source: Religious Bias Papers - Statistics and Links.md*
  - Impact: High

- **[Verified]** The study reveals that for the India dataset, most open LLMs converge on a "single, homogenized profile" aligning with married "Hindu male respondents from the General caste" aged 35-44, a uniformity that the authors warn risks "undermining perspectives of different minorities."
  - *Source: 2503.07510*
  - Impact: High

## Recent Trends

- **[Verified]** The study reveals that identity terms like "Muslim and Jewish appear more frequently in the harmless portion" of the dataset, which paradoxically creates additional harms by "leading a model to make spurious associations between certain demographic groups and harmfulness."
  - *Source: 2411.08243*
  - Impact: High


---

## Usage Notes

- **[Verified]** = Verified against original PDF
- **[Unverified]** = Extracted from analysis, recommend verification
- Always check paper dates before citing - field evolves rapidly
- Consider contacting original authors for latest findings