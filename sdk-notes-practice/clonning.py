
#! Cloning Agent – Kya Hota Hai?
# 🔸 Definition:
# Cloning Agent ka matlab hai ek existing agent ka exact duplicate (clone) banana — jisme uske tools, prompts, instructions, context, behavior sab same ho.

# Yeh clone tum:

# Customize kar sakti ho

# Doosre user ya task ke liye reuse kar sakti ho

# Experiment/test kar sakti ho bina asli agent ko affect kiye

#  Use Cases of Cloning an Agent
# Scenario	Purpose
# ✅ Testing	Original agent safe rahe, clone pe test karo
# ✅ A/B Experiments	Alag prompts ke sath 2 clones run kar ke compare karo
# ✅ Multi-user agents	Har user ke liye personal cloned agent
# ✅ Fine-tuned version	Clone lo aur kuch behavior change karke custom banao

# 🔧 Example: Clone Agent Manually in Code
# Agar tum main_agent bana chuki ho, toh tum uska clone bana sakti ho jese:


# from agents import agent, RunContextWrapper

#? ✅ Original agent
# @agent(name=\"main_agent\")  
# def main(ctx: RunContextWrapper):
#     ctx.llm.messages.append({
#         \"role\": \"system\",
#         \"content\": \"You are a friendly Java assistant.\"
#     })
#     ctx.llm.messages.append({
#         \"role\": \"user\",
#         \"content\": ctx.input
#     })
#     result = ctx.llm.complete()
#     print(\"Main Agent Reply:\", result.content)

#? ✅ Cloned agent — same logic but new name or modified behavior
# @agent(name=\"main_agent_clone\")
# def cloned_agent(ctx: RunContextWrapper):
#     ctx.llm.messages.append({
#         \"role\": \"system\",
#         \"content\": \"You are a stricter Java tutor. Focus only on syntax.\"
#     })
#     ctx.llm.messages.append({
#         \"role\": \"user\",
#         \"content\": ctx.input
#     })
#     result = ctx.llm.complete()
#     print(\"Cloned Agent Reply:\", result.content)
# 📁 Clone via Files (Advanced)
# Agar tum agents.yaml ya tools.json use karti ho, to tum ek agent ka YAML block copy-paste karke name change karke clone bana sakti ho:


# agents:
#   - name: main_agent
#     entrypoint: main.py:main
#     tools: [greet_user]

#   - name: main_agent_clone
#     entrypoint: main.py:cloned_agent
#     tools: [greet_user]

#? 🔐 Important:
# Cloned agents independent hote hain — unki memory, local context, instructions alag hote hain.
# Tum ctx.local, ctx.llm.messages sab separately use kar sakti ho.

#? 🔁 Difference Between Clone and Instance
# Concept	Meaning
# Clone	Naya agent bana same behavior ke sath
# Instance	Same agent run hua kisi specific context (user/task) ke liye

#? ✅ Summary:
# Point	Detail
# Clone Agent	Ek existing agent ka exact duplicate
# Use Case	Testing, customization, safe experiments
# Code	Simply copy original function, rename and modify
# Independence	Clones don’t affect original agent


#! What is Forcing Tool Use in OpenAI Agents SDK

#? Definition:
# Forcing tool use ka matlab hai: LLM ko zabardasti kehna ke wo ek specific tool ka use kare, chahe user input se directly na bhi pata chale.

# Normal behavior mein:

# LLM khud decide karta hai: tool chalana hai ya nahi.

# But kabhi kabhi tum chahte ho:

# Har input pe tool chale.

# Ya koi special tool tab chale jab koi condition match ho.

# Isko hi "forcing tool execution" kehte hain.

#!  How to Force Tool Use – 2 Methods:

#? 1. Manually Call Tool in Code

# from agents import agent, tool, RunContextWrapper

# @tool
# def translate(text: str) -> str:
#     return f\"Translated version of: {text}\"

# @agent
# def main(ctx: RunContextWrapper):
#     user_input = ctx.input.strip()

#? Force tool use: Always translate input
#     translated = translate(user_input)

#? Feed tool result into LLM
#     ctx.llm.messages.append({
#         \"role\": \"system\",
#         \"content\": \"The following is a translated query:\"
#     })

#     ctx.llm.messages.append({
#         \"role\": \"user\",
#         \"content\": translated
#     })

