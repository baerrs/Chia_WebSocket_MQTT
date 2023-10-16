import requests
import urllib3
import json
urllib3.disable_warnings()
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
urllib3.disable_warnings()

def get_balance():
    headers = {'Content-Type': 'application/json'}
    url = "https://localhost:9256/get_wallet_balance"
    data = '{"wallet_id": 1}'
    cert = ('ssl/wallet/private_wallet.crt', 'ssl/wallet/private_wallet.key')
    response = json.loads(requests.post(url, data=data, headers=headers, cert=cert, verify=False).text)
    return response
# Print the Response
print(get_balance())
