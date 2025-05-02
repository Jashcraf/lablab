import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import re


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],
                                         '/slack/events', app)

# Load token from .env file
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]

def clean_bot_mention(text):
    # Remove any <@BOTID> mentions from the text
    cleaned_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    return cleaned_text

@slack_events_adapter.on("app_mention")
def respond_to_app_mention(payload):

    event_data = payload['event']

    # clean recieved text
    clean_event_text = clean_bot_mention(event_data['text'])

    if BOT_ID != event_data['user']:
        if "who's a good".lower() in clean_event_text.lower():
            MESSAGE_TO_SEND = "Me!"

    client.chat_postMessage(channel=event_data['channel'], text=MESSAGE_TO_SEND)

if __name__ == '__main__':
    # client.chat_postMessage(channel="#postdocs", text="I'M ALIVE!")
    app.run(debug=True)