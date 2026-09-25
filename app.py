import streamlit as st

from pdf_processor import extract_pages, create_chunks
from rag_engine import RAGEngine
from llm_manager import LLMManager


# -------------------------
# Page configuration
# -------------------------

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)


# -------------------------
# Title
# -------------------------

st.title("🤖 AI Document Assistant")

st.caption(
    "Multi-Document RAG Question Answering"
)


# -------------------------
# Initialize components
# -------------------------

if "rag" not in st.session_state:

    st.session_state.rag = RAGEngine()


if "llm" not in st.session_state:

    st.session_state.llm = LLMManager()


if "messages" not in st.session_state:

    st.session_state.messages = []


if "documents_loaded" not in st.session_state:

    st.session_state.documents_loaded = False


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("📚 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write(
            f"{len(uploaded_files)} PDF(s) selected"
        )

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}"
            )

        if st.button(
            "Process Documents",
            use_container_width=True
        ):

            with st.spinner(
                "Reading and processing PDFs..."
            ):

                documents = extract_pages(
                    uploaded_files
                )

                chunks = create_chunks(
                    documents
                )

                st.session_state.rag.build_index(
                    chunks
                )

                st.session_state.documents_loaded = True

                st.session_state.messages = []

            st.success(
                f"Processed {len(uploaded_files)} "
                f"PDF(s) and created "
                f"{len(chunks)} chunks."
            )

    st.divider()

    if st.session_state.documents_loaded:

        st.success(
            "RAG system ready."
        )

    else:

        st.info(
            "Upload PDFs and click "
            "'Process Documents'."
        )


# -------------------------
# Display previous messages
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# -------------------------
# Chat input
# -------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:

    # -------------------------
    # Check documents
    # -------------------------

    if not st.session_state.documents_loaded:

        st.warning(
            "Please upload and process "
            "your PDFs first."
        )

        st.stop()


    # -------------------------
    # Display user question
    # -------------------------

    with st.chat_message("user"):

        st.markdown(question)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # -------------------------
    # Search documents
    # -------------------------

    with st.spinner(
        "Searching documents..."
    ):

        results = st.session_state.rag.search(
            question,
            top_k=5
        )


    # -------------------------
    # No results
    # -------------------------

    if not results:

        answer = (
            "I could not find relevant "
            "information in the uploaded "
            "documents."
        )

        provider = "None"


    else:

        # -------------------------
        # Build context
        # -------------------------

        context_parts = []

        for number, result in enumerate(
            results,
            start=1
        ):

            context_parts.append(
                f"""
SOURCE {number}

Document:
{result['source']}

Page:
{result['page']}

Content:
{result['text']}
"""
            )

        context = "\n\n".join(
            context_parts
        )


        # -------------------------
        # Generate answer
        # -------------------------

        with st.spinner(
            "Generating answer..."
        ):

            response = (
                st.session_state.llm.generate(
                    question,
                    context
                )
            )

        answer = response["answer"]

        provider = response["provider"]


    # -------------------------
    # Display answer
    # -------------------------

    with st.chat_message(
        "assistant"
    ):

        st.markdown(answer)

        st.caption(
            f"AI Provider: {provider}"
        )


        # -------------------------
        # Sources
        # -------------------------

        if results:

            st.markdown("---")

            st.markdown(
                "### 📚 Sources"
            )

            seen = set()

            for result in results:

                source = result["source"]

                page = result["page"]

                key = (
                    source,
                    page
                )

                if key in seen:

                    continue

                seen.add(key)

                st.markdown(
                    f"📄 **{source}** — "
                    f"Page **{page}**"
                )


    # -------------------------
    # Save assistant message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )