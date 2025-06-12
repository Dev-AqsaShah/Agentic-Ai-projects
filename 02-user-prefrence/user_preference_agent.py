# user_preference_agent.py
def handle_user_preference(user_input, user_id, memory):
    if user_id not in memory:
        memory[user_id] = {}

    if "my name is" in user_input.lower():
        name = user_input.split("is")[-1].strip()
        memory[user_id]['name'] = name
        return f"Got it! I’ll remember your name is {name}."

    elif "my password is" in user_input.lower():
        password = user_input.split("is")[-1].strip()
        memory[user_id]['password'] = password
        return "Thanks! I saved your password."

    elif "what is my name" in user_input.lower():
        name = memory[user_id].get('name')
        return f"Your name is {name}." if name else "I don't know your name yet. Please tell me."

    elif "what is my password" in user_input.lower():
        password = memory[user_id].get('password')
        return f"Your password is {password}." if password else "I don't have your password yet."

    else:
        return "I'm not sure what to do with that info."
