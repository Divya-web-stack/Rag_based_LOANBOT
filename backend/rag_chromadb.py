from langchain_chroma import Chroma                          # fixed: no more deprecation warning
from langchain_huggingface import HuggingFaceEmbeddings      # fixed: no more deprecation warning
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import glob
import shutil

# Folder paths
SCRIPT_DIR = Path(__file__).resolve().parent
CHROMA_DIR = SCRIPT_DIR / "embeddings"
DOCS_DIR   = SCRIPT_DIR / "data" / "documents"


embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

# ---------------------------------------------------------------------------
# ChromaDB client — loaded ONCE at startup, reused every query
# ---------------------------------------------------------------------------
_vectorstore: Chroma | None = None

def _get_vectorstore() -> Chroma:
    """Return the singleton ChromaDB vectorstore, loading it once."""
    global _vectorstore
    if _vectorstore is None:
        if not CHROMA_DIR.exists():
            raise FileNotFoundError(
                f"ChromaDB directory not found at {CHROMA_DIR}. "
                "Run rebuild_index() first."
            )
        print("[RAG] Loading ChromaDB into memory...")
        _vectorstore = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model,
        )
        print("[RAG] ChromaDB loaded")
    return _vectorstore


# ---------------------------------------------------------------------------
# Query documents — original signature kept so nodes.py / callers don't break
# ---------------------------------------------------------------------------
def query_docs(query: str, k: int = 3) -> list:
    """Query ChromaDB for relevant policy chunks (content only)."""
    try:
        db = _get_vectorstore()
        prefixed_query = BGE_QUERY_INSTRUCTION + query
        docs = db.similarity_search(prefixed_query, k=k)
        return [doc.page_content for doc in docs] if docs else []
    except Exception as e:
        print(f"[RAG ERROR] {e}")
        return []


# ---------------------------------------------------------------------------
# NEW: Query with metadata/ids/scores — needed for retrieval evaluation
# ---------------------------------------------------------------------------
def query_docs_with_meta(query: str, k: int = 3) -> list:
    """
    Same retrieval as query_docs(), but returns id + metadata + similarity
    score for each chunk. Use this in eval scripts, not in the live agent
    (keeps nodes.py simple and unchanged).
    """
    try:
        db = _get_vectorstore()
        prefixed_query = BGE_QUERY_INSTRUCTION + query
        results = db.similarity_search_with_score(prefixed_query, k=k)
        out = []
        for doc, score in results:
            out.append({
                "content": doc.page_content,
                "id": doc.metadata.get("chunk_id", "UNKNOWN_ID"),
                "source": doc.metadata.get("source", "UNKNOWN_SOURCE"),
                "score": float(score),
            })
        return out
    except Exception as e:
        print(f"[RAG ERROR] {e}")
        return []


# ---------------------------------------------------------------------------
# Load and chunk policy documents from disk — now returns id + source too
# ---------------------------------------------------------------------------
def load_policy_docs():
    """
    Load all .txt documents from the documents folder and chunk them.
    Returns a list of dicts: {"id": ..., "text": ..., "source": ...}
    so every chunk has a stable, human-readable ID for evaluation.

    Chunking strategy (v2):
    - Smaller chunk_size (220 chars) so each chunk holds a handful of related
      bullets instead of 8+ unrelated facts crammed together. Fewer facts per
      chunk = a sharper, less "blurry" embedding per chunk.
    - Split preferentially on bullet boundaries ("\\n- ") rather than mid-line,
      so a fact is never cut in half across two chunks.
    - Every chunk is prefixed with its document's title (e.g. "Personal Loan
      Policy") before embedding. Small embedding models like all-MiniLM-L6-v2
      struggle to place a short, topic-less fragment (e.g. just a documents
      list) near the right query — repeating the title anchors every chunk
      to its topic even when the chunk itself doesn't restate it.
    """
    chunks_out = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=220,
        chunk_overlap=30,
        separators=["\n\n", "\n- ", "\n", ". ", " "],
    )

    if not DOCS_DIR.exists():
        print(f"Documents folder not found: {DOCS_DIR}")
        return []

    files = glob.glob(str(DOCS_DIR / "*.txt"))
    if not files:
        print(f"No text files found in {DOCS_DIR}")
        return []

    for file in files:
        stem = Path(file).stem  # e.g. "personal_loan_policy"
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"Skipping empty file: {file}")
                continue

            # First non-empty line is treated as the section title
            first_line = next(
                (line.strip() for line in content.splitlines() if line.strip()),
                stem,
            )
            title = first_line if not first_line.startswith("Q:") else stem

            raw_chunks = text_splitter.split_text(content)
            for i, chunk_text in enumerate(raw_chunks):
                chunk_text = chunk_text.strip()
                # Avoid double-prefixing the chunk that already starts with the title
                if chunk_text.startswith(title):
                    enriched_text = chunk_text
                else:
                    enriched_text = f"{title}\n{chunk_text}"

                chunks_out.append({
                    "id": f"{stem}_chunk_{i}",
                    "text": enriched_text,
                    "source": stem,
                })
            print(f"Processed {file}: {len(raw_chunks)} chunks")

    print(f"Loaded {len(chunks_out)} total chunks from {len(files)} files.")
    return chunks_out


# ---------------------------------------------------------------------------
# Rebuild index — now stores ids + metadata so chunks are individually
# addressable for evaluation (and for debugging which file an answer came from)
# ---------------------------------------------------------------------------
def rebuild_index():
    """Recreate ChromaDB embeddings from policy documents."""
    global _vectorstore

    chunks = load_policy_docs()
    if not chunks:
        print("No data available to reindex.")
        return

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    metadatas = [{"chunk_id": c["id"], "source": c["source"]} for c in chunks]

    print("Creating new ChromaDB index...")
    new_store = Chroma.from_texts(
        texts,
        embedding=embedding_model,
        ids=ids,
        metadatas=metadatas,
        persist_directory=str(CHROMA_DIR),
    )
    _vectorstore = new_store
    print("New Chroma index created and loaded into memory.")


if __name__ == "__main__":
    rebuild_index()