import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Caminhos e modelos
INDEX_PATH = "data/faiss_index"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Inicializa os embeddings e carrega FAISS
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Prompt customizado (opcional)
template = """
Você é um assistente útil. Responda com base nos documentos abaixo:

{context}

Pergunta: {question}
Resposta:
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff",
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

def get_answer(question: str):
    result = qa_chain({"query": question})
    answer = result["result"]
    sources = []

    for doc in result["source_documents"]:
        metadata = doc.metadata
        if "source" in metadata:
            sources.append(metadata["source"])
        elif "filename" in metadata:
            sources.append(metadata["filename"])

    return answer, list(set(sources))  # Remove duplicatas
