# main.py
import os
import json
from utils import load_data, semantic_search, summarize_papers

# List of queries for multi-query mode
QUERIES = [
    "machine learning",
    "autonomous agents",
    "neural architecture search",
    "reinforcement learning"
]

def main():
    # Load dataset
    df = load_data()
    print("=== 🚀 Deep Research Agent — Multi‑Query Mode ===\n")
    
    all_results = {}

    for query in QUERIES:
        print("="*80)
        print(f" 🔍 Processing Query: {query}")
        print("="*80 + "\n")
        
        # Semantic search
        top_results = semantic_search(df, query)
        
        # Display top results
        for idx, row in top_results.iterrows():
            print("-"*80)
            print(f"Title: {row['title']}")
            print(f"Abstract Preview: {row['abstract'][:75]}...")
            print(f"Authors: {row['authors']}\n")
        print("-"*80 + "\n")
        
        # Summarize results
        summaries = summarize_papers(top_results)
        all_results[query] = summaries
    
    # Ensure output directory exists
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all query results to JSON
    output_file = os.path.join(output_dir, "multi_query_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f"\n✅ All query results saved to: {output_file}\n")
    print("=== Finished 🚀 ===")

if __name__ == "__main__":
    main()
    