# 🧠 AI Content Engine for E-commerce

An AI-powered content generation tool that helps e-commerce brands create high-converting product descriptions, ad copy, and brand-specific content using a Retrieval-Augmented Generation (RAG) system.

Built with Streamlit and Python.

---

## 🚀 Features

### 📝 Product Description Generator

Generate persuasive product descriptions tailored to a brand’s voice.

Each output includes:
- Hook  
- Benefits  
- Emotional triggers  
- Call-to-action (CTA)  

Multiple variants are generated, and the best one is automatically selected.

---

### 📢 Ad Copy Generator

Create conversion-focused ad copy based on brand context and product input.

Quickly generate multiple variations for testing and marketing campaigns.

---

### ⚔️ Multi-Brand Comparison

Compare how different brands would market the same product.

**Useful for:**
- Competitor analysis  
- Brand positioning  
- Copy inspiration  

---

### 🧠 Brand-Aware AI (RAG)

The system retrieves relevant brand data using a vector store to ensure that all generated content:
- Matches the brand voice  
- Targets the correct audience  
- Aligns with brand positioning  

---

## 🏗️ Tech Stack

- Streamlit  
- Python  
- Retrieval-Augmented Generation (RAG)  
- Vector embeddings & semantic search  
- dotenv for environment configuration  

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
