from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import re

template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_folder)

API_KEY = "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"
MODEL = "qwen/qwen-2.5-coder-32b-instruct:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_openrouter(prompt, personality="cute_panda"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Hardcoded name and backstory for specific identity-related queries
    if "what is your name" in prompt.lower() or "who are you" in prompt.lower():
        return "Hello! 🐼 My name is Puchu, and I was created with care by Rakshash! 💖"
    
    if "who made you" in prompt.lower():
        return "Rakshash made me! 🐼💖"
    
    if "who coded you" in prompt.lower():
        return "Rakshash coded me! 🐼💻💖"

    # Inject personality into the prompt for other responses
    if personality == "cute_panda":
        prompt = f"Respond in a friendly, cute, and playful panda style. Keep it sweet but simple, with a warm tone and emojis. Also your name is puchu {prompt}"
    elif personality == "formal":
        prompt = f"Respond politely and formally. {prompt}"
    elif personality == "witty":
        prompt = f"Respond in a witty and humorous manner. {prompt}"
    else:
        prompt = f"Respond neutrally. {prompt}"

    # Payload to send to OpenRouter API
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        raw_text = response.json()["choices"][0]["message"]["content"]
        
        # Clean up the response if needed (e.g., remove special formatting)
        clean_text = re.sub(r'\\boxed\{(.*?)\}', r'\1', raw_text, flags=re.DOTALL)
        
        return clean_text.strip()
    else:
        return "Oops! Something went wrong... 😟"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    bot_response = query_openrouter(user_message)
    return jsonify({"response": bot_response})

@app.route("/clear", methods=["POST"])
def clear():
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
