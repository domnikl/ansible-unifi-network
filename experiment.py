import os
import requests

host = os.environ["UNIFI_HOST"]
api_key = os.environ["UNIFI_API_KEY"]
verify_ssl = os.environ["UNIFI_VERIFY_SSL"].lower() == "true"

r = requests.get(f"https://{host}/proxy/network/integration/v1/sites", headers={"X-API-Key": api_key}, verify=verify_ssl)
print(r.status_code)
print(r.json())
