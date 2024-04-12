import os
import csv
from flask import Flask, request, session
from api_whatsapp import API_Whatsapp
from model import Message
from flask_sqlalchemy import SQLAlchemy
import gemini

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Global variables
csv_file_path = "F:\Chatbot\chatbot.csv"

def the_final_prompt(message):
    s1 = "Based on the message given to you, create a new question.\n"
    s1 += f"Message: {message}"
    return s1

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as file:
         reader = csv.DictReader(file)
         for row in reader:
             data.append(row)
    return data


@app.route('/back_reply', methods=['POST'])
def get_reply():
    print(request.form)
    sms_status = request.form.get('SmsStatus')
    if sms_status == 'delivered':
        session['counter'] = (session.get('counter', 0) +1) % len(read_csv(csv_file_path))   
    return "Success"


@app.route('/whatsapp', methods=['POST'])
def wa_reply():
    global counter
    query = request.form.get('Body').lower()
    print("User query: %s" % query)
    
    csv_data = read_csv(csv_file_path)
    print("session ", session)
    counter = session.get('counter', 0) % len(csv_data) 
    session['counter'] = counter + 1
    print(counter)
    data_for_gemini = csv_data[0].get(str(counter))

    print('data_for_gemini -', data_for_gemini)
    final_prompt = the_final_prompt(data_for_gemini)
    print("final _prompt: " + final_prompt)
    generate_ans = gemini.get_gemini_response(final_prompt)
    
    wa_api = API_Whatsapp()
    if len(generate_ans) > 1600:
        chunks = [generate_ans[i:i+1600] for i in range(0, len(generate_ans), 1600)]
        for chunk in chunks:
            response = wa_api.message_2(chunk)
    else:
        response = wa_api.message_2(generate_ans)
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)
