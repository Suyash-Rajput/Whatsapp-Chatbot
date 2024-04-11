from flask import Flask
import gemini 
import api_whatsapp as api_wa
app = Flask(__name__)

@app.route('/whatsapp', methods = ['POST'])
def wa_reply():
    query = request.form.get('Body').lower()
    print("User query  %s" % query)
    generate_ans =  gemini.get_gemini_response(query)
    return   api_wa.message_2(generate_ans)