from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from agents import Agent, Runner
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput
import chainlit as cl

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gpt-4o",
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

# ✅ MAIN AGENT: Move this OUTSIDE the function
main_agent = Agent(
    name="Python Expert Agent",
    instructions="You are a Python expert agent. You only respond to Python-related questions.",
    model=model,
    input_guardrails=[input_guardrails_func]
)

# Chainlit chat start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="I'm ready to assist you!").send()
