import certifi
import requests
from dotenv import load_dotenv
import os
import schedule
import smtplib
import ssl
from email.message import EmailMessage

load_dotenv()  # load .env variables

# Weather details
city = os.getenv('CITY')
API_key = os.getenv('API_KEY')
units = 'imperial'
URL = f'https://api.openweathermap.org/data/2.5/onecall?APPID={API_key}&q={city}&units={units}'

# Store the weather details in a .json file
weather_data = requests.get(URL).json()

# Email details
sender_email = os.getenv('FROM')
receiver_email = os.getenv('TO')

subject = 'Daily weather forecast'
body = 'Hello'

em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context(cafile=certifi.where())

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender_email, os.getenv('PASS'))
    smtp.sendmail(sender_email, receiver_email, em.as_string())


