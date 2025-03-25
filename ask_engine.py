import os
from typing import Tuple, List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
INDEX_PATH = "data/faiss_index"
INDEX_FILE = os.path.join(INDEX_PATH, "index.faiss")


def get_answer(question: str) -> Tuple[str, List[str]]:
    # Verifica se o índice existe
    if not os.path.exists(INDEX_FILE):
        return "❌ O índice ainda não foi criado. Use o endpoint /index antes de perguntar.", []

    # Carrega embeddings e FAISS sob demanda
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Prompt customizado
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Você é um assistente útil. Responda com base nos documentos abaixo:

{context}

Pergunta: {question}
Resposta:
""",
    )

    # Cadeia de resposta com OpenAI
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    # Executa a pergunta
    result = qa_chain({"query": question})
    answer = result["result"]

    sources = []
    for doc in result["source_documents"]:
        metadata = doc.metadata
        if "source" in metadata:
            sources.append(metadata["source"])
        elif "filename" in metadata:
            sources.append(metadata["filename"])

    return answer, list(set(sources))