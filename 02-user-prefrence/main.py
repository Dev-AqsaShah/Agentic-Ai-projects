# main.py

from front_end_agent import front_end_agent

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Agent: Goodbye!")
        break
    response = front_end_agent(user_input)
    print("Agent:", response)
