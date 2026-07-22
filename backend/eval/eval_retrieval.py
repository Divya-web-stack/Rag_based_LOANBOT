
import json
from pathlib import Path
from statistics import mean

from backend.rag_chromadb import query_docs_with_meta

EVAL_SET_PATH = Path(__file__).parent / "eval_set.json"
K = 5


def precision_recall_hit_mrr(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)

    num_hits = sum(1 for rid in retrieved_k if rid in relevant_set)

    precision = num_hits / k if k else 0
    recall = num_hits / len(relevant_set) if relevant_set else 0
    hit = 1 if num_hits > 0 else 0

    mrr = 0
    for rank, rid in enumerate(retrieved_k, start=1):
        if rid in relevant_set:
            mrr = 1 / rank
            break

    return precision, recall, hit, mrr


def run_eval(k: int = K):
    with open(EVAL_SET_PATH, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    rows = []
    for item in eval_set:
        query = item["query"]
        relevant_ids = item["relevant_chunk_ids"]

        results = query_docs_with_meta(query, k=k)
        retrieved_ids = [r["id"] for r in results]

        p, r, hit, mrr = precision_recall_hit_mrr(retrieved_ids, relevant_ids, k)
        rows.append({
            "query": query,
            "precision": p,
            "recall": r,
            "hit": hit,
            "mrr": mrr,
            "retrieved_ids": retrieved_ids,
            "relevant_ids": relevant_ids,
        })

        print(f"\nQuery: {query}")
        print(f"  Retrieved: {retrieved_ids}")
        print(f"  Relevant : {relevant_ids}")
        print(f"  Precision@{k}: {p:.2f} | Recall@{k}: {r:.2f} | Hit: {hit} | MRR: {mrr:.2f}")

    print("\n" + "=" * 60)
    print(f"AVERAGE over {len(rows)} queries (k={k})")
    print(f"  Precision@{k}: {mean(r['precision'] for r in rows):.3f}")
    print(f"  Recall@{k}:    {mean(r['recall'] for r in rows):.3f}")
    print(f"  Hit Rate@{k}:  {mean(r['hit'] for r in rows):.3f}")
    print(f"  MRR:           {mean(r['mrr'] for r in rows):.3f}")

    out_path = Path(__file__).parent / "retrieval_eval_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"\nDetailed results saved to {out_path}")


if __name__ == "__main__":
    run_eval()