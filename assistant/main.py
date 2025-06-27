import os
from dotenv import load_dotenv
import chainlit as cl
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Subject specialist
SUBJECT = "Physics"

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

@cl.on_message
async def main(message: cl.Message):
    question = message.content

    # Only answer subject-related questions
    if SUBJECT.lower() not in question.lower():
        await cl.Message(content=f"❌ I'm a specialist in **{SUBJECT}** only. Please ask related questions.").send()
        return

    try:
        response = model.generate_content(
            f"You are a subject matter expert in {SUBJECT}. Only answer questions related to {SUBJECT}.\n\nUser Question: {question}"
        )
        await cl.Message(content=response.text).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {e}").send()
