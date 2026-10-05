# Analysis Update - 2026-10-05 12:10

**New papers analyzed:** 1

## WHAT IS LOST IN POST-TRAINING? DEFAULT COLLAPSE AND THE LOSS OF IN-CONTEXT STEERABILITY ACROSS DIVERSE PERSPECTIVES

[https://arxiv.org/pdf/2610.02614](https://arxiv.org/pdf/2610.02614)

**Date:** 2026-10-02

The paper evaluated how one-sided post-training (fine-tuning) affects a large language model's default behavior, recognition, and in-context steerability regarding religious perspectives. Specifically, it measured 'default collapse' (the tendency to favor one side by default) and 'steerability loss' (the inability to faithfully enact opposing views when explicitly prompted) on survey questions where the opposing poles represented the majority positions of Atheists versus Protestants. On religious survey questions (Atheist vs. Protestant), the base model's default behavior was relatively balanced (52% / 48%) but exhibited low steerability (42%) and recognition (14%). One-sided training (supervised fine-tuning) caused 'default collapse', leaning 89% toward the trained religious group, and further reduced steerability to 32% and recognition to 19%. However, applying 'recognition tuning' successfully restored steerability to 78% and recognition to 78% while maintaining the newly collapsed default behavior (89%).

