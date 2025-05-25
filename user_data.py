from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

class ActionLogMessage(Action):
    def name(self) -> str:
        return "action_log_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get("text")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] User: {user_message}\n")
        
        return []
