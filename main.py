import certifi
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import schedule
import smtplib
import ssl
from email.message import EmailMessage

load_dotenv()  # load .env variables

# Weather details
city = os.getenv('CITY')
API_key = os.getenv('API_KEY')
params = {'q':city, 'appid':API_key, 'units':'imperial'}
URL = 'http://api.openweathermap.org/data/2.5/weather'

# access the url
response = requests.get(URL, params=params)

weather_data = response.json()

#Store data
min_temp = weather_data['main']['temp_min']
max_temp = weather_data['main']['temp_max']
forecast = weather_data['weather'][0]['main']
sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).time().strftime('%I:%M %p')

#---------------------------------------------------- SMTP CODE

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

# Add SSL (layer of security)
context = ssl.create_default_context(cafile=certifi.where())

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender_email, os.getenv('PASS'))
    smtp.sendmail(sender_email, receiver_email, em.as_string())
