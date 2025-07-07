import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def index():
    """Render form for user input."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle form submission and query ChatGPT."""
    user_message = request.form.get('message', '')
    if not user_message:
        return render_template('index.html', error='Please enter a message')

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"Error communicating with OpenAI API: {e}"
    return render_template("index.html", user_message=user_message, response=response)

if __name__ == '__main__':
    app.run(debug=True)
