from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings


def search_policies(query):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    docs = [
        "Loan EMI must not exceed 50% of income.",
        "Minimum credit score required is 700.",
        "Pre-approved customers enjoy instant disbursal."
    ]
    db = FAISS.from_texts(docs, embeddings)
    result = db.similarity_search(query, k=1)
    return result[0].page_content
