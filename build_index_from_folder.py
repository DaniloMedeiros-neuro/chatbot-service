import os
from utils.indexer import build_faiss_index
from langchain_community.document_loaders import (
    TextLoader,
    PyMuPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredHTMLLoader,
)

FOLDER = "docs"

def carregar_arquivos():
    documentos = []
    print("📂 Lendo arquivos da pasta 'docs/'...\n")

    for filename in os.listdir(FOLDER):
        path = os.path.join(FOLDER, filename)
        ext = filename.lower().split(".")[-1]

        try:
            if ext == "txt":
                loader = TextLoader(path, encoding="utf-8")
            elif ext == "pdf":
                loader = PyMuPDFLoader(path)
            elif ext in ["doc", "docx"]:
                loader = UnstructuredWordDocumentLoader(path)
            elif ext == "html":
                loader = UnstructuredHTMLLoader(path)
            else:
                print(f"❌ Arquivo ignorado (formato não suportado): {filename}")
                continue

            docs = loader.load()
            for d in docs:
                d.metadata["filename"] = filename
                d.metadata["source"] = filename
                documentos.append({
                    "filename": filename,
                    "content": d.page_content
                })
            print(f"✅ {filename} lido com sucesso ({len(docs)} página(s))")

        except Exception as e:
            print(f"⚠️ Erro ao ler {filename}: {e}")

    print(f"\n📊 Total de documentos processados: {len(documentos)}")
    return documentos


if __name__ == "__main__":
    docs = carregar_arquivos()
    print("\n⚙️ Gerando índice FAISS com embeddings...\n")
    build_faiss_index(docs)
    print("\n🏁 Processo finalizado com sucesso.\n")