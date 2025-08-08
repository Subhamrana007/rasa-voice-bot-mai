# actions/actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

class ActionAskGemini(Action):

    def name(self) -> Text:
        return "action_ask_gemini"

    async def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_question = tracker.latest_message.get('text')
        dispatcher.utter_message(text="Let me think about that for a moment...")

        try:
            # --- SECURELY LOAD THE API KEY ---
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                dispatcher.utter_message(text="Error: The Gemini API key is not configured on the server.")
                return []

            chat_history = [{"role": "user", "parts": [{"text": user_question}]}]
            payload = {"contents": chat_history}
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

            response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            response.raise_for_status()

            result = response.json()
            if (result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts')):
                
                answer = result['candidates'][0]['content']['parts'][0]['text']
                dispatcher.utter_message(text=answer)
            else:
                dispatcher.utter_message(text="I'm sorry, I couldn't get a clear answer.")

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            dispatcher.utter_message(text="I'm having trouble connecting to my knowledge base.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            dispatcher.utter_message(text="An unexpected error occurred.")

        return []


class ActionTellFact(Action):

    def name(self) -> Text:
        return "action_tell_fact"

    async def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            fact = data.get("text")

            if fact:
                dispatcher.utter_message(text=f"Here is a random fact for you: {fact}")
            else:
                dispatcher.utter_message(text="I couldn't fetch a fact right now, sorry!")

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            dispatcher.utter_message(text="I'm having trouble connecting to my knowledge base for facts.")

        return []
