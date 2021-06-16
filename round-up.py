import requests
import os
import math
import uuid
from json import dumps as jd

SANDBOX_URL = "https://api-sandbox.starlingbank.com/api/v2"


class roundUp:

    def __init__(self):
        self.accessToken = os.environ.get(
            'SANDBOX_ACCESS_TOKEN')  # ! Set TOKEN in os env
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.accessToken}"
        }
        acc = self.getreq('/accounts')
        self.accountUid = acc['accounts'][0]['accountUid']
        self.defaultCategory = acc['accounts'][0]['defaultCategory']

        sav = self.getreq(f'/account/{self.accountUid}/savings-goals')
        self.savingsGoalUid = sav['savingsGoalList'][0]['savingsGoalUid']

    def getreq(self, request_params):
        """api-sandbox GET request

        Args:
            request_params (string): url parameters inc. queries

        Returns:
            json-content of response: sandbox 
        """

        r = requests.get(
            SANDBOX_URL + request_params,
            headers=self._headers
        ).json()

        if 'error' in r:
            raise Exception(r['error_description'])
        return r

    def calcSavings(self, min_dt, max_dt):
        """Round up to calculate savings

        Args:
            min_dt (String): minTransactionTimestamp
            max_dt (String): maxTransactionTimestamp

        Returns:
            int: minorUnits of savings
        """
        feed = f"/feed/account/{main.accountUid}/category/{main.defaultCategory}/transactions-between?minTransactionTimestamp={min_dt}&maxTransactionTimestamp={max_dt}"
        resp = main.getreq(feed)['feedItems']
        tot = 0
        for i in range(len(resp)):
            x = resp[i]['amount']['minorUnits'] / 100
            tot += math.ceil(x) - x
        # print(tot)
        minor_units = int(round(tot, 2) * 100)
        return minor_units

    def addToSavings(self, _savings):
        """Add "round_up" to savings

        Args:
            _savings (float): .calcSavings
        """
        payload = {
            "amount": {
                "currency": "GBP",
                "minorUnits": _savings
            }
        }
        sav_params = f"/account/{main.accountUid}/savings-goals/{self.savingsGoalUid}/add-money/{str(uuid.uuid4())}"
        r = requests.put(
            SANDBOX_URL + sav_params,
            headers=self._headers,
            data=jd(payload)
        )
        print(r.content)


minTransactionTimestamp = "2021-06-01T12%3A34%3A56.000Z"
maxTransactionTimestamp = "2021-07-01T12%3A34%3A56.000Z"

main = roundUp()
savings = main.calcSavings(minTransactionTimestamp, maxTransactionTimestamp)
main.addToSavings(savings)
