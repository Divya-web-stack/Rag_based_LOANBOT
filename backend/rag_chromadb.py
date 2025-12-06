# backend/rag_chromadb.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, glob

# Folder paths
CHROMA_DIR = "backend/embeddings"
DOCS_DIR = "backend/data/documents"

# Initialize embedding model
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


# -----------------------------------------------------------
# 1️⃣ Load and (optionally) re-index policy documents
# -----------------------------------------------------------
def load_policy_docs():
    """Load all text documents from the dataset folder."""
    docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    if not os.path.exists(DOCS_DIR):
        print(f"❌ Documents folder not found: {DOCS_DIR}")
        return []

    files = glob.glob(f"{DOCS_DIR}/*.txt")
    if not files:
        print(f"⚠️ No text files found in {DOCS_DIR}")
        return []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"⚠️ Skipping empty file: {file}")
                continue
            chunks = text_splitter.split_text(content)
            docs.extend(chunks)
            print(f"✅ Processed {file}: {len(chunks)} chunks")

    print(f"📘 Loaded {len(docs)} total text chunks from {len(files)} files.")
    return docs


# -----------------------------------------------------------
# 2️⃣ Create a retriever for querying ChromaDB
# -----------------------------------------------------------
def get_retriever():
    """Return a retriever from ChromaDB for semantic search."""
    if not os.path.exists(CHROMA_DIR):
        raise FileNotFoundError(f"ChromaDB directory not found at {CHROMA_DIR}")

    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    return retriever


# -----------------------------------------------------------
# 3️⃣ Query documents from vector store (RAG)
# -----------------------------------------------------------
def query_docs(query: str) -> str:
    """Query ChromaDB for relevant policy chunks."""
    try:
        retriever = get_retriever()
        docs = retriever.get_relevant_documents(query)
        if not docs:
            return "No relevant policy data found."
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"[RAG ERROR] {e}")
        return "Error retrieving documents from vector database."


# -----------------------------------------------------------
# 4️⃣ (Optional) Rebuild index dynamically
# -----------------------------------------------------------
def rebuild_index():
    """Recreate ChromaDB embeddings if you’ve updated policy docs."""
    from langchain_community.vectorstores import Chroma

    docs = load_policy_docs()
    if not docs:
        print("❌ No data available to reindex.")
        return

    os.makedirs(CHROMA_DIR, exist_ok=True)
    print("🔹 Creating new ChromaDB index...")
    vectorstore = Chroma.from_texts(docs, embedding=embedding_model, persist_directory=CHROMA_DIR)
    vectorstore.persist()
    print("✅ New Chroma index created successfully.")


if __name__ == "__main__":
    # You can rebuild manually by running:
    rebuild_index()
