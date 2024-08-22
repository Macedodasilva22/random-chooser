from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot import Pedro
from database import create_user, check_user, get_user_choices, save_choice

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    response_data = pedro.process_input(user_message)
    return jsonify(response=response_data['response'], next_state=response_data.get('next_state', 0))

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
        response = pedro.process_input(selected_dilemma)
        return jsonify({'response': response})

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

@app.route('/analytics')
def analytics():
    data = pedro.get_analytics_data()
    return render_template('analytics.html', data=data)

@app.route('/statistics')
def statistics():
    stats = pedro.get_dilemma_statistics()
    return render_template('statistics.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
