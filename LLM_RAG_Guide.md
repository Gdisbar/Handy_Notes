
---

# 1) One-minute elevator 

* **LLMs = large Transformer-based decoder models** trained on massive unsupervised corpora; they’re *foundation models* you adapt via prompting, retrieval, or fine-tuning.

---

# 2) Quick model-selection checklist (how to pick a model)

1. **Requirement**: zero-shot chat, code, or high-safety domain?

   * Chat + safety → GPT-4 / Claude family.
   * Code-heavy → StarCoder, CodeGemma, Phind-70B.
   * On-device / small latency → Mistral 7B, Phi family, MobileLLM.
2. **Budget & infra**: big models = higher cost/latency; prefer smaller models + RAG if you need domain knowledge.
3. **License & openness**: Llama variants and many open models offer self-hosting; check license before productizing. ([aman.ai][1])

---

# 3) Core industry patterns (short, say-it-like-you-use-it)

* **Prompting (no training)** — fastest to iterate; use for prototypes and low-budget tasks.
* **RAG (Retrieval-Augmented Generation)** — best when you need up-to-date or private knowledge without re-training. (See recipe below.) ([aman.ai][1])
* **Fine-tuning / Instruction-tuning / LoRA / QLoRA** — for custom behaviors, domain adaptation, or cost reduction at inference (LoRA keeps base model frozen, small adapters).
* **Hybrid**: base model + RAG + small RLHF/Instruction-tuning for safety and alignment.

---

# 4) RAG — industry recipe (the single most practical pattern)

Goal: make an LLM answer with accurate, up-to-date, private info.

Step-by-step cookbook:

1. **Source selection**: choose high-quality docs (SOPs, KB, product docs).
2. **Preprocessing**: chunk documents to ~500–1,500 tokens (overlap 10–20%). Keep chunks semantically coherent (paragraph boundaries).
3. **Embeddings**: compute embeddings for each chunk and store in a vector DB (Milvus, Pinecone, Weaviate).
4. **Indexing**: configure vector DB with metric (cosine/dot), metadata (source, chunk id, title).
5. **Retrieval**: on query, embed query → nearest neighbors → filter by recency/source.
6. **Prompt assembly**: template:

   ```
   <Instruction>
   Use ONLY the following retrieved context. If the answer isn't in the context, say "I don't know".
   Context:
   <doc1_excerpt>
   <doc2_excerpt>
   Question:
   <user question>
   ```

   Limit total context tokens to model’s window; include provenance (source ids).
7. **Post-process**: validate / hallucination check (e.g., verify facts against sources), attach citations.
8. **Monitoring**: log queries + retrieved docs + final answer for drift and evaluation.

Practical tips:

* Prefer **top-k** retrieval + *reranking* (embedding similarity → cross-encoder rerank if latency budget allows).
* For long documents, chunk smaller; for short factual docs (APIs), larger chunks ok. ([aman.ai][1])

---

# 5) Prompt engineering — quick practical knobs

* **System/instruction prompt**: set role, constraints, output format.
* **Chain-of-Thought vs. Direct**: only request chain-of-thought in private evaluation (safety); use structured steps otherwise (“Step 1: … Step 2: …”).
* **Few-shot**: provide 2–5 examples if model struggles; place examples in instruction area.
* **Temperature/top_p**: temperature ~0–0.4 for factual tasks; 0.7+ for creative.
* **Max tokens & stop sequences**: constrain to avoid runaways.
* **Tooling**: use prompt templates + placeholders, and put retrieval output *before* the user question in the prompt. ([aman.ai][1])

---

# 6) Fine-tuning vs prompting vs RAG — when to choose

* **Prompting**: fast, cheap, no infra changes. Use if you can accept occasional hallucinations and the knowledge is general.
* **RAG**: best for private/up-to-date corpora with moderate infra complexity.
* **Fine-tuning / LoRA**: use if you need consistent style/behavior, offline adaptation, or to reduce prompt-engineering brittleness. LoRA/QLoRA are preferred for adapter-style low-cost tuning. ([aman.ai][1])

---

# 7) Production & infra tips (deployment checklist)

* **Quantization**: use 8-bit/4-bit quantization to reduce memory. Test quality drop.
* **FlashAttention / optimized kernels**: huge speed wins; use vendor libraries.
* **Multi-query attention (MQA)**: reduces memory for large batch serving.
* **Context caching**: cache embeddings for repeated queries / partial prompts.
* **Batching & async inference**: increase throughput; but respect latency SLAs.
* **Safety layer**: integrate content filters and reject unsafe outputs upstream. ([aman.ai][1])

