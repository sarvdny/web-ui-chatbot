import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.form.get('message')
    if not user_message:
        return "No message provided", 400
    response = chat(user_message, None)
    return response

@app.route('/')
def home():
    return render_template('index.html')

load_dotenv("./.env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def chat(message, _):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)