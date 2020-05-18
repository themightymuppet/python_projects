from envyaml import EnvYAML
import requests
import json
import os
import re

env = EnvYAML('config.yaml')

OktaAPI = env['Okta']['apiKey']
OktaURL = env['Okta']['baseURL']
email = env['Okta']['userEmail']

class User:
    def __init__(self,user):
        self.user = user

    def __repr__(self):
        return self.user

    def director(self):
        while True:
            url = OktaURL + '/api/v1/users/' + self.user
            payload = {}
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + OktaAPI
            }
            response = requests.request("GET", url, headers=headers, data = payload)
            payload = (response.json())
            if payload['profile']['email'] == self.user:
                if payload['profile']['peopleManagerType'] == 'Director':
                    return self.user
                elif payload['profile']['peopleManagerType'] == 'Executive':
                    return self.user
                else:
                    self.user = payload['profile']['managerEmail']

user = User(email)
print(user.director())