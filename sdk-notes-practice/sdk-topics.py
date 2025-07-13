# from pydantic import BaseModel

# class UserInfo(BaseModel):
#     name: str 
#     age: int
    
# user = UserInfo(name="Muhammad Fasih", age=20)

# print(user)



#? Local Context:
# Local machine (ya local memory) ka context.

# Fast, private, and no API cost.

# Small-scale memory jese temporary variables ya user data.

#?  LLM Context:
# Large Language Model (LLM) ko diya gaya context.

# Basically wo data jo tum model ko "samjhane" k liye provide karti ho prompt ke zariye.

# Iska use tab hota jab model ko kisi kaam ke liye relevant data chahiye ho.

#?  2. Local Context (Step-by-Step with Code)
#  Use Case: Store user info locally without sending to LLM.
#  Step-by-step:
# from agents import RunContextWrapper — run context ko wrap karta hai.

# Create class for local storage (e.g. UserInfo).

# Use ctx.local to store/retrieve info.

# Example Code: Local Context
# python
# Copy code
#? Step 1: Import necessary modules
# from agents import RunContextWrapper
# from pydantic import BaseModel

#? Step 2: Define a model for user data using Pydantic
# class UserInfo(BaseModel):
#     name: str
#     age: int

#? Step 3: Create a wrapper around the context (usually provided in agents)
# def main(ctx: RunContextWrapper):
#     # Step 4: Store user info in local context
#     ctx.local.user = UserInfo(name="Aqsa", age=22)

#? Step 5: Access and print that local info
#     print(f"Hello {ctx.local.user.name}, you are {ctx.local.user.age} years old.")

#?  Yeh function kisi agent ke context mein run hota hai.
#? For testing, you would simulate 'ctx' yourself.
#  3. LLM Context (Step-by-Step with Code)
#  Use Case: Jab tum chahti ho ke model ko specific context diya jae prompt mein.
#  Step-by-step:
# ctx.llm.messages.append(...) – context add karo.

# Is context k through model se sawal pocho ya task karwao.

#? Example Code: LLM Context
# python
# Copy code
# from agents import RunContextWrapper

# def main(ctx: RunContextWrapper):
#     # Step 1: Add some context for LLM (example: product description)
#     ctx.llm.messages.append({
#         "role": "system",
#         "content": "You are a helpful assistant that answers about Java."
#     })

#     # Step 2: User message that triggers the LLM with this context
#     user_question = "What is the difference between if and else in Java?"
#     ctx.llm.messages.append({
#         "role": "user",
#         "content": user_question
#     })

#? Step 3: Call the LLM to get a response
#     response = ctx.llm.complete()

#? Step 4: Print the answer from LLM
#     print("LLM Answer:", response.content)
#  4. Difference Table (Quick Recap)
# Feature	Local Context	LLM Context
# Where Stored	Locally (RAM/memory)	In prompt/token of LLM
# Use Case	Save user state, preferences	Give instructions/data to the model
# Persistent?	No (unless coded)	No (context resets with each new call)
# Privacy	High (local only)	Depends on API settings
# Speed	Very fast	Slower (calls LLM)




#!  Guardrails in OpenAI Agents SDK

#* Rules, filters, ya constraints jo tum apne agent ke behavior ko control karne ke liye lagati ho — taake model kuch galat, risky, irrelevant ya unwanted reply na de.

#* from agents import RunContextWrapper

#* def main(ctx: RunContextWrapper):
#*     user_input = ctx.input
    
#*     # Guardrail 1: Only allow Java-related questions
#*     if "java" not in user_input.lower():
#*         ctx.llm.messages.append({
#*             "role": "assistant",
#*             "content": "Sorry, I can only answer questions related to Java programming."
#*         })
#*         return
    
#*     # Else: normal LLM flow
#*     ctx.llm.messages.append({"role": "user", "content": user_input})
#*     response = ctx.llm.complete()
#*     print(response.content)

#? Why Are Guardrails Important?
#? Benefit	Explanation
#?  Safer Responses	Koi toxic ya harmful jawab nahi deta
#?  Focused Agent	Sirf defined domain pe kaam karta hai
#?  Control & Clarity	Tumhari terms par kaam karta hai
#?  Avoid Hallucination	Agent kuch ghalat ya guesswork na kare


#!  Full Example of OpenAI Agent SDK with:
#! - Local Context
#! - LLM Context
#! - Guardrails (trigger + filter)
#! - Step-by-step comments



# from agents import agent, tool, RunContextWrapper
# from pydantic import BaseModel

#? Step 1: Define a local context model
# task_history = []

# class UserInfo(BaseModel):
#     name: str
#     age: int

#? Step 2: Define a tool that the agent can use
# @tool
# def greet_user(name: str) -> str:
#     """Returns a greeting message."""
#     return f"Hello {name}, welcome to the Java Help Agent!"

