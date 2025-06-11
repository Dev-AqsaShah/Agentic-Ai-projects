# main.py
from frontend_agent import frontend_agent

def main():
    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        reply = frontend_agent(user_msg)
        print("Agentia Bot:", reply)

if __name__ == "__main__":
    main()
