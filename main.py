import certifi
import requests
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.message import EmailMessage
import google.generativeai as genai



load_dotenv()

# Store important data
google_key = os.getenv('GEMINI_KEY')
weather_key = os.getenv('WEATHER_API_KEY')
city = os.getenv('CITY')
params = {'q': city, 'appid': weather_key, 'units': 'imperial'}
url = 'http://api.openweathermap.org/data/2.5/weather'

# Call weather API and configure Gemini
weather_data = requests.get(url, params=params).json()
genai.configure(api_key=google_key)
model = genai.GenerativeModel('gemini-pro')

# Send text prompt to Gemini
response = model.generate_content(f"""
Please generate a message giving a detailed summary of the weather forecast given the following .JSON data:
{weather_data}
insert a new line after every sentence.
""")
message = response.text

# Email formatting
sender_email = os.getenv('FROM')
receiver_email = os.getenv('TO')
subject = 'Daily weather forecast'
em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.set_content(message)

# Add SSL
context = ssl.create_default_context(cafile=certifi.where())

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender_email, os.getenv('PASS'))
    smtp.sendmail(sender_email, receiver_email, em.as_string())

