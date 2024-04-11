from flask import Flask, request
import gemini 
from api_whatsapp import API_Whatsapp


app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def wa_reply():
    query = request.form.get('Body').lower()
    print("User query: %s" % query)
    generate_ans = gemini.get_gemini_response(query)
    wa_api = API_Whatsapp()
    response = wa_api.message_2(generate_ans)
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)
