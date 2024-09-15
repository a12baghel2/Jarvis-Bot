import os
import google.cloud.dialogflow_v2 as dialogflow
from urllib.request import urlopen
import json
import requests
import random
from geopy.geocoders import Nominatim


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "jarvis-otgtwd"



def detect_intent_from_text(text,session_id,language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID,session_id)
    text_input = dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def get_reply(query,chat_id):
    response =  detect_intent_from_text(query,chat_id)

    if response.intent.display_name == "corona status":
        return "corona status", dict(response.parameters)
    elif response.intent.display_name == "get_quotes":
        return "get_quotes",dict(response.parameters)
    elif response.intent.display_name == "show climate":
        return "show climate",dict(response.parameters)
    elif response.intent.display_name == "mars":
        return "mars",dict(response.parameters)
    elif response.intent.display_name == "planet_pic":
        return "planet_pic",dict(response.parameters)
    elif response.intent.display_name == "get_news":
        return "get_news",dict(response.parameters)
    else:
        return "small_talk",response.fulfillment_text

def fetch_quote(parameters):
    url = "https://programming-quotesapi.vercel.app/api/random"
    quoteRes = urlopen(url)
    quoteData = quoteRes.read()
    quoteData = json.loads(quoteData)
    return quoteData["quote"]

def get_news(parameters):
    category = parameters.get("news_topic")
    url = "https://api.currentsapi.services/v1/search?language=en&type=1&country=IN&category={}&apiKey=W6NmMtdMLbobjXAZi4yBrKbifC-lJ_cwwDzFnO2SCyY_yUwR".format(category)
    response = requests.get(url)
    data = response.json()
    data = data['news']
    return data

def mars(parameters):
    camera = parameters.get("nasa_fetch")
#    print(type(camera))
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&page=1&camera={}&api_key={api_key}".format(random.randint(900,2200),camera)
    marsRes = urlopen(url)
    marsData = marsRes.read()
    marsData = json.loads(marsData)
#    print(marsData)
    return marsData

def getPic(parameters):
    date = parameters.get("date-time")
    date = date[:10]
    url = "https://api.nasa.gov/planetary/apod?&date={}&api_key={api_key}".format(date)
    picData = urlopen(url).read()
    picData = json.loads(picData)
    return picData

def fetch_weather(parameters):
    location = parameters.get('geo-city')
    geolocator = Nominatim(user_agent="Abhimanyu")
    loc = geolocator.geocode(location)
    lat,lon = loc.latitude, loc.longitude
    w_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=en&exclude=daily&units=metric&appid=5a9b5d475522296b6babad68ec068724".format(lat,lon)
    w_res = requests.get(w_url)
    data = w_res.content.decode('utf-8')
    data = json.loads(data)
    data = data["current"]
    weather = data["weather"][0]
    return "This is i've got.\nTemp: {}C\nFeels Like: {}C\nHumidity: {}\nUV index: {}\nWind Speed: {}m/s\nWeather: {}".format(data["temp"],data["feels_like"],data["humidity"],data["uvi"],data["wind_speed"],weather["description"])

def fetch_status(parameters):
    location = parameters.get('geo-country')
    location = location.lower().replace(" ","-")
    url = "https://api.covid19api.com/country/{}".format(location)
    url_res =  urlopen(url)
    url_data = url_res.read()
    url_data = json.loads(url_data)
    if location == "united-kingdom":
        data = url_data[-6]
    elif location == "canada":
        data = url_data[-7]
    else:
        data = url_data[-1]
    return "Here is the information you asked for\nTotal Confirmed: {}.\nTotal Recovered: {}.\nTotal Deaths: {}.\nTotal Active: {}".format(data["Confirmed"],data["Recovered"],data["Deaths"],data["Active"])


camera_keyboard = [["FHAZ","RHAZ","MAST"],["NAVCAM","CHEMCAM","MAHLI"]] 

news_topic = [["lifestyle","business","technology"],["entertainment","sports","politics"],["culture","education","health"]]