---

# 8) Hallucination & evaluation — practical controls

* **Prevention**: RAG with provenance + prompt “If not in sources, say you don’t know.”
* **Detection**: automatic fact-checkers, model self-critique prompts, cross-check with external APIs.
* **Metrics to track**: accuracy/precision, factuality, helpfulness (human eval), latency, cost per 1k tokens, hallucination rate. ([aman.ai][1])

---

# 9) Context window scaling — what matters (short list)

* If long context is core: prefer **Long-context models** or engineering tricks: chunking + retrieval, positional interpolation (RoPE scaling), sparse attention, or models designed for 1M tokens. For most products, RAG + context extension techniques beat training a truly ultra-long model. ([aman.ai][1])

---

# 10) Quick list: popular models & where to mention them

* **GPT family** — best generalist (chat + reasoning).
* **Llama / Llama2/3** — self-hostable foundation models.
* **Mistral** / **Mixtral** — performant smaller models.
* **Falcon** — open, strong on many tasks.
* **Claude** — safety+long context focus.
* **StarCoder / Code models** — code generation.
  Mention these and their tradeoffs (license, cost, self-host vs API) in interviews. ([aman.ai][1])

---

# 11) One-page checklist 

* What pattern would you choose (Prompt / RAG / Fine-tune)? — state reasons.
* If RAG: list chunk size, embedding model, vector DB, top-k, rerank step.
* If fine-tuning: mention LoRA/QLoRA to save cost.
* For production: mention quantization, FlashAttention, caching, and monitoring for hallucination.
* For evaluation: state clear metrics and human evaluation plan.

---

# 12) Short QnA (snippets)

* **Q: How do you reduce hallucinations?**
  A: Use RAG with provenance, conservative prompts ("answer only if supported"), reranking, and post-hoc verification. ([aman.ai][1])
* **Q: When to fine-tune?**
  A: When you need persistent behavior/style and have sufficient domain data; else RAG + prompt engineering. ([aman.ai][1])
* **Q: How to serve low-latency LLMs?**
  A: Use smaller distilled models, quantize, use optimized kernels (FlashAttention), serve on GPUs with batching & cached context. ([aman.ai][1])

---
---


[1]: https://aman.ai/primers/ai/LLM/ "Aman's AI Journal • Primers • Overview of Large Language Models"

---
---
---

# **📘 LLM / RAG Production Cheat Sheet**

---

# **1. Monitoring LLM/RAG Systems (What & Why)**

LLMs degrade silently — monitoring is **mandatory**.

### **What to log**

* **User Query** (raw + normalized)
* **Retrieved Chunks**:

  * chunk IDs
  * similarity scores
  * source document
  * timestamp / version
* **Final Prompt assembled for LLM**
* **LLM Output** + citations / refusal phrases
* **Retrieval pipeline metadata** (top-k, reranker scores)
* **Latency metrics** (DB + reranker + model)
* **Safety flags**
* **Token usage & cost**

### **Metrics to track**

* Retrieval precision@k
* Avg similarity per retrieval
* Irrelevant retrieval %
* Answer correctness (based on eval set)
* Hallucination rate (unsupported claims)
* Latency P50/P95/P99
* Cost per query
* Safety violation rate

### **Drift signals & reactions**

* ↓Average similarity → **Re-embed documents**, adjust chunking.
* ↑Hallucinations → **Tighten RAG prompt**, add reranker, or reduce top-k.
* ↑Latency → optimize batching, caching, vector DB index.

---

# **2. Retrieval Optimization: Top-K + Reranking**

Two-stage retrieval is standard in industry.

### **Stage 1 — Vector Search (Fast, approximate)**

* Retrieve **top-k = 10–50** candidates using embeddings.

### **Stage 2 — Reranker (Slow, accurate)**

* Cross-encoder ranks (query, chunk) pairs.
* Select **top 3–5** final chunks.

### **Rules of thumb**

* Use reranker if latency budget ≥ **200–400ms**.
* If corpus is noisy / long documents → reranker is **mandatory**.
* If ultra-low latency required → reduce k or remove reranker.

### **Benefits**

* Less hallucination
* Higher semantic precision
* More stable answers across paraphrased queries

---

# **3. Context Caching (Major performance lever)**

### **A) Embedding Cache**

Avoid recomputing embeddings.

Cache key =

```
hash(raw_text) + embedding_model_version
```

Useful for:

* Repeated queries
* Repeat document chunks
* Semantic caching (find similar queries via nearest neighbor)

Huge cost saver.

---

### **B) KV-Cache (Model attention cache)**

Transformer stores keys/values of previous tokens.

