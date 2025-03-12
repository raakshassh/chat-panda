from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import re

app = Flask(__name__, template_folder=r"C:\\Users\\ashut\\OneDrive\\Desktop\\project job\\chatbot\\templates")

API_KEY = "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"
MODEL = "mistralai/mistral-small-24b-instruct-2501:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        raw_text = response.json()["choices"][0]["message"]["content"]
        
        # Correctly remove \boxed{{...}} using regex
        clean_text = re.sub(r'\\boxed\{(.*?)\}', r'\1', raw_text, flags=re.DOTALL)
        
        return clean_text.strip()
    else:
        return "Error: Unable to fetch response from OpenRouter."

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
