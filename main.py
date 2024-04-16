import requests
from dotenv import load_dotenv
import os
import schedule

load_dotenv()  # load .env variables

city = os.getenv('CITY')
API_key = os.getenv('API_KEY')
units = 'imperial'
URL = f'https://api.openweathermap.org/data/2.5/onecall?APPID={API_key}&q={city}&units={units}'

weather_data = requests.get(URL).json()

if __name__ == '__main__':
    print(weather_data)

