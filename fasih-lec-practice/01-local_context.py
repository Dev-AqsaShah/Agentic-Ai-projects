# from pydantic import BaseModel

# class UserInfo(BaseModel):
#     name: str 
#     age: int
    
# user = UserInfo(name="Muhammad Fasih", age=20)

# print(user)







# ✅ Local Context:
# Local machine (ya local memory) ka context.

# Fast, private, and no API cost.

# Small-scale memory jese temporary variables ya user data.

# ✅ LLM Context:
# Large Language Model (LLM) ko diya gaya context.

# Basically wo data jo tum model ko "samjhane" k liye provide karti ho prompt ke zariye.

# Iska use tab hota jab model ko kisi kaam ke liye relevant data chahiye ho.

# 🔶 2. Local Context (Step-by-Step with Code)
# 🧠 Use Case: Store user info locally without sending to LLM.
# ✅ Step-by-step:
# from agents import RunContextWrapper — run context ko wrap karta hai.

# Create class for local storage (e.g. UserInfo).

# Use ctx.local to store/retrieve info.

# ✅ 🔧 Example Code: Local Context
# python
# Copy code
# # Step 1: Import necessary modules
# from agents import RunContextWrapper
# from pydantic import BaseModel

# # Step 2: Define a model for user data using Pydantic
# class UserInfo(BaseModel):
#     name: str
#     age: int

# # Step 3: Create a wrapper around the context (usually provided in agents)
# def main(ctx: RunContextWrapper):
#     # Step 4: Store user info in local context
#     ctx.local.user = UserInfo(name="Aqsa", age=22)

#     # Step 5: Access and print that local info
#     print(f"Hello {ctx.local.user.name}, you are {ctx.local.user.age} years old.")

# # ✅ Yeh function kisi agent ke context mein run hota hai.
# # For testing, you would simulate 'ctx' yourself.
# 🔶 3. LLM Context (Step-by-Step with Code)
# 🧠 Use Case: Jab tum chahti ho ke model ko specific context diya jae prompt mein.
# ✅ Step-by-step:
# ctx.llm.messages.append(...) – context add karo.

# Is context k through model se sawal pocho ya task karwao.

# ✅ 🔧 Example Code: LLM Context
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

#     # Step 3: Call the LLM to get a response
#     response = ctx.llm.complete()

#     # Step 4: Print the answer from LLM
#     print("LLM Answer:", response.content)
# 🔶 4. Difference Table (Quick Recap)
# Feature	Local Context	LLM Context
# Where Stored	Locally (RAM/memory)	In prompt/token of LLM
# Use Case	Save user state, preferences	Give instructions/data to the model
# Persistent?	No (unless coded)	No (context resets with each new call)
# Privacy	High (local only)	Depends on API settings
# Speed	Very fast	Slower (calls LLM)

