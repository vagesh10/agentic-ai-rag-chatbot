import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

from google import genai
from google.genai import types

from src.config import (
    GEMINI_API_KEY,
    PINECONE_INDEX_NAME,
)


PDF_PATH = "data/Ebook-Agentic-AI.pdf"


class GeminiEmbeddings:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = "gemini-embedding-2"
        self.dimension = 1536

    def embed_documents(self, texts):

        all_embeddings = []

        batch_size = 50

        for i in range(0, len(texts), batch_size):

            batch = texts[i:i + batch_size]

            start = i + 1
            end = i + len(batch)

            print(
                f"Embedding chunks {start} to {end} "
                f"of {len(texts)}..."
            )

            while True:

                try:

                    response = self.client.models.embed_content(
                        model=self.model,
                        contents=[
                            types.Content(
                                parts=[
                                    types.Part.from_text(
                                        text=text
                                    )
                                ]
                            )
                            for text in batch
                        ],
                        config=types.EmbedContentConfig(
                            output_dimensionality=self.dimension
                        )
                    )

                    break

                except Exception as error:

                    error_message = str(error)

                    if (
                        "429" in error_message
                        or "RESOURCE_EXHAUSTED"
                        in error_message
                    ):

                        print(
                            "Gemini embedding quota reached."
                        )

                        print(
                            "Waiting 65 seconds..."
                        )

                        time.sleep(65)

                    else:

                        raise error

            batch_embeddings = [
                embedding.values
                for embedding in response.embeddings
            ]

            all_embeddings.extend(
                batch_embeddings
            )

            print(
                f"Successfully embedded "
                f"{len(batch_embeddings)} chunks."
            )

            if end < len(texts):

                print(
                    "Waiting 65 seconds "
                    "before next batch..."
                )

                time.sleep(65)

        print(
            f"Total embeddings created: "
            f"{len(all_embeddings)}"
        )

        return all_embeddings

    def embed_query(self, text):

        while True:

            try:

                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                    config=types.EmbedContentConfig(
                        output_dimensionality=self.dimension
                    )
                )

                return response.embeddings[0].values

            except Exception as error:

                error_message = str(error)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED"
                    in error_message
                ):

                    print(
                        "Gemini embedding quota reached."
                    )

                    print(
                        "Waiting 65 seconds..."
                    )

                    time.sleep(65)

                else:

                    raise error


def run_ingestion():

    print("=" * 60)
    print("STARTING RAG INGESTION")
    print("=" * 60)

    # -----------------------------------------
    # Load PDF
    # -----------------------------------------

    print("\nLoading PDF...")

    loader = PyPDFLoader(
        PDF_PATH
    )

    documents = loader.load()

    print(
        f"Loaded {len(documents)} pages."
    )

    # -----------------------------------------
    # Split PDF
    # -----------------------------------------

    print(
        "\nSplitting document into chunks..."
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    # -----------------------------------------
    # Create embeddings
    # -----------------------------------------

    print(
        "\nCreating Gemini embedding model..."
    )

    embeddings = GeminiEmbeddings()

    print(
        f"Embedding model: {embeddings.model}"
    )

    print(
        f"Embedding dimension: "
        f"{embeddings.dimension}"
    )

    # -----------------------------------------
    # Upload to Pinecone
    # -----------------------------------------

    print(
        "\nUploading vectors to Pinecone..."
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    # -----------------------------------------
    # Done
    # -----------------------------------------

    print("\n" + "=" * 60)
    print(
        "INGESTION COMPLETED SUCCESSFULLY!"
    )
    print("=" * 60)

    print(
        f"Pages processed: {len(documents)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    print(
        f"Embedding dimension: "
        f"{embeddings.dimension}"
    )

    print(
        f"Pinecone index: "
        f"{PINECONE_INDEX_NAME}"
    )

    print("=" * 60)


if __name__ == "__main__":
    run_ingestion()