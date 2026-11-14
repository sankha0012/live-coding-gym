# The LLM stack: embeddings, vector search, RAG, evaluation

## The problem it solves

A language model only knows what was in its training data. It does not know your company's documents, and it can make things up. Retrieval-augmented generation (RAG) fixes this: before asking the model, you look up the most relevant pieces of your own text and put them in the prompt. The model then answers from that text.

The parts:

- Embedding: a list of numbers (a vector) that represents the meaning of a text. Similar texts have similar vectors.
- Vector database: stores embeddings and finds the nearest ones fast. Examples are Pinecone, Weaviate, Qdrant, Chroma and pgvector. For small data, a numpy array is enough.
- Chunking: cutting long documents into smaller pieces before embedding, because one vector for a whole book is too vague.
- Framework: LangChain and LlamaIndex wire these steps together.
- Evaluation: checking that answers are good, since there is no simple accuracy number.

## Where it sits in a pipeline

Two phases. Indexing, done offline: load documents, chunk them, embed each chunk, store vectors with the original text. Query, done online: embed the question, find the top-k nearest chunks, build a prompt with those chunks, call the model, return the answer (often with the sources).

Production concerns: refresh the index when documents change, and watch latency (embedding, search, generation) and per-token cost.

## A minimal real example

This runs with numpy only. The embedding here is a toy word-count vector, so the retrieval is crude, but the shape of the code is the real one. A real system swaps `embed` for a call to an embedding model.

```python
import numpy as np

VOCAB = ["refund", "days", "shipping", "free", "password", "reset", "email"]


def embed(text: str) -> np.ndarray:
    words = text.lower().replace(".", "").replace("?", "").split()
    return np.array([words.count(w) for w in VOCAB], dtype=float)


def chunk(text: str, size: int = 12, overlap: int = 2) -> list[str]:
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / denom) if denom else 0.0


docs = [
    "Refund requests are accepted within 30 days of purchase.",
    "Shipping is free for orders above 50 dollars.",
    "To reset your password, use the reset link sent by email.",
]
chunks = [c for d in docs for c in chunk(d)]
index = np.stack([embed(c) for c in chunks])

query = "How many days do I have for a refund?"
q = embed(query)
scores = [cosine(q, row) for row in index]
top = [chunks[i] for i in np.argsort(scores)[::-1][:1]]
prompt = "Answer using only this context:\n" + "\n".join(top) + f"\n\nQuestion: {query}"
print(prompt)
```

Chunk size and overlap are tuning knobs. Too small loses context. Too large adds noise and tokens. Overlap keeps a sentence from being cut at the border.

A framework does exactly these steps in fewer lines. Its API changes often, so check the current docs.

## Evaluating LLM outputs

You cannot just compute accuracy. Practical approach:

- Build a small fixed set of questions with expected answers or expected source documents. Keep it in version control.
- Evaluate retrieval separately from generation. Retrieval metric: for each question, is the right chunk in the top k (recall at k)? This is plain code and fully deterministic.
- Evaluate generation: does the answer match the facts in the context (groundedness), does it refuse when the context lacks the answer, is the format valid.
- Run the set on every prompt, model or chunking change, like a regression test.

Cost grows with tokens in plus tokens out, so fewer and shorter chunks help. Cache repeated questions, set timeouts and retries with backoff, and log token counts.

## What to say in an interview

- Explain RAG in one breath: retrieve relevant text, put it in the prompt, answer from it, show sources.
- Retrieval quality limits answer quality: if the right chunk is missing, no prompt fixes it.
- Say you evaluate retrieval and generation separately, with a fixed test set.
- Your prompt is judged too: be specific about task, format, constraints and edge cases.

What NOT to claim:

- Do not claim production experience with a specific vector database or framework if you have not used it.
- Do not say RAG removes hallucination. It reduces it.

## Three likely questions

**1. What is RAG and why use it instead of fine-tuning?**
RAG fetches relevant documents at question time and gives them to the model. It is cheaper, easy to update (change the index, not the model), and it can cite sources. Fine-tuning is better for changing style or behaviour, not for adding facts that change.

**2. How would you choose the chunk size?**
Start with a few hundred tokens and some overlap, then measure recall at k on a test set and try other sizes. Use the evaluation, not guesswork. Splitting on headings or paragraphs usually beats a blind cut.

**3. How do you know the system answers well?**
I keep a fixed question set. I measure whether the right chunk is retrieved, and whether the answer is grounded in the context and refuses when it should. I rerun it on every change, and I review a sample by hand, even when an LLM judge is used.
