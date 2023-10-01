from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from typing import List


def doc_search(texts: List[str], embeddings: OpenAIEmbeddings) -> FAISS:
    f"""
    Build document searching from FAISS.
    """
    docsearch = FAISS.from_texts(texts, embeddings)
    return docsearch