
import json
import re
from pathlib import Path
from statistics import mean

from backend.langgraph_agent.graph import run_langgraph_agent
from backend.langgraph_agent.nodes import call_llm
from backend.rag_chromadb import query_docs

EVAL_SET_PATH = Path(__file__).parent / "generation_eval_set.json"

JUDGE_PROMPT = """You are evaluating an AI banking assistant's answer.

Question: {question}
Retrieved policy context: {context}
Assistant's answer: {answer}

Rate the answer on two dimensions, each from 1 (worst) to 5 (best):

1. Faithfulness: Is the answer fully supported by the policy context, with no
   invented facts? IMPORTANT: if the context does NOT contain the information
   needed to answer the question, and the assistant honestly says it doesn't
   have that information (e.g. "I don't have that information, please contact
   support"), that is a CORRECT and FAITHFUL answer — score it 5, not low.
   Only score faithfulness low if the assistant stated something as fact that
   is NOT supported by the context, or contradicted the context.

2. Relevance: Does the answer directly address the question asked? A correct,
   honest refusal ("I don't have that information") to a question the context
   can't answer IS relevant — score it 5. Only score relevance low if the
   answer is off-topic, evasive when it shouldn't be, or ignores the question.

Respond ONLY in this exact format, nothing else:
Faithfulness: <score>
Relevance: <score>
"""


def parse_scores(judge_output: str):
    f_match = re.search(r"Faithfulness:\s*(\d)", judge_output)
    r_match = re.search(r"Relevance:\s*(\d)", judge_output)
    faithfulness = int(f_match.group(1)) if f_match else None
    relevance = int(r_match.group(1)) if r_match else None
    return faithfulness, relevance


def run_eval():
    with open(EVAL_SET_PATH, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    rows = []
    for i, item in enumerate(eval_set):
        query = item["query"]
        session_id = f"eval_session_{i}"

        answer = run_langgraph_agent(query, session_id=session_id)

        # Re-derive the context that was likely used. For a perfectly accurate
        # signal, have _rag_node also return retrieved_passages up through
        # run_langgraph_agent and use that instead of re-querying here.
        context = "\n".join(query_docs(query, k=3))

        judge_prompt = JUDGE_PROMPT.format(question=query, context=context, answer=answer)
        judge_output = call_llm(judge_prompt)
        faithfulness, relevance = parse_scores(judge_output)

        rows.append({
            "query": query,
            "answer": answer,
            "faithfulness": faithfulness,
            "relevance": relevance,
        })

        print(f"\nQuery: {query}")
        print(f"Answer: {answer}")
        print(f"Faithfulness: {faithfulness} | Relevance: {relevance}")

    valid_f = [r["faithfulness"] for r in rows if r["faithfulness"] is not None]
    valid_r = [r["relevance"] for r in rows if r["relevance"] is not None]

    print("\n" + "=" * 60)
    print(f"AVERAGE over {len(rows)} queries")
    print(f"  Faithfulness: {mean(valid_f):.2f} / 5" if valid_f else "  Faithfulness: N/A")
    print(f"  Relevance:    {mean(valid_r):.2f} / 5" if valid_r else "  Relevance: N/A")

    out_path = Path(__file__).parent / "generation_eval_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"\nDetailed results saved to {out_path}")


if __name__ == "__main__":
    run_eval()