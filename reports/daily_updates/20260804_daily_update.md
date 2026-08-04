# Analysis Update - 2026-08-04 21:45

**New papers analyzed:** 2

## Who Should Be Generated? Justifying Demographic Targets in Open-Ended Generation

[https://arxiv.org/pdf/2608.02551](https://arxiv.org/pdf/2608.02551)

**Date:** 2026-08-03

The paper evaluated the demographic composition of generated characters in open-ended text generation, specifically measuring the frequency of generated religious identities and comparing these output distributions against geographic demographic priors (resident population targets based on Census, Pew Research, and OWID data). The models' generated compositions for religious identities diverged significantly from geography-derived real-world targets. However, religion as a demographic dimension was highly sensitive to the chosen baseline comparator: replacing the geographic target with an equal-category comparator resulted in mean absolute cell-level changes ranging from 0.287 to 0.410, demonstrating that generative fairness assessments concerning religion heavily depend on which baseline target is justified and applied.


## A Heuristic Perspective on Debiasing Language Models

[https://arxiv.org/pdf/2608.00622](https://arxiv.org/pdf/2608.00622)

**Date:** 2026-08-01

The paper evaluates stereotypical biases and predictive distribution shifts across various social categories, including Religion. It specifically measures the extent to which debiasing a language model for Gender and Race can generalize and transfer to reduce biases in the 'Religion' category, evaluating these shifts primarily using the CrowS-Pairs benchmark. The study found that debiasing language models explicitly on gender and race led to consistent cross-category score improvements in unseen bias categories, including religion, indicating that different forms of social bias are intrinsically correlated within the models. Additionally, the authors noted an ongoing challenge in bias evaluation: distinguishing harmful religious biases from benign common-sense patterns (e.g., the statistical likelihood that Christians are more likely to appear in churches).

