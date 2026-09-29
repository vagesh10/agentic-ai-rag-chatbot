# Agentic AI RAG Chatbot

A document-grounded Retrieval-Augmented Generation (RAG) chatbot built using Python, LangGraph, Pinecone, Google Gemini, FastAPI, and Streamlit.

The chatbot uses the Agentic AI ebook as its knowledge source and answers questions only from retrieved document context.

## 🚀 Live Demo

**Streamlit App:**  
https://agentic-ai-rag-chatbot-a2j4fnxdrwjwxwvw3abrue.streamlit.app/

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
Embedding dimension: 1536
```

### Generation Model

```text
gemini-2.5-flash
```

## Project Structure

```text
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
```

## RAG Architecture

The deployed Streamlit application follows this workflow:

```text
User Question
      │
      ▼
Streamlit Frontend
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
```

FastAPI is also provided as a separate REST API through `app.py`.

## LangGraph Workflow

The LangGraph workflow contains two main nodes:

```text
START
  ↓
Retrieve
  ↓
Generate
  ↓
END
```

### Retrieve Node

The retrieve node:

- Receives the user's question.
- Searches the Pinecone vector index.
- Retrieves the top 4 relevant chunks.
- Calculates the highest similarity score.
- Passes the retrieved context to the generation node.

### Generate Node

The generate node:

- Checks the retrieval similarity score.
- Rejects questions below the relevance threshold.
- Sends only the retrieved document context to Gemini.
- Generates an answer using the supplied context.
- Does not use outside knowledge.

The current relevance threshold is:

```text
0.70
```

## Pinecone Configuration

The project uses the following Pinecone index configuration:

```text
Index Name: agentic-ai-gemini
Dimension: 1536
Metric: cosine
```

## Data Ingestion

The Agentic AI ebook is loaded using PyPDF and split into overlapping chunks.

Configuration:

```text
Chunk Size: 1000
Chunk Overlap: 200
```

The ingestion process:

```text
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
```

To run ingestion:

```bash
python -m src.ingestion
```

The completed ingestion produced:

- 60 pages
- 119 chunks
- 119 embeddings
- 1536 dimensions

## Environment Variables

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-gemini
GEMINI_API_KEY=your_gemini_api_key
```

Never commit the `.env` file or API keys to GitHub.

For Streamlit Community Cloud, configure these values in the application's Secrets settings.

## Installation

Create and activate a virtual environment:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify dependencies:

```bash
pip check
```

## Running the Backend

Start FastAPI:

```bash
uvicorn app:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start Streamlit:

```bash
streamlit run frontend.py
```

The Streamlit application will open in the browser.

## API Endpoint

### POST `/chat`

Request:

```json
{
  "question": "What is Agentic AI?"
}
```

Response:

```json
{
  "answer": "Agentic AI refers to systems capable of autonomous decision-making and action in pursuit of specific objectives.",
  "retrieved_chunks": [
    {
      "content": "Retrieved document content...",
      "metadata": {},
      "score": 0.8495
    }
  ],
  "confidence_score": 0.8495
}
```

The actual response contains the retrieved document chunks.

## Sample Queries

The project was tested using the following queries:

1. What is Agentic AI?
2. What is the role of memory in Agentic AI?
3. How do AI agents differ from traditional automation systems?
4. What are the core components of an Agentic Architecture?
5. Who won the 2022 FIFA World Cup?

## Validation

### 1. In-Context Query — Agentic AI

**Question:**

```text
What is Agentic AI?
```

**Result:**

Grounded answer generated successfully.

**Similarity score:** `0.8495`

### 2. In-Context Query — Memory

**Question:**

```text
What is the role of memory in Agentic AI?
```

**Result:**

Grounded answer generated successfully.

**Similarity score:** `0.7869`

### 3. In-Context Query — Agents vs Traditional Automation

**Question:**

```text
How do AI agents differ from traditional automation systems?
```

**Result:**

Grounded answer generated successfully.

**Similarity score:** `0.7684`

### 4. In-Context Query — Core Components

**Question:**

```text
What are the core components of an Agentic Architecture?
```

**Result:**

Grounded answer generated successfully.

**Similarity score:** `0.8006`

### 5. Out-of-Context Query

**Question:**

```text
Who won the 2022 FIFA World Cup?
```

**Result:**

```text
I don't have enough information in the provided document to answer that question.
```

**Similarity score:** `0.5276`

Because the score is below the `0.70` relevance threshold, the system refuses to generate an answer using outside knowledge.

## Output

The application provides:

- Final answer
- Retrieved document chunks
- Source page information
- Individual chunk similarity scores
- Overall retrieval similarity score

## Security

- API keys are loaded through environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- Example environment configuration is provided in `.env.example`.
- Real API keys are never stored in the repository.

## Assignment Context

This project was developed as part of a technical recruitment assignment for a Data Engineering role.

## License

This project was created as part of a technical recruitment assignment.