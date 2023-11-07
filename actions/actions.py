from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet ,Restarted
from rasa_sdk.executor import CollectingDispatcher
import sqlalchemy
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, List, Any, Dict

class ActionCheckBooking(Action):
    def name(self):
        return "action_check_booking"

    def run(self, dispatcher, tracker, domain):
        booking_id = tracker.get_slot("booking_id")

        # Configure your database connection
        database_url = "mysql://root:root@localhost:3306/hotel"
        engine = sqlalchemy.create_engine(database_url)

        # Define your SQL query to check if the booking ID exists
        query = f"SELECT COUNT(*) FROM booking_id WHERE id = '{booking_id}'"

        # Execute the query and fetch the result
        with engine.connect() as connection:
            result = connection.execute(query)
            count = result.scalar()

        button = [{"title": "feedback", "payload": "/give_feedback"},
            
            ]

        # Check if the booking ID exists    
        if count > 0:
            dispatcher.utter_button_message("Great! Your booking is valid. How can I assist you further?",
                                            button
                                            )
            return [SlotSet("booking_id_found", True)]
        else:
            dispatcher.utter_message("Sorry, the provided booking ID is not valid. Please try again with correct ID.")
            return [SlotSet("booking_id_found", False)]



class ActionSaveFeedback(Action):
    def name(self):
        return "action_save_feedback"

    def run(self, dispatcher, tracker, domain):
        feedback = tracker.latest_message['text']
        booking_id = tracker.get_slot("booking_id")
        # Add logic to save feedback to the database
        save_feedback(booking_id, feedback)
        return []




class ActionRestarted(Action):
    """ This is for restarting the chat"""

    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]
