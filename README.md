# 📚 Assistente de Perguntas sobre Documentos (Google Drive + LangChain + FAISS)

Este projeto permite consultar documentos armazenados no Google Drive usando inteligência artificial com LangChain, FAISS e OpenAI (GPT-3.5).

---

## 🔧 Estrutura do Projeto

| Componente        | Função                                                   |
|-------------------|----------------------------------------------------------|
| Google Apps Script| Interface HTML + acesso aos arquivos no Google Drive     |
| API Python (Render)| Busca semântica, geração de embeddings, ChatGPT         |
| FAISS             | Indexação vetorial local com metadados de origem         |

---

## 🚀 Fluxo de Funcionamento

1. O Google Apps Script acessa os arquivos do Google Drive.
2. Ele envia os textos para a API Python hospedada (ex: Render).
3. A API indexa os documentos com FAISS e responde perguntas via ChatGPT.
4. As respostas são exibidas no painel HTML do GAS.

---

## 📁 Estrutura do Backend Python

chatbot_langchain/ ├── main.py ├── ask_engine.py ├── requirements.txt ├── utils/ │ ├── indexer.py │ └── (opcional) file_loader.py ├── data/ │ ├── documents/ │ └── faiss_index/



---

## ☁️ Como subir no Render

### 1. Crie um repositório no GitHub com os arquivos do projeto

### 2. Vá para [https://render.com](https://render.com)

- Clique em **New > Web Service**
- Conecte sua conta GitHub
- Selecione o repositório
- Defina:
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
  - **Environment**:
    - `OPENAI_API_KEY` = sua chave da OpenAI
- Escolha **Python 3.10+**
- Porta: Render detecta automaticamente (use `port 10000` se quiser forçar)

---

## 🔐 Configuração do Google Apps Script

### 1. Crie um novo projeto do GAS

- Inclua os arquivos:
  - `Code.gs` → lógica do servidor + integração
  - `index.html` → interface do painel

### 2. Defina o ID da pasta do Google Drive no topo do `Code.gs`:

```js
const FOLDER_ID = "ID_DA_SUA_PASTA_AQUI";

const API_BASE = "https://seu-backend.onrender.com";
