import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


st.set_page_config(
    page_title="Agentic AI RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Agentic AI RAG Chatbot")
st.caption(
    "Ask questions about the Agentic AI ebook. "
    "Answers are grounded only in the retrieved document context."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            score = message.get("confidence_score")

            if score is not None:
                st.caption(
                    f"Retrieval similarity score: {score:.4f}"
                )

            chunks = message.get("retrieved_chunks", [])

            if chunks:

                with st.expander(
                    f"View {len(chunks)} retrieved document chunks"
                ):

                    for index, chunk in enumerate(
                        chunks,
                        start=1,
                    ):

                        metadata = chunk.get("metadata", {})
                        content = chunk.get("content", "")
                        chunk_score = chunk.get("score", 0)

                        page = metadata.get(
                            "page_label",
                            metadata.get("page", "Unknown"),
                        )

                        st.markdown(
                            f"**Chunk {index}**"
                        )

                        st.caption(
                            f"Page: {page}  •  "
                            f"Similarity: {chunk_score:.4f}"
                        )

                        st.write(content)

                        if index < len(chunks):
                            st.divider()


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask a question about Agentic AI..."
)


if question:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # -----------------------------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the Agentic AI knowledge base..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=120,
                )

                response.raise_for_status()

                result = response.json()

                answer = result["answer"]
                chunks = result.get(
                    "retrieved_chunks",
                    [],
                )
                confidence_score = result.get(
                    "confidence_score",
                    0,
                )

                # -----------------------------------------
                # ANSWER
                # -----------------------------------------

                st.markdown(answer)

                st.caption(
                    f"Retrieval similarity score: "
                    f"{confidence_score:.4f}"
                )

                # -----------------------------------------
                # RETRIEVED SOURCES
                # -----------------------------------------

                if chunks:

                    with st.expander(
                        f"View {len(chunks)} retrieved document chunks"
                    ):

                        for index, chunk in enumerate(
                            chunks,
                            start=1,
                        ):

                            metadata = chunk.get(
                                "metadata",
                                {},
                            )

                            content = chunk.get(
                                "content",
                                "",
                            )

                            chunk_score = chunk.get(
                                "score",
                                0,
                            )

                            page = metadata.get(
                                "page_label",
                                metadata.get(
                                    "page",
                                    "Unknown",
                                ),
                            )

                            st.markdown(
                                f"**Chunk {index}**"
                            )

                            st.caption(
                                f"Page: {page}  •  "
                                f"Similarity: {chunk_score:.4f}"
                            )

                            st.write(content)

                            if index < len(chunks):
                                st.divider()

                # -----------------------------------------
                # SAVE ASSISTANT MESSAGE
                # -----------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "retrieved_chunks": chunks,
                        "confidence_score": confidence_score,
                    }
                )

            except requests.exceptions.RequestException:

                error_message = (
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running on "
                    "http://127.0.0.1:8000."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

            except Exception as error:

                error_message = (
                    f"An unexpected error occurred: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )