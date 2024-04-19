import os
from . import gemini
import requests
from . import prompts as pt
from pathlib import Path
from flask import Flask, request, session
from .api_whatsapp import API_Whatsapp
from .Bigquery import GCP_big_query
from mcw import main_context_window as mcw
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

BASE_DIR = Path(__file__).resolve().parent
parent_dir = os.path.dirname(BASE_DIR)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(parent_dir, 'json_files/autotask-loreal-dv-dd0494ce10d7.json')

gcp = GCP_big_query()
wa_api = API_Whatsapp()
dataset_id = "Chatbot_messages_dataset"
table_id = "chatbot_messages"

def fetch_file_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching file from URL:", e)
        return None


@app.route('/whatsapp', methods=['POST'])
def wa_reply():
    current_time = datetime.now()
    message_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    query = request.form.get('Body').lower()
    generate_ans = ""
    query = query
    print("User query: %s" % query)
    if query.startswith('http://') or query.startswith('https://'):
       print('Its a file format')
       query = fetch_file_from_url(query)
    print(' user query: ', query)    
    recipient_number = request.form.get('From')
    print(recipient_number)
    session['To'] = recipient_number
    mcw.update_context(session, query, recipient_number)
    gcp.create_dataset(dataset_id)
    gcp.create_table(table_id, dataset_id)   
    rows_to_insert = [{"message_sender":  recipient_number, "message_receiver" : request.form.get('To'),"message_time": message_time,"message_text" : str(query)}]
    gcp.insert_data(rows_to_insert, table_id, dataset_id)
    session_started_time = session.get('time_started', None)
    
    final_prompt = pt.the_final_prompt(session['__question'], session['__prompt'])
    print("final _prompt: " + str(final_prompt))
    generate_ans = gemini.get_gemini_response(final_prompt)
    wa_api.from_phone =  request.form.get('To')
    wa_api.to_phone = recipient_number
    if session['__state'] == 'S8':
        response = wa_api.message_2(session['__question'])
        session.clear()
        message_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_to_insert = [{"message_sender":  recipient_number, "message_receiver" : request.form.get('To'),"message_time": message_time,"message_text" : str(response.body)}]
        gcp.insert_data(rows_to_insert, table_id, dataset_id)
        return str(response.body)
    if query.strip().lower() == "reset":
        session.clear()  # Reset session data
        response = wa_api.message_2("Session reset successfully.")
        message_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_to_insert = [{"message_sender":  recipient_number, "message_receiver" : request.form.get('To'),"message_time": message_time,"message_text" : str(response.body)}]
        gcp.insert_data(rows_to_insert, table_id, dataset_id)
        return str(response.body)

    if len(generate_ans) > 1600:
        chunks = [generate_ans[i:i + 1600] for i in range(0, len(generate_ans), 1600)]
        for chunk in chunks:
            response = wa_api.message_2(chunk)
    else:
        print("-------------")
        response = wa_api.message_2(generate_ans)
    message_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_to_insert = [{"message_sender":  request.form.get('To'), "message_receiver" : recipient_number,"message_time": message_time,"message_text" : str(response.body)}]
    gcp.insert_data(rows_to_insert, table_id, dataset_id)
    # session.clear()
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)



# message_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# if session.get('__state') == 'S8':
#     response_text = session.pop('__question')
# elif query.strip().lower() == "reset":
#     session.clear()  # Reset session data
#     response_text = "Session reset successfully."
# else:
#     response_text = generate_ans[:1600] if len(generate_ans) > 1600 else generate_ans

# response = wa_api.message_2(response_text)

# rows_to_insert = [{
#     "message_sender": recipient_number if session.get('__state') == 'S8' else request.form.get('To'),
#     "message_receiver": request.form.get('To') if session.get('__state') == 'S8' else recipient_number,
#     "message_time": message_time,
#     "message_text": str(response.body)
# }]

# gcp.insert_data(rows_to_insert, table_id, dataset_id)

# return str(response.body)
