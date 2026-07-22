from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

SCRIPT_DIR = Path(__file__).resolve().parent
CHROMA_DIR = SCRIPT_DIR / "embeddings"

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embedding_model)

# Get all documents from ChromaDB
docs = db.get()
print(f"Total chunks: {len(docs['documents'])}\n")
for i, chunk in enumerate(docs['documents'], 1):
    print(f"--- CHUNK {i} ---\n{chunk}\n")
