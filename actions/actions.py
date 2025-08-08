# actions/actions.py

# --- THESE ARE THE MISSING IMPORTS ---
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
# --- END OF FIX ---

class ActionAskGemini(Action):

    def name(self) -> Text:
        return "action_ask_gemini"

    async def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the last message the user sent
        user_question = tracker.latest_message.get('text')
        
        dispatcher.utter_message(text="Let me think about that for a moment...")

        # --- Call the Gemini API ---
        try:
            # Prepare the payload for the Gemini API
            chat_history = [{"role": "user", "parts": [{"text": user_question}]}]
            payload = {"contents": chat_history}
            api_key = "AIzaSyDOYA4cYVz1k9gF0GxW1-s5p4Wlsh1XbBI" # IMPORTANT: Paste your key here
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

            # Make the API call
            response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # Extract the text from the response
            result = response.json()
            if (result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts')):
                
                answer = result['candidates'][0]['content']['parts'][0]['text']
                dispatcher.utter_message(text=answer)
            else:
                dispatcher.utter_message(text="I'm sorry, I couldn't get a clear answer. Please try asking in a different way.")

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            dispatcher.utter_message(text="I'm having trouble connecting to my knowledge base right now. Please try again later.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            dispatcher.utter_message(text="An unexpected error occurred. I'm sorry about that.")

        return []


class ActionTellFact(Action):

    def name(self) -> Text:
        return "action_tell_fact"

    async def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # This is the URL for the free, no-key-required facts API
        api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status() # Raise an exception for bad status codes

            data = response.json()
            fact = data.get("text")

            if fact:
                dispatcher.utter_message(text=f"Here is a random fact for you: {fact}")
            else:
                dispatcher.utter_message(text="I couldn't fetch a fact right now, sorry about that!")

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            dispatcher.utter_message(text="I'm having trouble connecting to my knowledge base for facts.")

        return []
