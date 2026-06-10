import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
# 2. Obtenemos los valores desde las variables de entorno
TWILIO_Account_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_Auth_Token = os.getenv('TWILIO_AUTH_TOKEN')
Twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
API_KEY_WAPI = os.getenv('API_KEY_WAPI')
#from clave.twilio_config import TWILIO_Account_SID , TWILIO_Auth_Token , Twilio_phone_number , API_KEY_WAPI
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from bs4  import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

#Armado de la URL
Query = 'buenos aires'
Api_key = API_KEY_WAPI
url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+Api_key+'&q='+Query+'&days=1&aqi=no&alerts=no' 

response = requests.get(url_clima).json()
#print(response)

###Buscar Campos Importantes####
response.keys()
response['forecast']['forecastday'][0].keys()
len(response['forecast']['forecastday'][0]['hour'])
response['forecast']['forecastday'][0]['hour'][1]['time'].split()[0] #Fecha
int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0]) #hora
response['forecast']['forecastday'][0]['hour'][1]['condition']['text']#condicion
response['forecast']['forecastday'][0]['hour'][0]['temp_c']#Temperatura
response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']#llovera
response['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']#probabilidad de lluvia

### Armar Dataframe ####
def get_forecart(response, i):

    Fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    Hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    Condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    Temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    Lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    Probabilidad_lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return Fecha, Hora, Condicion, Temperatura, Lluvia, Probabilidad_lluvia

datos =[]
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])),colour='green'):
    
    datos.append(get_forecart(response, i))

datos[0]
col= [ 'Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Probabilidad_lluvia']
df =pd.DataFrame(datos, columns=col)
print(df)

##Resultado DF
df_rain = df[(df['Lluvia']==1) & (df['Hora']> 6) & (df['Hora']< 23)]

if df_rain.empty:
    default_data = pd.DataFrame({
        'Hora': [24], 
        'Condicion': ['sin probabilidad']
    })
    default_data.set_index('Hora', inplace=True)
    df_rain = default_data
else:
    df_rain = df_rain[['Hora', 'Condicion']]
    df_rain.set_index('Hora', inplace=True)

print(df_rain)

####Armar Template ######
print('\nHola! \n\n\n El pronostico del tiempo hoy '+ df['Fecha'][0] +' en ' + Query +' es : \n\n\n ' + str(df_rain))
print(Twilio_phone_number)

######## Enviar Mensaje SMS Desde Twilio ##########
time.sleep(2)
account_sid = TWILIO_Account_SID  
auth_token = TWILIO_Auth_Token

client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body='\nHola! \n\n El pronostico de lluvia hoy ' + str(df['Fecha'][0]) + ' en ' + Query + ' es : \n\n ' + str(df_rain),
        from_='whatsapp:+14155238886',
        to='whatsapp:+5491125194837'
    )
    print('Mensaje Enviado ' + message.sid)
except Exception as e:
    print(f"Error al enviar el mensaje: {e}")
