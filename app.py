import streamlit as st

from backend import detect_news


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fake News Detection",
    page_icon="📰",
    layout="wide"
)


# =====================================================
# LOAD CSS
# =====================================================

with open("style.css", "r", encoding="utf-8") as f:

    st.markdown(
        "<style>" + f.read() + "</style>",
        unsafe_allow_html=True
    )


# =====================================================
# MOVING BACKGROUND NEWS
# =====================================================

st.markdown(
    '<div class="news-bg">'
    '<div class="news-row row1">'
    'BREAKING NEWS • AI TECHNOLOGY • GLOBAL UPDATE • DIGITAL NEWS • '
    'BREAKING NEWS • AI TECHNOLOGY • GLOBAL UPDATE •'
    '</div>'

    '<div class="news-row row2">'
    'LATEST UPDATE • WORLD NEWS • TECHNOLOGY NEWS • '
    'VERIFY BEFORE YOU SHARE • LATEST UPDATE • WORLD NEWS •'
    '</div>'

    '<div class="news-row row3">'
    'NEWS ALERT • FACT CHECK • TODAY NEWS • IMPORTANT UPDATE • '
    'NEWS ALERT • FACT CHECK • TODAY NEWS •'
    '</div>'

    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# SMALL NEWSPAPERS IN BACKGROUND
# =====================================================

st.markdown(
    '<div class="background-papers">'

    '<div class="mini-paper mini1">'
    'THE DAILY<br>'
    '<b>BREAKING NEWS</b><br>'
    'Latest Update'
    '</div>'

    '<div class="mini-paper mini2">'
    'NEWS TODAY<br>'
    '<b>WORLD NEWS</b><br>'
    'Fact Check'
    '</div>'

    '<div class="mini-paper mini3">'
    'DAILY TIMES<br>'
    '<b>AI NEWS</b><br>'
    'Technology'
    '</div>'

    '<div class="mini-paper mini4">'
    'NEWS ALERT<br>'
    '<b>TOP STORY</b><br>'
    'Verified News'
    '</div>'

    '<div class="mini-paper mini5">'
    'THE TRUTH<br>'
    '<b>NEWS UPDATE</b><br>'
    'Read Carefully'
    '</div>'

    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# MAIN TITLE
# =====================================================

st.markdown(
    '<div class="main-title">'
    '📰 Fake News Detection'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="tagline">'
    'AI-Powered News Verification System'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# MAIN COLUMNS
# =====================================================

left, right = st.columns(
    [1, 2],
    gap="large"
)


# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.markdown(
        '<div class="info-box">'

        '<h2>🔍 What We Do?</h2>'

        '<p>'
        'Fake News Detection System helps users analyze news '
        'and identify whether the information is likely to be '
        '<b>REAL</b> or <b>FAKE</b>.'
        '</p>'

        '<p>'
        'Enter a news headline or article and our AI system '
        'analyzes the information to provide a prediction.'
        '</p>'

        '<div class="feature">'
        '⚡ Fast Analysis'
        '</div>'

        '<div class="feature">'
        '🤖 AI Based Detection'
        '</div>'

        '<div class="feature">'
        '📰 News Verification'
        '</div>'

        '</div>',

        unsafe_allow_html=True
    )


# =====================================================
# RIGHT SIDE - NEWSPAPER PREVIEW
# =====================================================

with right:

    st.markdown(
        '<div class="news-box">'

        '<h2>🗞️ News Verification</h2>'

        '<div class="papers">'

        # =============================================
        # REAL NEWSPAPER
        # =============================================

        '<div class="paper">'

        '<div class="paper-name">'
        'THE DAILY TRUTH'
        '</div>'

        '<div class="date">'
        'TRUSTED NEWS • 2026'
        '</div>'

        '<div class="line"></div>'

        '<h3>'
        'Breaking News'
        '</h3>'

        '<p>'
        'Scientists announce a major discovery '
        'that could change the future of technology.'
        '</p>'

        '<div class="real-stamp">'
        '✓ REAL'
        '</div>'

        '<div class="paper-footer">'
        'VERIFIED NEWS'
        '</div>'

        '</div>'


        # =============================================
        # FAKE NEWSPAPER
        # =============================================

        '<div class="paper">'

        '<div class="paper-name">'
        'DAILY ALERT'
        '</div>'

        '<div class="date">'
        'DAILY NEWS • 2026'
        '</div>'

        '<div class="line"></div>'

        '<h3>'
        'Shocking News!'
        '</h3>'

        '<p>'
        'Government announces free smartphones '
        'for every citizen starting tomorrow.'
        '</p>'

        '<div class="fake-stamp">'
        '✕ FAKE'
        '</div>'

        '<div class="paper-footer">'
        'SUSPICIOUS NEWS'
        '</div>'

        '</div>'

        '</div>'

        '</div>',

        unsafe_allow_html=True
    )


# =====================================================
# INPUT SECTION
# =====================================================

st.markdown(
    '<div class="input-title">'
    '📝 Check Your News'
    '</div>',
    unsafe_allow_html=True
)


news = st.text_area(
    "News",
    placeholder=(
        "Paste your news headline or article here..."
    ),
    height=150,
    label_visibility="collapsed"
)


# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button(
    "🔍 ANALYZE NEWS",
    use_container_width=True
):
    # CHECK EMPTY INPUT
    if news.strip() == "":

        st.warning(
            "⚠️ Please enter some news first."
        )


    else:

        # =========================================
        # CALL BACKEND
        # =========================================

        prediction, reason, error_text = detect_news(news)


        # =========================================
        # ERROR
        # =========================================

        if error_text:

            if "503" in error_text:

                st.error(
                    "⚠️ Gemini server is currently busy. "
                    "Please try again after a few minutes."
                )

            else:

                st.error(
                    "❌ Gemini API connection error."
                )

            st.caption(
                error_text
            )


        # =========================================
        # SHOW RESULT
        # =========================================

        else:

            if prediction == "FAKE":

                st.error("❌ FAKE NEWS")


            elif prediction == "REAL":

                st.success("✅ REAL NEWS")


            else:

                st.warning("⚠️ UNCERTAIN NEWS")


            st.markdown(
                f"**Prediction:** {prediction}"
            )


            st.markdown(
                f"**Reason:** {reason}"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    '<div class="footer">'

    '<div class="footer-title">'
    '📰 Fake News Detection System'
    '</div>'

    '<div>'
    'Developed by '
    '<b>Saumya Singh & Shruti Tiwari</b>'
    '</div>'

    '<div class="footer-small">'
    'AI-Powered News Verification'
    '</div>'

    '</div>',

    unsafe_allow_html=True
) 