import random

class Pedro:  # Rename ChatBot to Pedro
    def __init__(self):
        self.state = 0
        self.dilemma = ""
        self.num_options = 0
        self.options = []

    def process_input(self, user_message):
        if self.state == 0:
            self.dilemma = user_message
            self.state += 1
            return f"Got it! Now, between how many options are you debating?"
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
            self.options = user_message.split(',')
            if len(self.options) != self.num_options:
                return f"Please provide exactly {self.num_options} options separated by commas."
            self.state += 1
            return "Thank you! Let me choose one for you..."
        elif self.state == 3:
            chosen_option = random.choice(self.options)
            self.state = 0  # Reset state for next interaction
            return f"My choice for '{self.dilemma}' is: {chosen_option.strip()}"

# For testing purposes
if __name__ == "__main__":
    pedro = Pedro()  # Instantiate Pedro
    user_input = "I don't know what to wear"
    response = pedro.process_input(user_input)
    print(response)
