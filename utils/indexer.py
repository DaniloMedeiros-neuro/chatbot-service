import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

INDEX_PATH = "data/faiss_index"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def build_faiss_index(documents: list):
    """
    Recebe uma lista de documentos no formato:
    [{"filename": "arquivo.txt", "content": "texto..."}]
    Gera o índice FAISS com embeddings.
    """
    # Splitter: chunks de ~500 caracteres com sobreposição de 50
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    docs = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for chunk in splits:
            docs.append(Document(
                page_content=chunk,
                metadata={"filename": doc["filename"], "source": doc["filename"]}
            ))

    # Gera os embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = FAISS.from_documents(docs, embeddings)

    # Cria a pasta se não existir
    os.makedirs(INDEX_PATH, exist_ok=True)

    # Salva o índice
    db.save_local(INDEX_PATH)
    print(f"✅ Índice FAISS salvo em: {INDEX_PATH}")
