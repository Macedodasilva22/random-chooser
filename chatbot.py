import sqlite3
import random

class Pedro:
    def __init__(self):
        self.state = 0
        self.dilemma = ""
        self.options = []
        self.username = None
        self.db_path = 'database.db'

    def set_username(self, username):
        self.username = username

    def process_input(self, user_message):
        user_message = user_message.strip()

        if self.state == 0:
            self.dilemma = user_message
            self.state += 1
            return {
                "response": "Got it! Now, please enter your options, one per line. Press enter after each option.",
                "next_state": 1
            }

        elif self.state == 1:
            if not user_message:
                return {"response": "Please provide the options.", "next_state": self.state}
            
            # Accept options separated by newlines
            self.options = [opt.strip() for opt in user_message.splitlines()]
            if len(self.options) < 2:
                return {"response": "Please provide at least two options.", "next_state": self.state}
            
            self.state += 1
            return {"response": "Thank you! Let me choose one for you...", "next_state": 2}

        elif self.state == 2:
            if not self.options:
                return {"response": "Error: No options available to choose from.", "next_state": self.state}
            chosen_option = random.choice(self.options)
            self.state = 0
            if self.username:
                self.save_choice(self.dilemma, chosen_option)
            return {"response": f"My choice for '{self.dilemma}' is: {chosen_option}", "next_state": self.state}

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
