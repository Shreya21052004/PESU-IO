# 🩺 Medical Assistant Chatbot

An **Agentic RAG-based medical chatbot** that answers disease and symptom-related queries using a local medical knowledge base.

## 🚀 Features

- **Agentic RAG** using LlamaIndex `ReActAgent`
- Semantic search using **Jina AI Embeddings**
- **Groq Llama 3 70B** for response generation
- Persistent **VectorStoreIndex** for efficient retrieval
- Conversational interface built with **Streamlit**
- Disease and symptom-focused query handling
- Conversational memory using `ChatMemoryBuffer`

## 🏗️ Architecture

```text
Medical Documents
       │
       ▼
Jina AI Embeddings
       │
       ▼
VectorStoreIndex
       │
       ▼
ReAct Agent
       │
       ├── Search Tool
       ├── Symptom Tool
       └── Disease Tool
       │
       ▼
Query Engine
       │
       ▼
Relevant Medical Context
       │
       ▼
Groq Llama 3 70B
       │
       ▼
Generated Response
```

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core development |
| **Streamlit** | Chatbot interface |
| **LlamaIndex** | RAG, vector indexing & agent framework |
| **ReActAgent** | Agentic tool orchestration |
| **Groq** | LLM inference |
| **Llama 3 70B** | Response generation |
| **Jina AI Embeddings** | Semantic embeddings |
| **Pydantic** | Data validation |
| **python-dotenv** | Environment configuration |

## 📂 Project Structure

```text
PROJECT/
│
├── data/
│   ├── disease.md
│   ├── medical.md
│   └── medical2.md
│
├── index/
│   └── persisted vector index
│
├── utils/
│   └── schema.py
│
├── main.py
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install streamlit llama-index llama-index-llms-groq llama-index-embeddings-jinaai pydantic python-dotenv
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
JINA_API_KEY=your_jina_api_key
```

### 3. Add Medical Data
Place the medical knowledge documents inside the `data/` directory.

### 4. Run the Application
```bash
streamlit run main.py
```
*Note: The vector index is created from the documents in `data/` during the first run and reused on subsequent runs.*

## 🔄 RAG Workflow

```text
User Query
    ↓
ReAct Agent
    ↓
Tool Selection
    ↓
Semantic Retrieval
    ↓
Relevant Medical Context
    ↓
Groq Llama 3 70B
    ↓
Final Response
```

## ⚠️ Disclaimer

This project is intended for educational and informational purposes only. It does not provide medical diagnosis or treatment and should not be used as a substitute for professional medical advice.