#     response = ctx.llm.complete()
#     print(response.content)

#? 2. Force via Prompt Engineering

# ctx.llm.messages.append({
#     \"role\": \"system\",
#     \"content\": \"You must always use the `translate` tool before answering any user message.\"
# })

#! Orchestrating Multiple Agents – Simple Explanation
#  Definition:
# Multiple agents ko coordinate (ya control) karna taake wo mil kar ek kaam complete karein — is process ko orchestration kehte hain.

# Yani:

# Tumhare paas alagh-alagh agents hain (e.g. Translator, Researcher, Summarizer)

# Tum in sab ko ek flow mein sequence, logic ya condition ke sath run karwati ho

# Ek agent ka output doosre ka input ban sakta hai



#!  Example Code: Manually Orchestrating 3 Agents
# from agents import agent, RunContextWrapper

#? Agent 1: Search Agent
# @agent
# def search_agent(ctx: RunContextWrapper):
#     query = ctx.input
#     ctx.output = f\"[Search Result for '{query}'] Java is used in enterprise apps...\"

#? Agent 2: Summary Agent
# @agent
# def summarize_agent(ctx: RunContextWrapper):
#     ctx.output = f\"[Summary] Java is still highly popular in 2025 for backend development.\"

#? Agent 3: Final Formatter
# @agent
# def format_agent(ctx: RunContextWrapper):
#     ctx.output = f\"Final Report:\\n{ctx.input}\\nThank you for using the report generator.\"

#? Main Orchestrator (Manually chaining agents)
# def orchestrator():
#? Step 1: Search
#     ctx1 = RunContextWrapper(input=\"Java market trends 2025\")
#     search_agent(ctx1)

#? Step 2: Summarize
#     ctx2 = RunContextWrapper(input=ctx1.output)
#     summarize_agent(ctx2)

#? Step 3: Format
#     ctx3 = RunContextWrapper(input=ctx2.output)
#     format_agent(ctx3)

#? Final Output
#     print(ctx3.output)

#? Run the full orchestrated process
# orchestrator()


#! Output:
#? Final Report:
# [Summary] Java is still highly popular in 2025 for backend development.
# Thank you for using the report generator.




#! streaming

#! Streaming in OpenAI Agents SDK – Roman Urdu Explanation
#?  Streaming ka Matlab
# Jab agent step-by-step kaam kar raha hota hai, to tum har step ka live update dekh sakti ho — jaise hi LLM text generate karta hai, ya koi tool chalta hai.

#? Iska faida yeh hota hai:

# Real-time progress dikhana user ko

# Live output print karna

# User ko wait nahi karwana pura response ka

#? ✅ 1. Runner.run_streamed() kaam kya karta hai?
# Ye function agent ko streamed (live mode) mein run karta hai. 
# result = Runner.run_streamed(agent, input="Hello")

#? ✅ 2. result.stream_events() kya karta hai?
# Ye ek async stream return karta hai jisme tum har event ko ek-ek karke read karti ho — jese:

# Text ka token aa raha ho (Hello, world, etc)

# Tool chala ho

# Message generate hua ho

#? 🔹 3. Raw Event (LLM Token-by-token)

# if event.type == "raw_response_event":
#     print(event.data.delta)
#  Matlab:
# Jaise hi LLM ek word ya token likhta hai, wo turant print hota hai.

# Yeh live typing jesa feel deta hai.

#? 🔹 4. High-Level Events (Tool ya Message Updates)

# elif event.type == "run_item_stream_event":
#     # tool call, tool output, message output
# Yahan 3 main cheezein stream hoti hain:

# Type	Matlab
# tool_call_item	Tool chal gaya
# tool_call_output_item	Tool ka result mil gaya
# message_output_item	Agent ne user ko final message bhej diya

#? 🔹 5. Agent Updated Event

# elif event.type == "agent_updated_stream_event":
#     print(event.new_agent.name)
# Agar agent handoff ya change ho jaye during process, tumhe pata chal jata hai.


#! Overall Flow Samajho:
# 1. User ne bola "Tell me 5 jokes"
# 2. Agent ne pehle tool call kiya `how_many_jokes()`
# 3. Tool ne bola: "Give 7 jokes"
# 4. Agent ne 7 jokes token by token likhna start kiya
# 5. Har token stream ho raha hai screen par
# 6. End mein agent ne message complete kiya


