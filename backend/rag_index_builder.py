from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, glob

# Step 1: Initialize embedding model
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 2: Prepare Chroma directory
CHROMA_DIR = "backend/embeddings"
os.makedirs(CHROMA_DIR, exist_ok=True)

# Step 3: Read and split text files
def create_rag_index():
    docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for file in glob.glob("backend/data/documents/*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            chunks = text_splitter.split_text(content)
            docs.extend(chunks)
            print(f"✅ Processed {file}: {len(chunks)} chunks")

    # Step 4: Build Chroma vectorstore
    vectorstore = Chroma.from_texts(docs, embedding=embedding_model, persist_directory=CHROMA_DIR)
    vectorstore.persist()
    print("✅ Knowledge base successfully embedded and saved to ChromaDB.")

if __name__ == "__main__":
    create_rag_index()
