from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

class ActionGetTime(Action):
    def name(self) -> str:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        dispatcher.utter_message(text=f"Сейчас {current_time}.")
        return []

class ActionGetDate(Action):
    def name(self) -> str:
        return "action_get_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        dispatcher.utter_message(text=f"Сегодня {current_date}.")
        return []
