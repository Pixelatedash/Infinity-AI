import os
import time
import shutil
import difflib
from gpt4all import GPT4All

MODEL_PATH = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"  # Change to your model file path
AGENT_FILE = "agent.py"
HISTORY_DIR = "history"

os.makedirs(HISTORY_DIR, exist_ok=True)
model = GPT4All(MODEL_PATH)

def backup_code():
    ts = time.strftime("%Y%m%d-%H%M%S")
    shutil.copy(AGENT_FILE, f"{HISTORY_DIR}/agent_{ts}.py")

def load_code():
    with open(AGENT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_code(code):
    with open(AGENT_FILE, "w", encoding="utf-8") as f:
        f.write(code)

def should_fix(response, last_input):
    if last_input.strip() == "!fix":
        print("⚠️ Manual fix command detected.")
        return True
    fail_phrases = ["i don't know", "doesn't make sense", "i'm still learning", "sorry"]
    return any(phrase in response.lower() for phrase in fail_phrases)

def show_diff(old, new):
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="")
    print("\n".join(diff))

def rewrite_code(current_code, last_question):
    prompt = f"""
You are a Python developer AI.

The following Python code in 'agent.py' failed to answer this question well:
\"\"\"{last_question}\"\"\"

Please provide a fully corrected, working Python script named 'agent.py' that can respond correctly.

Only output the full Python code — no explanations.

Current code:
\"\"\"
{current_code}
\"\"\"

New complete agent.py code:
"""
    new_code = model.generate(prompt, max_tokens=2048)
    return new_code.strip()

def run_chat():
    print("🤖 AI Infinity - type 'exit' to quit, '!fix' to fix the code.")
    backup_code()
    current_code = load_code()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("🤖 Goodbye!")
            break

        if user_input.lower() == "!fix":
            print("⚠️ Fix command triggered. Rewriting agent.py...")
            new_code = rewrite_code(current_code, last_question="Last response was poor or fix requested.")
            show_diff(current_code, new_code)
            save_code(new_code)
            print("✅ agent.py updated. Please restart the program to apply changes.")
            break

        # Simulate calling the agent.py logic by sending the question to the model
        prompt = f"You are an AI assistant. Answer the question:\n{user_input}\nAnswer:"
        response = model.generate(prompt, max_tokens=300).strip()
        print(f"🤖 {response}")

        if should_fix(response, user_input):
            print("⚠️ Poor response detected, you can type '!fix' to fix the AI code.")

if __name__ == "__main__":
    run_chat()
