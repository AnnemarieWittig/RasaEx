# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
#
class ActionValues():
    URL='http://20.79.206.115:8000'

    @staticmethod
    def get_messagetext (tracker: Tracker):
        return {
            'text': tracker.latest_message['text']
        }

class ActionEvaluateBirthday(Action):

    def name(self) -> Text:
        return "action_evaluate_birthday"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = tracker.latest_message
        r = requests.get(ActionValues.URL + '/name?text=' + msg['text'])
        reply = r.json()

        # TODO Do what you need, generate reply here; see the following important_values object for values you might need

        important_values = {
            'intent': msg['intent']['name'], 
            'entities': msg['entities'],
            'text': msg['text'],
            'recognized_first_name': reply["First Name"],
            'recognized_middle_name': reply["Middle Name"],
            'recognized_last_name': reply["Last Name"],
        }

        # This function must be used to return a response
        dispatcher.utter_message(text=json.dumps(important_values))

        return []
    

# layout tracker.latest_message: {'intent': {'name': 'nameRecognition', 'confidence': 1.0}, 'entities': [{'entity': 'name', 'start': 8, 'end': 17, 'confidence_entity': 0.9952344298362732, 'value': 'annemarie', 'extractor': 'DIETClassifier'}], 'text': 'ich bin annemarie', 'message_id': '942e2fc667044c7590566793b6ad3e5e', 'metadata': {}, 'text_tokens': [[0, 3], [4, 7], [8, 17]], 'intent_ranking': [{'name': 'nameRecognition', 'confidence': 1.0}, {'name': 'addressRecognition', 'confidence': 1.7928288853497065e-09}, {'name': 'bot_challenge', 'confidence': 1.5357760896339556e-10}, {'name': 'goodbye', 'confidence': 1.4474441090150947e-10}, {'name': 'greet', 'confidence': 1.0441349174161729e-10}], 'response_selector': {'all_retrieval_intents': [], 'default': {'response': {'responses': None, 'confidence': 0.0, 'intent_response_key': None, 'utter_action': 'utter_None'}, 'ranking': []}}}
