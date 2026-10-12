import streamlit as st
from auth import init_db, create_user, authenticate_user
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
# LOGIN AND SIGNUP SYSTEM
# =====================================================

init_db()

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if st.session_state.authenticated_user is None:

    st.markdown("""
        <style>
        /* Clean login page background */
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #f4f6fa !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Center the login content */
        [data-testid="stMainBlockContainer"] {
            max-width: 850px;
            padding-top: 2rem;
        }

        /* Login heading */
        h1 {
            color: #10213a !important;
            text-align: center;
            font-size: 2.5rem !important;
        }

        /* Subtitle */
        [data-testid="stMarkdownContainer"] p {
            color: #475569;
        }

        /* Visible Login and Create Account tabs */
        [data-testid="stTabs"] button {
            color: #10213a !important;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #dc2626 !important;
            border-bottom-color: #dc2626 !important;
        }

        /* White form card */
        [data-testid="stForm"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.08);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center;'>📰 Fake News Detection</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Sign in to access your news analysis dashboard."
        "</p>",
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

    with login_tab:
        with st.form("login_form"):
            identifier = st.text_input(
                "Username or Email"
            )
            password = st.text_input(
                "Password",
                type="password"
            )

            login_clicked = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_clicked:
            if not identifier.strip() or not password:
                st.warning(
                    "Enter your username/email and password."
                )
            else:
                user = authenticate_user(
                    identifier,
                    password
                )

                if user:
                    st.session_state.authenticated_user = user
                    st.rerun()
                else:
                    st.error(
                        "Invalid username/email or password."
                    )

    with signup_tab:
        with st.form("signup_form"):
            username = st.text_input(
                "Choose Username"
            )
            email = st.text_input(
                "Email Address"
            )
            new_password = st.text_input(
                "Create Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            signup_clicked = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if signup_clicked:
            if not all([
                username.strip(),
                email.strip(),
                new_password,
                confirm_password
            ]):
                st.warning("Please fill in all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                success, message = create_user(
                    username,
                    email,
                    new_password
                )

                if success:
                    st.success(message)
                    st.info(
                        "Now open the Login tab to sign in."
                    )
                else:
                    st.error(message)

    st.stop()


# =====================================================
# LOGGED-IN USER AND LOGOUT
# =====================================================

current_user = st.session_state.authenticated_user

with st.sidebar:
    st.subheader("Your Account")
    st.write(f"**{current_user['username']}**")
    st.caption(current_user["email"])

    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated_user = None
        st.rerun()


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