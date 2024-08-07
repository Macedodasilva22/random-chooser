import sqlite3
import random

class Pedro:
    def __init__(self):
        self.state = 0
        self.dilemma = ""
        self.num_options = 0
        self.options = []
        self.username = None
        self.db_path = 'test_database.db'

    def set_username(self, username):
        self.username = username

    def process_input(self, user_message):
        if self.state == 0:
            self.dilemma = user_message
            self.state += 1
            return "Got it! Now, between how many options are you debating?"
        elif self.state == 1:
            try:
                self.num_options = int(user_message)
                if self.num_options <= 1:
                    return "Please enter a number greater than 1."
                self.state += 1
                return f"Great! Please enter the {self.num_options} options separated by commas."
            except ValueError:
                return "Please enter a valid number for the options."
        elif self.state == 2:
            self.options = [opt.strip() for opt in user_message.split(',')]
            if len(self.options) != self.num_options:
                return f"Please provide exactly {self.num_options} options separated by commas."
            self.state += 1
            return "Thank you! Let me choose one for you..."
        elif self.state == 3:
            chosen_option = random.choice(self.options)
            self.state = 0
            if self.username:
                self.save_choice(self.dilemma, chosen_option)
            return f"My choice for '{self.dilemma}' is: {chosen_option}"

    def save_choice(self, dilemma, choice):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO choices (username, dilemma, choice) VALUES (?, ?, ?)", (self.username, dilemma, choice))
            conn.commit()
        except Exception as e:
            print(f"An error occurred while saving the choice: {e}")
        finally:
            conn.close()

    def get_past_choices(self):
        if not self.username:
            return []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT dilemma, choice FROM choices WHERE username = ?", (self.username,))
            choices = cursor.fetchall()
            return choices
        except Exception as e:
            print(f"An error occurred while retrieving choices: {e}")
            return []
        finally:
            conn.close()

    def get_dilemma_count(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT dilemma) FROM choices")
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0
        finally:
            conn.close()

    def get_choice_count(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM choices")
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0
        finally:
            conn.close()

    def get_dilemma_statistics(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dilemma, choice, COUNT(*)
                FROM choices
                GROUP BY dilemma, choice
                ORDER BY COUNT(*) DESC
            """)
            stats = cursor.fetchall()
            return stats
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    def get_analytics_data(self):
        return {
            'dilemmas': self.get_dilemma_count(),
            'choices': self.get_choice_count()
        }


def setup_database():
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS choices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        dilemma TEXT,
                        choice TEXT)''')
    conn.commit()
    conn.close()

def insert_test_data():
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO choices (username, dilemma, choice) VALUES (?, ?, ?)",
                   ('test_user', 'What to eat?', 'Pizza'))
    cursor.execute("INSERT INTO choices (username, dilemma, choice) VALUES (?, ?, ?)",
                   ('test_user', 'What to eat?', 'Burger'))
    conn.commit()
    conn.close()

def test_get_past_choices():
    setup_database()
    insert_test_data()
    
    pedro = Pedro()
    pedro.db_path = 'test_database.db'
    pedro.set_username('test_user')
    
    choices = pedro.get_past_choices()
    
    assert len(choices) == 2
    assert ('What to eat?', 'Pizza') in choices
    assert ('What to eat?', 'Burger') in choices

    print("Test passed.")

def cleanup_database():
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS choices")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    test_get_past_choices()
    cleanup_database()
