import os
import csv
from flask import Flask, request, session
from api_whatsapp import API_Whatsapp
from model import Message
from flask_sqlalchemy import SQLAlchemy
import gemini
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
# Global variables
csv_file_path = "F:\Chatbot\chatbot.csv"

def the_final_prompt(message):
    s1 = "Based on the message given to you, create a new question.\n"
    s1 += f"Message: {message} \n"
    s1 + " Modify the Message in a best way \n"
    return s1

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as file:
         reader = csv.DictReader(file)
         for row in reader:
             data.append(row)
    return data

def print_time_taken(start_time, end_time):
    end_time_aware = end_time.replace(tzinfo=timezone.utc)
    duration = end_time_aware - start_time
    total_time_seconds = duration.total_seconds()
    print(f"Time taken - : {total_time_seconds:.6f} seconds")
    seconds =  round(total_time_seconds,0)
    minutes = seconds // 60
    return  minutes

@app.route('/whatsapp', methods=['POST'])
def wa_reply():
    query = request.form.get('Body').lower()
    print("User query: %s" % query)
    counter = 0
    generate_ans = ""
    time_diff = 12
    # del session['counter']
    # del session['To']
    # del session['time_started']    
    csv_data = read_csv(csv_file_path)
    recipient_number = request.form.get('From')
    print(recipient_number)
    session_started_time = session.get('time_started', None)
    
    if session_started_time is not None:
        time_diff = print_time_taken(session['time_started'], datetime.now())
    
    if 'To' in session and session['To'] == recipient_number and time_diff < 10 and session.get('counter', 0) <= len(csv_data[0]):
        print("Is present ------------", session['counter'])
        counter = session['counter']
    else:
        session['counter'] = 0
        session['time_started'] = datetime.now()
    
    session['To'] = recipient_number
    session['counter'] += 1
    print("counter :- ", counter, " len(csv_data) :- ", len(csv_data[0]))
    
    if counter == len(csv_data[0]):
        generate_ans = "Thanks for the response ...."
    else:
        data_for_gemini = csv_data[0].get(str(counter))
        print('data_for_gemini -', data_for_gemini)
        final_prompt = the_final_prompt(data_for_gemini)
        print("final _prompt: " + final_prompt)
        generate_ans = gemini.get_gemini_response(final_prompt)
    
    wa_api = API_Whatsapp()
    wa_api.from_phone = request.form.get('To')
    wa_api.to_phone =  recipient_number
    if len(generate_ans) > 1600:
        chunks = [generate_ans[i:i+1600] for i in range(0, len(generate_ans), 1600)]
        for chunk in chunks:
            response = wa_api.message_2(chunk)
    else:
        response = wa_api.message_2(generate_ans)
    
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)
