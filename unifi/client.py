import requests

class UnifiClient:
    def __init__(self, host, api_key, verify_ssl=True):
        self.host = host
        self.api_key = api_key
        self.verify_ssl = verify_ssl

    def get_sites(self):
        r = requests.get(f"https://{self.host}/proxy/network/integration/v1/sites", headers={"X-API-Key": self.api_key}, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()

    def get_dns_policies(self, site_id):
        r = requests.get(f"https://{self.host}/proxy/network/integration/v1/sites/{site_id}/dns-policies", headers={"X-API-Key": self.api_key}, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()
