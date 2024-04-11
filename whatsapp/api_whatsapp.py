from twilio.rest import Client

account_sid = 'ACaf472b38e2ea546ab4f0cd042a02471b'
auth_token = 'd794f3d0e011bd2c76127b68a9980028'
client = Client(account_sid, auth_token)



class API_Whatsapp():
 
  def __init__(self):
    
    self.account_sid = 'ACaf472b38e2ea546ab4f0cd042a02471b'
    self.auth_token = 'd794f3d0e011bd2c76127b68a9980028'
    self.client = Client(self.account_sid, self.auth_token)
    
    self.from_phone = "whatsapp:+16592263686"
    self.to_phone = "whatsapp:+6588206625"

  
  def message_1(self):
    print(f"{self.to_phone}")
    message = self.client.messages.create(
      body = 'Your Twilio code is 1238432',
      from_ = self.from_phone,
      to = self.to_phone
    )
    
    print(message.body)
    return message   
  
  def receive_message(self):
    pass 
    
if __name__ == "__main__":
  WAPI = API_Whatsapp()
  WAPI.message_1()