# front_end_agent.py

from greeting_agent import handle_greeting
from user_preference_agent import handle_user_preference

# Type annotation for conversation state
from typing import Dict, Any

# Global state for storing user data
conversation_state: Dict[str, Dict[str, Any]] = {}

def front_end_agent(user_input: str, user_id: str = "1234") -> str:
    user_input_lower = user_input.lower()

    if any(word in user_input_lower for word in ["hi", "hello", "hey"]):
        return handle_greeting(user_input)

    elif "my name is" in user_input_lower or "my password is" in user_input_lower:
        return handle_user_preference(user_input, user_id, conversation_state)

    elif "what is my name" in user_input_lower or "what is my password" in user_input_lower:
        return handle_user_preference(user_input, user_id, conversation_state)

    else:
        return "I can handle greetings or your name/password for now."
