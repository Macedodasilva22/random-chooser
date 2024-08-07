import random
import sqlite3

class Pedro:
    def __init__(self):
        self.state = 0
        self.dilemma = ""
        self.num_options = 0
        self.options = []
        self.username = None
        self.db_path = 'database.db'

    def set_username(self, username):
        self.username = username

    def process_input(self, user_message):
        if self.state == 0:
            self.dilemma = user_message
            self.state = 1
            return "Got it! Now, between how many options are you debating?"
        elif self.state == 1:
            try:
                self.num_options = int(user_message)
                if self.num_options <= 1:
                    return "Please enter a number greater than 1."
                self.state = 2
                return f"Great! Please enter the {self.num_options} options separated by commas."
            except ValueError:
                return "Please enter a valid number for the options."
        elif self.state == 2:
            self.options = [opt.strip() for opt in user_message.split(',')]
            if len(self.options) != self.num_options:
                return f"Please provide exactly {self.num_options} options separated by commas."
            self.state = 3
            return "Thank you! Let me choose one for you..."
        elif self.state == 3:
            chosen_option = random.choice(self.options)
            self.state = 0
            if self.username:
                self._save_choice(self.dilemma, chosen_option)
            return f"My choice for '{self.dilemma}' is: {chosen_option}"

    def _save_choice(self, dilemma, choice):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO choices (username, dilemma, choice) VALUES (?, ?, ?)", (self.username, dilemma, choice))
                conn.commit()
        except Exception as e:
            print(f"An error occurred while saving the choice: {e}")

    def get_past_choices(self):
        if not self.username:
            return []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT dilemma, choice FROM choices WHERE username = ?", (self.username,))
                return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred while retrieving choices: {e}")
            return []
