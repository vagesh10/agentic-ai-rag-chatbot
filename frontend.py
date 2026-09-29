import streamlit as st

from src.graph import ask_question


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


# Display chat history
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
                    f"📚 View {len(chunks)} Retrieved Sources"
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

                        st.markdown(f"**Chunk {index}**")

                        st.caption(
                            f"Page: {page}  • "
                            f"Similarity: {chunk_score:.4f}"
                        )

                        st.write(content)

                        if index < len(chunks):
                            st.divider()


# Chat input
question = st.chat_input(
    "Ask a question about Agentic AI..."
)


if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the Agentic AI knowledge base..."
        ):

            try:

                # Directly run the RAG pipeline
                result = ask_question(question)

                answer = result["answer"]
                chunks = result.get("context", [])
                confidence_score = result.get("score", 0)

                # Answer
                st.markdown(answer)

                st.caption(
                    f"Retrieval similarity score: "
                    f"{confidence_score:.4f}"
                )


                # Retrieved sources
                if chunks:

                    with st.expander(
                        f"📚 View {len(chunks)} Retrieved Sources"
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
                                f"Page: {page}  • "
                                f"Similarity: {chunk_score:.4f}"
                            )

                            st.write(content)

                            if index < len(chunks):
                                st.divider()


                # Save assistant message
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "retrieved_chunks": chunks,
                        "confidence_score": confidence_score,
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