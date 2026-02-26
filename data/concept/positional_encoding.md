# Positional Encoding

## Result Snapshot

Positional Encoding is a technique used in Transformers to inject information about the position of tokens in a sequence, since self-attention alone has no notion of order.

Without positional encoding, the Transformer would treat the input as a bag of tokens.

---

## Definition

Positional encoding is a vector added to token embeddings to provide information about token position within a sequence.

It enables the model to understand word order in a fully parallel architecture.

---

## Intuition

Self-attention processes all tokens simultaneously and does not inherently know:

- Which token comes first
- Which token comes later
- Relative distances between tokens

Example:

The sentences:

    "dog bites man"
    "man bites dog"

Contain the same words but different meanings.

Without positional encoding, the model cannot distinguish them.

---

## Mechanism

In the original Transformer paper, positional encoding is defined using sine and cosine functions:

For position `pos` and dimension `i`:

    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

Where:
- `pos` = token position
- `i` = embedding dimension index
- `d_model` = embedding dimension

These encodings are added to token embeddings:

    final_embedding = token_embedding + positional_encoding

---

## Why Sine and Cosine?

1. Allows model to generalize to longer sequences.
2. Encodes relative position information.
3. Different frequencies capture both short and long-range relationships.
4. Smooth and continuous function.

---

## Learned Positional Encoding

Instead of fixed sine/cosine, some models use:

- Learnable position embeddings
- Each position has a trainable vector

This allows the model to adapt positional information during training.

---

## Complexity

Time Complexity: O(n)  
Space Complexity: O(n × d_model)

Positional encoding is computed once per sequence.

---

## Advantages

- Preserves order information
- Works with fully parallel computation
- No recurrence required
- Can generalize (fixed version)

---

## Limitations

- Fixed sinusoidal encoding may not be optimal for all tasks
- Learned encoding does not generalize beyond trained sequence length
- Still limited by self-attention quadratic complexity

---

## Common Misconceptions

- Positional encoding is not part of self-attention computation.
- It does not change attention formula directly.
- It is added before attention, not applied inside softmax.

---

## Follow-Up Questions

- What is the difference between absolute and relative positional encoding?
- How does Rotary Positional Encoding (RoPE) work?
- Why do modern LLMs prefer RoPE?
- How does positional encoding affect long-context performance?