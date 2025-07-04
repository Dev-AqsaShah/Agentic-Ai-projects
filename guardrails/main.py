from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from agents import Agent, Runner
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput,InputGuardrailTripwireTriggered
import chainlit as cl

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Output type
class OutputPython(BaseModel):
    is_python_related: bool
    reasoning: str

# Guardrail agent
input_guardrails_agent = Agent(
    name="input Guardrail Checker",
    instructions="Check if the user's question is related to Python programming. If yes, return true; otherwise, return false.",
    model=model,
    output_type=OutputPython
)

# Guardrail function
@input_guardrail
async def input_guardrails_func(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrails_agent, input)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_python_related
    )

#  MAIN AGENT: Move this OUTSIDE the function
main_agent = Agent(
    name="University Subject Expert",
    instructions = (
    "You are a subject matter expert AI assistant created by Aqsa Shah for students of the University of Sindh, "
    "Batch 2025 (Second Semester). You specialize in answering questions related to the following subjects:\n\n"
    "- Digital Logic Design\n"
    "- Java and Java OOP\n"
    "- Pre-Calculus\n"
    "- Civics and Community Engagement\n"
    "- Expository Writing\n"
    "- Financial Accounting\n"
    "- Islamic Studies\n\n"
    "You should only respond to questions that are directly related to these subjects. Politely refuse to answer "
    "unrelated topics. Your goal is to provide clear, accurate, and helpful answers to help students understand and "
    "succeed in their coursework."
),
    input_guardrails=[input_guardrails_func]
)

# Chainlit chat start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content=(
            "👋 **AssalamuAllaikum**\n\n"
            "I'm your personalized academic assistant, created by *Aqsa Shah* specifically for **University of Sindh** students, **Batch 2025 (Second Semester)**.\n\n"
            "📘 I'm specialized in the following subjects:\n"
            "- Digital Logic Design\n"
            "- Java & Java OOP\n"
            "- Pre-Calculus\n"
            "- Civics and Community Engagement\n"
            "- Expository Writing\n"
            "- Financial Accounting\n"
            "- Islamic Studies\n\n"
            "💡 Feel free to ask me any questions related to these subjects.\n"
            "This assistant is available for unlimited use for the next **1 month**.\n\n"
            "Let’s start learning together! 😊"
        )
    ).send()
@cl.on_message
async def on_message(message: cl.Message):
    try:
        result = await Runner.run(
            main_agent,
            input=message.content
        )
        print("Result:", result.final_output)
        await cl.Message(content=result.final_output.reasoning).send()

    except InputGuardrailTripwireTriggered:
        await cl.Message(content="Please try subject related questions").send()
