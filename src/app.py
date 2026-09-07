import streamlit as st
from src.rag.pipeline import ask_question


st.set_page_config(
    page_title="Chatbot Zakat MUI Riau",
    page_icon="🕌",
    layout="centered",
)


st.title("🕌 Chatbot Informasi Zakat")
st.caption(
    "Prototype chatbot berbasis LLM dan Retrieval-Augmented Generation (RAG)"
)


# Inisialisasi history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Tampilkan seluruh history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            sources = message.get("sources", [])

            if sources:
                st.markdown("#### 📚 Sumber")

                for source, page in sources:
                    st.write(f"- {source}, halaman {page}")


# Input pertanyaan
question = st.chat_input("Tanyakan sesuatu tentang zakat...")


if question:

    # Ambil jawaban dari RAG
    with st.spinner("Sedang mencari informasi..."):
        answer, documents = ask_question(question)

    # Ambil sumber
    sources = sorted(set(
        (
            document.metadata.get("source"),
            document.metadata.get("page"),
        )
        for document in documents
    ))

    # Simpan pertanyaan user
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    # Simpan jawaban assistant
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })

    # Tampilkan ulang history
    st.rerun()