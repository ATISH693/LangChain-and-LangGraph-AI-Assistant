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

The application uses PostgreSQL for both vector storage and workflow persistence.

Database:

```
PostgreSQL + pgvector
```

Hosted on:

```
Supabase
```

## Vector Database

Used for storing document embeddings.

Stores:

| Column | Purpose |
|---|---|
| Document Content | Original text chunks |
| Embedding Vector | Numerical representation of text |
| Metadata | Source information |

Used by:

```
LangChain PGVector Retriever
```

for similarity search.

---

## LangGraph Checkpoint Database

Stores workflow execution state.

Stores:

| Data | Purpose |
|---|---|
| Thread ID | Unique workflow session |
| Checkpoints | Saved workflow state |
| Interrupt State | Human approval status |

Implemented using:

```
langgraph-checkpoint-postgres
PostgresSaver
```

---

## Chat History Database

A separate table stores user conversations.

Table:

```
chat_history
```

Schema:

| Column | Description |
|---|---|
| id | Message ID |
| thread_id | Conversation identifier |
| role | User / Assistant |
| title | Question |
| message | Chat content |
| timestamp | Message time |

Used by Streamlit to:

- Load previous conversations
- Create new chats
- Maintain chat sessions

---

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
