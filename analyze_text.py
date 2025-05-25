from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import logging

logger = logging.getLogger(__name__)

class ActionAnalyzeText(Action):
    def name(self) -> Text:
        logger.info("ActionAnalyzeText name() called")
        return "action_analyze_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logger.info("ActionAnalyzeText run() started")
        
        try:
            text = next(tracker.get_latest_entity_values("text"), None) or \
                  tracker.latest_message.get("text", "")
            
            if "разбери текст" in text.lower():
                text = text.lower().replace("разбери текст", "").strip()
            
            if not text:
                dispatcher.utter_message(text="Не получилось извлечь текст для анализа")
                return []

            analysis = (
                f"📝 Анализ текста:\n"
                f"• Текст: '{text}'\n"
                f"• Длина: {len(text)} символов\n"
                f"• Слов: {len(text.split())}"
            )
            
            dispatcher.utter_message(text=analysis)
            return []
            
        except Exception as e:
            logger.error(f"Error in ActionAnalyzeText: {str(e)}")
            dispatcher.utter_message(text="Произошла ошибка при анализе текста")
            return []
