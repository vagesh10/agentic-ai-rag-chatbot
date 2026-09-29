# Agentic AI RAG Chatbot

A document-grounded Retrieval-Augmented Generation (RAG) chatbot built using Python, LangGraph, Pinecone, Gemini, and FastAPI.

The chatbot uses the Agentic AI eBook as its knowledge source and answers questions only from retrieved document context.

## Features

- PDF document ingestion
- Text chunking with overlapping chunks
- Gemini embeddings
- Pinecone vector database
- Semantic similarity search
- LangGraph-based RAG workflow
- Grounded Gemini responses
- Out-of-context question refusal
- Retrieval relevance/confidence score
- FastAPI REST API
- Swagger API documentation

## Architecture

```text
Agentic AI PDF
      |
      v
PDF Loader
      |
      v
Text Chunking
      |
      v
Gemini Embeddings
      |
      v
Pinecone Vector Database
      |
      v
User Question
      |
      v
LangGraph
      |
      +------> Retrieve relevant chunks
      |
      v
Relevance Threshold
      |
      +------> Insufficient context
      |              |
      |              v
      |         Refusal response
      |
      v
Gemini Generation
      |
      v
Final Answer + Retrieved Chunks + Score
      |
      v
FastAPI
Technology Stack
Python 3.11
LangChain
LangGraph
Pinecone
Google Gemini API
FastAPI
Uvicorn
PyPDF
python-dotenv
Models
Embedding Model

The project uses:

gemini-embedding-2

Embedding dimension:

1536
Generation Model

The project uses:

gemini-3.8-flash
Project Structure
rag-agentic-ai/
│
├── data/
│   └── Ebook-Agentic-AI.pdf
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── create_pinecone_index.py
│   ├── graph.py
│   └── ingestion.py
│
├── app.py
├── tests_sample_queries.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Setup
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd rag-agentic-ai
2. Create a Virtual Environment
python -m venv venv

On Windows:

venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the project root.

Use .env.example as the template:

OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=agentic-ai-gemini
GEMINI_API_KEY=your_gemini_api_key_here

Do not commit .env or API keys to GitHub.

Pinecone Index

The project uses a Pinecone dense vector index with:

Index name: agentic-ai-gemini
Dimension: 1536
Metric: cosine

The index can be created using:

python -m src.create_pinecone_index
Document Ingestion

Place the Agentic AI eBook at:

data/Ebook-Agentic-AI.pdf

Run the ingestion pipeline:

python -m src.ingestion

The ingestion pipeline performs the following steps:

Loads the PDF.
Splits the document into overlapping chunks.
Generates Gemini embeddings.
Stores vectors and metadata in Pinecone.

The current ingestion run processed:

Pages: 60
Chunks: 119
Embedding dimension: 1536
Run the API

Start the FastAPI server:

uvicorn app:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

API Endpoint
POST /chat

Request:

{
  "question": "What is Agentic AI?"
}

Response:

{
  "answer": "Based on the provided document, Agentic AI refers to...",
  "retrieved_chunks": [
    {
      "content": "...",
      "metadata": {
        "page": 17
      },
      "score": 0.80
    }
  ],
  "confidence_score": 0.80
}

The confidence_score represents the highest retrieval similarity score returned for the question.

RAG Workflow

The LangGraph workflow consists of two main nodes:

START
  |
  v
Retrieve
  |
  v
Generate
  |
  v
END
Retrieve Node

The retrieve node:

Converts the user question into an embedding.
Searches the Pinecone vector database.
Retrieves the top relevant document chunks.
Calculates similarity scores.
Generate Node

The generate node:

Checks the retrieval relevance threshold.
Rejects insufficient context.
Passes the retrieved chunks to Gemini.
Instructs Gemini to answer only using the supplied document context.
Grounding and Out-of-Context Handling

The chatbot is designed to answer questions only from the Agentic AI eBook.

A relevance threshold is used before generation.

If the retrieved context does not meet the configured threshold, the chatbot refuses to answer instead of relying on outside knowledge.

Example:

Question:
Who won the 2022 FIFA World Cup?

Response:
I don't have enough information in the provided document to answer that question.

This provides a safeguard against answering questions that are outside the knowledge contained in the document.

Sample Tests

The project includes six sample queries in:

tests_sample_queries.py

The queries are:

What is Agentic AI?
What is the role of memory in Agentic AI?
What are the main components of an Agentic AI system?
How is Agentic AI different from traditional automation?
Who won the 2022 FIFA World Cup?
What is the role of planning in Agentic AI?

The fifth query is an out-of-context test and verifies that the chatbot refuses to provide an unsupported answer.

Validation Results

The RAG pipeline was tested through the FastAPI /chat endpoint.

Test	Result
Agentic AI definition	Passed
Role of memory	Passed
Main components of Agentic AI	Passed
Agentic AI vs traditional automation	Passed
Out-of-context FIFA question	Correctly refused
Role of planning	Passed
RAG Components
1. Document Loading

The Agentic AI eBook is loaded from the data/ directory using a PDF loader.

2. Chunking

The document is split into smaller overlapping chunks so that relevant sections can be retrieved efficiently.

3. Embeddings

Each document chunk is converted into a vector representation using Gemini embeddings.

4. Vector Storage

The embeddings and document metadata are stored in Pinecone.

5. Retrieval

When a user asks a question, the question is embedded and compared against the vectors stored in Pinecone.

The most relevant chunks are retrieved.

6. Generation

The retrieved context is passed to Gemini through the LangGraph generation node.

The generation prompt explicitly instructs the model to use only the retrieved document context.

7. API

FastAPI exposes the RAG workflow through the /chat endpoint.

The API returns:

Final answer
Retrieved chunks
Retrieval score
Security

API keys are stored in the local .env file.

The .env file is excluded from Git using .gitignore.

Never commit real API keys to the repository.

Assignment Context

This project was developed as part of a technical recruitment assignment for a Data Engineering role.

The implementation demonstrates:

Data ingestion
PDF processing
Text chunking
Embedding generation
Vector database indexing
Semantic retrieval
LangGraph orchestration
Grounded LLM generation
Out-of-context handling
REST API development


License

This project was created as part of a technical recruitment assignment.




