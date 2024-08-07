from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot import Pedro
from database import create_user, authenticate_user, get_user_choices, save_user_choice

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management
pedro = Pedro()

chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = pedro.process_input(user_message)
    chat_history.append({"user_message": user_message, "chatbot_response": response})
    
    if 'username' in session:
        save_user_choice(session['username'], pedro.dilemma, response)
    
    return jsonify(response=response, chat_history=chat_history)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    chat_history.clear()
    return jsonify(success=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('chat_page'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat_page')
def chat_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
