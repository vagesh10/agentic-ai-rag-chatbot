# Agentic AI RAG Chatbot

A document-grounded Retrieval-Augmented Generation (RAG) chatbot built using Python, LangGraph, Pinecone, Google Gemini, FastAPI, and Streamlit.

The chatbot uses the Agentic AI ebook as its knowledge source and answers questions only from relevant retrieved document context. Out-of-context questions are rejected instead of being answered using outside knowledge.

## 🚀 Live Demo

**Streamlit App:**  
https://agentic-ai-rag-chatbot-bpxbvewfsanjuncjsglamo.streamlit.app/

## ✨ Features

- PDF document ingestion using PyPDF
- Text chunking with overlapping chunks
- Gemini-based text embeddings
- Pinecone vector storage and similarity search
- LangGraph-based RAG workflow
- Top-4 relevant chunk retrieval
- Retrieval similarity scoring
- Relevance threshold for out-of-context questions
- Strict document-grounded generation
- Gemini-powered answer generation
- FastAPI REST API
- Swagger API documentation
- Streamlit chat interface
- Retrieved source chunks and metadata
- Out-of-context question handling

## 🛠️ Tech Stack

- Python 3.11
- LangChain
- LangGraph
- Pinecone
- Google Gemini API
- FastAPI
- Streamlit
- PyPDF
- python-dotenv

## 🤖 Models

