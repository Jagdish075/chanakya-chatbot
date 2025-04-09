from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Custom Q&A patterns
def check_custom_reply(user_message):
    message = user_message.lower()

    if "your name" in message or "what is your name" in message:
        return "My name is Chanakya ⚡."
    elif "who created you" in message or "your creator" in message or "who made you" in message or "your developer" in message:
        return "I was created by Jagdish Jorewar."
    
    return None  # No match

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Check for custom replies
    custom_reply = check_custom_reply(user_message)
    if custom_reply:
        return jsonify({"reply": custom_reply})

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Bhai error aa gaya: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
