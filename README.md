# Interview-Copilot

A Retrieval-Augmented Generation (RAG) based mock interview assistant 
that generates structured explanations and verified Python solutions 
for technical interview practice.

## Features

- Structured coding answers (idea → code → complexity → pitfalls)
- Concept explanations (definition → intuition → mechanism → trade-offs)
- Retrieval-grounded responses with curated knowledge base
- Router-based question type classification

## Architecture

User Question
    ↓
Router (classify type)
    ↓
Retriever (vector search over curated notes)
    ↓
LLM Generator (structured output format)
    ↓
Answer + Self-check + Follow-up