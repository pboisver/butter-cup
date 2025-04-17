import os
import json
import subprocess
import argparse
import openai
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# CONFIGURATION
openai.api_key = os.getenv("OPENAI_API_KEY")
APPS_DIR = "./risk_apps"
INDEX_FILE = "tool_index.faiss"
METADATA_FILE = "tool_metadata.pkl"
EMBED_MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(EMBED_MODEL)


def load_metadata():
    tools = []
    for folder in os.listdir(APPS_DIR):
        folder_path = os.path.join(APPS_DIR, folder)
        metadata_path = os.path.join(folder_path, "metadata.json")
        if os.path.isdir(folder_path) and os.path.exists(metadata_path):
            with open(metadata_path) as f:
                metadata = json.load(f)
                tools.append(
                    {
                        "condition_name": metadata["condition_name"],
                        "required_features": metadata["required_features"],
                        "description": metadata.get("description", ""),
                        "path": folder_path,
                    }
                )
    return tools


def build_vector_index(tools):
    descriptions = [
        tool["description"] + " | " + tool["condition_name"] for tool in tools
    ]
    embeddings = model.encode(descriptions)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(tools, f)
    return index, tools


def load_vector_index():
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "rb") as f:
        tools = pickle.load(f)
    return index, tools


def search_condition(index, tools, query):
    embedding = model.encode([query])
    D, I = index.search(embedding, 1)
    best_match = tools[I[0][0]] if I[0][0] < len(tools) else None
    return best_match


def collect_patient_data(required_fields):
    print("\nPlease provide the following patient information:")
    data = {}
    for field in required_fields:
        value = input(f"- {field}: ")
        data[field] = value
    return data


def run_tool(folder_path, patient_data):
    process = subprocess.run(
        ["python", os.path.join(folder_path, "main.py")],
        input=json.dumps(patient_data),
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Run the Patient Risk Assessment CLI")
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Force rebuild of the FAISS vector index",
    )
    args = parser.parse_args()

    print("== Patient Risk Assessment CLI ==")

    if args.rebuild_index or not (
        os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE)
    ):
        print("[INFO] Building vector index from metadata...")
        tools = load_metadata()
        index, tools = build_vector_index(tools)
    else:
        print("[INFO] Loading existing vector index...")
        index, tools = load_vector_index()

    question = input("\nAsk your question about a patient's risk: ")
    tool = search_condition(index, tools, question)

    if not tool:
        print("Sorry, I couldn't identify a matching condition.")
        return

    print(f"\nIdentified condition: {tool['condition_name']}")
    patient_data = collect_patient_data(tool["required_features"])

    print("\nCalculating risk...")
    result = run_tool(tool["path"], patient_data)
    print(f"\nRisk Assessment Result:\n{result}")


if __name__ == "__main__":
    main()
