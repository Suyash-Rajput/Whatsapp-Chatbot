import os
import sys
import datetime
import PIL.Image
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key="AIzaSyDvG42G5QGo99i4OOlJtL8TVR4qqhL9HNI")
gp_model = genai.GenerativeModel("gemini-pro-vision")
model = genai.GenerativeModel("gemini-pro")

def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))

def get_gemini_response(the_final_prompt):
    response = model.generate_content(the_final_prompt)
    return response.text

def get_gemini_response_at_temp(the_final_prompt):
    response = model.generate_content(the_final_prompt, generation_config = genai.types.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.7))
    resp_dict =  dict(response.parts[0])
    return resp_dict['text']

def get_answer(img_path, final_prompt):
    print("Entering get_answer()", img_path, final_prompt)
    img = PIL.Image.open(img_path)
    response = gp_model.generate_content([final_prompt, img])
    response.resolve()
    print("response.prompt_feedback :- ", response.prompt_feedback)
    if "block_reason" in response.prompt_feedback:
        print("\n Giving Block_Reason for image :-", img_path, "\n")
        return  "tbd"
    gen_response = response.text 
    stripped = gen_response.strip().lower()
    print("Exiting get_answer()", stripped)
    return stripped
