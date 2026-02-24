#!/usr/bin/python

from __future__ import annotations
import requests

class UnifiClient:
    def __init__(self, host, api_key, verify_ssl=True):
        self.host = host
        self.api_key = api_key
        self.verify_ssl = verify_ssl

    def list_sites(self):
        # TODO: pagination!
        r = requests.get(f"https://{self.host}/proxy/network/integration/v1/sites?limit=200", headers={"X-API-Key": self.api_key}, verify=self.verify_ssl)
        r.raise_for_status()
        response = r.json()["data"]
        return [UnifiSite(site['id'], site['name']) for site in response]

    def list_dns_policies(self, site_id):
        # TODO: pagination!
        r = requests.get(f"https://{self.host}/proxy/network/integration/v1/sites/{site_id}/dns/policies?limit=200", headers={"X-API-Key": self.api_key}, verify=self.verify_ssl)
        r.raise_for_status()
        response = r.json()["data"]
        return [UnifiDNSPolicy(policy['id'], policy['type'], policy['domain'], policy.get('ipv4_address'), policy.get('ttl_seconds', 3600), policy.get('enabled', True)) for policy in response]

    def create_or_update_dns_policy(self, site_id, dns_policy):
        json_data = {
            "type": dns_policy.type,
            "domain": dns_policy.domain,
            "ipv4Address": dns_policy.ipv4_address,
            "ttlSeconds": dns_policy.ttl_seconds,
            "enabled": dns_policy.enabled
        }

        if dns_policy.id:
            # Update existing policy
            r = requests.put(f"https://{self.host}/proxy/network/integration/v1/sites/{site_id}/dns/policies/{dns_policy.id}", headers={"X-API-Key": self.api_key}, json=json_data, verify=self.verify_ssl)
            r.raise_for_status()
            return r.json()

        r = requests.post(f"https://{self.host}/proxy/network/integration/v1/sites/{site_id}/dns/policies", headers={"X-API-Key": self.api_key}, json=json_data, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()

    def delete_dns_policy(self, site_id, policy_id):
        r = requests.delete(f"https://{self.host}/proxy/network/integration/v1/sites/{site_id}/dns/policies/{policy_id}", headers={"X-API-Key": self.api_key}, verify=self.verify_ssl)
        r.raise_for_status()
        return True

class UnifiSite:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class UnifiDNSPolicy:
    def __init__(self, id, type, domain, ipv4_address=None, ttl_seconds=3600, enabled=True):
        self.id = id
        self.type = type
        self.domain = domain
        self.ipv4_address = ipv4_address
        self.ttl_seconds = ttl_seconds
        self.enabled = enabled

    def to_dict(self):
        return {
            "type": self.type,
            "domain": self.domain,
            "ipv4_address": self.ipv4_address,
            "ttl_seconds": self.ttl_seconds,
            "enabled": self.enabled
        }

__all__ = ['UnifiClient', 'UnifiDNSPolicy', 'UnifiSite']
