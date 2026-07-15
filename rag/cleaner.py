import re
from langchain_core.documents import Document


def clean_document(document: Document) -> Document:

    text = document.page_content


    # Remove imports
    text = re.sub(
        r"^import\s+.*?$",
        "",
        text,
        flags=re.MULTILINE
    )


    # Remove JS blocks completely
    text = re.sub(
        r":::js.*?:::",
        "",
        text,
        flags=re.DOTALL
    )


    # Keep python but remove wrapper
    text = text.replace(":::python", "")
    text = text.replace(":::", "")


    # Remove MDX snippet components
    text = re.sub(
        r"<[A-Za-z0-9_]+(?:Py|Js)\s*/>",
        "",
        text
    )


    # Remove HTML comments
    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL
    )


    # Remove JSX tags
    text = re.sub(
        r"</?[A-Za-z][^>]*>",
        "",
        text
    )


    # Remove markdown links
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )


    # Remove MDX references
    text = re.sub(
        r"@\[`([^`]+)`\]",
        r"\1",
        text
    )


    text = re.sub(
        r"@\[[^\]]*\](?:\[[^\]]*\])?",
        "",
        text
    )


    # Remove directives
    text = re.sub(
        r"^:::[^\n]*$",
        "",
        text,
        flags=re.MULTILINE
    )


    # Remove images
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text
    )


    # Remove mermaid
    text = re.sub(
        r"```mermaid.*?```",
        "",
        text,
        flags=re.DOTALL
    )


    # Remove code annotations
    text = re.sub(
        r"\s*#\s*\[!code.*?\]",
        "",
        text
    )


    # Remove table formatting
    text = re.sub(
        r"\|[-:\s|]+\|",
        "",
        text
    )

    text = text.replace("|"," ")


    # Keep python code but remove language marker
    text = text.replace(
        "```python",
        "```"
    )


    # Normalize spaces
    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )


    return Document(
        page_content=text.strip(),
        metadata=document.metadata
    )


def clean_all_documents(documents):

    return [
        clean_document(doc)
        for doc in documents
    ]