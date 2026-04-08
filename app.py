import streamlit as st
from dotenv import load_dotenv
import os

# Utils
from utils.functions import load_brand_data
from utils.functions import create_vectorstore
from utils.functions import get_context
from utils.functions import parse_brand_data
from utils.functions import generate_variants
from utils.functions import pick_best

# ----------------------------
# LOAD ENV + Data folder
# ----------------------------
load_dotenv()
DATA_FOLDER = os.getenv("DATA_FOLDER")

# ----------------------------
# PAGE CONFIG (MUST BE FIRST)
# ----------------------------
st.set_page_config(page_title="AI Content Engine", page_icon="🧠")
st.title("🧠 AI Content Engine for E-commerce")

# ----------------------------
# BRAND SYSTEM
# ----------------------------
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
tab1, tab2, tab3 = st.tabs(["📝 Product Description", "📢 Ad Copy", "⚔️ Brand Comparison"])

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

with tab3:
    st.subheader("⚔️ Multi-Brand Comparison")

    product_name_cmp = st.text_input("Product Name", key="cmp_product")
    category_cmp = st.text_input("Category",key="cmp_category")
    features_cmp = st.text_area("Features",key="cmp_features")

    selected_brands = st.multiselect(
        label="Select Brands to Compare", 
        options=brands, 
        default=brands[:2])
    
    if st.button("Compare Brands 🚀"):
        if not selected_brands:
            st.warning("Select at least one brand")
            st.stop()

        results = {}
        with st.spinner("Generating for multiple brands..."):
            for brand in selected_brands:
                
                # Load brand data
                brand_text = load_brand_data(brand)
                vectorstore = create_vectorstore(brand_text)

                # Get context/chunks
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                docs = retriever.invoke(product_name_cmp)
                context = "\n".join([doc.page_content for doc in docs])

                # Prompt
                prompt = f"""
                You are an expert e-commerce copywriter.

                Brand context:
                {context}

                Write a HIGH-CONVERTING product description.

                Product: {product_name_cmp}
                Category: {category_cmp}
                Features: {features_cmp}

                Adapt tone to match the brand voice.

                Include:
                - Hook
                - Benefits
                - Emotional triggers
                - CTA
                """
                variants = generate_variants(prompt)
                best = pick_best(variants)
                results[brand] = best
        
        st.markdown("## 🔥 Comparison Results")
        cols = st.columns(len(results))
        for i, (brand, text) in enumerate(results.items()):
            with cols[i]:
                st.markdown(f"### 🏷 {brand}")
                st.success(text)


# ----------------------------
# Preview
# ----------------------------
brand_text = load_brand_data(brand_name=selected_brand)
brand_data = parse_brand_data(brand_text)

st.info(f"Currently generating content for: {brand_data.get('Brand Name','Unknown Brand')}")

col1,col2 = st.columns(2)
with col1:
    st.markdown("### 🧠 Brand Voice")
    st.write(brand_data["Brand Voice"])
with col2:
    st.markdown("### 🎯 Target Audience")
    st.write(brand_data["Target Audience"])

st.markdown("### 🛍 Products")
for p in brand_data["Products"]:
    st.write(f"- {p}")