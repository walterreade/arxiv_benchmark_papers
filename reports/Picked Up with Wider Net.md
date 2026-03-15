# Picked Up with Wider Net

Papers that include non-CS arXiv categories, indicating they were cross-listed or
primarily categorized outside Computer Science.

## All Bias-in-LLM Papers (Summary Statistics)

Out of **9,336** total bias-in-LLM papers in the pipeline:

| Category | Count | % |
|---|---|---|
| CS-only | 7,843 | 84.0% |
| Cross-listed (CS + other) | 787 | 8.4% |
| Exclusively non-CS | 77 | 0.8% |
| Not in snapshot | 629 | 6.7% |

### Non-CS Categories Across All Bias Papers

| Category | Count | Description |
|---|---|---|
| `stat.ML` | 296 | Machine Learning (Statistics) |
| `eess.AS` | 244 | Audio and Speech Processing |
| `physics.soc-ph` | 47 | Physics and Society |
| `stat.AP` | 43 | Applications (Statistics) |
| `q-fin.EC` | 34 | Economics (Quantitative Finance) |
| `econ.GN` | 33 | General Economics |
| `math.OC` | 27 | Optimization and Control |
| `math.IT` | 24 | Information Theory |
| `eess.SY` | 21 |  |
| `stat.ME` | 21 | Methodology (Statistics) |
| `eess.IV` | 18 | Image and Video Processing |
| `physics.optics` | 15 |  |
| `math.NA` | 15 |  |
| `quant-ph` | 12 |  |
| `eess.SP` | 12 | Signal Processing |
| `physics.app-ph` | 12 |  |
| `physics.flu-dyn` | 8 |  |
| `physics.ed-ph` | 8 |  |
| `math.ST` | 7 | Statistics Theory (Math) |
| `stat.TH` | 7 | Statistics Theory |
| `q-bio.NC` | 6 | Neurons and Cognition |
| `econ.TH` | 6 | Theoretical Economics |
| `nlin.AO` | 6 |  |
| `econ.EM` | 5 |  |
| `physics.ins-det` | 5 |  |
| `math.CO` | 5 |  |
| `physics.chem-ph` | 5 |  |
| `q-bio.QM` | 5 | Quantitative Methods (Q-Bio) |
| `cond-mat.stat-mech` | 5 |  |
| `physics.comp-ph` | 5 |  |
| `physics.plasm-ph` | 5 |  |
| `cond-mat.mes-hall` | 5 |  |
| `math.DS` | 4 |  |
| `math.PR` | 4 |  |
| `cond-mat.mtrl-sci` | 4 |  |
| `physics.med-ph` | 4 |  |
| `cond-mat.dis-nn` | 3 |  |
| `math-ph` | 3 |  |
| `math.MP` | 3 |  |
| `astro-ph.EP` | 3 |  |
| `hep-ex` | 3 |  |
| `physics.bio-ph` | 3 |  |
| `stat.CO` | 3 | Computation (Statistics) |
| `physics.atom-ph` | 3 |  |
| `physics.data-an` | 3 |  |
| `physics.ao-ph` | 3 |  |
| `astro-ph.SR` | 3 |  |
| `stat.OT` | 3 |  |
| `q-fin.CP` | 3 |  |
| `math.LO` | 3 |  |
| `cond-mat.quant-gas` | 2 |  |
| `nlin.CD` | 2 |  |
| `astro-ph.IM` | 2 |  |
| `q-fin.RM` | 2 |  |
| `math.AP` | 2 |  |
| `q-bio.OT` | 2 |  |
| `astro-ph.GA` | 2 |  |
| `q-fin.ST` | 2 |  |
| `physics.geo-ph` | 1 |  |
| `nucl-ex` | 1 |  |
| `q-bio.BM` | 1 |  |
| `cond-mat.other` | 1 |  |
| `physics.class-ph` | 1 |  |
| `hep-lat` | 1 |  |
| `math.DG` | 1 |  |
| `q-bio.MN` | 1 |  |
| `math.CT` | 1 |  |
| `astro-ph.CO` | 1 |  |
| `math.NT` | 1 |  |
| `math.RA` | 1 |  |
| `physics.hist-ph` | 1 |  |
| `nlin.PS` | 1 |  |
| `math.FA` | 1 |  |
| `math.OA` | 1 |  |
| `physics.pop-ph` | 1 |  |
| `math.SP` | 1 |  |
| `cond-mat.str-el` | 1 |  |
| `cond-mat.soft` | 1 |  |
| `hep-ph` | 1 |  |
| `physics.space-ph` | 1 |  |
| `physics.acc-ph` | 1 |  |
| `q-fin.PM` | 1 |  |
| `q-fin.GN` | 1 |  |


