import requests
import os
import math
import uuid


class roundUp:

    def __init__(self):
        self.accessToken = os.environ.get(
            'SANDBOX_ACCESS_TOKEN')  # ! Set TOKEN in os env

        acc = self.getreq('/api/v2/accounts')
        self.accountUid = acc['accounts'][0]['accountUid']
        self.defaultCategory = acc['accounts'][0]['defaultCategory']

        sav = self.getreq(f'/api/v2/account/{self.accountUid}/savings-goals')
        self.savingsGoalUid = sav['savingsGoalList'][0]['savingsGoalUid']

    def getreq(self, request_params):
        """api-sandbox GET request

        Args:
            request_params (string): url parameters inc. queries

        Returns:
            json-content of response: sandbox 
        """

        r = requests.get(
            'https://api-sandbox.starlingbank.com' + request_params,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.accessToken}"
            }
        ).json()

        return r

    def calcSavings(self, min_dt, max_dt):
        feed = f"/api/v2/feed/account/{main.accountUid}/category/{main.defaultCategory}/transactions-between?minTransactionTimestamp={min_dt}&maxTransactionTimestamp={max_dt}"
        resp = main.getreq(feed)['feedItems']
        tot = 0
        for i in range(len(resp)):
            x = resp[i]['amount']['minorUnits'] / 100
            tot += math.ceil(x) - x
        return round(tot, 2)

    def addToSavings(self, _savings):
        payload = {
            "amount": {
                "currency": "GBP",
                "minorUnits": _savings * 100
            }
        }
        sav_url = f"/api/v2/account/{main.accountUid}/savings-goals/{self.savingsGoalUid}/add-money/{str(uuid.uuid4())}"
        r = requests.put(
            'https://api-sandbox.starlingbank.com' + sav_url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.accessToken}"
            },
            data=payload
        )

        print(r.content)


minTransactionTimestamp = "2021-06-01T12%3A34%3A56.000Z"
maxTransactionTimestamp = "2021-07-01T12%3A34%3A56.000Z"

main = roundUp()
savings = main.calcSavings(minTransactionTimestamp, maxTransactionTimestamp)
main.addToSavings(savings)