#? Step 3: Define the agent's main function
# @agent
# def main(ctx: RunContextWrapper):
#     user_input = ctx.input.strip()

    #?  Guardrail 1: Block inappropriate or non-java questions
    # if not user_input.lower().startswith("java"):
    #     ctx.llm.messages.append({
    #         "role": "assistant",
    #         "content": "Sorry, I can only answer questions related to Java programming."
    #     })
    #     return

    #?  Store user info in local context
    # ctx.local.user = UserInfo(name="Aqsa", age=22)

    #?  Use tool for greeting (simulate logic flow)
    # greeting = greet_user(ctx.local.user.name)
    # print(greeting)  #* Optional: Log to console

    #?  Add system prompt to guide LLM
    # ctx.llm.messages.append({
    #     "role": "system",
    #     "content": "You are a Java expert helping students understand Java programming concepts."
    # })

    #? Add user input to chat
    # ctx.llm.messages.append({
    #     "role": "user",
    #     "content": user_input
    # })

    #?  Get model's reply
    # reply = ctx.llm.complete()
    # print("LLM Reply:", reply.content)

    #? Save history (optional)
    # task_history.append({"question": user_input, "response": reply.content})

    #? Final response
    # ctx.llm.messages.append({
    #     "role": "assistant",
    #     "content": reply.content
    # })

#? Step 4 (Optional): Add a guardrail trigger via a separate function
# @agent(trigger="shutdown")
# def shutdown(ctx: RunContextWrapper):
#     """Ends the agent with a goodbye message."""
#     return "Agent shutting down. Thank you!"

#! Note:
# - This agent will only answer Java-related questions
# - Uses a simple greeting tool
# - Tracks user history (in memory only)
# - Uses ctx.local and ctx.llm context management



#! Dynamic Instructions – Kya Hotay Hain?

#? Definition:
#? Dynamic Instructions wo real-time prompts ya rules hotay hain jo tum runtime par model ko deti ho, taake wo apna behavior ya jawab usi waqt ke context ke mutabiq badal sake.

#? Ye instructions:

#? Predefined nahi hotay (jese system prompt har baar same ho)

#? Balkay user input ya local data ke basis par runtime mein generate hotay ha


#? Simple Example:
#? 🔹 Static Instruction (hardcoded):

#? “You are a helpful assistant.”

#? 🔹 Dynamic Instruction (based on user name):

#? “You are helping Aqsa, a 22-year-old student learning Java. Be polite and explain clearly.”



# from agents import agent, RunContextWrapper
# from pydantic import BaseModel

# class UserInfo(BaseModel):
#     name: str
#     level: str  # beginner, intermediate, expert

# @agent
# def main(ctx: RunContextWrapper):
#?Let's assume this user info is stored locally
#     ctx.local.user = UserInfo(name="Aqsa", level="beginner")
    
#     user_input = ctx.input.strip()

#?  Create dynamic instruction based on local context
#     dynamic_instruction = f"""
#     You are helping {ctx.local.user.name}, who is a {ctx.local.user.level} Java learner.
#     Explain things clearly, with examples, and avoid complex jargon.
#     """

#? Add dynamic instruction to system prompt
#     ctx.llm.messages.append({
#         "role": "system",
#         "content": dynamic_instruction.strip()
#     })

#? Add user input
#     ctx.llm.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#? Get response
#     response = ctx.llm.complete()
#     print(response.content)

#? Add response back to message history
#     ctx.llm.messages.append({
#         "role": "assistant",
#         "content": response.content
#     })


#!  Hands-off in OpenAI Agents SDK – Simple Explanation
#? Definition:
#? Hands-off mode ka matlab hota hai ke tum model ko full freedom deti ho taake wo khud decide kare kya karna hai, kaunsa tool chalana hai, aur kya jawab dena hai — bina developer ke manually control kiye


#?  How to Enable Hands-off Mode?
#? Actually, hands-off koi flag ya function nahi hota — jab tum model ko:

#? Tools do

#? Instructions do

#? Aur usay freely run karne do

#? Toh wo hands-off mode ban jaata hai.

#?  Example: Hands-off Behavior with Tools
#? python
#? Copy
#? Edit
#? from agents import agent, tool, RunContextWrapper

#! Step 1: Define a tool
# @tool
# def get_weather(city: str) -> str:
#     return f"The weather in {city} is 35°C and sunny."

#? Step 2: Agent with hands-off behavior
# @agent
# def main(ctx: RunContextWrapper):
#? Hands-off instruction: model should decide what to do
#     ctx.llm.messages.append({
#         "role": "system",
#         "content": "You are an assistant that helps with weather, news, and tax. Use tools as needed."
#     })

#     ctx.llm.messages.append({
#         "role": "user",
#         "content": ctx.input
#     })

#? LLM will decide whether to call tool or not
# result = ctx.llm.complete()
# print(\"Response:\", result.content)


#!  Input Example (User says):
#? "What's the weather in Karachi?"

#!  Output:
#? Model will automatically:

#? Detect weather intent

#? Use get_weather("Karachi")

#? Return response








