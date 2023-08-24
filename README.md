# Slackusers
Download the list of users from a workspace

## Setup
In order to use this tool an access token and a cookie needs to be retrieved from Slack.
This can be done by opening slack in the Chrome browser with the URL `https://<your workspace>.slack.com`.
Now open developer mode in the browser, click the `Network` tab and reload the page.
Then search for a POST request that uses the slack API (e.g. `apps.profile.get`).

### Token
The payload of this POST request contains the `token` which starts with the string `xoxc-`.

### Cookie
The same request should contain a cookie `d` that is also required to successfully use the Slack API.
It should start with the string `xoxd-`.

## Usage
Run the script `slackusers.py` to produce an Excel file with all users in the workspace.
```
usage: slackusers.py [-h] -t TOKEN -c COOKIE [-x XLS_OUTPUT]

Get users from slack workspace

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Access token for the Slack workspace.
  -c COOKIE, --cookie COOKIE
                        Access cookie for the Slack workspace.
  -x XLS_OUTPUT, --xls_output XLS_OUTPUT
                        Excel output file name.
```
