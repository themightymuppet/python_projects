#! /usr/bin/env python3
import os
import requests
import json
import slack
from slackbot import slackclient

# Need to clean this up to use slash command

# grab token from env var, error if not found
def extract_api_token(env_var_name):
    token = os.environ.get(env_var_name)
    if token:
        return token
    else:
        print('Could not retrieve token from env var')

# grab slack token from env var
# authenticate from slack app to read emoji.list scope
SLACK_TOKEN = 'SLACK_TOKEN'
slack_token = extract_api_token('SLACK_TOKEN')
client = slack.WebClient(token=slack_token)

# JSON output of emoji.list
payload = str(client.api_call("emoji.list"))
# convert to dictionary
payload = eval(payload)
# ignore k/v pairs outside of emojis
payload = payload['emoji']

# unpack dictionary to ignore links and format as :emoji: for payload
def unpack_emoji(dict):
    emojis = ''
    for k in dict:
        emojis += ':' + k + ': '   
    return emojis

# convert emoji string to list to truncate for slack payload limits
emoji_list = unpack_emoji(payload).split(' ')
emoji_list.sort() # sort alphabetically for ease

# generate pairs of 50 emoji and convert back to string
# need to rewrite this as a function/algorithm so it's
# less manual and supports an unlimited number of emoji
e50 = ' '.join(emoji_list[:50:])
e100 = ' '.join(emoji_list[51:100:])
e150 = ' '.join(emoji_list[101:150:])
e200 = ' '.join(emoji_list[151:200:])
e250 = ' '.join(emoji_list[201:250:])
e300 = ' '.join(emoji_list[251:300:])
e350 = ' '.join(emoji_list[301:350:])
e400 = ' '.join(emoji_list[351:400:])
e450 = ' '.join(emoji_list[401:450:])
e500 = ' '.join(emoji_list[451:500:])
e550 = ' '.join(emoji_list[501:550:])
e600 = ' '.join(emoji_list[551:600:])

# send payload to specified channel
# sending in sectioned blocks for ease of sending
# multiple payloads at once.
# probably need to rewrite this too for algorithm based on above
client.chat_postMessage(
  channel="test-alerts-keri",
  blocks=[
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e50) + str(e100)
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e150) + str(e200)
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e250) + str(e300)
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e350) + str(e400)
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e450) + str(e500)
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": str(e550) + str(e600)
        },
    }
  ]
)