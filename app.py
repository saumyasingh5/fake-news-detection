
import streamlit as st
from backend import detect_news
from pathlib import Path


st.set_page_config(
    page_title="Fake News Detection",
    page_icon="📰",
    layout="wide"
)


# Load the existing stylesheet
css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )


st.title("📰 Fake News Detection System")

st.write(
    "Analyze a news claim using AI, web search and available "
    "fact-check reports."
)

st.info(
    "The result is an AI-assisted assessment, not a guarantee "
    "of truth. Always check the linked sources."
)


left, right = st.columns(2)

with left:
    st.markdown("### 🔎 How it works")
    st.write("1. Enter a news claim.")
    st.write("2. Search for supporting or contradicting evidence.")
    st.write("3. Review the prediction and source links.")

with right:
    st.markdown("### 🛡️ Prediction guide")
    st.write("**REAL:** Reliable evidence supports the claim.")
    st.write("**FAKE:** Reliable evidence disproves the claim.")
    st.write("**UNCERTAIN:** Evidence is insufficient or conflicting.")


st.markdown("---")
st.subheader("Check a news claim")

news = st.text_area(
    "Paste the news headline or claim here:",
    height=160,
    placeholder=(
        "Example: Paste a news headline, statement, "
        "or an older news claim..."
    )
)

if st.button("🔍 Analyze News", use_container_width=True):
    if not news.strip():
        st.warning("Please enter a news claim first.")
    else:
        prediction, reason, error_text = detect_news(news)

        if error_text:
            st.error(error_text)

        else:
            st.markdown("---")
            st.subheader("📊 Detection Report")

            if prediction == "REAL":
                st.success("MODEL PREDICTION: REAL")
            elif prediction == "FAKE":
                st.error("MODEL PREDICTION: FAKE")
            else:
                st.warning("MODEL PREDICTION: UNCERTAIN")

            st.markdown("### 🤖 AI Explanation")
            st.markdown(reason)

            st.caption(
                "Verification status: Check the evidence and "
                "source links above. A prediction alone is not "
                "confirmed verification."
            )


st.markdown("---")
st.markdown(
    "<div style='text-align:center;'>"
    "Developed by Saumya Singh & Shruti Tiwari"
    "</div>",
    unsafe_allow_html=True
)
