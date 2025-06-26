import os
import chainlit as cl
from dotenv import load_dotenv
import openai

# Load environment variables (like your OpenAI key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the subjects you're supporting
SUBJECTS = [
    "digital logic design",
    "object oriented programming",
    "java",
    "pre calculus",
    "civics and community engagement",
    "expository writing",
    "financial accounting",
    "islamic studies"
]

# When chat starts, send this intro message
@cl.on_chat_start
async def on_chat_start():
    intro_message = """
👋 **Hello! I am your Personal Assistant**  
📘 I specialize in the following subjects for **Sindh University students (Batch 2025)**:

🔹 Digital Logic Design  
🔹 Object Oriented Programming (Java)  
🔹 Pre Calculus  
🔹 Civics and Community Engagement  
🔹 Expository Writing  
🔹 Financial Accounting  
🔹 Islamic Studies  

💬 Ask me anything related to these subjects!
"""
    await cl.Message(content=intro_message).send()
    cl.user_session.set("history", [])

# Function to ask OpenAI a question
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
        messages=[
            {
                "role": "system",
                "content": "You are a university tutor helping students of Sindh University, Batch 2025. Give clear, concise answers in simple English."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response.choices[0].message["content"]

# Message handler
@cl.on_message
async def on_message(message: cl.Message):
    user_question = message.content.lower()
    history = cl.user_session.get("history", [])

    # Check if the question relates to supported subjects
    if any(subject in user_question for subject in SUBJECTS):
        # Get answer from OpenAI
        try:
            reply = ask_openai(message.content)
        except Exception as e:
            reply = f"❌ Error getting answer from OpenAI: {str(e)}"
    else:
        reply = (
            "⚠️ I'm trained to help with specific subjects for "
            "**Sindh University (Batch 2025)**.\n"
            "Please ask something related to one of these:\n\n"
            + ", ".join([s.title() for s in SUBJECTS])
        )

    history.append({"role": "user", "content": message.content})
    history.append({"role": "assistant", "content": reply})
    cl.user_session.set("history", history)

    await cl.Message(content=reply).send()
