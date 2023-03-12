import random
from twilio.rest import Client

if __name__ == '__main__':
    from saleapp import app
    with app.app_context():
        # send_otp("+84345809638")
        account_sid = 'AC99204c3540a27bd83aede03e43b83312'
        auth_token = '6660059774e9c35882ef7e4fa354ec56'
        client = Client(account_sid, auth_token)
        otp = random.randint(100000, 999999)
        message = client.messages.create(
            messaging_service_sid='MGcebeadd059e80d3835f92442700abaaa',
            body=f'Hiếu test otp {otp}',
            to='+84359505026'
        )
        print(message.sid)
        print(otp)
