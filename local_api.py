import os
import subprocess
from flask import Flask, request, jsonify
from llama_cpp import Llama

MODEL_REPO_URL = "https://huggingface.co/bartowski/deepseek-r1-qwen-2.5-32B-ablated-GGUF/resolve/main/deepseek-r1-qwen-2.5-32B-ablated-IQ2_M.gguf"
MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "deepseek.gguf")

HF_TOKEN = os.getenv("HF_TOKEN")       # optional if repo is public
PORT = int(os.getenv("PORT", 8080))    # Render provides PORT

def ensure_model_exists():
    """Download GGUF file if not already present."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    if os.path.exists(MODEL_FILE):
        print(f"✅ Model already present at {MODEL_FILE}")
        return
    print("⬇️ Downloading model from Hugging Face (this can take a while)...")
    cmd = ["wget", "-O", MODEL_FILE, MODEL_REPO_URL]
    if HF_TOKEN:
        cmd.insert(1, "--header")
        cmd.insert(2, f"Authorization: Bearer {HF_TOKEN}")
    subprocess.run(cmd, check=True)
    print("✅ Model downloaded successfully!")

def load_model():
    """Load the GGUF model."""
    if not os.path.exists(MODEL_FILE):
        ensure_model_exists()
    print("🧠 Loading model into memory...")
    llm = Llama.from_pretrained(filename=MODEL_FILE)
    print("✅ Model loaded successfully!")
    return llm

app = Flask(__name__)
llm = None

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Missing 'prompt' field"}), 400
    try:
        result = llm(prompt, max_tokens=512, temperature=0.7)
        text = result["choices"][0]["text"].strip()
        return jsonify({"text": text})
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    ensure_model_exists()
    llm = load_model()
    print(f"🚀 API running on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