#!  Roman Urdu Summary – Points mein:
# Streaming ka matlab hai live output dikhana step by step.

# Tum Runner.run_streamed() use karti ho agent ko live chalane ke liye.

# result.stream_events() async loop deta hai jahan har event milta hai.

# raw_response_event LLM ka token-by-token output deta hai (like typing effect).

# run_item_stream_event se pata chalta hai tool kab chala, kya output aya, aur message kab bana.

# agent_updated_stream_event se pata chalta hai agent change hua ya handoff hua.

# Ye system tumhare AI app ko interactive aur responsive banata hai — perfect for chatbots, dashboards, ya web UIs. 


#! Tools in Agents SDK – Easy Roman Urdu Explanation
# Tools woh hotay hain jise Agent use karta hai action lene ke liye — jaise data lana, code chalana, translation, file read karna, image generate karna, etc.


#! Hosted Tools – Built-in Tools from OpenAI
# Ye tools tumhe milte hain bina custom code likhe — sirf include karo aur kaam chalu.


#! Function Calling – Python Function as Tool
# Tum koi bhi Python function @function_tool laga ke tool bana sakti ho. Agent us function ko call karega jab zarurat ho.


# ✅ Example:
# @function_tool
# async def fetch_weather(location: dict) -> str:
#     return "Today is sunny."

# @function_tool(name_override="read_file")
# def read_file(ctx, path: str) -> str:
#     return "<File content here>"
# 🧠 Automatic Benefits:
# Function ka name → tool ka naam

# Docstring se description bhi ban jaata hai

# Function ke arguments → tool ke input schema

#? 3. Custom Function Tool (Manual)
# Agar tum khud tool banana chahti ho bina @function_tool decorator, to FunctionTool(...) ka use karo aur on_invoke_tool() define karo.


# ✅ Example:
# from agents import FunctionTool
# from pydantic import BaseModel

# class Args(BaseModel):
#     username: str
#     age: int

# async def run_tool(ctx, args: str) -> str:
#     parsed = Args.model_validate_json(args)
#     return f"{parsed.username} is {parsed.age} years old"

# tool = FunctionTool(
#     name="process_user",
#     description="Process user data",
#     params_json_schema=Args.model_json_schema(),
#     on_invoke_tool=run_tool
# )

#? 4. Agents as Tools
# Tum ek agent ko doosre agent ka tool bana sakti ho, taake ek central agent unse kaam karwaye (without full handoff).


# ✅ Example:
# spanish_agent = Agent(name="Spanish", instructions="Translate to Spanish")
# french_agent = Agent(name="French", instructions="Translate to French")

# orchestrator_agent = Agent(
#     name="Main",
#     instructions="Use tools to translate.",
#     tools=[
#         spanish_agent.as_tool(tool_name="to_spanish", tool_description="Translate to Spanish"),
#         french_agent.as_tool(tool_name="to_french", tool_description="Translate to French")
#     ]
# )
# 🧪 5. Custom Output Extraction
# Agar tum agent-tool ka output filter, clean, ya JSON format mein extract karna chahti ho — to custom_output_extractor use karo.


# ✅ Example:
# async def extract_json_payload(run_result):
#     for item in reversed(run_result.new_items):
#         if item.output.strip().startswith("{"):
#             return item.output
#     return "{}"

# json_tool = data_agent.as_tool(
#     tool_name="get_json_data",
#     tool_description="Only return JSON",
#     custom_output_extractor=extract_json_payload
# )

#? 6. Tool Error Handling
# Agar function-tool mein error aata hai, to tum:

# Default error message bhej sakti ho

# Ya apna custom error message de sakti ho

# Ya exception ko re-raise bhi kar sakti ho (advance)

# ✅ Example:
# @function_tool(failure_error_function=my_custom_error_function)
# def my_tool(): ...


#! Roman Urdu Summary – Important Points:
# 3 types ke tools hain: Hosted, Function, Agents-as-tools

# Hosted tools → ready-made tools by OpenAI (web, image, shell, etc.)

# Function tools → tumhare Python functions tools ban jaate hain with @function_tool

# Agents as tools → ek agent doosre agent ko tool ki tarah use karta hai

# Automatic input schema & description milta hai from function signature

# Custom output extractor use karo agar sirf JSON ya clean response chahiye

# Tool crash ho to tum custom error bhi bhej sakti ho model ko

