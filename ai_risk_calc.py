import os
import json
import subprocess
import openai

# CONFIGURATION
openai.api_key = os.getenv("OPENAI_API_KEY")
APPS_DIR = "./risk_apps"  # Path to your folders containing tools


def load_metadata():
    tools = {}
    for folder in os.listdir(APPS_DIR):
        folder_path = os.path.join(APPS_DIR, folder)
        metadata_path = os.path.join(folder_path, "metadata.json")
        if os.path.isdir(folder_path) and os.path.exists(metadata_path):
            with open(metadata_path) as f:
                metadata = json.load(f)
                tools[metadata["condition_name"].lower()] = {
                    "path": folder_path,
                    "required_features": metadata["required_features"],
                    "description": metadata.get("description", ""),
                }
    return tools


def identify_condition(tools, user_question):
    tool_list = ", ".join([f"'{name}'" for name in tools.keys()])
    system_prompt = f"""You are a medical assistant. Match the user's question to one of the known conditions: {tool_list}. Return only the condition name, or 'unknown'."""

    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
    )
    return response.choices[0].message.content.strip().lower()


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
    print("== Patient Risk Assessment CLI ==")
    tools = load_metadata()

    question = input("\nAsk your question about a patient's risk: ")
    condition = identify_condition(tools, question)

    if condition == "unknown" or condition not in tools:
        print("Sorry, I couldn't identify the condition in your question.")
        return

    print(f"\nIdentified condition: {condition.capitalize()}")
    required_features = tools[condition]["required_features"]
    patient_data = collect_patient_data(required_features)

    print("\nCalculating risk...")
    result = run_tool(tools[condition]["path"], patient_data)
    print(f"\nRisk Assessment Result:\n{result}")


if __name__ == "__main__":
    main()
