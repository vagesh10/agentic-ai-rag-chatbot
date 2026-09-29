# Agentic AI RAG Chatbot

A document-grounded Retrieval-Augmented Generation (RAG) chatbot built using Python, LangGraph, Pinecone, Google Gemini, FastAPI, and Streamlit.

The chatbot uses the Agentic AI ebook as its knowledge source and answers questions only from retrieved document context.

## Features

- PDF document ingestion
- Text chunking with overlapping chunks
- Gemini-based text embeddings
- Pinecone vector storage and similarity search
- LangGraph-based RAG workflow
- Strict document-grounded generation
- Relevance threshold for out-of-context questions
- Gemini-powered answer generation
- FastAPI REST API
- Streamlit chat interface
- Retrieved source chunks displayed in the UI
- Retrieval similarity score
- Out-of-context question handling

## Tech Stack

- Python 3.11
- LangChain
- LangGraph
- Pinecone
- Google Gemini API
- FastAPI
- Streamlit
- PyPDF
- python-dotenv

## Models

### Embedding Model

```text
gemini-embedding-2

Embedding dimension:

1536
Generation Model
gemini-2.5-flash
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
├── frontend.py
├── tests_sample_queries.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
RAG Architecture

The application follows this workflow:

User Question
      │
      ▼
Streamlit Frontend
      │
      ▼
FastAPI /chat
      │
      ▼
LangGraph
      │
      ▼
Retrieve from Pinecone
      │
      ▼
Relevant Document Chunks
      │
      ▼
Relevance Check
      │
      ├── Low relevance
      │       ↓
      │   Refuse to answer
      │
      └── Relevant
              ↓
        Gemini Generation
              │
              ▼
          Final Answer
LangGraph Workflow

The LangGraph workflow contains two main nodes:

START
  ↓
Retrieve
  ↓
Generate
  ↓
END
Retrieve Node

The retrieve node:

Receives the user's question.
Searches the Pinecone vector index.
Retrieves the top 4 relevant chunks.
Calculates the highest similarity score.
Passes the retrieved context to the generation node.
Generate Node

The generate node:

Checks the retrieval similarity score.
Rejects questions below the relevance threshold.
Sends only the retrieved document context to Gemini.
Generates an answer using the supplied context.
Does not use outside knowledge.

The current relevance threshold is:

0.70
Pinecone Configuration

The project uses the following Pinecone index configuration:

Index Name: agentic-ai-gemini
Dimension: 1536
Metric: cosine
Data Ingestion

The Agentic AI ebook is loaded using PyPDF and split into overlapping chunks.

Configuration:

Chunk Size: 1000
Chunk Overlap: 200

The ingestion process:

PDF
 ↓
PyPDFLoader
 ↓
Text Splitting
 ↓
Gemini Embeddings
 ↓
1536-dimensional vectors
 ↓
Pinecone

To run ingestion:

python -m src.ingestion

The completed ingestion produced:

60 pages
119 chunks
119 embeddings
1536 dimensions
Environment Variables

Create a .env file in the project root:

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-gemini
GEMINI_API_KEY=your_gemini_api_key

Never commit the .env file or API keys to GitHub.

Installation

Create and activate a virtual environment:

py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Verify dependencies:

pip check
Running the Backend

Start FastAPI:

uvicorn app:app --reload

The API will run at:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Running the Frontend

Open a second terminal and activate the virtual environment:

.\venv\Scripts\Activate.ps1

Start Streamlit:

streamlit run frontend.py

The Streamlit application will open in the browser.

API Endpoint
POST /chat

Request:

{
  "question": "What is Agentic AI?"
}

Response:

{
  "answer": "Agentic AI refers to systems capable of autonomous decision-making and action in pursuit of specific objectives.",
  "retrieved_chunks": [],
  "confidence_score": 0.8495
}

The actual response contains the retrieved document chunks.

Sample Queries

The project was tested using the following queries:

What is Agentic AI?
What is the role of memory in Agentic AI?
What are the main components of an Agentic AI system?
How is Agentic AI different from traditional automation?
Who won the 2022 FIFA World Cup?
What is the role of planning in Agentic AI?
Validation
In-Context Query

Question:

What is Agentic AI?

Result:

Grounded answer generated successfully
Similarity score: 0.8495
Memory Query

Question:

What is the role of memory in Agentic AI?

Result:

Grounded answer generated successfully
Similarity score: 0.7869
Out-of-Context Query

Question:

Who won the 2022 FIFA World Cup?

Result:

I don't have enough information in the provided document to answer that question.

Similarity score:

0.5276

Because the score is below the 0.70 threshold, the system refuses to generate an answer from outside knowledge.

Output

The application provides:

Final answer
Retrieved document chunks
Source page information
Individual chunk similarity scores
Overall retrieval similarity score
Security

API keys are loaded through environment variables.

The .env file is excluded from Git using .gitignore.

Example environment configuration is provided in:

.env.example

Never commit real API keys to the repository.

Assignment Context

This project was developed as part of a technical recruitment assignment for a Data Engineering role.

License

This project was created as part of a technical recruitment assignment.