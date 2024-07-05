from flask import Flask, render_template, request, jsonify
from chatbot import Pedro  # Import Pedro instead of ChatBot

app = Flask(__name__)
pedro = Pedro()  # Instantiate Pedro

chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = pedro.process_input(user_message)  # Use pedro instead of chatbot
    chat_history.append({"user_message": user_message, "chatbot_response": response})
    return jsonify(response=response, chat_history=chat_history)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    chat_history.clear()  # Clear chat history
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
