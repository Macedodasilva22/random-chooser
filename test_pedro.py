import random
import sqlite3

class Pedro:
    def __init__(self):
        self.state = 0
        self.dilemma = ""
        self.num_options = 0
        self.options = []
        self.username = None

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
            conn = sqlite3.connect('database.db')
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
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT dilemma, choice FROM choices WHERE username = ?", (self.username,))
            choices = cursor.fetchall()
            return choices
        except Exception as e:
            print(f"An error occurred while retrieving choices: {e}")
            return []
        finally:
            conn.close()

def test_pedro():
    pedro = Pedro()
    pedro.set_username("test_user")

    while True:
        if pedro.state == 0:
            user_input = input("Enter your dilemma: ")
        elif pedro.state == 1:
            user_input = input("Enter the number of options: ")
        elif pedro.state == 2:
            user_input = input("Enter the options separated by commas: ")
        else:
            print(pedro.process_input(""))
            continue

        response = pedro.process_input(user_input)
        print(response)
        if pedro.state == 0:
            print("Past choices:", pedro.get_past_choices())
            break

if __name__ == "__main__":
    test_pedro()