from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("question")
    
    response = client.chat.completions.create(
        model="openai/gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant"},
            {"role": "user", "content": query}
        ],
        temperature=0.7,
        max_tokens=512
    )
    answer = response.choices[0].message.content.strip()
    return jsonify({"response": answer}), 200


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        email_text = request.form.get("email")

        response = client.chat.completions.create(
            model="openai/gpt-5.4-mini",
            messages=[
                {"role": "system", "content": "Summarize this email in 2-3 sentences"},
                {"role": "user", "content": email_text}
            ],
            temperature=0.3,
            max_tokens=150
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({"response": summary}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 