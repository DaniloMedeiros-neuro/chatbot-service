from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ask_engine import get_answer
from utils.indexer import build_faiss_index
import os

app = FastAPI()


# Modelos de entrada
class Question(BaseModel):
    question: str


class DocumentInput(BaseModel):
    filename: str
    content: str


class IndexRequest(BaseModel):
    documents: List[DocumentInput]


@app.post("/ask")
async def ask_question(q: Question):
    try:
        print(f"🧠 Pergunta recebida: {q.question}")
        answer, sources = get_answer(q.question)
        print(f"✅ Resposta gerada. Fontes: {sources}")
        return {
            "success": True,
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        print(f"❌ Erro ao responder pergunta: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/index")
async def index_documents(request: IndexRequest):
    try:
        print("🔍 Recebendo documentos para indexação...")
        docs = [doc.dict() for doc in request.documents]
        print(f"📦 Total de documentos recebidos: {len(docs)}")
        filenames = [d["filename"] for d in docs]
        print(f"🗂️ Nomes dos arquivos: {filenames}")

        build_faiss_index(docs)

        print("✅ Indexação concluída.")
        return {
            "success": True,
            "message": f"{len(request.documents)} documentos indexados com sucesso."
        }
    except Exception as e:
        print(f"❌ Erro ao indexar documentos: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
