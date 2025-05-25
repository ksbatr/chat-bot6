from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetWeather(Action):
    def name(self) -> str:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        city = tracker.get_slot("city")
        if not city:
            dispatcher.utter_message(text="Для какого города проверить погоду?")
            return []

        API_KEY = "083e1d1fe7c88dcf28e4d76c493fa34b"  # Замените на ваш ключ
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        
        try:
            response = requests.get(url)
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            dispatcher.utter_message(text=f"В городе {city} сейчас {desc}, температура {temp}°C.")
        except:
            dispatcher.utter_message(text="Не удалось получить погоду. Проверьте название города.")
        return []
