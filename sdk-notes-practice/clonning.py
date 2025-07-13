
#! Cloning Agent – Kya Hota Hai?
# 🔸 Definition:
# Cloning Agent ka matlab hai ek existing agent ka exact duplicate (clone) banana — jisme uske tools, prompts, instructions, context, behavior sab same ho.

# Yeh clone tum:

# Customize kar sakti ho

# Doosre user ya task ke liye reuse kar sakti ho

# Experiment/test kar sakti ho bina asli agent ko affect kiye

# 📌 Use Cases of Cloning an Agent
# Scenario	Purpose
# ✅ Testing	Original agent safe rahe, clone pe test karo
# ✅ A/B Experiments	Alag prompts ke sath 2 clones run kar ke compare karo
# ✅ Multi-user agents	Har user ke liye personal cloned agent
# ✅ Fine-tuned version	Clone lo aur kuch behavior change karke custom banao

# 🔧 Example: Clone Agent Manually in Code
# Agar tum main_agent bana chuki ho, toh tum uska clone bana sakti ho jese:

# python
# Copy
# Edit
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

# yaml
# Copy
# Edit
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