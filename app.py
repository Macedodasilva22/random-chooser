from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from chatbot import Pedro

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
pedro = Pedro()

# Initialize chat history in the session
def init_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = []

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        pedro.set_username(username)
        past_choices = pedro.get_past_choices()
        chat_history = session.get('chat_history', [])
        return render_template('index.html', chat_history=chat_history, past_choices=past_choices)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            init_chat_history()
            return redirect(url_for('index'))
        else:
            return "Login failed. Check your username and/or password."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = create_user(username, password)
        if error:
            return f"Registration failed: {error}"
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('chat_history', None)  # Clear chat history on logout
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = pedro.process_input(user_message)
    chat_history = session.get('chat_history', [])
    chat_history.append({"user_message": user_message, "chatbot_response": response})
    session['chat_history'] = chat_history
    return jsonify(response=response, chat_history=chat_history)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    session['chat_history'] = []  # Clear chat history in the session
    return jsonify(success=True)

def create_user(username, password):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while creating the user."
    finally:
        conn.close()
    return None

def check_user(username, password):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
