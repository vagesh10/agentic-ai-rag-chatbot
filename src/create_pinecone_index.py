from pinecone import Pinecone, ServerlessSpec

from src.config import (
    PINECONE_API_KEY,
)


INDEX_NAME = "agentic-ai-gemini"


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]


if INDEX_NAME in existing_indexes:

    print(
        f"Index '{INDEX_NAME}' already exists."
    )

else:

    print(
        f"Creating index '{INDEX_NAME}'..."
    )

    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print(
        "Index created successfully!"
    )