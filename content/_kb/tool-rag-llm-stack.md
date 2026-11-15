---
title: "The LLM stack: embeddings, vector databases, RAG"
summary: RAG looks up relevant chunks of your own text and puts them in the prompt, so the model answers from them.
tags: [ml tools, rag, embeddings]
---
- A language model does not know your company's documents, and it can make things up.
- RAG (retrieval-augmented generation): retrieve relevant text, put it in the prompt, answer from it, show sources.
- Indexing is offline: load documents, chunk them, embed each chunk, store vectors with the original text.
- Query is online: embed the question, find the top-k nearest chunks, build the prompt, call the model.
- Key terms: embedding, vector database, chunking, top-k, recall at k, groundedness.
- Retrieval quality limits answer quality. If the right chunk is missing, no prompt fixes it.

<!-- more -->

## Details

- **Embedding**: a vector that represents the meaning of a text. Similar texts have similar vectors.
- **Vector database**: stores embeddings and finds the nearest ones fast. Examples are Pinecone, Weaviate, Qdrant, Chroma and pgvector.
- **Chunking**: cutting long documents into smaller pieces before embedding.
- **Framework**: LangChain and LlamaIndex wire these steps together.

Chunk size and overlap are tuning knobs. Too small loses context. Too large adds noise and tokens. Overlap keeps a sentence from being cut at the border.

Evaluation has no simple accuracy number:

- Keep a small fixed set of questions with expected answers or sources.
- Evaluate retrieval separately: is the right chunk in the top k (recall at k)?
- Evaluate generation: is the answer grounded in the context, and does it refuse when the context lacks the answer?

## What to say and what not to claim

Say: "RAG retrieves relevant text, puts it in the prompt and answers from it with sources. I evaluate retrieval and generation separately, with a fixed test set."

Do not claim production experience with a specific vector database or framework if you have not used it. Do not say RAG removes hallucination. It reduces it.

## Likely interview questions

- **Why RAG instead of fine-tuning?** It is cheaper, easy to update by changing the index, and can cite sources; fine-tuning is better for style or behaviour.
- **How would you choose the chunk size?** Start with a few hundred tokens and some overlap, then measure recall at k on a test set.
- **How do you know the system answers well?** A fixed question set, retrieval and groundedness checks rerun on every change, plus a hand review of a sample.

## See also

- [Embeddings, cosine similarity and top-k retrieval](#/kb/ai-embeddings-topk)
- [Chunking text with overlap](#/kb/ai-chunking)
- [A tiny evaluation harness](#/kb/ai-eval-harness)
