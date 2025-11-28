from flask import Blueprint, render_template, request, jsonify
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load Environment Variables
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL", "google/gemma-2-2b-it")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN missing in .env")


client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)


chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


chat_history = [
    {"role": "system", "content": "You are a helpful virtual nurse. Provide friendly, short medical advice."}
]


@chatbot_bp.route("/")
def chatbot():
    return render_template("chatbot.html")


# API endpoint
@chatbot_bp.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"response": "Please enter a message."})

       
        chat_history.append({"role": "user", "content": user_msg})

       
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=chat_history,
            max_tokens=150
        )

        bot_reply = completion.choices[0].message["content"]

       
        chat_history.append({"role": "assistant", "content": bot_reply})

        return jsonify({"response": bot_reply})

    except Exception as e:
        print("\n❌ BACKEND ERROR:", e, "\n")
        return jsonify({"response": "⚠️ Something went wrong. Please try again."})   
