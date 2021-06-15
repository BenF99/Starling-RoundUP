import requests
import os


# * API Credentials



class roundUp:

    def __init__(self, weekStart):
        self.weekStart = weekStart
        self.accessToken = os.environ.get('SANDBOX_ACCESS_TOKEN') # * environment variable
        self.accountUid = None
        self.defaultCategory = None

    
    def getreq(self, request_params):

        """api-sandbox GET request

        Args:
            request_params (string): url parameters inc. queries

        Returns:
            json-content of response: sandbox 
        """
        
        return requests.get(
            'https://api-sandbox.starlingbank.com' + request_params,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.accessToken}"
            }
        ).json()
    
    
    def setcreds(self, r):
        
        """SET sandbox customer credentials

        Args:
            r (json dict): GET response from sandbox
        """
        
        self.accountUid = r['accounts'][0]['accountUid']
        self.defaultCategory = r['accounts'][0]['defaultCategory']
        
main = roundUp(None)
accounts = main.getreq('/api/v2/accounts')
main.setcreds(accounts)
# feed = f"/api/v2/feed/account/{accountUid}/category/{defaultCategory}/transactions-between?minTransactionTimestamp=2021-06-01T12%3A34%3A56.000Z&maxTransactionTimestamp=2021-07-01T12%3A34%3A56.000Z"