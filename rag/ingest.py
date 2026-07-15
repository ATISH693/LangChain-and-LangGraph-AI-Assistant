from rag.loader import load_documents
from rag.cleaner import clean_all_documents
from rag.chunking import split_documents
from rag.vector_store import get_vector_store
import os
from dotenv import load_dotenv

load_dotenv(override=True)

print(os.getenv("DATABASE_URL"))

print("Loading documents...")

langchain_docs = load_documents("docs/langchain")
langgraph_docs = load_documents("docs/langgraph")

documents = langchain_docs + langgraph_docs

print(f"Loaded {len(documents)} documents")


print("Cleaning...")
documents = clean_all_documents(documents)


print("Chunking...")
chunks = split_documents(documents)
print(f"Created {len(chunks)} chunks")


print("Connecting to PostgreSQL...")
vector_store = get_vector_store()


print("Generating embeddings and storing...")
vector_store.add_documents(chunks)


print("Done!")