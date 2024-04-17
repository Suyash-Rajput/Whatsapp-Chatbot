import os
import gemini
import requests
from pathlib import Path
from flask import Flask, request, session
from api_whatsapp import API_Whatsapp
from Bigquery import GCP_big_query
import mcw.main_context_window as mcw
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
    user_query = ""
    print("User query: %s" % query)
    if query.startswith('http://') or query.startswith('https://'):
       user_query = fetch_file_from_url(query)
       
    mcw.update_context(session, user_query)
    gcp.create_dataset(dataset_id)
    gcp.create_table(table_id, dataset_id)   
    csv_data = read_csv(csv_file_path)
    recipient_number = request.form.get('From')
    print(recipient_number)
    rows_to_insert = [{"message_sender":  recipient_number, "message_receiver" : request.form.get('To'),"message_time": message_time,"message_text" : str(query)}]
    gcp.insert_data(rows_to_insert, table_id, dataset_id)
    session_started_time = session.get('time_started', None)

    final_prompt = the_final_prompt(session[__question])
    print("final _prompt: " + final_prompt)
    generate_ans = gemini.get_gemini_response(final_prompt)

    wa_api.from_phone =  recipient_number
    wa_api.to_phone = request.form.get('To')

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
        response = wa_api.message_2(generate_ans)
    message_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_to_insert = [{"message_sender":  recipient_number, "message_receiver" : request.form.get('To'),"message_time": message_time,"message_text" : str(response.body)}]
    gcp.insert_data(rows_to_insert, table_id, dataset_id)
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)
