from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import torch
from functools import lru_cache

load_dotenv()
torch.set_num_threads(1)

MODEL_PATH = "/app/models/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embedding_model():

    model = HuggingFaceEmbeddings( model_name=MODEL_PATH, model_kwargs={"device": "cpu"}, encode_kwargs = {"normalize_embeddings": True, "batch_size": 1})

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