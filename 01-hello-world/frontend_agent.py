from greeting_agent import greeting_agent

def frontend_agent(user_input):
    # yahan pe simple routing logic hoga
    if any(word in user_input.lower() for word in ["hello", "hi", "good morning", "how are you"]):
        response = greeting_agent(user_input)
    else:
        response = "I'm just a simple front-end agent. Try saying 'Hello'."
    return response
