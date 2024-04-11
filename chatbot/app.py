import gemini 
from flask import Flask, request
from api_whatsapp import API_Whatsapp
from model import Message
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/whatsapp', methods=['POST'])
def wa_reply():
    query = request.form.get('Body').lower()
    print("User query: %s" % query)
    generate_ans = gemini.get_gemini_response(query)
    
    incoming_message = Message(sender=request.form.get('From'), recipient=request.form.get('To'), body=query)
    db.session.add(incoming_message)
    
    wa_api = API_Whatsapp()
    if len(generate_ans) > 1600:
        chunks = [generate_ans[i:i+1600] for i in range(0, len(generate_ans), 1600)]
        for chunk in chunks:
            response = wa_api.message_2(chunk)
    else:
        response = wa_api.message_2(generate_ans)
        
    outgoing_message = Message(sender=request.form.get('To'), recipient=request.form.get('From'), body=generate_ans)
    db.session.add(outgoing_message)
    
    db.session.commit()
    return str(response.body)

    
if __name__ == "__main__":
    app.run(debug=True)
