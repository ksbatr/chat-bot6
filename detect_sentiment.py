from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)

class ActionDetectSentiment(Action):
    def name(self) -> Text:
        return "action_detect_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            text = tracker.latest_message.get("text", "")
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.2:
                sentiment = "positive"
                response = "utter_sentiment_positive"
            elif polarity < -0.2:
                sentiment = "negative"
                response = "utter_sentiment_negative"
            else:
                sentiment = "neutral"
                response = "utter_sentiment_neutral"
            
            return [
                {"event": "slot", "name": "sentiment", "value": sentiment},
                {"event": "followup", "name": response}
            ]
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return []
