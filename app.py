from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot import Pedro
from database import create_user, check_user, get_user_choices, save_choice

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize a global Pedro instance
pedro = Pedro()

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        pedro.set_username(username)
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
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

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print(f"Received message: {user_message}")  # Debugging line
    response = pedro.process_input(user_message)
    print(f"Response: {response}")  # Debugging line
    return jsonify(response=response)

@app.route('/view_past_choices')
def view_past_choices():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    past_choices = get_user_choices(username)
    return render_template('past_choices.html', past_choices=past_choices)

@app.route('/rerun_dilemma', methods=['GET', 'POST'])
def rerun_dilemma():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        selected_dilemma = request.form['dilemma']
        return pedro.process_input(selected_dilemma)

    past_choices = get_user_choices(username)
    return render_template('rerun_dilemma.html', past_dilemmas=[d[0] for d in past_choices])

@app.route('/get_suggestions')
def get_suggestions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    past_choices = get_user_choices(username)
    suggestions = pedro.get_past_choices()
    return render_template('suggestions.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
