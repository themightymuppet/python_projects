# Slack Emoji Digest
---
### Initial Setup: brew

Before you start, Make sure you have brew installed:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
or just check to make sure you're up to date:
```
brew upgrade
```

Then install python@2:

```
brew install python@2
```
and python@3
```
brew install python@3
```

### Initial Setup: SlackApp

In your slack workspace, create a new slack app. Give it a bot user (I named mine @emojiBot)and add the following scopes under oAuth & Permissions:

- bot
- emoji:read
- chat:write:bot

When you're done, make sure to install the app into your workspace to make it active and to generate your slack oAuth token and signing secret. You will need to be a workspace admin to complete that task, otherwise you'll need someone to do that step for you.

---

## emoji_listall.py setup

List all custom emojis in a specified channel.
This currently runs off of a Python3 environment. Need to fix for consistency to emoji_events.

### Create your python@3 environment:
If python@2 is set as your primary, switch to python@3:
```
brew unlink python@2
brew link python@3
```
Then create a python3 env. Since we're just doing this in our working directory, make sure to give the env a unique name:
```
virtuanenv py3_env
```
Activate your env:
```
source py3_env/bin/activate
```
and install the requirements
```
pip3 install -r requirements.txt
```

### Create your env var:
Once your app is installed, copy the **Bot User OAuth Access Token**  from your oAuth & Permissions panel. Set your SLACK_TOKEN environment var to the token you copied:
```
export SLACK_TOKEN=xoxb-000000000-000000000-xXxXxxxxXXXXxxxXx
```

### Edit the script to post to your channel:
Before you run the script, be sure to edit the **channel** string to the name of the slackchannel you want your bot to post to. You should also invite your bot to that channel for it actively post there.

### Ship it!
Okay! Now you're ready to run the script
```
python3 emoji_listall.py
```
This will post a list of up to 600 emoji with all the custom emojis in your workspace.

### Wrapping up
When you're done working in this env, don't forget to deactivate!
```
deactivate
```

---

## emoji_events.py setup

This script listens for emoji_changed events from slack and posts the details to a specified channel. This currently runs on a python@2 env for compatibility with the slackeventsapi.

### Create your python@2 environment:
If python@3 is set as your primary, switch to python@2:
```
brew unlink python@3
brew link python@2
```
Then create a python2 env with a unique name in your working directory:
```
virtuanenv py2_env
```
Activate your env:
```
source py2_env/bin/activate
```
and install the requirements
```
pip install -r requirements.txt
```

### Set up a localtunnel:

If you don't already have ngrok installed, you can install it from brew:
```
brew install ngrok
```
You'll also need to setup an account at [ngrok](https://ngrok.com/) to get your authorization token. Once you're logged in, you'll see the authtoken in the setup & installation instructions. Copy your authtoken and run this command to add it to your ngrok config:
```
ngrok authtoken xXxXxxXXXxxxxxxXXXXX
```
Once you've added your authtoken to the config, start a localtunnel:
```
ngrok http 3000
```
You should get an output that looks like this:
```
Session Status                online 
Account                       [Your Name] (Plan: Free)
Version                       2.3.35 
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040                                                        
Forwarding                    http://#########..ngrok.io -> http://localhost:3000                            
Forwarding                    https://#########.ngrok.io -> http://localhost:3000   
```

### Set up your env vars

From your Slack App, open the Basic Information panel and copy the **Signing Secret**. Then set the signing secret as an env var:
```
export SLACK_SECRET=xXxXxxXXXxxxxxxXXXXX
```
Next open up the oAuth & Permissions panel and grab your **Bot User OAuth Access Token**. Set it as an env var:
```
export SLACK_TOKEN=xoxb-000000000-000000000-xXxXxxxxXXXXxxxXx
```

## Set up the Listener

In order to use Slack's Events API, you'll need to have the localtunnel active and the script listening in. (FYI the localtunnel is just for development. This shouldn't be used for prod) 

So first make any edits you need to the script (ex. updating the channel var string or the message output)

Then start your script:
```
python2 emoji_events.py
```
It should look like this:
```
 * Serving Flask app "slackeventsapi.server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
 ```

 ## Setting up the Slack Events

 Now back in your Slack App settings, hop over to the **Event Subscriptions** panel and enable it. We're going to set up your Event.

 First, enter your Request URL. You get this from the ngrok command you started earlier and we append `/slack/events` to the end of it. Be sure to use the SSL (https) link forwarding. Your Request URL should look something like this:
 ```
 https://########.ngrok.io/slack/events
 ```
 Slack events needs a tunnel because it posts a `challenge` to that URL that needs to be accepted. So long as both ngrok and your script are running, it should verify.

 Next, open up the **Subscribe to Workspace Events** menu and add **emoji_changed** as an event. It'll look like this:
 <img src="https://i.imgur.com/AnZ8J6p.png" width="350"/>

Once you save those settings, your script should start working it's magic!
To test, you (or rather a slack admin) can [add a custom slack emoji](https://slack.com/customize/emoji).

### Wrapping up
When you're done working in this env, don't forget to deactivate!
```
deactivate
```
Also keep in mind that if you stop your script and/or your local tunnel, you will need to walk through these steps again. The localtunnel will generate a new forwarding url each time so you'll need to re-verify your request URL.