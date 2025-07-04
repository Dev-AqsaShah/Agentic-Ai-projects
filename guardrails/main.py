from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from agents import Agent, Runner
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
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

# ✅ Step 1: Correct output type
class OutputSubjectCheck(BaseModel):
    is_subject_related: bool
    reasoning: str

# ✅ Step 2: Updated guardrail agent for subject checking
input_guardrails_agent = Agent(
    name="Subject Relevance Checker",
    instructions=(
        "Check if the users question is related to any of the following subjects:\n"
        "- Digital Logic Design\n"
        "- Java / Java OOP\n"
        "- Pre-Calculus\n"
        "- Civics and Community Engagement\n"
        "- Expository Writing\n"
        "- Financial Accounting\n"
        "- Islamic Studies\n\n"
        "If yes, return `is_subject_related=True`, otherwise `False`. Also explain why."
    ),
    model=model,
    output_type=OutputSubjectCheck
)

# ✅ Step 3: Guardrail function using is_subject_related
@input_guardrail
async def input_guardrails_func(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrails_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_subject_related
    )

# ✅ Step 4: Main agent for subject answering
main_agent = Agent(
    name="University Subject Expert",
    instructions=(
        "You are a subject expert assistant created by Aqsa Shah for students of University of Sindh, "
        "Batch 2025 (Second Semester). You only respond to questions from these subjects:\n"
        "- Digital Logic Design\n"
        "- Java and Java OOP\n"
        "- Pre-Calculus\n"
        "- Civics and Community Engagement\n"
        "- Expository Writing\n"
        "- Financial Accounting\n"
        "- Islamic Studies\n\n"
        "For all other questions, you should politely decline."
    ),
    input_guardrails=[input_guardrails_func],
    model=model
)

# ✅ Step 5: Chainlit UI start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content=(
        "👋 **AssalamuAlaikum**\n\n"
        "I'm your personalized academic assistant, created by *Aqsa Shah* for **University of Sindh** students, "
        "**Batch 2025 (Second Semester)**.\n\n"
        "📘 Subjects I'm specialized in:\n"
        "- Digital Logic Design\n"
        "- Java & Java OOP\n"
        "- Pre-Calculus\n"
        "- Civics and Community Engagement\n"
        "- Expository Writing\n"
        "- Financial Accounting\n"
        "- Islamic Studies\n\n"
        "💡 Ask anything from these subjects. You can use me for **1 month unlimited**.\n\n"
        "Lets learn together! 😊"
    )).send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        result = await Runner.run(
            main_agent,
            input=message.content
        )
        print("Result:", result.final_output)
        await cl.Message(content=result.final_output).send()

    except InputGuardrailTripwireTriggered:
        await cl.Message(content="❌ Please ask questions only related to the supported subjects.").send()
