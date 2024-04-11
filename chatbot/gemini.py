import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDvG42G5QGo99i4OOlJtL8TVR4qqhL9HNI")
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(the_final_prompt):
    response = model.generate_content(the_final_prompt)
    print(response.text)
    return response.text
