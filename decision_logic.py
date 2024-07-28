def get_suggestions(user_input):
    categories = {
        'food': ["Pizza", "Burger", "Sushi"],
        'movie': ["Inception", "The Matrix", "Interstellar"],
        'activity': ["Running", "Reading", "Gardening"],
       
    }

    user_input_lower = user_input.lower()
    for category, options in categories.items():
        if category in user_input_lower:
            return options

   
    return ["Option 1", "Option 2", "Option 3"]
