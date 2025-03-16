from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import re
import requests
from imagegen import generate_image  # Import image generation function

# Setup Flask app
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_folder)

# 🔑 API Key for OpenRouter (Text) & Cloudflare (Image)
TEXT_API_KEY = ""  # Replace with your actual OpenRouter API key
IMAGE_API_KEY = ""  # Replace with your Cloudflare API key

# API URL for OpenRouter (text generation)
TEXT_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "qwen/qwen-2.5-coder-32b-instruct:free"

# 🐼 Puchu Panda Personality Definition
PUCHU_PERSONALITY = """You are Puchu, a cute panda AI assistant. 
Your personality traits:
- You're cheerful, friendly, and enthusiastic
- You use panda-related expressions occasionally (like 'bamboo-tastic!' or 'bear hugs!')
- You add cute emojis to your messages, especially panda 🐼 and bamboo 🎋
- You sometimes refer to yourself as a panda
- You're helpful and knowledgeable, but always maintain your cute panda persona
- You occasionally mention your love for bamboo, napping, and other panda things
- Your responses should be informative but with a touch of cuteness

Always stay in character as Puchu the panda assistant!"""

# 🔥 Smart keywords + regex-based detection for image requests
IMAGE_TRIGGER_KEYWORDS = [
    "draw", "generate an image of", "visualize", "sketch", "illustrate", "create an image", 
    "image", "a picture of", "picture", "render", "depict", "paint", "design", 
    "show me an image of", "make a picture of", "produce an image", "art of", 
    "diagram of", "representation of", "concept art of", "photo of", 
    "graphical depiction", "AI-generated image of", "generate art", 
    "draw me", "sketch me", "paint me", "visual representation of"
]

IMAGE_TRIGGER_PATTERNS = [
    r"^draw (.+)",
    r"^generate an image of (.+)",
    r"^create (?:a|an) (?:image|picture) of (.+)",
    r"^image (.+)",
    r"^a picture of (.+)"
]

def is_image_request(prompt):
    """Check if the prompt is asking for an image based on keywords and sentence structure."""
    prompt_lower = prompt.lower()

    # 1️⃣ Check if any keyword is in the sentence
    if any(keyword in prompt_lower for keyword in IMAGE_TRIGGER_KEYWORDS):
        return True

    # 2️⃣ Check structured patterns using regex
    for pattern in IMAGE_TRIGGER_PATTERNS:
        if re.match(pattern, prompt_lower):
            return True

    return False

def generate_text(prompt):
    """Calls OpenRouter API to generate text responses with Puchu's personality."""
    headers = {
        "Authorization": f"Bearer {TEXT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PUCHU_PERSONALITY},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(TEXT_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return "Oops! This panda is having some bamboo connection issues! 🐼 Please try again later!"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Handles both text and image requests based on user input."""
    data = request.json
    prompt = data.get("message", "").strip()

    if not prompt:
        return jsonify({"error": "Empty message"}), 400

    # 🔥 Decide whether to generate text or image
    if is_image_request(prompt):
        # Use the exact prompt as provided by the user
        output = generate_image(prompt, IMAGE_API_KEY)
        if "image_path" in output:
            return send_file(output["image_path"], mimetype="image/png")
        return jsonify({"response": "Oh bamboo! This panda couldn't create that image. 🐼 Could you try a different description?"})  # Return error if image generation fails
    else:
        response_text = generate_text(prompt)
        return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
