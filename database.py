import sqlite3

DATABASE = 'database.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                dilemma TEXT NOT NULL,
                choice TEXT NOT NULL
            )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        conn.close()

def create_user(username, password):
    try:
        conn = sqlite3.connect(DATABASE)
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
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

def save_choice(username, dilemma, choice):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO choices (username, dilemma, choice) VALUES (?, ?, ?)", (username, dilemma, choice))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while saving the choice: {e}")
    finally:
        conn.close()

def get_user_choices(username):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT dilemma, choice FROM choices WHERE username = ?", (username,))
        choices = cursor.fetchall()
        return choices
    except Exception as e:
        print(f"An error occurred while fetching user choices: {e}")
        return []
    finally:
        conn.close()
