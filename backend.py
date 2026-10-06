import streamlit as st
from google import genai


# =====================================================
# GEMINI API KEY
# =====================================================

API_KEY = st.secrets["GEMINI_API_KEY"]


# =====================================================
# FAKE NEWS DETECTION FUNCTION
# =====================================================

def detect_news(news):

    try:

        # =============================================
        # GEMINI CLIENT
        # =============================================

        client = genai.Client(
            api_key=API_KEY
        )


        # =============================================
        # PROMPT
        # =============================================

        prompt = f"""
You are an AI news analysis assistant.

Analyze the following news text carefully.

NEWS:
{news}

Give your answer in exactly this format:

Prediction: REAL / FAKE / UNCERTAIN

Reason:
Give a short and simple explanation in 2-3 sentences.

Important rules:

1. Do not pretend that you performed live web fact-checking.
2. If the information cannot be determined reliably,
   choose UNCERTAIN.
3. Do not invent sources or facts.
4. Be careful before calling something REAL or FAKE.
"""


        # =============================================
        # GEMINI API
        # =============================================

        with st.spinner("🔄 Analyzing the news..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )


        # =============================================
        # GET RESPONSE
        # =============================================

        result = response.text.strip()


        # =============================================
        # FIND PREDICTION
        # =============================================

        result_upper = result.upper()


        if "PREDICTION: FAKE" in result_upper:

            prediction = "FAKE"
            icon = "❌"


        elif "PREDICTION: REAL" in result_upper:

            prediction = "REAL"
            icon = "✅"


        else:

            prediction = "UNCERTAIN"
            icon = "⚠️"


        # =============================================
        # FIND REASON
        # =============================================

        if "Reason:" in result:

            reason = result.split(
                "Reason:",
                1
            )[1].strip()


        elif "REASON:" in result:

            reason = result.split(
                "REASON:",
                1
            )[1].strip()


        else:

            reason = result


        return prediction, reason, None


    # =============================================
    # ERROR
    # =============================================

    except Exception as e:

        error_text = str(e)

        return None, None, error_text