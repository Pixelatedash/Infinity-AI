# web_ui.py
from flask import Flask, render_template, request, jsonify
from gpt4all import GPT4All

app = Flask(__name__)
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data["message"]
    response = model.generate(prompt, max_tokens=512)
    return jsonify({"response": response.strip()})

if __name__ == "__main__":
    app.run(debug=True)
