import sqlite3
import json
from datetime import datetime
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Используем базу данных в памяти
DB_CONNECTION = sqlite3.connect(":memory:")

def init_db():
    """Инициализация in-memory базы данных"""
    cursor = DB_CONNECTION.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT,
        theme TEXT,
        language TEXT,
        email TEXT,
        city TEXT,
        hobbies TEXT,
        last_activity TEXT
    )
    """)
    
    DB_CONNECTION.commit()

# Инициализируем БД при загрузке модуля
init_db()

class ActionSaveUserMemory(Action):
    def name(self) -> Text:
        return "action_save_user_memory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cursor = DB_CONNECTION.cursor()
        
        hobbies = tracker.get_slot("hobbies")
        hobbies_json = json.dumps(hobbies) if hobbies else None
        
        user_data = (
            tracker.sender_id,
            tracker.get_slot("username"),
            tracker.get_slot("theme"),
            tracker.get_slot("language"),
            tracker.get_slot("email"),
            tracker.get_slot("city"),
            hobbies_json,
            datetime.now().isoformat()
        )
        
        cursor.execute("""
        INSERT INTO users (user_id, username, theme, language, email, city, hobbies, last_activity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            theme = excluded.theme,
            language = excluded.language,
            email = excluded.email,
            city = excluded.city,
            hobbies = excluded.hobbies,
            last_activity = excluded.last_activity
        """, user_data)
        
        DB_CONNECTION.commit()
        
        return []

class ActionLoadUserMemory(Action):
    def name(self) -> Text:
        return "action_load_user_memory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cursor = DB_CONNECTION.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (tracker.sender_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return []
        
        # Распаковываем данные из кортежа
        (_, username, theme, language, email, city, hobbies_json, _) = user_data
        
        # Обработка hobbies
        hobbies = []
        if hobbies_json:
            try:
                hobbies = json.loads(hobbies_json)
            except json.JSONDecodeError:
                hobbies = []
        
        return [
            SlotSet("username", username),
            SlotSet("theme", theme),
            SlotSet("language", language),
            SlotSet("email", email),
            SlotSet("city", city),
            SlotSet("hobbies", hobbies)
        ]
