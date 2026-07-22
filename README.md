# 🚀 LoanBot — Smart AI Loan Assistant

LoanBot is an intelligent, RAG-powered loan assistance chatbot built with **FastAPI**, **LangChain/LangGraph**, **ChromaDB**, and a **React + TypeScript** frontend. It uses a multi-agent orchestration architecture to intelligently route user queries through specialized loan processing domains — sales, verification, underwriting, and sanction — while grounding all answers in official policy documents via Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- **💬 Multi-Domain AI Chat** — Routes loan queries to the right specialist agent (Sales, Verification, Underwriting, Sanction) using a LangGraph state machine.
- **📄 RAG over Policy Documents** — All answers are grounded in official loan policy texts stored in ChromaDB (personal loans, home loans, gold loans, FAQs, company terms).
- **🧠 LangGraph Orchestration** — A stateful workflow manages conversation flow, domain persistence, and memory across turns.
- **🎤 Voice Input/Output** — Speech-to-text (Vosk) and Text-to-Speech (Coqui TTS) for hands-free interaction.
- **📎 Document Upload** — Upload policy documents or customer files; automatically rebuilds the vector index.
- **🔍 Context-Aware Routing** — Short follow-ups and sticky phrases stay locked to the current domain; new keywords trigger intelligent re-routing.
- **🧪 Evaluation Suite** — Built-in retrieval and generation evaluation scripts with pre-built test sets.
- **🌐 Modern Web UI** — React + TypeScript + Tailwind CSS frontend with a clean landing page and chat interface.

---

## 📁 Project Structure

```
LoanBot/
├── backend/                          # Python backend (FastAPI)
│   ├── main_l.py                     # FastAPI app entry point, CORS, route registration
│   ├── master_agent.py               # ReAct agent orchestrator (Ollama + LangChain)
│   ├── rag_chromadb.py               # ChromaDB vector store — embed, query, rebuild index
│   ├── rag_index_builder.py          # Standalone script to build ChromaDB index from documents
│   ├── print_chunks.py               # Utility to inspect ChromaDB document chunks
│   ├── memory_manager.py             # Legacy conversation buffer memory
│   ├── audio_utils.py                # Speech-to-Text (Vosk) & Text-to-Speech (Coqui TTS)
│   │
│   ├── langgraph_agent/              # LangGraph state-machine agent
│   │   ├── graph.py                  # StateGraph definition, node wiring, conditional edges
│   │   ├── state.py                  # LoanBotState TypedDict schema
│   │   ├── nodes.py                  # Router node + domain nodes (sales/verification/underwriting/sanction) with RAG
│   │   └── memory.py                 # SessionMemory — per-session conversation history
│   │
│   ├── routes/                       # FastAPI route modules
│   │   ├── chat.py                   # POST /chat, DELETE /chat/{session_id}
│   │   ├── upload.py                 # POST /upload (document upload + re-index)
│   │   ├── audio.py                  # POST /stt, POST /tts
│   │   └── health.py                 # GET / health check
│   │
│   ├── models/                       # Pydantic request/response models
│   │   ├── chat.py                   # ChatRequest, ChatResponse
│   │   ├── upload.py                 # UploadResponse
│   │   └── audio.py                  # STTResponse, TTSResponse
│   │
│   ├── services/
│   │   └── memory.py                 # MemoryService — conversation history manager
│   │
│   ├── worker_agents/                # Specialized domain agent tools
│   │   ├── sales_agent.py            # Loan product offers & information
│   │   ├── verification_agent.py     # KYC / CRM customer data verification
│   │   ├── underwritting_agent.py    # Eligibility rules (income, credit score, etc.)
│   │   └── sanction_agent.py         # Sanction letter / approval document generation
│   │
│   ├── data/
│   │   ├── documents/                # Raw policy text files (RAG source)
│   │   │   ├── personal_loan_policy.txt
│   │   │   ├── home_loan.txt
│   │   │   ├── gold_loan.txt
│   │   │   ├── loan_faq.txt
│   │   │   └── company_terms.txt
│   │   └── customers.csv             # (optional) Simulated CRM customer data
│   │
│   ├── embeddings/                   # ChromaDB persisted vector store (auto-generated)
│   │
│   └── eval/                         # Evaluation suite
│       ├── eval_retrieval.py         # Retrieval quality evaluation
│       ├── eval_generation.py        # Generation quality evaluation
│       ├── eval_set.json             # Retrieval test set
│       ├── generation_eval_set.json  # Generation test set
│       ├── retrieval_eval_results.json
│       └── generation_eval_results.json
│
├── frontend/
│   ├── index.html                    # Legacy plain HTML frontend
│   └── chat-frontend/                # React + TypeScript + Vite frontend
│       ├── index.html                # Vite entry HTML
│       ├── package.json              # Dependencies (React, React Router, Tailwind, Lucide)
│       ├── vite.config.ts            # Vite build configuration
│       ├── tsconfig.json             # TypeScript configuration
│       ├── postcss.config.js         # PostCSS config (Tailwind)
│       ├── tailwind.config.js        # Tailwind CSS configuration
│       ├── src/
│       │   ├── main.tsx              # React DOM entry point
│       │   ├── App.tsx               # Router (LandingPage / ChatPage)
│       │   ├── types.ts              # Shared TypeScript types
│       │   ├── pages/
│       │   │   ├── LandingPage.tsx    # Hero, Navbar, Footer — intro screen
│       │   │   └── ChatPage.tsx       # Main chat interface layout
│       │   ├── components/
│       │   │   ├── Navbar.tsx         # Top navigation bar
│       │   │   ├── HeroSection.tsx    # Landing page hero with CTA
│       │   │   ├── ChatBox.tsx        # Message display area
│       │   │   ├── ChatInput.tsx      # User text input bar
│       │   │   ├── MessageBubble.tsx  # Individual message bubble
│       │   │   ├── Sidebar.tsx        # Conversation history sidebar
│       │   │   └── Footer.tsx         # Page footer
│       │   └── index.css             # Tailwind base styles
│       └── public/
│           └── vite.svg              # Vite favicon
│
├── requirements.txt                   # Python dependencies
└── .gitignore                         # Git ignore patterns
```

