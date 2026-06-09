# 🧠 AI Content Engine for E-commerce

A production-inspired AI content generation system that helps e-commerce brands create high-converting product descriptions, ad copy, and brand-aligned marketing content using Retrieval-Augmented Generation (RAG).

Built with Python and Streamlit, the system combines LLM reasoning with semantic brand retrieval to ensure consistent, context-aware content generation.

---

## 🚀 Key Features

### 📝 Product Description Generator
Generates persuasive, conversion-focused product descriptions tailored to a specific brand voice.

Each output includes:
- Hook
- Key benefits
- Emotional triggers
- Call-to-action (CTA)

Multiple variants are generated and ranked to select the most effective version.

---

### 📢 Ad Copy Generator
Creates high-conversion marketing copy for ads across different platforms.

Supports:
- Multiple copy variations
- Tone adaptation based on brand context
- Quick iteration for A/B testing

---

### ⚔️ Multi-Brand Comparison Engine
Enables comparison of how different brands would market the same product.

Useful for:
- Competitor analysis
- Brand positioning insights
- Copywriting inspiration

---

### 🧠 Brand-Aware RAG System
A Retrieval-Augmented Generation pipeline ensures all outputs are grounded in brand-specific context.

The system retrieves relevant brand information from a vector database to ensure:
- Consistent brand voice
- Audience alignment
- Context-aware marketing messaging

---

## 🏗️ System Architecture

User Input (Product / Brand Query)  
→ Streamlit UI  
→ Query Processing Layer  
→ Embedding-Based Retrieval (Vector Store)  
→ Context Injection (RAG Layer)  
→ LLM Content Generator  
→ Output Ranking & Selection  
→ Final Marketing Content

---

## ⚙️ Tech Stack

- Python
- Streamlit
- Retrieval-Augmented Generation (RAG)
- Vector embeddings & semantic search
- LLM APIs (OpenAI / similar)
- dotenv for environment configuration

---

## 🧩 Design Principles

- Brand context always grounded via retrieval (RAG-first design)
- LLM used as reasoning + generation engine
- Modular pipeline for easy extension
- Separation of retrieval, generation, and ranking layers
- Optimized for marketing and e-commerce workflows

---

## 📂 Project Structure

```bash
project/
│── app.py
│── utils/
│   ├── functions.py
│── data/
│   ├── brand1.txt
│   ├── brand2.txt
│── .env
