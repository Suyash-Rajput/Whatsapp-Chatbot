import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDvG42G5QGo99i4OOlJtL8TVR4qqhL9HNI")
gp_model = genai.GenerativeModel("gemini-pro-vision")
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(the_final_prompt):
    response = model.generate_content(the_final_prompt)
    return response.text
