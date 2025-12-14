# System Design

[ML System Design](https://www.youtube.com/watch?v=ZjNoipQAqRM&list=PLrtCHHeadkHqYX7O5cjHeWHzH2jzQqWg5&index=8)

[ML case studies](https://github.com/Engineer1999/A-Curated-List-of-ML-System-Design-Case-Studies)

# FoundationAI

```
!jq 'del(.metadata.widgets)' Source.ipynb > Target.ipynb ## use this one in colab to avoid Github Metadata error
```

[Zero-Transformer BERT](https://www.kaggle.com/code/tanulsingh077/deep-learning-for-nlp-zero-to-transformers-bert)

[Transformers](https://aigents.co/data-science-blog/publication/the-transformers-architecture-in-detail-whats-the-magic-behind-llms)

[Transformer from scratch](https://www.kaggle.com/code/arunmohan003/transformer-from-scratch-using-pytorch)

[Understanding LLM](https://magazine.sebastianraschka.com/p/understanding-large-language-models)

[Build Small LLM](https://www.youtube.com/watch?v=KOXaH7-0gEE)

[Reproduce GPT-2](https://www.youtube.com/watch?v=l8pRSuU81PU)

[Reproduce Deepseek](https://www.youtube.com/playlist?list=PL0ioahleXcwvhkQ1z8ygRQI0EVg38Z0gf)

# Applications

[Google Translate for NLP Augmentation](https://www.kaggle.com/code/tuckerarrants/using-google-translate-for-nlp-augmentation)

[Stock Exchange Prediction](https://www.kaggle.com/code/chumajin/easy-to-understand-the-competition)


# FineTuning


## Github - AWS + GenAI

[AWS Sagemaker Deployment](https://www.youtube.com/watch?v=U72q95dHpRo)

[GenAI+AWS](https://github.com/aws-samples/generative-ai-on-aws-immersion-day)


# GPU Training

[Gemma-2 9b 4-bit QLoRA fine-tuning](https://www.kaggle.com/code/emiz6413/training-gemma-2-9b-4-bit-qlora-fine-tuning)

# Training for custom application 

[Training Small Language Model](https://github.com/AIAnytime/Training-Small-Language-Model/blob/main/Training_a_Small_Language_Model.ipynb)

[Multi-label classification](https://www.kaggle.com/code/owaiskhan9654/multi-label-classification-of-pubmed-articles#-Training-the-model)

[Prompt Prediction - Miztral,Gemma,Llama](https://www.kaggle.com/code/aatiffraz/prompt-prediction-w-mixtral-mistral7b-gemma-llama)

[Code Interpreter Baseline](https://www.kaggle.com/code/huikang/code-interpreter-baseline)

# RAG

[AI-Bank Statement RAG](https://github.com/johnsonhk88/AI-Bank-Statement-Document-Automation-By-LLM-And-Personal-Finanical-Analysis-Prediction)

[Claud Cookbook](https://github.com/anthropics/claude-cookbooks)

[QA-and-RAG-Series](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/)

[Coding Crash Course](https://www.youtube.com/watch?v=yRicPGSGuZE)

https://github.com/NirDiamant/agents-towards-production

https://github.com/NirDiamant/GenAI_Agents


# E2E System 

[End-End Research Agent](https://github.com/jamwithai/arxiv-paper-curator)

[Coffeeshop chatbot](https://www.youtube.com/watch?v=KyQKTJhSIak)

# RL

[RLHF - DPO](https://www.youtube.com/watch?app=desktop&v=aI8cyr-gH6M)

# PPO logging 🧭

| Category                        | Metric                                           | Meaning                                            | Healthy Range / Watch For     |
| ------------------------------- | ------------------------------------------------ | -------------------------------------------------- | ----------------------------- |
| 🎯 **Reward**                   | `env/reward_mean`                                | Avg. reward (performance)                          | ↑ steadily over training      |
|                                 | `env/reward_std`                                 | Reward variability                                 | Moderate; not exploding       |
|                                 | `env/reward_dist`                                | Reward distribution                                | Balanced; no long tails       |
| 🔀 **KL Divergence**            | `objective/kl`                                   | Divergence old↔new policy                          | Small positive (≈ 0.01–0.1)   |
|                                 | `objective/kl_coef`                              | KL penalty coefficient                             | Increases if KL too high      |
|                                 | `ppo/mean_non_score_reward`                      | Mean KL penalty (–KL loss)                         | Should not dominate rewards   |
|                                 | **Watch:**                                       | If KL ↑ → over-optimization; KL ↓ → under-training |                               |
| 🎲 **Entropy**                  | `objective/entropy`                              | Policy randomness                                  | High early → ↓ gradually      |
|                                 | `ppo/policy/entropy`                             | Same (softmax-based)                               | Tracks exploration level      |
| ⚖️ **Policy Stability**         | `ppo/policy/clipfrac`                            | Fraction of clipped ratios                         | < 0.2 ideally                 |
|                                 | `ppo/policy/approxkl`                            | Approx. KL (fast estimator)                        | < 0.01–0.05                   |
|                                 | `ppo/policy/ratio`                               | π_new / π_old                                      | ≈ 1; >200 = unstable          |
|                                 | `ppo/policy/advantages_mean`                     | Avg. GAE advantage                                 | Centered near 0               |
|                                 | `ppo/policy/advantages`                          | Advantage distribution                             | Balanced (not skewed)         |
| 📈 **Value Function**           | `ppo/val/mean`, `ppo/val/var`                    | Predicted values                                   | Stable variance               |
|                                 | `ppo/val/error`                                  | Value MSE vs. returns                              | Should ↓ smoothly             |
|                                 | `ppo/val/var_explained`                          | % variance explained by critic                     | > 0.8 = good                  |
|                                 | `ppo/val/clipfrac`                               | Clipped value updates                              | Low (too high → overfit)      |
|                                 | `ppo/returns/mean`, `ppo/returns/var`            | TD(λ) returns                                      | Check scaling consistency     |
| ⚙️ **Losses**                   | `ppo/loss/policy`                                | Actor loss                                         | Stable, small oscillations ok |
|                                 | `ppo/loss/value`                                 | Critic loss                                        | No NaNs or big spikes         |
|                                 | `ppo/loss/total`                                 | Combined objective                                 | Gradual ↓ trend               |
| ✏️ **Token Stats** *(for RLHF)* | `tokens/queries_len_mean` / `responses_len_mean` | Avg. token length                                  | Monitor for drift             |
|                                 | `tokens/responses_len_std`                       | Variability                                        | Not exploding                 |
| 📊 **Log-Probs**                | `objective/logprobs`, `objective/ref_logprobs`   | Log-probs of actions vs. ref                       | Inspect for shifts            |

# Crucial Values to Remember 🚨

| Metric                | Ideal Behavior             | Problem If                |
| --------------------- | -------------------------- | ------------------------- |
| `objective/kl`        | Small positive (~0.01–0.1) | Too high → instability    |
| `ppo/policy/ratio`    | ≈ 1                        | > 200 → over-optimization |
| `ppo/policy/clipfrac` | < 0.2                      | High → aggressive updates |
| `ppo/loss/value`      | Stable                     | NaN/spikes → bad critic   |
| `env/reward_mean`     | Increasing                 | Plateau → stagnation      |

# Core RL Concepts 🧠

| Term                                       | Definition                                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **Policy (π)**                             | Function mapping states to action probabilities.                                           |
| **Value Function (V(s))**                  | Expected cumulative reward from a state under π.                                           |
| **Advantage (A(s,a))**                     | How much better action *a* is than average at state *s*.                                   |
| **Return (Gₜ)**                            | Discounted sum of future rewards: Σ γⁿ rₜ₊ₙ                                                |
| **Entropy**                                | Randomness in policy — promotes exploration.                                               |
| **KL Divergence**                          | Measures how much new policy diverges from old policy.                                     |
| **Clipping (PPO)**                         | Restricts how much the policy ratio can deviate from 1, to avoid destructive updates.      |
| **GAE (Generalized Advantage Estimation)** | Smoothed advantage estimator balancing bias–variance.                                      |
| **Explained Variance**                     | Fraction of variance in returns explained by the critic — measures value function quality. |

🧩 TL;DR — What to Remember

Reward mean ↑ → Learning works.

KL small & positive → Stable policy updates.

Entropy ↓ slowly → Controlled exploration to exploitation.

Clipfrac < 0.2, ratio ≈ 1 → PPO updates stable.

Value loss steady, explained variance high → good critic.

