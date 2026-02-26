# Multi-Head Attention

## Result Snapshot

Multi-Head Attention extends self-attention by running multiple attention mechanisms in parallel, allowing the model to capture different types of relationships in the same sequence.

It improves representation power without increasing model depth.

---

## Definition

Multi-head attention splits the embedding into multiple subspaces (heads), performs self-attention independently on each head, and then concatenates the results.

Formally:

    MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W_O

Where each head is defined as:

    head_i = Attention(QW_Q^i, KW_K^i, VW_V^i)

---

## Intuition

A single attention mechanism may focus on only one type of relationship.

Example in a sentence:

- One head may focus on grammatical structure.
- One head may focus on subject-object relationships.
- One head may focus on long-range dependencies.
- One head may focus on local context.

Multi-head attention allows the model to learn multiple perspectives simultaneously.

---

## Mechanism

1. Input embeddings are projected into:
   - Q (Query)
   - K (Key)
   - V (Value)

2. Instead of one projection, we create multiple projection matrices:
   - W_Q^1, W_Q^2, ..., W_Q^h
   - W_K^1, W_K^2, ..., W_K^h
   - W_V^1, W_V^2, ..., W_V^h

3. Each head performs scaled dot-product attention independently.

4. The outputs of all heads are concatenated.

5. A final linear projection W_O combines them.

---

## Why Multiple Heads?

If we only use one attention head:

- The model learns a single representation subspace.
- Limited diversity in attention patterns.

With multiple heads:

- Each head operates in a lower-dimensional space.
- The model captures richer relationships.
- Parallel attention increases expressiveness.

---

## Dimensionality

If:

    d_model = 512
    num_heads = 8

Then each head operates in:

    d_k = 512 / 8 = 64 dimensions

This keeps total computation similar to single-head attention.

---

## Complexity

Time Complexity: O(n²)
Space Complexity: O(n²)

The quadratic cost comes from attention, not the number of heads.

Multi-head does not change asymptotic complexity.

---

## Advantages

- Captures diverse relationships
- Improves representation learning
- Maintains parallel computation
- Empirically improves performance

---

## Limitations

- Still quadratic in sequence length
- More parameters
- Harder to interpret individual heads
- Some heads may become redundant

---

## Common Misconceptions

- Multi-head attention does not reduce complexity.
- It does not increase sequence length capacity.
- It is not the same as stacking multiple attention layers.

---

## Follow-Up Questions

- Why does increasing number of heads sometimes hurt performance?
- How does head pruning work?
- What is the difference between multi-head attention and grouped-query attention?
- How is multi-head attention implemented efficiently on GPUs?