import asyncio
import json
import random
import socket
import time

import teams #We have made changes to pymsteams module so please use teams.py DO NOT USE pymsteams.py
from walkoff_app_sdk.app_base import AppBase

class MsTeams(AppBase):
    __version__ = "1.0.0"
    app_name = "Microsoft Teams"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # Write your data inside this function
    def send_simple_text(self, webhook_url, message):
        try:
            myTeamsMessage = teams.connectorcard(str(webhook_url))    # You must create the connectorcard object with the Microsoft Webhook URL
            myTeamsMessage.text(message)     # Add text to the message.
            myTeamsMessage.send()# send the message.
        except Exception as e:
            return f'{e.__class__} occured'

        return f'Message Sent'

    def send_rich_text(self, webhook_url, title, message, link_button_text, link_button_url):
        try:
            myTeamsMessage = teams.connectorcard(webhook_url)    # You must create the connectorcard object with the Microsoft Webhook URL
            myTeamsMessage.title(title) # title for your card
            myTeamsMessage.text(message)     # Add text to the message.
            myTeamsMessage.addLinkButton(str(link_button_text), str(link_button_url)) # for button
            myTeamsMessage.send()# send the message.
        except Exception as e:
            return f'{e.__class__} occured'

        return f'Message Sent'

    def send_actionable_msg(self, webhook_url, title, message, added_information, choices, callback_url):
        try:
            myTeamsMessage = teams.connectorcard(webhook_url)    # You must create the connectorcard object with the Microsoft Webhook URL
            myTeamsMessage.title(title) # title for your card
            myTeamsMessage.text(message)     # Add text to the message.
            myTeamsPotentialAction3 = teams.potentialaction(_name = "Select_Action")

            if choices:
                for choice in choices.split(","):
                    choice = choice.strip()
                    value = {
                        "choice": choice,
                        "extra": added_information,
                    }

                    try:
                        choice_value = json.dumps(value)
                    except:
                        print("FAILED ENCODING {}".format(choice))
                        choice_value = choice

                    myTeamsPotentialAction3.choices.addChoices(choice, choice_value) #option 1

            else:
                value = {
                    "choice": "ACCEPT",
                    "extra": added_information,
                }

                #print(f"VALUE: {value}")

                try:
                    accept = json.dumps(value)
                except:
                    print("FAILED ENCODING ACCEPT")
                    accept = "ACCEPT"

                myTeamsPotentialAction3.choices.addChoices("Accept", accept) #option 1

                value["choice"] = "REJECT"
                try:
                    deny = json.dumps(value)
                except:
                    print("FAILED ENCODING REJECT")
                    deny = "REJECT"

                myTeamsPotentialAction3.choices.addChoices("Reject", deny) #option 2

            myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select Action", False) #Dropdown menu
            myTeamsPotentialAction3.addAction("HttpPost","Submit",callback_url) #post request to Shuffle
            myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)
            myTeamsMessage.send()# send the message.
        except Exception as e:
            return f'{e} occured'

        return f'Message Sent'

    def get_user_input(self, webhook_url, title, message, callback_url):
        try:
            myTeamsMessage = teams.connectorcard(webhook_url)  # You must create the connectorcard object with the Microsoft Webhook URL
            myTeamsMessage.title(title) # Title for your card
            myTeamsMessage.text(message) # Add text to the message.
            myTeamsPotentialAction1 = teams.potentialaction(_name = "Comment")
            myTeamsPotentialAction1.addInput("TextInput","comment", "Your text here..",False)
            myTeamsPotentialAction1.addCommentAction("HttpPost","Submit", callback_url)
            myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
            myTeamsMessage.send()
        except Exception as e:
            return f'{e.__class__} occured'

        return f'Message Sent'

if __name__ == "__main__":
    MsTeams.run()
