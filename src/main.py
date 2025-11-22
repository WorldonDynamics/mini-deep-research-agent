import json
import os
from utils import load_data, semantic_search, summarize_papers

def run_queries(queries):
    df = load_data()
    results = {}

    for query in queries:
        print("\n" + "="*80)
        print(f" 🔍 Processing Query: {query}")
        print("="*80)

        top_results = semantic_search(df, query)
        summaries = summarize_papers(top_results)

        results[query] = summaries

        for summary in summaries:
            print("\n" + "-"*80)
            print(summary)
            print("-"*80)

    return results


def main():
    # Get the folder where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Ensure output folder exists relative to script
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # 🟦 Add / modify queries here
    queries = [
        "machine learning",
        "autonomous agents",
        "neural architecture search",
        "reinforcement learning",
    ]

    print("\n=== 🚀 Deep Research Agent — Multi‑Query Mode ===\n")

    results = run_queries(queries)

    # Save output for later
    output_path = os.path.join(output_dir, "multi_query_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n\n📁 Results saved to: {output_path}")
    print("✨ Done!\n")


if __name__ == "__main__":
    main()
