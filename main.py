import certifi
import requests
import schedule
from dotenv import load_dotenv
import os
from datetime import datetime
import time
from schedule import every, repeat
import smtplib
import ssl
from email.message import EmailMessage

import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


load_dotenv()  # load .env variables

# Store important data
google_key = os.getenv('GEMINI_KEY')
city = os.getenv('CITY')
weather_key = os.getenv('API_KEY')
params = {'q': city, 'appid': weather_key, 'units': 'imperial'}
url = 'http://api.openweathermap.org/data/2.5/weather'

# Access the url and turn response into .json
weather_data = requests.get(url, params=params).json()

# Store data
min_temp = weather_data['main']['temp_min']
max_temp = weather_data['main']['temp_max']
forecast = weather_data['weather'][0]['main']
sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).time().strftime('%I:%M %p')

# Email details
sender_email = os.getenv('FROM')
receiver_email = os.getenv('TO')

subject = 'Daily weather forecast'

body = f'''                                                                                              
Hello,                                                                                                   
                                                                                                         
Today the forecast is supposed to be {forecast}, with a minimum temperature of {min_temp}°F              
and a maximum temperature of {max_temp}°F.  The sun will set at {sunset} too.                        
                                                                                                                                                                                                                  
Best,                                                                                                    
Your favorite python-based weatherman                                                                    
'''

em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.set_content(body)

# Add SSL
context = ssl.create_default_context(cafile=certifi.where())

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender_email, os.getenv('PASS'))
    smtp.sendmail(sender_email, receiver_email, em.as_string())