**Embedding Model**
```text
gemini-embedding-2
Dimension: 1536

Generation Model

gemini-2.5-flash
📂 Project Structure
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
🏗️ RAG Architecture
User Question
      ↓
Streamlit / FastAPI
      ↓
LangGraph
      ↓
Pinecone Vector Search
      ↓
Top Relevant Document Chunks
      ↓
Relevance Check
      ↓
   ┌───────────────┐
   │               │
Low Relevance   Relevant
   │               │
   ↓               ↓
Refuse          Gemini
Answer          Generation
                   ↓
              Final Answer
🔄 LangGraph Workflow
START
  ↓
Retrieve
  ↓
Generate
  ↓
END
Retrieve Node
Receives the user's question
Searches the Pinecone vector index
Retrieves the top 4 relevant chunks
Calculates similarity scores
Passes retrieved context to the generation node
Generate Node
Checks retrieval relevance
Rejects low-relevance questions
Sends only retrieved document context to Gemini
Generates a grounded answer
Does not use outside knowledge

Relevance Threshold:

0.70
🎯 Groundedness and Relevance

The system uses the Pinecone similarity score as a retrieval-confidence signal.

If the highest retrieved score is below 0.70, the system returns:

I don't have enough information in the provided document to answer that question.

When the retrieved context is relevant, Gemini receives only the retrieved document context.

The generation prompt instructs the model to:

Use only retrieved context
Avoid outside knowledge
Avoid unsupported information
Avoid inventing facts
Answer using the closest clearly supported concept
Refuse when the context is insufficient
🗄️ Pinecone Configuration
Index Name: agentic-ai-gemini
Dimension: 1536
Metric: cosine
Top-K: 4
📄 Data Ingestion

The Agentic AI ebook is processed using PyPDF.

PDF
 ↓
PyPDF
 ↓
Text Extraction
 ↓
Text Splitting
 ↓
Gemini Embeddings
 ↓
1536-Dimensional Vectors
 ↓
Pinecone

Configuration:

Chunk Size: 1000
Chunk Overlap: 200

Completed ingestion:

Pages: 60
Chunks: 119
Embeddings: 119
Dimension: 1536

Run ingestion:

python -m src.ingestion
🔐 Environment Variables

Create a .env file in the project root:

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-gemini
GEMINI_API_KEY=your_gemini_api_key

Never commit .env or real API keys to GitHub.

For Streamlit Community Cloud, configure these values in the application's Secrets settings.

💻 Installation

Clone the repository:

git clone https://github.com/vagesh10/agentic-ai-rag-chatbot.git
cd agentic-ai-rag-chatbot

Create a Python 3.11 virtual environment:

py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Verify dependencies:

pip check
🚀 Run FastAPI
uvicorn app:app --reload

API:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
🌐 Run Streamlit
streamlit run frontend.py
🔌 API Endpoint
POST /chat

Request:

{
  "question": "What is Agentic AI?"
}

Response:

{
  "query": "What is Agentic AI?",
  "final_answer": "Agentic AI provides a practical framework for leveraging interconnected AI systems capable of autonomous decision-making...",
  "retrieved_context_chunks": [
    {
      "content": "Retrieved document content...",
      "metadata": {
        "page": 10,
        "source": "data/Ebook-Agentic-AI.pdf"
      },
      "score": 0.8123
    }
  ],
  "confidence_score": 0.8123
}
🧪 Validation

The chatbot was tested using six validation queries.

1. Agentic AI Definition

Question:

What is the core definition of Agentic AI as outlined in the eBook?

Result: PASS
Confidence: 0.8123

2. Agentic Architecture

Question:

What are the main architectural components required to build agentic systems?

Result: PASS
Confidence: 0.8018

3. Industry Use Cases

Question:

What real-world industry use cases for Agentic AI are discussed in the eBook?

Result: PASS
Confidence: 0.7917

4. Agentic AI vs Traditional Generative AI Chatbots

Question:

How does Agentic AI differ from traditional generative AI chatbots according to the text?

Result: PASS
Confidence: 0.7895

The retrieved context describes Agentic AI as autonomous, goal-oriented, proactive, adaptive, and impact-focused. Other AI systems are described as output-focused, reactive, and static.

5. Challenges and Limitations

Question:

What key challenges or limitations of Agentic AI are mentioned in the document?

Result: PASS
Confidence: 0.7875

The retrieved content discusses communication and coordination, interoperability, conflict management, agent selection, scalability, and fault tolerance.

6. Out-of-Context Question

Question:

What is the capital of France?

Result: PASS — Correctly Refused
Confidence: 0.5472

Response:

I don't have enough information in the provided document to answer that question.

Since the score is below the 0.70 relevance threshold, the system does not generate an answer using outside knowledge.

📊 Validation Summary
Test	Type	Result	Confidence
Agentic AI definition	In-context	PASS	0.8123
Agentic architecture	In-context	PASS	0.8018
Industry use cases	In-context	PASS	0.7917
Agentic AI vs traditional chatbots	In-context	PASS	0.7895
Challenges and limitations	In-context	PASS	0.7875
Capital of France	Out-of-context	PASS - Refused	0.5472
📤 Output

The application provides:

Original query
Final answer
Retrieved document chunks
Source page information
Source metadata
Individual similarity scores
Overall retrieval similarity score
Out-of-context refusal
🔍 Retrieval Confidence

The confidence_score represents the highest Pinecone similarity score among the retrieved chunks.

It is used as a retrieval relevance signal and should not be interpreted as a guaranteed probability that the generated answer is factually correct.

🔐 Security
API keys are loaded through environment variables.
.env is excluded using .gitignore.
.env.example contains placeholder values.
Real API keys are not stored in the repository.
API keys should never be committed to GitHub.
Streamlit secrets are configured through deployment settings.
📚 Knowledge Source

The chatbot uses:

Ebook-Agentic-AI.pdf

as its knowledge source.

The document is processed, chunked, embedded using Gemini, and stored in Pinecone.

🎯 Assignment Context

This project was developed as part of an AI Engineer technical assessment focused on building a document-grounded RAG chatbot using:

LangGraph
Pinecone
Vector embeddings
Document retrieval
LLM-based generation
Agentic AI ebook as the knowledge source

The implementation provides both a REST API and an interactive Streamlit interface.

📌 Key Design Decisions
Pinecone

Used for vector storage and semantic similarity search.

LangGraph

Used to define the RAG workflow as a stateful graph containing retrieval and generation steps.

Google Gemini

Used for document embeddings and final answer generation.

FastAPI

Used to expose the RAG pipeline through a REST API.

Streamlit

Used to provide an interactive chatbot interface.

🔄 End-to-End Flow
Agentic AI Ebook
       ↓
PDF Loader
       ↓
Text Chunking
       ↓
Gemini Embeddings
       ↓
Pinecone Vector DB
       ↓
User Question
       ↓
LangGraph
       ↓
Similarity Search
       ↓
Top 4 Chunks
       ↓
Relevance Check
       ↓
Gemini 2.5 Flash
       ↓
Grounded Final Answer
✅ Final Validation Status

All six validation scenarios passed:

[PASS] Agentic AI definition
[PASS] Agentic architecture
[PASS] Industry use cases
[PASS] Agentic AI vs traditional chatbots
[PASS] Challenges and limitations
[PASS] Out-of-context question refusal
📄 License

This project was created as part of a technical recruitment assignment and is intended for evaluation and demonstration purposes.