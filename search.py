from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import urllib.parse

class ActionSearchWeb(Action):
    def name(self) -> str:
        return "action_search_web"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        query = tracker.get_slot("search_query")
        if not query:
            dispatcher.utter_message(text="Укажите, что искать. Например: 'Найди котиков'.")
            return []

        encoded_query = urllib.parse.quote_plus(query)
        webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
        dispatcher.utter_message(text=f"Открываю поиск для: '{query}'.")
        return []
