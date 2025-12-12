
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



