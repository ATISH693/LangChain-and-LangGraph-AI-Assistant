from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path

load_dotenv()

MODEL_PATH = "/app/models/bge-small-en-v1.5"

def get_embedding_model():

    model = HuggingFaceEmbeddings( model_name=MODEL_PATH, model_kwargs={"device": "cpu"}, encode_kwargs = {"normalize_embeddings": True})

    return model 


def generate_embeddings( documents: list[Document] ) :
    """
    Generate embeddings for document chunks.

    Returns:
        documents: original LangChain documents
        embeddings: list of vectors
    """

    embedding_model = get_embedding_model()

    texts = [ doc.page_content for doc in documents ]

    vectors = embedding_model.embed_documents(
        texts
    )

    return documents, vectors