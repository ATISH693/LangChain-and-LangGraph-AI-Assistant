from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()

model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

def get_embedding_model():
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