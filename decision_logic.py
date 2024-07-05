def get_suggestions(user_input):
    categories = {
        'food': ["Pizza", "Burger", "Sushi"],
        'movie': ["Inception", "The Matrix", "Interstellar"],
        'activity': ["Running", "Reading", "Gardening"],
        # Add more categories and suggestions as needed
    }

    user_input_lower = user_input.lower()
    for category, options in categories.items():
        if category in user_input_lower:
            return options

    # Default suggestions if no specific category matches
    return ["Option 1", "Option 2", "Option 3"]
