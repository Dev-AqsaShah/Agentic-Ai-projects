import os
import chainlit as cl
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro")  # ✅ Working now!

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

@cl.on_chat_start
async def on_chat_start():
    welcome = """
👋 **Hi! I'm your subject assistant.**  
🎓 I specialize in these subjects (Sindh University Batch 2025):

🔸 Digital Logic Design  
🔸 Object Oriented Programming  
🔸 Java  
🔸 Pre Calculus  
🔸 Civics and Community Engagement  
🔸 Expository Writing  
🔸 Financial Accounting  
🔸 Islamic Studies  

💬 Ask your subject-related questions.
"""
    await cl.Message(content=welcome).send()
    cl.user_session.set("history", [])

@cl.on_message
async def on_message(message: cl.Message):
    question = message.content.lower()
    history = cl.user_session.get("history", [])

    if any(sub in question for sub in SUBJECTS):
        try:
            response = model.generate_content(
                f"You are a helpful university tutor. Answer in simple English:\n\n{message.content}"
            )
            reply = response.text
        except Exception as e:
            reply = f"❌ Gemini Error: {str(e)}"
    else:
        reply = "⚠️ I only assist with specific subjects:\n\n" + "\n".join(f"🔹 {s.title()}" for s in SUBJECTS)

    history.append({"role": "user", "content": message.content})
    history.append({"role": "assistant", "content": reply})
    cl.user_session.set("history", history)

    await cl.Message(content=reply).send()
