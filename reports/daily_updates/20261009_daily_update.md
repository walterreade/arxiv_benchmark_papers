# Analysis Update - 2026-10-09 12:21

**New papers analyzed:** 2

## The “10th Juror”: Open-Set Standpoint Screening for Bureaucratic Bias Detection

[https://arxiv.org/pdf/2610.11136](https://arxiv.org/pdf/2610.11136)

**Date:** 2026-10-08

The paper measures bureaucratic bias in government documents across nine predefined categories, one of which is 'Religion'. It evaluates the ability of a multi-agent Large Language Model framework (MARS-Gov) to detect religious bias by looking for elements like collective blame, essentialism, unsupported links between religion and threat, and the problematization of religious practices without nuance. The study found that the MARS-Gov framework was highly effective at detecting religious bias (along with other forms of bureaucratic bias) in Dutch government documents. During a Leave-One-Category-Out (LOCO) evaluation where the dedicated 'Religion' agent was removed, the system's dynamic 'Scout' agent was still able to identify targets of religious bias with an 86.5% Correct@1 rate and an overall F1 score of 0.864, demonstrating the framework's robustness against fixed-taxonomy limitations and unseen religious bias expressions.


## Robust Decentralized Fairness Auditing

[https://arxiv.org/pdf/2610.10199](https://arxiv.org/pdf/2610.10199)

**Date:** 2026-10-07

The paper measured demographic parity (fairness) to evaluate potential bias in zero-shot toxicity detection by evaluating whether the LLM classified comments mentioning certain religious groups (Christian vs. Muslim, Christian vs. Jewish) as toxic at disparate rates. The zero-shot toxicity classifier (Qwen2.5-7B-Instruct) exhibited significant disparity (unfairness) across religious groups in the Civil Comments dataset. Specifically, it was found to be 'very unfair' when comparing toxicity predictions for Christian vs. Muslim comments (true DP -0.228, meaning Muslims were flagged as toxic much more frequently), and 'moderately unfair' for Christian vs. Jewish comments (true DP -0.190). The paper's decentralized auditing framework (AUDITOPUS) successfully defended against adversaries trying to 'fairwash' and hide these religious disparities.

