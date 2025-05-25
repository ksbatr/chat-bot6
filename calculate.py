from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re

class ActionCalculate(Action):
    def name(self) -> str:
        return "action_calculate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        expression = tracker.latest_message.get("text")
        match = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", expression)
        
        if not match:
            dispatcher.utter_message(text="Некорректный ввод. Пример: '5+3'.")
            return []

        num1, op, num2 = match.groups()
        try:
            result = eval(f"{num1}{op}{num2}")  # Осторожно с eval в продакшене!
            dispatcher.utter_message(text=f"Результат: {result}")
        except:
            dispatcher.utter_message(text="Ошибка вычисления.")
        return []
