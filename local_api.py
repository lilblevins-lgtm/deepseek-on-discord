from flask import Flask, request, jsonify
from llama_cpp import Llama
import os

# ---- Load GGUF model ----
model_path = "models/deepseek.gguf"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

llm = Llama.from_pretrained(filename=model_path)

# ---- Flask setup ----
app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    """
    JSON payload: {"prompt": "your input text"}
    Returns: {"text": "model output"}
    """
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    output = llm(prompt, max_tokens=512, temperature=0.7)
    text = output["choices"][0]["text"]
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
