# LangChain and LangGraph RAG AI Assistant

A Retrieval Augmented Generation (RAG) AI Assistant built using LangGraph, LangChain, FastAPI, PostgreSQL, pgvector, Streamlit, Docker, and AWS EC2.

The application allows users to query a custom knowledge base, retrieves relevant documents using vector similarity search, generates context-aware responses using an LLM, and supports human-in-the-loop approval for uncertain responses.

---

## Live Demo

[Streamlit App](https://langchain-and-langgraph-ai-assistant-ifqrqbl6f9unnw57pwc2rb.streamlit.app/)

FastAPI Swagger Documentation:

https://your-ec2-public-ip:8000/docs

---

# Features

- Retrieval Augmented Generation (RAG) pipeline
- Semantic document search using vector embeddings
- PostgreSQL database with pgvector extension
- LangGraph-based stateful workflow
- Confidence-based response routing
- Human-in-the-loop approval system
- Persistent conversation history
- Thread-based workflow checkpoints
- Streaming responses using FastAPI
- Dockerized deployment on AWS EC2

---

# Application Workflow

```
User
 |
 v
Streamlit Frontend
 |
 v
FastAPI Backend
 |
 v
LangGraph Workflow
 |
 +--> Retrieve Documents
 |
 +--> Evaluate Confidence
 |
 +--> Generate Response
 |
 v
Final Answer
```

If the retrieved information has low confidence, the workflow pauses and waits for human approval before continuing.

---

# RAG Implementation

The system uses a vector-based retrieval pipeline.

Flow:

```
Documents
    |
    v
Text Chunking
    |
    v
Embedding Generation
    |
    v
PostgreSQL + pgvector
    |
    v
Similarity Search
    |
    v
LLM Response Generation
```

Embedding Model:

```
BAAI/bge-small-en-v1.5
```

The embedding model runs locally inside the backend container.

---
# Database Architecture

The application uses a single PostgreSQL database hosted on Supabase.

The database handles three major responsibilities:

- Vector storage for RAG retrieval
- LangGraph workflow persistence
- User conversation history


Database:

```
PostgreSQL + pgvector
```

---

## Database Tables

| Table | Purpose |
|---|---|
| `langchain_pg_collections` | Stores PGVector collection information |
| `langchain_pg_embeddings` | Stores document chunks, embeddings, and metadata for similarity search |
| `checkpoints` | Stores LangGraph workflow checkpoints and thread state |
| `checkpoint_blobs` | Stores serialized checkpoint data |
| `checkpoint_writes` | Stores workflow state updates |
| `chat_history` | Stores user messages, assistant responses, and conversation history |

---

## Vector Storage (RAG)

The RAG pipeline uses PostgreSQL with the pgvector extension.

Documents are processed as:

```
Documents
    |
    v
Text Chunks
    |
    v
Embedding Generation
    |
    v
PostgreSQL pgvector
    |
    v
Similarity Search
    |
    v
Retrieved Context
    |
    v
LLM Response
```

Embedding model:

```
BAAI/bge-small-en-v1.5
```

Stored in:

```
langchain_pg_embeddings
```

Contains:

- Document chunks
- Vector embeddings
- Metadata
- Collection references

Used by:

```
LangChain PGVector Retriever
```

for semantic similarity search.

---

## LangGraph Workflow Persistence

LangGraph uses PostgreSQL checkpoint storage to maintain workflow state.

Tables:

```
checkpoints
checkpoint_blobs
checkpoint_writes
```

Stores:

- Thread IDs
- Workflow execution state
- Interrupt information
- Human approval state
- Resume checkpoints

Implemented using:

```
langgraph-checkpoint-postgres
PostgresSaver
```

This allows workflows to pause and resume without losing execution state.

---

## Chat History Storage

The Streamlit application uses a separate table in the same PostgreSQL database:

```
chat_history
```

Stores:

| Column | Description |
|---|---|
| `id` | Unique message identifier |
| `thread_id` | Conversation identifier |
| `role` | User or assistant |
| `title` | Question |
| `message` | Message content |
| `timestamp` | Message creation time |

Used for:

- Loading previous conversations
- Maintaining chat sessions
- Creating new chats
- Displaying conversation history

# LangGraph Workflow

The workflow is implemented using LangGraph.

```
START

 |
 v

Retrieve Documents

 |
 v

Confidence Check

 |
 +----------------+
 |                |
 v                v

High Confidence   Low Confidence

 |                |

 v                v

Generate Answer   Human Review

 |
 v

END
```

Human approval is implemented using:

- LangGraph interrupt
- Checkpoint resume mechanism

---

# Backend API

Built using FastAPI.

| Endpoint | Description |
|---|---|
| GET `/` | Health check |
| POST `/ask` | Runs RAG workflow |
| POST `/resume` | Resumes workflow after approval |

---

# Frontend

Built using Streamlit.

Features:

- Chat interface
- Conversation history
- New chat creation
- Workflow status display
- Human approval interface

---

# Deployment

The backend is containerized using Docker.

Deployment:

```
AWS EC2 Instance

        |

        v

Docker Container

        |

        v

FastAPI Application
```
---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| Workflow | LangGraph |
| Framework | LangChain |
| LLM | Groq Llama-3.3-70b-versatile |
| Embeddings | HuggingFace BAAI/bge-small-en-v1.5 |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Database Hosting | Supabase |
| Containerization | Docker |
| Cloud | AWS EC2 |


---

# Future Improvements

- User authentication
- Multi-user chat support
- RAG evaluation framework
- Monitoring and logging
- Scalable cloud architecture

---

# Author

Atish Sawant
