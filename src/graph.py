from typing import TypedDict
import time

from langgraph.graph import StateGraph, START, END
from langchain_pinecone import PineconeVectorStore

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY, PINECONE_INDEX_NAME
from src.ingestion import GeminiEmbeddings


# =========================================================
# CONFIGURATION
# =========================================================
GENERATION_MODEL = "gemini-2.5-flash"

# Based on the actual scores observed during testing:
# Relevant query:    0.8495
# Irrelevant query:  0.5276
RELEVANCE_THRESHOLD = 0.70

TOP_K = 4

MAX_GENERATION_RETRIES = 4
BASE_RETRY_DELAY = 5


# =========================================================
# GEMINI CLIENT
# =========================================================

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# GRAPH STATE
# =========================================================

class GraphState(TypedDict):
    question: str
    context: list
    answer: str
    score: float


# =========================================================
# EMBEDDINGS
# =========================================================

embeddings = GeminiEmbeddings()


# =========================================================
# PINECONE VECTOR STORE
# =========================================================

vector_store = PineconeVectorStore(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
)


# =========================================================
# RETRIEVE NODE
# =========================================================

def retrieve(state: GraphState):
    """
    Retrieve the most relevant chunks from Pinecone.
    """

    question = state["question"]

    print("\nRetrieving relevant documents...")

    results = vector_store.similarity_search_with_score(
        question,
        k=TOP_K,
    )

    context = []
    scores = []

    for document, score in results:

        score = float(score)

        context.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "score": score,
            }
        )

        scores.append(score)

    if scores:
        best_score = max(scores)
    else:
        best_score = 0.0

    print(f"Retrieved {len(context)} chunks.")
    print(f"Best relevance score: {best_score:.4f}")

    return {
        "context": context,
        "score": best_score,
    }


# =========================================================
# GENERATE NODE
# =========================================================

def generate(state: GraphState):
    """
    Generate an answer using ONLY the retrieved context.
    """

    question = state["question"]
    context = state["context"]
    score = state["score"]

    # -----------------------------------------------------
    # RELEVANCE CHECK
    # -----------------------------------------------------

    if not context or score < RELEVANCE_THRESHOLD:

        return {
            "answer": (
                "I don't have enough information in the provided "
                "document to answer that question."
            )
        }

    # -----------------------------------------------------
    # FORMAT RETRIEVED CONTEXT
    # -----------------------------------------------------

    formatted_context = "\n\n".join(
        [
            f"--- Retrieved Chunk {i + 1} ---\n"
            f"{item['content']}"
            for i, item in enumerate(context)
        ]
    )

    # -----------------------------------------------------
    # GROUNDED PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are a strict document-grounded RAG assistant.

Your job is to answer the user's question using ONLY the
retrieved context provided below.

STRICT RULES:

1. Use only information contained in the retrieved context.
2. Do not use your own general knowledge.
3. Do not invent or assume facts.
4. Do not add information that is not supported by the context.
5. If the context does not contain enough information to
   answer the question, say:

"I don't have enough information in the provided document
to answer that question."

6. Give a concise and clear answer.
7. Do not mention the retrieval process unless necessary.

RETRIEVED CONTEXT:

{formatted_context}

USER QUESTION:

{question}
"""

    print("\nGenerating answer with Gemini...")

    # -----------------------------------------------------
    # GEMINI GENERATION WITH RETRY
    # -----------------------------------------------------

    for attempt in range(MAX_GENERATION_RETRIES):

        try:

            response = gemini_client.models.generate_content(
                model=GENERATION_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a strict RAG assistant. "
                        "Answer only from the supplied document "
                        "context. Never use outside knowledge."
                    ),
                    max_output_tokens=800,
                ),
            )

            # Make sure Gemini actually returned text.
            if not response.text:

                return {
                    "answer": (
                        "I don't have enough information in the "
                        "provided document to answer that question."
                    )
                }

            return {
                "answer": response.text.strip()
            }

        except Exception as error:

            error_message = str(error)

            # -------------------------------------------------
            # TRANSIENT GEMINI ERRORS
            # -------------------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                if attempt < MAX_GENERATION_RETRIES - 1:

                    wait_time = BASE_RETRY_DELAY * (2 ** attempt)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return {
                        "answer": (
                            "The Gemini generation service is "
                            "temporarily unavailable. Please try "
                            "again in a moment."
                        )
                    }

            else:

                # Unknown error — don't hide it.
                raise


# =========================================================
# BUILD LANGGRAPH
# =========================================================

workflow = StateGraph(GraphState)

# Nodes
workflow.add_node(
    "retrieve",
    retrieve
)

workflow.add_node(
    "generate",
    generate
)

# Edges
workflow.add_edge(
    START,
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "generate"
)

workflow.add_edge(
    "generate",
    END
)

# Compile
graph = workflow.compile()


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(question: str):
    """
    Run the complete RAG pipeline.
    """

    result = graph.invoke(
        {
            "question": question,
            "context": [],
            "answer": "",
            "score": 0.0,
        }
    )

    return result


# =========================================================
# COMMAND LINE TEST
# =========================================================

if __name__ == "__main__":

    question = input("\nEnter your question: ").strip()

    if not question:
        print("Please enter a question.")
        raise SystemExit

    result = ask_question(question)

    # -----------------------------------------------------
    # ANSWER
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(result["answer"])

    # -----------------------------------------------------
    # RELEVANCE SCORE
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("RELEVANCE SCORE")
    print("=" * 60)

    print(f"{result['score']:.4f}")

    # -----------------------------------------------------
    # RETRIEVED CHUNKS
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("RETRIEVED CHUNKS")
    print("=" * 60)

    for i, item in enumerate(
        result["context"],
        start=1
    ):

        print(f"\n--- Chunk {i} ---")

        print(
            f"Score: {item['score']:.4f}"
        )

        print(
            f"Metadata: {item['metadata']}"
        )

        print()

        print(
            item["content"][:1000]
        )