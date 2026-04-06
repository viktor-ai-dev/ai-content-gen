import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# LangChain (stable imports)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# ----------------------------
# LOAD ENV + CLIENT
# ----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# PAGE CONFIG (MUST BE FIRST)
# ----------------------------
st.set_page_config(page_title="AI Content Engine", page_icon="🧠")
st.title("🧠 AI Content Engine for E-commerce")

# ----------------------------
# FUNCTIONS
# ----------------------------
def generate_text(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return res.choices[0].message.content


def generate_variants(prompt, n=3):
    return [generate_text(prompt) for _ in range(n)]


def score_output(text):
    score = 0
    if "!" in text:
        score += 1
    if "you" in text.lower():
        score += 1
    if len(text) > 200:
        score += 1
    return score


def pick_best(outputs):
    scored = [(text, score_output(text)) for text in outputs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]


def get_context(query):
    if st.session_state["vectorstore"] is None:
        return ""

    db = st.session_state["vectorstore"]
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    return "\n".join([doc.page_content for doc in docs])


def load_brand_data(brand_name):
    with open(f"{DATA_FOLDER}/{brand_name}.txt", "r", encoding="utf-8") as f:
        return f.read()


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
# BRAND SYSTEM
# ----------------------------
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    st.error("❌ 'data' folder not found")
    st.stop()

brands = [f.replace(".txt", "") for f in os.listdir(DATA_FOLDER)]

selected_brand = st.selectbox("Select Brand", brands)

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None
    st.session_state["current_brand"] = None

if selected_brand != st.session_state["current_brand"]:
    brand_text = load_brand_data(selected_brand)
    st.session_state["vectorstore"] = create_vectorstore(brand_text)
    st.session_state["current_brand"] = selected_brand
    st.success(f"Loaded brand: {selected_brand}")


# ----------------------------
# TABS
# ----------------------------
tab1, tab2 = st.tabs(["📝 Product Description", "📢 Ad Copy"])


# ----------------------------
# TAB 1 (FIXED)
# ----------------------------
with tab1:
    st.subheader("📝 Product Description Generator")

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("Product Name", key="prod_name")
        category = st.text_input("Category", key="category")

    with col2:
        tone = st.selectbox(
            "Tone",
            ["Auto (from brand)", "Casual", "Luxury", "Persuasive"],
            key="tone"
        )

    features = st.text_area("Features", key="features")

    st.markdown("---")

    if st.button("🚀 Generate Description"):

        context = get_context(product_name)

        if tone == "Auto (from brand)":
            tone_instruction = "Match the brand voice from context"
        else:
            tone_instruction = tone

        prompt = f"""
        You are an expert e-commerce copywriter.

        Brand context:
        {context}

        Product: {product_name}
        Category: {category}
        Features: {features}
        Tone: {tone_instruction}

        Include:
        - Hook
        - Benefits
        - Emotional triggers
        - CTA
        """

        with st.spinner("Generating..."):
            variants = generate_variants(prompt)
            best = pick_best(variants)

        st.markdown("## 🏆 Best Result")
        st.success(best)

        st.markdown("## 📊 Variants")
        for i, v in enumerate(variants):
            with st.expander(f"Variant {i+1}"):
                st.write(v)

        with st.expander("🧠 Context (RAG)"):
            st.write(context)


# ----------------------------
# TAB 2 (FIXED)
# ----------------------------
with tab2:
    st.subheader("📢 Ad Copy Generator")

    product_name_ad = st.text_input("Product Name", key="ad_product")

    if st.button("Generate Ad"):

        context = get_context(product_name_ad)

        prompt = f"""
        You are an expert ad copywriter.

        Brand context:
        {context}

        Create high-converting ad copy.

        Product: {product_name_ad}
        """

        with st.spinner("Generating..."):
            variants = generate_variants(prompt)
            best = pick_best(variants)

        st.markdown("## 🏆 Best Ad")
        st.success(best)

        st.markdown("## Variants")
        for v in variants:
            st.write(v)
            st.markdown("---")