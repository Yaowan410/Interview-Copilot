# Transformer Encoder

## Result Snapshot

The Transformer Encoder is a stack of identical layers composed of multi-head self-attention and feedforward networks, designed to process input sequences in parallel while capturing global dependencies.

It is the backbone of models like BERT and many encoder-based architectures.

---

## Definition

A Transformer Encoder layer consists of:

1. Multi-Head Self-Attention
2. Add & Layer Normalization
3. Position-wise Feedforward Network
4. Add & Layer Normalization

Multiple encoder layers are stacked to build deep representations.

---

## High-Level Architecture

For each encoder layer:

Input
   ↓
Multi-Head Self-Attention
   ↓
Add & LayerNorm
   ↓
Feedforward Network (FFN)
   ↓
Add & LayerNorm
   ↓
Output

This structure is repeated N times.

---

## Intuition

The encoder builds contextual representations of tokens.

Step-by-step:

- Self-attention allows each token to gather information from all other tokens.
- Feedforward network transforms the representation non-linearly.
- Residual connections help stabilize training.
- Layer normalization improves gradient flow.

By stacking layers, representations become increasingly abstract.

---

## Multi-Head Self-Attention

Each token attends to all other tokens in the sequence.

Outputs contextual embeddings.

Key idea:
Every token representation is updated based on the full sequence.

---

## Feedforward Network (FFN)

After attention, each token passes through a position-wise feedforward network:

    FFN(x) = max(0, xW1 + b1)W2 + b2

Properties:
- Applied independently to each token
- Increases model capacity
- Adds non-linearity

Typically expands dimension:
    d_model → 4*d_model → d_model

---

## Residual Connection

Instead of:

    y = F(x)

We compute:

    y = x + F(x)

This helps:
- Prevent vanishing gradients
- Enable deep stacking
- Improve optimization

---

## Layer Normalization

LayerNorm normalizes across embedding dimensions.

It stabilizes training and improves convergence.

Different from BatchNorm:
- Works well for sequence models
- Independent of batch size

---

## Complexity

Time Complexity per layer: O(n²)
Space Complexity per layer: O(n²)

Due to self-attention.

Total complexity depends on:
- Sequence length n
- Number of layers L
- Embedding dimension d_model

---

## Advantages

- Fully parallelizable
- Captures long-range dependencies
- Stable deep stacking
- Flexible architecture

---

## Limitations

- Quadratic attention cost
- Memory intensive
- Large training data requirements
- Encoder-only models cannot generate text autoregressively

---

## Common Misconceptions

- Transformer Encoder is not the full Transformer.
- Encoder-only models differ from encoder-decoder models.
- Attention is only one part; FFN is equally important.
- Depth contributes significantly to representation power.

---

## Follow-Up Questions

- What is the difference between Encoder-only and Decoder-only models?
- Why is FFN dimension usually 4x larger than d_model?
- How does pre-layer normalization differ from post-layer normalization?
- How do modern LLMs modify the encoder block?