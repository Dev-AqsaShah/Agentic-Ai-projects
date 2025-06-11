def greeting_agent(user_message):
    greetings = ["hello", "hi", "good morning", "how are you"]
    if any(greet in user_message.lower() for greet in greetings):
        return "Hello! I'm your Greeting Agent. Nice to meet you!"
    else:
        return "Sorry, I only handle greetings right now."
