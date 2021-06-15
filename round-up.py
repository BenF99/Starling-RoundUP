import requests
import os


# * API Credentials

accessToken = os.environ.get('SANDBOX_ACCESS_TOKEN')
accountUid = ""
defaultCategory = ""

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {accessToken}"
}

r = requests.get(
    'https://api-sandbox.starlingbank.com' + '/api/v2/accounts',
    headers = headers
).json()

accountUid, defaultCategory = r['accounts'][0]['accountUid'], r['accounts'][0]['defaultCategory']