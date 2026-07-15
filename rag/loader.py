import frontmatter
from pathlib import Path
from langchain_core.documents import Document

def load_single_document(file_path: Path) -> Document:
    """
    Load a single Markdown/MDX file and convert it into a LangChain Document.
    """

    post = frontmatter.load(file_path)

    return Document(
        page_content=post.content,
        metadata={
            "source": str(file_path),
            "title": post.metadata.get("title", file_path.stem),
        },
    )


def load_documents(docs_path: str | Path) -> list[Document]:
    """
    Recursively load all .md and .mdx files from the documentation directory.
    """

    docs_path = Path(docs_path)

    documents = []

    for file_path in docs_path.rglob("*"):

        if file_path.suffix.lower() not in {".md", ".mdx"}:
            continue

        documents.append(load_single_document(file_path))

    return documents