---

## 🧠 Architecture Overview

### AI Agent Workflow (LangGraph)

```
User Input
    │
    ▼
┌────────────────┐
│  Router Node   │  ← Intent classification only (no RAG)
│  (classify     │     Routes based on keywords / sticky phrases /
│   domain)      │     stored domain / AI memory context
└────┬───────────┘
     │
     │  Conditional routing based on query intent
     │
     ├──▶ Sales Node ───────────┐
     ├──▶ Verification Node ────┤
     ├──▶ Underwriting Node ────┤  Each domain node calls _rag_node()
     └──▶ Sanction Node ────────┘  which performs domain-specific RAG:
                                   1. ChromaDB retrieval (k=3 or k=4)
                                   2. Build prompt with policy context + history
                                   3. LLM generation via Ollama (gemma3:4b)
                                   4. Save to session memory
```

### Key Components

| Layer | Technology | Role |
|-------|-----------|------|
| **Backend API** | FastAPI | REST endpoints for chat, upload, audio, health |
| **AI Orchestration** | LangGraph (StateGraph) | Stateful workflow with domain routing |
| **RAG (Vector Store)** | ChromaDB + SentenceTransformer | Semantic search over loan policy documents |
| **LLM** | Ollama (gemma3:4b) | Local LLM for grounded response generation |
| **Worker Agents** | Python functions | Specialized domain logic for loan workflows |
| **Memory** | In-memory session store | Per-user conversation history (LangChain messages) |
| **Speech** | Vosk (STT) + Coqui TTS (TTS) | Voice input/output |
| **Frontend** | React + TypeScript + Vite + Tailwind | Modern chat UI |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** — Web framework
- **LangChain / LangGraph** — LLM orchestration & state machines
- **ChromaDB** — Vector database for RAG
- **Sentence Transformers** (`all-MiniLM-L6-v2`) — Embedding model
- **Ollama** (gemma3:4b) — Local LLM inference
- **Vosk** — Speech-to-text
- **Coqui TTS** — Text-to-speech

### Frontend
- **React 19** + **TypeScript**
- **Vite** — Build tool
- **Tailwind CSS** — Styling
- **React Router v7** — Client-side routing
- **Lucide React** — UI icons

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.ai/) installed and running locally with the `gemma3:4b` model pulled:
  ```bash
  ollama pull gemma3:4b
  ```

### Backend Setup

```bash
# 1. Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build the ChromaDB vector index from policy docs
python -m backend.rag_index_builder

# 4. Start the FastAPI server
uvicorn backend.main_l:app --reload --port 8000
```

The API will be available at **http://localhost:8000**.
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/

### Frontend Setup

```bash
cd frontend/chat-frontend
npm install
npm run dev
```

The frontend will be available at **http://localhost:5173**.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat` | Send a chat message (`{ message, session_id }`) |
| `DELETE` | `/chat/{session_id}` | Clear conversation history for a session |
| `POST` | `/upload` | Upload a document (auto-rebuilds vector index) |
| `POST` | `/stt` | Speech-to-text (upload WAV file) |
| `POST` | `/tts` | Text-to-speech (returns audio file path) |

---

## 🔮 Future Enhancements

- [ ] **Persistent storage** (PostgreSQL / Redis) for conversations & user data
- [ ] **Authentication & user management**
- [ ] **Real-time loan application tracking dashboard**
- [ ] **Multi-language support** for voice and text
- [ ] **Integration with actual CRM & banking APIs**
- [ ] **Document OCR** for uploaded identity proofs
- [ ] **Production deployment** with Docker & CI/CD

---

## 📄 License

This project is for educational and demonstration purposes.

---