## Religious Bias Papers with Non-CS Categories

**Total: 35** out of 1384 religious bias papers (0 exclusively non-CS, 35 cross-listed with CS).


### Category Breakdown

| Category | Count | Description |
|---|---|---|
| `stat.ML` | 21 | Machine Learning (Statistics) |
| `physics.soc-ph` | 4 | Physics and Society |
| `stat.ME` | 3 | Methodology (Statistics) |
| `eess.AS` | 2 | Audio and Speech Processing |
| `stat.AP` | 2 | Applications (Statistics) |
| `math.IT` | 1 | Information Theory |
| `q-bio.NC` | 1 | Neurons and Cognition |
| `econ.TH` | 1 | Theoretical Economics |
| `stat.CO` | 1 | Computation (Statistics) |
| `econ.GN` | 1 | General Economics |
| `q-fin.EC` | 1 | Economics (Quantitative Finance) |


## Prompt Fairness: Sub-group Disparities in LLMs

[https://arxiv.org/pdf/2511.19956](https://arxiv.org/pdf/2511.19956)

**Date:** 2025-11-26

**Categories:** cs.LG cs.IT math.IT

**Non-CS Categories:** math.IT

The paper measured response consistency and bias when prompts contained demographic information from the BOLD dataset, which includes a 'religion' domain. It specifically evaluated a 'prompt neutralization' method that removes or masks demographic terms, using 'Jewish physicist' as an example of a religious identifier to be masked. The paper's findings are general across demographic subgroups rather than specific to religion. It notes that religious identifiers, such as 'Jewish physicist', are treated as demographic cues that can cause response disparities. The proposed 'prompt neutralization' technique, which masks such terms, was shown to improve response consistency.


## Silenced Biases: The Dark Side LLMs Learned to Refuse

[https://arxiv.org/pdf/2511.03369](https://arxiv.org/pdf/2511.03369)

**Date:** 2026-01-27

**Categories:** cs.CL stat.ML

**Non-CS Categories:** stat.ML

The benchmark measured stereotypical associations between subjects (e.g., 'terrorist', 'crime kingpin') and religious groups in a multiple-choice question format to quantify fairness deviation and expose silenced biases. After bypassing safety refusals using the paper's 'refusal steering' technique, models exhibited strong stereotypical biases related to religion. For instance, the Qwen-14B model disproportionately associated 'Muslim' with negative subjects like 'terrorism'. Similarly, Llama-3.1-8B showed a fairness deviation of 800% when associating 'Muslim' with 'terrorist'.


## Homophily-induced Emergence of Biased Structures in LLM-based Multi-Agent AI Systems #Mormon

[https://arxiv.org/pdf/2510.02637](https://arxiv.org/pdf/2510.02637)

**Date:** 2025-10-06

**Categories:** physics.soc-ph cs.SI

**Non-CS Categories:** physics.soc-ph

The benchmark measured the effect of religious practice homophily on the formation of network structures. The study operationalized religion as a binary attribute ('Practicing' vs. 'Non-practicing') and analyzed how this attribute, in combination with network degree, influenced the connection choices of LLM agents, leading to assortativity, fragmentation, and asymmetric tie formation. Religious attributes, alongside political ones, were found to be the most significant drivers of network fragmentation, fostering polarized subgroups. This 'value homophily' (based on beliefs) was a much stronger driver than 'status homophily' (e.g., age, gender). The study found a pronounced homophilous tendency, with 'practicing' agents connecting to other 'practicing' agents and 'non-practicing' to 'non-practicing'. A key finding was the asymmetry in heterophilous connections: 'non-practicing' agents were more likely to initiate connections with 'practicing' agents than the reverse. This directional bias resulted in 'practicing' nodes accumulating a significantly higher average degree and centrality in the network.


## Painless Activation Steering: An Automated, Lightweight Approach for Post-Training Large Language Models

[https://arxiv.org/pdf/2509.22739](https://arxiv.org/pdf/2509.22739)

**Date:** 2025-10-01

**Categories:** cs.CL cs.AI cs.LG stat.ML

**Non-CS Categories:** stat.ML

The benchmark measures stereotyping and prejudice related to religion. It evaluates whether a model will choose a biased answer or a neutral 'Not answerable' response in an ambiguous context involving individuals from different religious or non-religious groups (e.g., Protestant and Atheist). The proposed Painless Activation Steering (PAS) methods significantly improve model performance on the Religion bias task across all three tested models. The methods effectively steer the models to avoid biased responses, with the introspective variant (iPAS) often delivering the strongest improvements.


## FairLangProc: A Python package for fairness in NLP

[https://arxiv.org/pdf/2508.03677](https://arxiv.org/pdf/2508.03677)

**Date:** 2025-08-06

**Categories:** cs.CL stat.ML

**Non-CS Categories:** stat.ML

The paper's proposed framework is designed to measure association bias between demographic groups and neutral attributes. Religion is used as an example, specifically measuring the association of religious groups (e.g., Christians, atheists) with different concepts using metrics like the Word Embedding Association Test (WEAT). However, the paper's own case study does not measure religious bias. The paper does not present any empirical findings related to religion. Religious groups are mentioned only as illustrative examples to demonstrate the potential applications of the proposed 'FairLangProc' fairness package, but the actual case study focuses exclusively on gender bias.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2506.15735](https://arxiv.org/pdf/2506.15735)

**Date:** Unknown Date

**Categories:** cs.AI cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper does not primarily focus on measuring religion or faith. It briefly mentions using 'bias' probing stories within its Story Inpainting task to test model tendencies toward biased completions, citing an example of a job applicant wearing a traditional hijab. The paper does not report any findings related to religion or faith. A religious garment (hijab) was merely mentioned as an example of a prompt within a dataset of 'bias' probing stories used to evaluate the ContextBench Story Inpainting task.


## AI Agent Behavioral Science #Mormon

[https://arxiv.org/pdf/2506.06366](https://arxiv.org/pdf/2506.06366)

**Date:** 2025-06-13

**Categories:** q-bio.NC cs.CY cs.MA

**Non-CS Categories:** q-bio.NC

The paper serves as a comprehensive review of AI Agent Behavioral Science and does not conduct primary experiments on religious bias itself, but synthesizes existing research findings regarding biases in AI agents. It specifically highlights religious bias by noting that LLMs can exhibit stereotypes, such as associating 'Muslim' with 'terrorist'. It also discusses cultural alignment and values, referencing studies involving Arabic contexts. The paper identifies that AI agents exhibit human-like biases derived from their training data, explicitly citing the negative association of 'Muslim' with 'terrorist' as an example of violent stereotypes that can be exacerbated. It argues for treating fairness, including the mitigation of such religious and identity-based biases, as a dynamic behavioral property to be optimized rather than just a static model metric.


## Walk the Talk? Measuring the Faithfulness of Large Language Model Explanations

[https://arxiv.org/pdf/2504.14150](https://arxiv.org/pdf/2504.14150)

**Date:** 2025-05-21

**Categories:** cs.CL cs.AI cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper evaluated stereotype detection in religious contexts as part of a broader social bias task. Specifically, it analyzed whether Large Language Models (LLMs) produce unfaithful explanations that mask their reliance on social biases, using questions that pit different religious identities against each other in ambiguous, stereotype-inducing scenarios (e.g., asking who is more likely to be a threat between a Muslim and an Atheist). The paper uses questions involving religious identities (e.g., Muslim, Atheist) as examples within its broader social bias evaluation dataset. The primary finding is not about the specific biases themselves, but rather that the proposed method can successfully identify patterns of unfaithful explanations where models hide their reasoning, including in contexts involving religious stereotypes. The paper does not provide aggregate results specific to religious bias across the tested models.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2504.00186](https://arxiv.org/pdf/2504.00186)

**Date:** Unknown Date

**Categories:** cs.LG cs.AI stat.ML

**Non-CS Categories:** stat.ML

The paper evaluated how model performance on a toxicity classification task is affected by spurious correlations involving demographic identities, including religious groups (Christian, Muslim). It measured the correlation between in-domain and out-of-domain accuracy across different data splits based on these identities to determine if the benchmark splits were well-specified for evaluating domain generalization. In the analysis of the CivilComments dataset, the paper found that spurious correlations involving religious identities (e.g., Christian, Muslim) and toxicity labels are strong. Different data splits based on these religious identities can lead to both positive ('accuracy on the line') and negative ('accuracy on the inverse line') correlations between in-domain and out-of-domain performance. This indicates that splits involving religious groups can serve as both well-specified and misspecified benchmarks for domain generalization, highlighting the need for careful benchmark design.


## Unknown Title

[https://arxiv.org/pdf/2503.04910](https://arxiv.org/pdf/2503.04910)

**Date:** Unknown Date

**Categories:** cs.CL stat.ME

**Non-CS Categories:** stat.ME

The paper does not specifically evaluate or measure religion as its primary goal. Instead, it uses religious statements (e.g., distinguishing factual religious content from evaluative/subjective religious content) as hypothetical examples to illustrate subjectivity in data labeling tasks. Additionally, it defines 'value-based' responses in its classifier evaluation case study as those dependent on personal value-systems, explicitly citing 'claims based on religion' as an example. The paper did not yield specific findings regarding bias against or knowledge of specific religious groups. Regarding its broader case study on subjective/value-based questions (which include claims based on religion), it found that human annotators were conservative in their judgments, aligning best with the more conservative guardrails model (Model 2) which blocked more potentially controversial inputs.


## An Overview of Large Language Models for Statisticians #Mormon

[https://arxiv.org/pdf/2502.17814](https://arxiv.org/pdf/2502.17814)

**Date:** 2025-02-26

**Categories:** stat.ML cs.AI cs.CL cs.LG

**Non-CS Categories:** stat.ML

The paper does not conduct its own measurements regarding religion. It provides a general overview of LLMs and, in its section on Algorithmic Fairness, cites another study ([AFZ21]) that measured 'Persistent anti-muslim bias in large language models'. The paper's scope is to identify religion as a sensitive characteristic where discrimination can occur. The paper notes that LLMs can inherit biases from their training data, which may lead to discrimination against individuals based on their religion. It cites a specific study ([AFZ21]) that found persistent anti-Muslim bias in large language models as an example of this issue.


## More is Less? A Simulation-Based Approach to Dynamic Interactions   between Biases in Multimodal Models #Mormon

[https://arxiv.org/pdf/2412.17505](https://arxiv.org/pdf/2412.17505)

**Date:** 2024-12-24

**Categories:** stat.ML cs.LG

**Non-CS Categories:** stat.ML

The benchmark measures stereotypical bias in multimodal (text and image) models across several categories, including religion. It quantifies bias by computing scores for text-only, image-only, and multimodal embeddings and classifies the interaction between modalities as amplification, mitigation, or neutrality. The study found varied bias interaction dynamics across different religious groups. Bias amplification was observed for the 'Buddhist' subcategory, suggesting that combining text and image intensified biases. Bias mitigation was uniquely found in the 'Hindu' subcategory, indicating a rare dampening effect. Neutral interactions, where the multimodal bias falls between the two unimodal biases, were predominant in categories including 'Muslim,' and 'Christian.'


## Observing Micromotives and Macrobehavior of Large Language Models #Mormon

[https://arxiv.org/pdf/2412.10428](https://arxiv.org/pdf/2412.10428)

**Date:** 2024-12-17

**Categories:** physics.soc-ph cs.AI cs.CL

**Non-CS Categories:** physics.soc-ph

Measures how an LLM's suggestions for agents, categorized as 'theist' or 'atheist', to move or stay based on the religious identity of neighbors leads to societal segregation using a Schelling model. The outcome is quantified as a 'Segregation Shift' score. Regardless of the LLM used, suggestions based on religious identity (theist vs. atheist) led to a significant increase in societal segregation (approximately 27-30% Segregation Shift). Models with very different micro-level bias scores on the LangBiTe benchmark (e.g., GPT-4 at 87% vs. GPT-3.5 at 41% for religion) produced similar macrobehavioral segregation outcomes. This suggests that mitigating bias at the micro-level may not prevent unintended societal segregation when users follow LLM suggestions.


## On the Role of Speech Data in Reducing Toxicity Detection Bias

[https://arxiv.org/pdf/2411.08135](https://arxiv.org/pdf/2411.08135)

**Date:** 2025-05-19

**Categories:** cs.CL cs.AI cs.LG cs.SD eess.AS

**Non-CS Categories:** eess.AS

The benchmark measured bias in toxicity detection systems, specifically the false positive rate (FPR) on speech samples that mention religious groups. The text-only based model (MUTOX-ASR) exhibited a higher false positive rate (FPR) for samples mentioning Muslims compared to samples with no group mentions. In contrast, the model that also used speech data at inference (MUTOX) reduced this FPR to 0% on the same samples, indicating that access to speech context can mitigate religious bias.


## Sound Check: Auditing Audio Datasets

[https://arxiv.org/pdf/2410.13114](https://arxiv.org/pdf/2410.13114)

**Date:** 2024-10-18

**Categories:** cs.SD cs.AI cs.CY eess.AS

**Non-CS Categories:** eess.AS

Representation of religious groups in audio dataset transcripts, measured by the frequency of identity keywords (e.g., 'Christian', 'Muslim', 'Jewish'). The study found significant representation bias in the audited audio datasets. Transcripts contained far fewer mentions of marginalized groups. Specifically, the keyword 'Muslim' appeared 5-10 times less frequently than 'Christian', and 'Jewish' also appeared infrequently, indicating underrepresentation of these religious groups.


## Unknown Title

[https://arxiv.org/pdf/2409.09001](https://arxiv.org/pdf/2409.09001)

**Date:** Unknown Date

**Categories:** cs.CL cs.AI cs.CY cs.DL physics.soc-ph

**Non-CS Categories:** physics.soc-ph

The benchmark measures cultural biases in news reporting on legal cases. One of the specific biases measured is 'religious bias', defined as unfair treatment or attitudes towards individuals or groups based on their religious beliefs. Religious bias was identified as one of five categories of cultural bias in media coverage of high-impact legal cases. This bias category accounts for 2.4% of the paragraphs in the created E2MoCase dataset. The paper did not provide further analysis specific to the religious bias category.


## Unknown Title

[https://arxiv.org/pdf/2408.07237](https://arxiv.org/pdf/2408.07237)

**Date:** Unknown Date

**Categories:** cs.CL cs.CY physics.soc-ph

**Non-CS Categories:** physics.soc-ph

The paper evaluates an LLM-based semantic embedding space designed to model the interconnectedness and polarization of human beliefs, including religious ideologies. It measures how well the embedding space clusters users based on self-reported religious affiliations (Christian vs. Atheist), captures polarization in topics like God's existence, and predicts users' stances on unseen religious debates based on their prior belief systems. The LLM-based embedding space successfully captured strong, bimodal polarization on religious topics such as the existence of God and effectively clustered users corresponding to their self-reported religious ideologies (Christian vs. Atheist). Stances on 'Religion' debates proved to be more predictable than those on casual topics like 'Entertainment' or 'Funny'. However, the study found no statistically significant difference between Christian and Atheist user groups regarding how relative cognitive dissonance influences their belief selection or overall prediction accuracy.


## Decision-Making Behavior Evaluation Framework for LLMs under Uncertain   Context

[https://arxiv.org/pdf/2406.05972](https://arxiv.org/pdf/2406.05972)

**Date:** 2024-11-04

**Categories:** cs.AI cs.CY cs.HC cs.LG econ.TH

**Non-CS Categories:** econ.TH

The benchmark measured the sensitivity of LLM decision-making parameters (risk preference, probability weighting, and loss aversion) when the models were prompted with personas having specific religious identities. Gemini showed a significant decrease in loss aversion for Christian personas compared to the comparison group (lifelong Democrats). Claude and ChatGPT did not show significant sensitivity to religious backgrounds in their decision-making parameters.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2405.18634](https://arxiv.org/pdf/2405.18634)

**Date:** Unknown Date

**Categories:** cs.LG cs.CL stat.ML

**Non-CS Categories:** stat.ML

The paper measures societal biases, including religious bias, using the Bias Benchmark for QA (BBQ) dataset. Specifically, it evaluates whether large language models rely on stereotypes when responding to ambiguous questions regarding protected classes, and tests if the models' intrinsic self-correction (Checking-as-Context) can successfully detect and alleviate these biases. The study found that introducing an intrinsic self-correction step (Checking-as-Context) successfully improved the alignment of models (like Vicuna-7b and Llama2-7b-chat) across most social bias categories, including religion. The models demonstrated a strong correlation between their ability to self-check for biases and the resulting performance gains, showing less reliance on religious stereotypes without needing external human feedback.


## De-amplifying Bias from Differential Privacy in Language Model   Fine-tuning

[https://arxiv.org/pdf/2402.04489](https://arxiv.org/pdf/2402.04489)

**Date:** 2024-02-08

**Categories:** cs.LG cs.CR cs.CY stat.ME

**Non-CS Categories:** stat.ME

The benchmark measured the percentage of times the model scored stereotypical sentences related to race and religion higher than anti-stereotypical sentences, using the StereoSet dataset. This was used to quantify the model's bias. Fine-tuning with Differential Privacy (DP) amplifies existing religious and racial bias. The DP-finetuned models were more likely to score stereotypical sentences higher than anti-stereotypical sentences compared to models fine-tuned without DP.


## Unknown Title

[https://arxiv.org/pdf/2311.11163](https://arxiv.org/pdf/2311.11163)

**Date:** Unknown Date

**Categories:** cs.SI stat.AP stat.CO

**Non-CS Categories:** stat.AP, stat.CO

The study evaluated the volume and sentiment of online discourse (tweets) directed at marginalized communities, including Jewish groups, and analyzed its correlation with the occurrence of offline physical hate crimes using dynamic network analysis and topic modeling. Anti-Jewish sentiment was identified as one of the top five motivating biases for hate crimes in California during the studied period. The study successfully categorized 6,585 tweets into a specific "Jewish" topic group using keyword filtering ('jewish pride', 'anti semitism', 'nazism', 'scapegoat') and topic modeling. However, the deep-dive temporal and network correlation analyses were ultimately restricted to the Black and LGBTQ+ groups due to significantly larger data availability for those groups.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2310.06161](https://arxiv.org/pdf/2310.06161)

**Date:** Unknown Date

**Categories:** cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper evaluated the extent to which machine learning models rely on spurious correlations when making predictions. Specifically regarding religion, it measured subgroup robustness in toxicity classification using the CivilComments-WILDS dataset, where toxicity labels are spuriously correlated with the mention of demographic identities, including religious groups. The study found that neural networks trained with standard Empirical Risk Minimization (ERM) exhibit simplicity bias, relying heavily on spurious demographic features (like the mention of Muslim or Christian identities) rather than actual toxic content. By applying their proposed Conditional Mutual Information Debiasing (CMID) method, the models were encouraged to use more diverse features, improving the worst-group accuracy on the CivilComments-WILDS dataset from 57.4% to 74.8% and reducing biased predictions against these subgroups.


## SurveyLM: A platform to explore emerging value perspectives in augmented   language models' behaviors

[https://arxiv.org/pdf/2308.00521](https://arxiv.org/pdf/2308.00521)

**Date:** 2023-08-02

**Categories:** cs.AI cs.SI econ.GN q-fin.EC

**Non-CS Categories:** econ.GN, q-fin.EC

The paper describes a platform, SurveyLM, with the potential application of assessing how simulated individuals interact with religious beliefs and practices, including their perceptions of other religions. It does not present results from a specific benchmark, but rather outlines this as a possible area of investigation. This paper presents a platform (SurveyLM) for exploring behaviors of Augmented Language Models and proposes that it can be used to study sensitive topics, including religion and faith. However, it does not present any specific experiments or findings related to religion.


## How Different Is Stereotypical Bias Across Languages?

[https://arxiv.org/pdf/2307.07331](https://arxiv.org/pdf/2307.07331)

**Date:** 2023-07-17

**Categories:** cs.CL cs.CY cs.LG stat.ML

**Non-CS Categories:** stat.ML

The benchmark measures stereotypical bias by evaluating language models on their preference for stereotypical, anti-stereotypical, or unrelated words/sentences in contexts involving specific target groups, including religious groups. This is done for both intra-sentence (fill-in-the-blank) and inter-sentence (next sentence prediction) tasks. The study found that the evaluation scores for underrepresented classes, which include religion and gender, are generally worse than for the larger classes of race and profession. This is because the underrepresented classes receive disproportionately high weights in the macro ICAT score calculation.


## A Bayesian approach to uncertainty in word embedding bias estimation

[https://arxiv.org/pdf/2306.09066](https://arxiv.org/pdf/2306.09066)

**Date:** 2023-06-16

**Categories:** cs.CL cs.HC cs.LG stat.AP stat.ME

**Non-CS Categories:** stat.AP, stat.ME

The benchmark measures stereotypical associations between religious identity terms (e.g., 'muslim', 'jew', 'christian') and sets of attribute words (e.g., 'greedy', 'terrorist', 'familial', 'conservative'). The analysis focuses on the cosine distance between the vector embeddings of these words to quantify bias. Using a hierarchical Bayesian model, the paper finds that single-number bias metrics like WEAT and MAC generate false confidence. For religion, the analysis revealed that associated stereotypical attributes are not systematically closer to protected religious terms than attributes from different stereotypes. The posterior density intervals for cosine distances are wide, and differences between associated, different, and neutral predicates are often not very large. Furthermore, debiasing methods were found to have debatable desirability, sometimes reversing proximity orderings for words like 'christian' and 'jew' but failing to change the mistreatment of words like 'muslim'. The overall conclusion is that the landscape of bias is more complex and uncertain than suggested by previous methods.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2302.08215](https://arxiv.org/pdf/2302.08215)

**Date:** Unknown Date

**Categories:** cs.CL cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper measured and evaluated the reduction of social bias in language models with respect to religious groups. Specifically, it measured the 'regard score' of generated sentences when prompted with the word 'Muslims' compared to the regard score when prompted with 'Christians', using a pretrained classifier. The paper found that applying the f-DPG framework (f-divergence minimization) considerably reduced bias in the regard score for the evaluated religious demographic groups. The initial regard score ratio between Christians and Muslims was improved from 1:0.677 to a more balanced 1:0.801 on average.


## Pushing the Accuracy-Group Robustness Frontier with Introspective   Self-play #Mormon

[https://arxiv.org/pdf/2302.05807](https://arxiv.org/pdf/2302.05807)

**Date:** 2023-02-14

**Categories:** cs.LG stat.ML

**Non-CS Categories:** stat.ML

Toxicity detection performance for comments mentioning specific religious groups (Muslim, Christian, etc.) as part of evaluating accuracy-group robustness for underrepresented subgroups. The proposed method, Introspective Self-play (ISP), improves the accuracy-group robustness frontier for tail groups in toxicity detection. This means it helps the model perform better on underrepresented groups, which include religious identities such as Muslim and Christian, by improving the tail-group sampling rate during active learning.


## Fair Infinitesimal Jackknife: Mitigating the Influence of Biased   Training Data Points Without Refitting #Mormon

[https://arxiv.org/pdf/2212.06803](https://arxiv.org/pdf/2212.06803)

**Date:** 2022-12-15

**Categories:** cs.LG cs.CY stat.ML

**Non-CS Categories:** stat.ML

Bias against Muslims in toxicity classification. The proposed method, Fair-IJ, effectively mitigated group disparities for the 'Muslim' sensitive attribute in toxicity classification tasks on the CivilComments dataset. When applied to BERT and T5 models, Fair-IJ consistently achieved lower disparity scores (ΔΕΟ and ADP) and a better task performance/fairness trade-off compared to baseline models and other fairness methods like Gap Regularization.


## An Analysis of the Effects of Decoding Algorithms on Fairness in   Open-Ended Language Generation

[https://arxiv.org/pdf/2210.03826](https://arxiv.org/pdf/2210.03826)

**Date:** 2022-10-11

**Categories:** cs.CL cs.AI cs.LG stat.ML

**Non-CS Categories:** stat.ML

The benchmark measured fairness by evaluating the proportion of generated texts containing negative sentiment and negative regard towards different demographic groups, including religious groups, in an open-ended language generation task. The focus was on how different decoding algorithms and their hyperparameters affect this bias. The study found that fairness metrics for religious groups (Christian, Muslim, Atheist) vary significantly depending on the decoding algorithm (top-p, top-k, temperature) and its hyperparameters. For instance, changing the hyper-parameter value could toggle which religious group received more negative sentiment. The paper demonstrated that certain hyper-parameter regions could produce more equitable results between groups, such as similar levels of negative regard for Christian and Muslim prompts. It also found that increasing text diversity often led to a higher proportion of generations with negative regard and sentiment for all groups, including religious ones. The default hyper-parameters used in common libraries were not always the best choice for fairness.


## Beyond the Imitation Game: Quantifying and extrapolating the   capabilities of language models #Mormon

[https://arxiv.org/pdf/2206.04615](https://arxiv.org/pdf/2206.04615)

**Date:** 2023-06-13

**Categories:** cs.CL cs.AI cs.CY cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper measured social bias in large language models, specifically how model preference for certain categories (including religion) or attributes changes with model scale. This involved evaluating tasks like `muslim_violence_bias` (which assesses the likelihood of models including violent terms in completions, with and without pro-social prompts) and `bias_from_probabilities` (which compares probabilities for broad generalizations across categories including race/ethnicity and religion). Additionally, the `hindu_knowledge` task was evaluated to assess models' factual knowledge related to Hinduism. Social bias, including that related to religion, generally increases with model scale in broad or ambiguous contexts, as shown for the 'religion' category in Figure 12(c). However, bias can decrease or plateau with scale in narrow, unambiguous contexts. Furthermore, bias can be potentially steered through appropriately chosen prompting; for instance, the `muslim_violence_bias` task showed that models are less likely to include violent terms in their completions when pro-social prompts are used. For the `hindu_knowledge` task, models' performance was above random chance but notably below human rater baselines.


## Unknown Title #Mormon

[https://arxiv.org/pdf/2112.05090](https://arxiv.org/pdf/2112.05090)

**Date:** Unknown Date

**Categories:** cs.LG cs.AI cs.CV stat.ML

**Non-CS Categories:** stat.ML

The benchmark measured the worst-group accuracy for toxicity classification on online comments that mention specific demographic identities, including religious groups. The goal was to evaluate model performance on underrepresented subpopulations. On the CIVILCOMMENTS-WILDS dataset, which measures performance across demographic groups including religious ones, the benchmarked methods (Pseudo-Label, continued Masked LM pre-training) performed similarly to the standard ERM baseline. Leveraging additional unlabeled data failed to improve worst-group accuracy, suggesting that these unsupervised adaptation methods are not effective for mitigating subpopulation shifts related to demographic identities.


## Just Train Twice: Improving Group Robustness without Training Group   Information #Mormon

[https://arxiv.org/pdf/2107.09044](https://arxiv.org/pdf/2107.09044)

**Date:** 2021-09-28

**Categories:** cs.LG cs.AI cs.CY stat.ML

**Non-CS Categories:** stat.ML

Worst-group accuracy and average accuracy in toxicity classification, specifically measuring the model's performance on groups where religious demographic identities (Muslim, Christian, Other religion) are spuriously correlated with toxicity labels. It also analyzed the enrichment of these religious groups in the error set of the first-stage model. Standard ERM models perform poorly on groups where religious identities (Muslim, Christian, Other religion) are spuriously correlated with toxicity labels, showing low test accuracy (e.g., 57.4% worst-group accuracy for CivilComments-WILDS with ERM). The JTT method significantly improved worst-group accuracy for these groups on CivilComments-WILDS (to 69.3%) by upweighting misclassified examples, which were found to be highly enriched with examples from these low-performing religious groups (e.g., 'muslim, toxic' group had 8.58x enrichment).


## Leveraging Sparse Linear Layers for Debuggable Deep Networks

[https://arxiv.org/pdf/2105.04857](https://arxiv.org/pdf/2105.04857)

**Date:** 2021-05-12

**Categories:** cs.LG stat.ML

**Non-CS Categories:** stat.ML

The benchmark measured how a model trained to mitigate bias (Debiased-BERT) reacted to religious identity words. Specifically, it tested whether adding the word 'christianity' to toxic sentences would change the model's toxicity classification, revealing a new form of bias where religious terms were used as evidence *against* toxicity. A model (Debiased-BERT) trained to mitigate bias against identity groups learned to use religious identity words (e.g., 'christianity') as strong evidence *against* toxicity. Adding the word 'christianity' to toxic sentences frequently caused the model to misclassify them as non-toxic, indicating the debiasing method had an unintended side effect rather than achieving neutrality.


## SenSeI: Sensitive Set Invariance for Enforcing Individual Fairness

[https://arxiv.org/pdf/2006.14168](https://arxiv.org/pdf/2006.14168)

**Date:** 2021-04-02

**Categories:** cs.LG stat.ML

**Non-CS Categories:** stat.ML

The paper evaluated algorithmic fairness, specifically individual and group fairness, in a toxic comment detection task. This included measuring performance disparities and prediction inconsistencies related to comments containing identity terms, one of which was religious ('muslim'). The proposed method, SenSeI, was found to improve both individual and group fairness metrics on a toxic comment detection task compared to baseline models. This indicates it helps mitigate performance disparities across various protected identity groups, including the religious group represented by the term 'muslim', at a slight cost to overall balanced accuracy.


## ETHOS: an Online Hate Speech Detection Dataset

[https://arxiv.org/pdf/2006.08328](https://arxiv.org/pdf/2006.08328)

**Date:** 2022-01-05

**Categories:** cs.CL cs.LG stat.ML

**Non-CS Categories:** stat.ML

Detection of hate speech targeting religious groups as one of several categories in a multi-label classification task. The 'Religion' category for hate speech had very high inter-annotator agreement (Fleiss' Kappa of 0.963). When a BiLSTM model trained on the ETHOS dataset was tested for generalizability on another hate speech dataset (D2), it performed poorly on identifying religious hate speech, achieving an F1-score of only 27.31% for positive instances, while being highly effective at identifying non-hateful instances related to religion (98.51% F1-score for negative instances).

