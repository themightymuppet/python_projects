#!/usr/bin/env python2
from slackeventsapi import SlackEventAdapter
from slackclient import slackclient
import os

# grab slack secret for events API
slack_signing_secret = os.environ["SLACK_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# get slack token and authenticate
slack_bot_token = os.environ["SLACK_TOKEN"]
slack_client = slackclient(slack_bot_token)

# listen for emoji_changed event
# if event is to add emoji, post message with emoji
# if event is to remove emoji, post message with deleted name
@slack_events_adapter.on("emoji_changed")
def emoji_changed(event_data):
    event = event_data["event"]
    subtype = event["subtype"]
    if 'name' in event:
        emoji = event["name"]
    elif 'names' in event:
        emoji = event["names"]
        names = ''
        for x in emoji:
            names += ' ' + x
    channel = 'test-alerts-keri'
    if subtype == "add":
        message = "A new Emoji was added: :%s: !" % emoji
        slack_client.api_call("chat.postMessage", channel=channel, text=message)
    elif subtype == "remove":
        message = "Sorry, an Emoji was deleted: %s :white_frowning_face:" % names
        slack_client.api_call("chat.postMessage", channel=channel, text=message)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)