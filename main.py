from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ask_engine import get_answer
from utils.indexer import build_faiss_index

app = FastAPI()

# Modelos de entrada
class Question(BaseModel):
    question: str

class DocumentInput(BaseModel):
    filename: str
    content: str

class IndexRequest(BaseModel):
    documents: List[DocumentInput]

# Endpoint para perguntas
@app.post("/ask")
async def ask_question(q: Question):
    try:
        answer, sources = get_answer(q.question)
        return {
            "success": True,
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Endpoint para indexação
@app.post("/index")
async def index_documents(request: IndexRequest):
    try:
        print("🔍 Recebendo documentos para indexação")
        docs = [doc.dict() for doc in request.documents]
        print(f"📄 Documentos recebidos: {len(docs)}")
        build_faiss_index(docs)
        return {
            "success": True,
            "message": f"{len(request.documents)} documentos indexados com sucesso."
        }
    except Exception as e:
        print(f"❌ Erro ao indexar: {e}")
        return {
            "success": False,
            "error": str(e)
        }

