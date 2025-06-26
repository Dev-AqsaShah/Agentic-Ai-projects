import google.generativeai as genai

genai.configure(api_key="AIzaSy...")  # Tumhari Gemini API key yahan lagao

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Explain Object-Oriented Programming in simple terms.")
print(response.text)
