import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from rag.embeddings import get_embedding_model
from functools import lru_cache

load_dotenv(override=True)

@lru_cache(maxsize=1)
def get_vector_store():
    """
    Create or connect to the PostgreSQL vector store.
    """

    vector_store = PGVector(
    embeddings=get_embedding_model(),
    collection_name="langgraph_docs",
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
    engine_args={
        "connect_args": {
            "prepare_threshold": None
            }
        }
    )
    return vector_store