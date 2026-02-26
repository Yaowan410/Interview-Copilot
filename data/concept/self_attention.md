# Self-Attention

## Result Snapshot

Self-attention is a mechanism that allows a model to dynamically weigh the importance of different tokens in a sequence when computing representations.

It is the core building block of Transformer models.

---

## Definition

Self-attention is a function that maps a sequence of input embeddings to a new sequence of embeddings by computing weighted sums of all tokens, where the weights are determined by similarity scores between tokens.

---

## Intuition

When reading a sentence, the meaning of a word depends on other words.

Example:

"The animal didn't cross the street because it was too tired."

The word "it" refers to "animal".  
Self-attention helps the model learn that relationship.

Instead of processing tokens sequentially like RNNs, self-attention allows every token to look at every other token.

---

## Mechanism

Each input token embedding is projected into three vectors:

- Query (Q)
- Key (K)
- Value (V)

Steps:

1. Compute similarity score between Q and K:
   
   score = Q · Kᵀ

2. Scale by √d_k to stabilize gradients:

   scaled_score = (Q · Kᵀ) / √d_k

3. Apply softmax to obtain attention weights.

4. Multiply weights by V to get weighted sum.

Final output:

    Attention(Q, K, V) = softmax(QKᵀ / √d_k) V

---

## Example (Simplified)

Suppose we have 3 tokens:

    X1, X2, X3

Each token produces Q, K, V vectors.

If X1 strongly matches X2 (high dot product), then X1 will attend more to X2.

The output representation of X1 becomes a weighted combination of all V vectors.

---

## Why Scaling by √d_k?

Without scaling, dot products grow large in high dimensions.
Large values push softmax into extreme regions, causing small gradients.

Dividing by √d_k stabilizes training.

---

## Complexity

Time Complexity: O(n²)
Space Complexity: O(n²)

Because each token attends to every other token.

---

## Advantages

- Fully parallelizable
- Captures long-range dependencies
- No recurrence required
- Flexible context modeling

---

## Limitations

- Quadratic complexity for long sequences
- High memory usage
- Requires large data to train effectively

---

## Common Misconceptions

- Self-attention is not just dot product; it includes scaling and softmax.
- Attention is not explanation; high attention weight does not guarantee causal importance.
- Transformer = Self-attention + Feedforward + LayerNorm + Residual connections.

---

## Follow-Up Questions

- What is multi-head attention?
- Why do we need positional encoding?
- How does self-attention differ from cross-attention?
- How can we reduce O(n²) complexity?