Used for:

* Chat histories
* Streaming generation
* Long prompts with shared prefix
* Multi-turn RAG sessions

Boosts speed by **5–20×** depending on prompt length.

---

### **C) Retrieval Cache**

For high-traffic systems:

* Cache `(query_embedding → top-k results)`
* Invalidate when corpus updates
* Use cosine similarity threshold > 0.9 for “near duplicate” queries

Result: **instant RAG** for repeated questions.

---

# **4. Batching & Async Inference (Serving Efficiency)**

### **Why batching?**

GPUs love parallelism.
One batch forward-pass = handle many users at same cost as one.

### **How batching works**

1. Incoming requests enter async queue
2. Server groups requests into a batch (tokens × requests)
3. Single forward pass
4. Responses streamed per-user

### **Advantages**

* Higher throughput
* Lower per-request GPU cost
* Great for SaaS-load patterns

### **Operational knobs**

* **Max batch delay = 5–10 ms** (controls P99 latency)
* **Dynamic batching** based on model load
* Use **vLLM, SGLang, TGI, Triton** for optimized serving

---

# **5. Safety Layer (Enterprise Standard)**

### **1) Input / Query Filtering (Before LLM)**

Detect and block:

* Toxicity
* Harassment
* PII
* Self-harm
* Prompt injection attempts
* Jailbreak patterns

Tools:

* Llama Guard
* OpenAI Moderation
* Detoxify

---

### **2) Output Filtering (After LLM)**

Re-evaluate LLM result:

* Remove PII
* Remove unsafe content
* Replace with fallback message if needed

---

### **3) Optional: LLM Self-Critique Step**

LLM reviews its own response:

* “Is this answer safe and grounded?”
* Regenerate if unsafe or ungrounded

---

# **6. Long-Context Engineering**

### **1. Chunking + Retrieval (Always Default)**

Stuffing 200k tokens in context ≠ reliable.
Best practice:

* Chunk text into **500–1500 token** coherent blocks
* Add 10–20% overlap
* Retrieve only relevant chunks via RAG

Handles long documents far better than giant context windows.

---

### **2. RoPE Scaling (Positional Interpolation)**

Models like Llama/Mistral use RoPE.
You can scale rotary embeddings to extend context length:

* No retraining
* Minor quality drop
* Supported in HF + inference libraries

---

### **3. Sparse Attention**

Reduces quadratic attention cost.

Patterns:

* Sliding-window
* Dilated attention
* Global attention tokens

Used by Longformer, BigBird, Mistral.

---

### **4. Segment-level Recurrence**

Process long documents by:

* Encoding chunks sequentially
* Passing a recurrent “state”
* Used in Transformer-XL, RWKV, Hyena models

Makes very long sequences manageable.

---

# **7. Production Optimizations**

### **FlashAttention**

* Optimized attention kernel
* Avoids large intermediate softmax matrices
* Gives **2–4× speedup** and lower GPU RAM usage
* Built into vLLM, TGI, SGLang, newer PyTorch versions

---

### **Caching (All Layers)**

* **KV-cache**: speeds long prompts
* **Embedding cache**: avoids recomputation
* **Retrieval cache**: speeds repeated queries

Caching = **most important** latency reduction technique.

---

### **Hallucination Monitoring**

Track:

* Unsupported claims
* Mismatch between answer content vs retrieved chunks
* Lack of citations
* “Confident but wrong” patterns

Techniques:

* LLM self-verification
* Second-model verifier
* Retrieval-based fact matching

---

# **8. Evaluation Framework (Industry Standard)**

### **Categories**

#### **1. Correctness**

* Factual accuracy
* Groundedness (based only on retrieved chunks)
* Hallucination rate

#### **2. Retrieval Metrics**

* Precision@k
* Coverage of relevant sources
* Similarity score distribution

#### **3. LLM Output Metrics**

* Clarity & format adherence
* Consistency
* Task success rate

#### **4. Performance**

* P50 / P95 / P99 latency
* Tokens/sec
* Throughput
* Cost per 1k tokens

#### **5. Safety**

* Toxicity rate
* PII leakage rate
* Prompt-injection success rate

---

# **Evaluation Process**

1. **Golden Dataset (300–1000 Qs)**

   * Manually validated
   * Run before every deployment

2. **A/B Testing**

   * Compare retrieval configs
   * Compare model versions
   * Measure resolution rate uplift

3. **Regular Human Review**

   * Weekly or bi-weekly sampling
   * Look for hallucinations + safety issues

4. **Continuous Monitoring**

   * Use live logs to detect drift
   * Flag sudden behavior changes





