import streamlit as st
from src.rag.pipeline import ask_question
from textwrap import dedent


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chatbot Informasi Zakat",
    page_icon="🕌",
    layout="centered",
)


# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 7rem;
    }

    /* Header */
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .header-icon {
        font-size: 3rem;
        margin-bottom: 0.3rem;
    }

    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .header-subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
    }

    /* Welcome card */
    .welcome-card {
        padding: 1.4rem;
        border-radius: 14px;
        background: #181b22;
        border: 1px solid #292d36;
        margin-bottom: 1.5rem;
    }

    .welcome-title {
        font-size: 2.10 rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: #b5bac5;
        font-size: 1 rem;
        line-height: 1.6;
    }

    .example {
        display: inline-block;
        padding: 0.45rem 0.7rem;
        margin: 0.3rem 0.2rem 0 0;
        border-radius: 8px;
        background: #222630;
        color: #d1d5db;
        font-size: 0.82rem;
    }

    /* Source section */
    .source-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .source-card {
        display: inline-block;
        padding: 0.45rem 0.7rem;
        margin: 0.2rem 0.2rem 0.2rem 0;
        border-radius: 8px;
        background: #1b1e26;
        border: 1px solid #2b303a;
        color: #bfc4ce;
        font-size: 0.8rem;
    }

    /* Chat spacing */
    [data-testid="stChatMessage"] {
        padding: 0.8rem 0;
    }

    /* Remove excessive top margin */
    h1 {
        margin-top: 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# HEADER
# =========================
st.markdown(
    dedent(
    """
    <div class="header">
        <div class="header-icon">🕌</div>
        <div class="header-title">Chatbot Informasi Zakat</div>
        <div class="header-subtitle">
            Majelis Ulama Indonesia Provinsi Riau
        </div>
    </div>
    """,
    ),
    unsafe_allow_html=True,
)


# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# WELCOME / EMPTY STATE
# =========================
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">
                👋 Selamat datang
            </div>
            <div class="welcome-text">
                Chatbot ini dapat membantu menjawab pertanyaan
                seputar zakat berdasarkan informasi yang terdapat
                dalam dokumen yang tersedia.
            </div>
            <br>
            <div class="welcome-text">
                Contoh pertanyaan:
            </div>
            <div>
                <span class="example">Apa itu zakat?</span>
                <span class="example">Berapa nisab zakat penghasilan?</span>
                <span class="example">Siapa yang wajib membayar zakat?</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# DISPLAY CHAT HISTORY
# =========================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:
                st.markdown(
                    '<div class="source-title">📚 Sumber</div>',
                    unsafe_allow_html=True,
                )

                for source, page in sources:
                    st.markdown(
                        f"""
                        <span class="source-card">
                            📄 {source} · Halaman {page}
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )


# =========================
# CHAT INPUT
# =========================
question = st.chat_input(
    "Tanyakan sesuatu tentang zakat..."
)


# =========================
# PROCESS QUESTION
# =========================
if question:

    # Show user message immediately
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner("Sedang mencari informasi..."):
        answer, documents = ask_question(question)

    # Get unique sources
    sources = sorted(
        set(
            (
                document.metadata.get("source"),
                document.metadata.get("page"),
            )
            for document in documents
        )
    )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )

    st.rerun()