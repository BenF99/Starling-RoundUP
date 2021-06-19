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
        }  # API Headers
        acc = self.getreq('/accounts')  # ! ACCOUNTS req
        # * SANDBOX ACCOUNT UID
        self.accountUid = acc['accounts'][0]['accountUid']
        # * SANDBOX CATEGORY ID
        self.defaultCategory = acc['accounts'][0]['defaultCategory']
        # ! SAVINGS req
        sav = self.getreq(f'/account/{self.accountUid}/savings-goals')
        # * SAVINGS GOAL UID - Requires existing savings goal
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
        feed = f"/feed/account/{self.accountUid}/category/{self.defaultCategory}/transactions-between?minTransactionTimestamp={min_dt}&maxTransactionTimestamp={max_dt}"
        resp = self.getreq(feed)['feedItems']

        if not resp:
            raise Exception("No transactions in specified week")

        tot = 0

        for i in range(len(resp)):
            # * Converts minorUnits to standard format
            x = resp[i]['amount']['minorUnits'] / 100
            # * Rounds up TRANSACTION, subtracts from actual value - summation (tot)
            tot += math.ceil(x) - x

        # * Converts round up to minor units with 2DP
        minor_units = int(round(tot, 2) * 100)

        return minor_units

    def addToSavings(self, _savings):
        """Add "round_up" to savings

        Args:
            _savings (float): .calcSavings
        """
        savload = {
            "amount": {
                "currency": "GBP",
                "minorUnits": _savings
            }
        }
        # * "uuid.uuid4" -> Generates random uuid
        sav_params = f"/account/{self.accountUid}/savings-goals/{self.savingsGoalUid}/add-money/{str(uuid.uuid4())}"
        r = requests.put(  # PUT request for savload
            SANDBOX_URL + sav_params,
            headers=self._headers,
            data=jd(savload)
        )
        print(r.content)  # * Testing.


def main(minTransactionTimestamp, maxTransactionTimestamp):
    """main function to execute round up savings

    Args:
        minTransactionTimestamp (str): the min timestamp
        maxTransactionTimestamp (str): the max timestamp (1 week)
    """

    main = roundUp()
    savings = main.calcSavings(
        minTransactionTimestamp, maxTransactionTimestamp)
    main.addToSavings(savings)

    return savings/100  # Return savings in standard format to be displayed on HTML page
