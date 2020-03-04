#!/usr/bin/python3
import requests
import os
# import re
# import sys
# import logging
from envyaml import EnvYAML
import json
from slackclient import SlackClient

env = EnvYAML('config.yaml')


# Notes/list of things to fix:
# Need to account for users outside of teams in schedule
# maybe just pull UIDs and store PD_ID_TO_SLACK_ID in a db?
# need to add escalations
# and channel get, channel currently set to #test-alerts-keri
# Also fix to run on slash command 



# def extract_api_token(env_var_name):
#     token = os.environ.get(env_var_name)
#     if token:
#         return token
#     else:
#         print(f'Could not retrieve token from env var {env_var_name}')

# init tokens
PD_TOKEN = env['apiKeys']['Pagerduty']
SLACK_TOKEN = env['apiKeys']['Slack']
CHANNEL_NAME = env['Channel']
SCHEDULE_ID = extract_api_token('SCHEDULE_ID')
TEAM_ID = extract_api_token('TEAM_ID')
# CHANNEL_ID = config.get('CHANNELS', 'NAME')

ONCALL_REGEX_PATTERN = extract_api_token('ONCALL_REGEX_PATTERN')
ONCALL_STRING = extract_api_token('ONCALL_STRING')
ESCALATIONS = []
P_BASEURL = 'https://api.pagerduty.com/'



PD_HEADERS = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=PD_TOKEN),
        "content-type": "application/json"
    }

PD_PARAMS = {
        'query': '',
        'limit': 100
    }

# log = logging.getLogger(__name__)

def get_team():
    url = 'https://api.pagerduty.com/teams'
    payload = requests.get(url, headers=PD_HEADERS, params=PD_PARAMS)
    result = (payload.json())['teams']
    for t in result:
        # unpack and convert results into separate dictionaries
        if t['name'].lower() == TEAM_ID.lower():
            return t['id']

def get_users(team,param):
    # returns list of users from specified team.
    url = 'https://api.pagerduty.com/users'
    p = {
        'query': '',
        'team_ids[]': team,
        'include[]': [],
        'limit': 100
    }
    payload = requests.get(url, headers=PD_HEADERS, params=p)
    # Convert to dictionary, start unpacking
    result = (payload.json())['users']
    users = ''
    uid = ''
    # Grabs email of users for slack lookup
    if param == 'email':
        for k in [x.items() for x in result]:
            for x,y in k:
                if x == 'email':
                    users += y + ','
                elif x != 'name':
                    continue
        users = users[:-1].split(',')
        return(users)
    # Grabs uid of users from PD 
    elif param == 'id':
        for k in [x.items() for x in result]:
            for x,y in k:
                if x == 'id':
                    uid += y + ','
                elif x != 'name':
                    continue
        uid = uid[:-1].split(',')
        return(uid)


def get_slackID(email):
    # Looks up user by email, grabs their slack uid
    url = f"https://slack.com/api/users.lookupByEmail?token={SLACK_TOKEN}&presence=1&email={email}"
    d = {}
    headers= {}

    payload = requests.request("GET", url, headers=headers, data = d)
    result = (payload.json())['user']['id']
    # Convert to dictionary, start unpacking
    user_id = ''
    for k in result:
        user_id += k 
    return user_id

def get_schedules():
    url = 'https://api.pagerduty.com/schedules'
    payload = requests.get(url, headers=PD_HEADERS, params=PD_PARAMS)
    # Convert to dictionary, start unpacking
    result = (payload.json())['schedules']
    schedules = []
    for k in result:
        if SCHEDULE_ID == k['name']:
            schedules.append(k['id'])
            return schedules

def list_channels():
    url = f'https://slack.com/api/channels.list?token={SLACK_TOKEN}&exclude_archived=1'
    d = {}
    headers= {}
    payload = requests.request("GET", url, headers=headers, data = d)
    result = (payload.json())['channels']
    channel_list = []
    channel_ids = []
    channel_id_oncall = ''
    for k in result:
        channel_list.append(k['name'])
        channel_ids.append(k['id'])
        # create easier to parse list of channels and IDs
        channels = dict(zip(channel_list,channel_ids))
        # return ID of specified channel
        if CHANNEL_NAME == k['name']:
            return k['id']

def get_oncall(schedule):
    # return oncall user by schedule
    # unpacks schedule IDs if multiple listed
    for gid in schedule:
        schedule = gid

    url = f'https://api.pagerduty.com/oncalls?schedule_ids%5B%5D={str(schedule)}'
    payload = requests.get(url, headers=PD_HEADERS, params=PD_PARAMS)
    result = (payload.json())
    # adams unpacking, grab UID of oncall user from schedule
    if result.get('oncalls'):
                on_call_user_id = result['oncalls'][0]['user']['id']
                return on_call_user_id

# adams main
def main(schedule,uids):
    #get oncall user and print details
    on_call_user = get_oncall(schedule)
    channel_oncall = list_channels()
    print(f'Oncall Channel is: {channel_oncall}')
    print(f'Oncall user is: {on_call_user}')
    print(f'Oncall user slack id is : {uids[on_call_user]}')

    slack_token = SLACK_TOKEN
    sc = SlackClient(slack_token)
    print("Attempting to retrieve current topic value")
    current_topic_val = new_topic_val = sc.api_call(
        'channels.info',
        channel=channel_oncall
    )['channel']['topic']['value']
    print(f"Current topic val: \'{current_topic_val}\'")
    if on_call_user:
        print("Substituting in the new on call entry")
        new_topic_val = (ONCALL_REGEX_PATTERN,
                               ONCALL_STRING.format(
                                   uids[on_call_user]))
                               
        sc.api_call(
            'channels.setTopic',
            channel=channel_oncall,
            topic=new_topic_val
        )
        print("Returned results were: %s", new_topic_val)

    elif new_topic_val != current_topic_val:
        # do slack update topic logic
        print("Attempting to update the slack topic with value: %s",
                 new_topic_val)
        results = sc.api_call(
            'channels.setTopic',
            channel=channel_oncall,
            topic=new_topic_val
        )
        print("Returned results were: %s", results)
    else:
        print("No changes in topic detected. Skipping updates")

    # TODO: do logic to post message to slack channel saying couldn't find
    # on_call user for this week


if __name__ == '__main__':
    # if team name known, return team ID. Else list teams
    while True:
        team_id = get_team()
        if not team_id:
            print('failed to fetch team details')
        elif team_id:
            print(f'Your team ID is: {team_id}')
            break
    email = get_users(team_id,'email')
    uid = get_users(team_id,'id')
    slackid = []

    # iterate on each email to generate slackID
    for u in email:
        slackid.append(get_slackID(u))

    # zip pagerdutyID : slackID in a dict
    PD_ID_TO_SLACK_ID = dict(zip(uid,slackid))
    print(PD_ID_TO_SLACK_ID)

    # if schedule name known, return schedule id, else list schedules
    while True:
        schedule_id = get_schedules()
        if not schedule_id:
            print('failed to fetch schedule details')
        elif schedule_id:
            print(f'Your schedule ID is: {schedule_id}')
            break
    main(schedule_id,PD_ID_TO_SLACK_ID)


