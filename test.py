from twilio.rest import Client
from twilio.rest import Client
from clave.twilio_config import TWILIO_Account_SID , TWILIO_Auth_Token , Twilio_phone_number , API_KEY_WAPI

# Reemplaza con tus datos reales
account_sid = TWILIO_Account_SID
auth_token = TWILIO_Auth_Token

client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body='Hola! Esta es una prueba de conexión desde Python.',
        from_='whatsapp:+14155238886',
        to='whatsapp:+5491125194837'
    )
    print(f"Mensaje enviado con SID: {message.sid}")
except Exception as e:
    print(f"Ocurrió un error: {e}")