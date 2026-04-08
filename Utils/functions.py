# LangChain (stable imports)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

# ----------------------------
# LOAD ENV + Data folder + Client
# ----------------------------
load_dotenv()
DATA_FOLDER = os.getenv("DATA_FOLDER")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# Generate Text
# ----------------------------
def generate_text(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return res.choices[0].message.content

# ----------------------------
# Generate Several variants
# using prompt
# ----------------------------
def generate_variants(prompt, n=3):
    return [generate_text(prompt) for _ in range(n)]

# ----------------------------
# Return Score
# ----------------------------
def score_output(text):
    score = 0
    if "!" in text:
        score += 1
    if "you" in text.lower():
        score += 1
    if len(text) > 200:
        score += 1
    return score

# ----------------------------
# Takes variants as input, return best
# ----------------------------
def pick_best(outputs):
    scored = [(text, score_output(text)) for text in outputs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]

# ----------------------------
# Return chunks/context from vectorstore
# ----------------------------
def get_context(query):
    if st.session_state["vectorstore"] is None:
        return ""

    db = st.session_state["vectorstore"]
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    return "\n".join([doc.page_content for doc in docs])

# ----------------------------
# Return brand data
# ----------------------------
def load_brand_data(brand_name):
    with open(f"{DATA_FOLDER}/{brand_name}.txt", "r", encoding="utf-8") as f:
        return f.read()

# ----------------------------
# Create vectorstore
# ----------------------------
def create_vectorstore(text):
    doc = Document(page_content=text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents([doc])

    embeddings = OpenAIEmbeddings()
    return Chroma.from_documents(chunks, embeddings)

# ----------------------------
# Parse brand data into a dictionary 
# below for easy access
# ----------------------------
def parse_brand_data(text: str):
    sections = {
        "Brand Name": "",
        "Brand Voice": "",
        "Target Audience": "",
        "Products": []
    }

    current_section = None

    for line in text.split("\n"):
        line = line.strip()

        # 🔥 Gör allt lowercase för jämförelse
        lower_line = line.lower()

        # ----------------------------
        # BRAND NAME
        # ----------------------------
        if lower_line.startswith("brand name:"):
            sections["Brand Name"] = line.split(":", 1)[1].strip()

        # ----------------------------
        # BRAND VOICE
        # ----------------------------
        elif lower_line.startswith("brand voice:"):
            current_section = "Brand Voice"

        # ----------------------------
        # TARGET AUDIENCE
        # ----------------------------
        elif lower_line.startswith("target audience:"):
            current_section = "Target Audience"

        # ----------------------------
        # PRODUCTS
        # ----------------------------
        elif lower_line.startswith("product:"):
            product_name = line.split(":", 1)[1].strip()
            sections["Products"].append(product_name)

        # ----------------------------
        # CONTENT LINES
        # ----------------------------
        elif current_section and line:
            sections[current_section] += line + " "

    return sections