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
    if len(generate_ans) > 1600:
        chunks = [generate_ans[i:i+1600] for i in range(0, len(generate_ans), 1600)]
        for chunk in chunks:
            response = wa_api.message_2(chunk)
    else:
        response = wa_api.message_2(generate_ans)
    
    return str(response.body)

if __name__ == "__main__":
    app.run(debug=True)
