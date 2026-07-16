from rag.vector_store import get_vector_store

def similarity_search(query: str, k: int = 3):
    """
    Create a retriever from the PostgreSQL vector store.
    """

    vector_store = get_vector_store()

    retriever = vector_store.similarity_search_with_score(
        k = k , query = query
    )

    return retriever


def retrieve(query: str, k : int = 3) -> tuple[list[dict], float]:
    """
    Retrieve the most relevant document chunks.
    """

    documents = similarity_search(query = query, k = k)

    final_docs = []

    best_score = 99999

    for doc, score in documents :

        final_docs.append( 
            {
                "content" : doc.page_content, 
                "source" : doc.metadata.get("source",""),
                "score" : score
            }
        )

        best_score = min(best_score, score)

    return final_docs, best_score 