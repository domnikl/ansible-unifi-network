#!/usr/bin/python

from __future__ import annotations

DOCUMENTATION = """
---
module: dns_policy

short_description: Create and manage DNS policies on a UniFi Network.

description:
    - Create, update and manage DNS policies on a UniFi Network.

author:
    - Dominik Liebler (@domnikl)

options:
    host:
        description:
            - Hostname or IP address of the UniFi Network controller.
        type: str
        required: true
    api_key:
        description:
            - API key for authentication with the UniFi Network controller.
        type: str
        required: true
        no_log: true
    site_name:
        description:
            - Name of the site where the DNS policy should be managed.
        type: str
        default: default
    verify_ssl:
        description:
            - Whether to verify SSL certificates.
        type: bool
        default: true
    type:
        description:
            - Type of the DNS policy to manage.
        type: str
        required: true
        choices: [ A_RECORD, CNAME_RECORD ]
    domain:
        description:
            - Domain of the DNS policy to manage.
        type: str
        required: true
    ipv4_address:
        description:
            - IPv4 address of the DNS policy to manage.
        type: str
    ttl_seconds:
        description:
            - TTL in seconds of the DNS policy to manage.
        type: int
        default: 0
    enabled:
        description:
            - Whether the DNS policy is enabled or not.
        type: bool
        default: true
    state:
        description:
            - Whether the DNS policy should be present or not.
        type: str
        default: present
        choices: [ present, absent ]
"""

EXAMPLES = """
- name: Create a A record for a server
  domnikl.unifi_network.dns_policy:
    host: unifi.example.com
    api_key: "{{ unifi_api_key }}"
    type: A_RECORD
    domain: my-server.example.com
    ipv4_address: 192.168.0.23
    ttl_seconds: 3600
    enabled: true
    state: present

- name: Delete a DNS policy
  domnikl.unifi_network.dns_policy:
    host: unifi.example.com
    api_key: "{{ unifi_api_key }}"
    domain: old-server.example.com
    state: absent
"""

RETURN = """
dns_policy:
    description: The DNS policy
    returned: Always
    type: dict
    contains:
        domain:
            description: Domain of the DNS policy
            returned: always
            type: str
            sample: my-server
"""

class DnsPolicy():
    @classmethod
    def define_module(cls):
        return AnsibleModule(
            argument_spec=dict(
                host={"type": "str", "required": True},
                api_key={"type": "str", "required": True, "no_log": True},
                site_name={"type": "str", "default": "default"},
                verify_ssl={"type": "bool", "default": True},
                type={"type": "str", "required": True, "choices": ["A_RECORD", "CNAME_RECORD"]},
                domain={"type": "str", "required": True},
                ipv4_address={"type": "str"},
                ttl_seconds={"type": "int", "default": 0},
                enabled={"type": "bool", "default": True},
                state={"type": "str", "default": "present", "choices": ["present", "absent"]}
            ),
            supports_check_mode=True
        )

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.domnikl.unifi_network.plugins.module_utils.unifi_client import UnifiClient, UnifiDNSPolicy

def find_dns_policy_by_domain(policies, domain):
    """Find a DNS policy by domain name."""
    for policy in policies:
        if policy.domain == domain:
            return policy
    return None

def main():
    module = DnsPolicy.define_module()

    # Get connection parameters
    host = module.params.get("host")
    api_key = module.params.get("api_key")
    site_name = module.params.get("site_name")
    verify_ssl = module.params.get("verify_ssl")
    
    # Get DNS policy parameters
    state = module.params.get("state")
    dns_policy_type = module.params.get("type")
    domain = module.params.get("domain")
    ipv4_address = module.params.get("ipv4_address")
    ttl_seconds = module.params.get("ttl_seconds")
    enabled = module.params.get("enabled")
    
    try:
        # Initialize UniFi client
        client = UnifiClient(host, api_key, verify_ssl)
        sites = client.list_sites()

        site_id = None
        site_id = next((site.id for site in sites if site.name.lower() == site_name.lower()), None)
        if not site_id:
            module.fail_json(msg=f"Site with name '{site_name}' not found on UniFi Network")
        
        # Get existing DNS policies
        existing_policies = client.list_dns_policies(site_id)
        existing_policy = find_dns_policy_by_domain(existing_policies, domain)

        if state == "absent":
            if existing_policy:
                # Policy exists and should be deleted
                policy_id = existing_policy.id
                if policy_id:
                    if not module.check_mode:
                        client.delete_dns_policy(site_id, policy_id)
                    module.exit_json(
                        changed=True,
                        msg=f"DNS policy for domain {domain} deleted",
                        dns_policy={
                            "domain": domain,
                            "state": "absent"
                        }
                    )
                else:
                    module.fail_json(msg=f"DNS policy for domain {domain} found but has no ID")
            else:
                # Policy doesn't exist, nothing to do
                module.exit_json(
                    changed=False,
                    msg=f"DNS policy for domain {domain} does not exist",
                    dns_policy={
                        "domain": domain,
                        "state": "absent"
                    }
                )
        elif state == "present":
            # Create UnifiDNSPolicy object
            dns_policy = UnifiDNSPolicy(
                id=None,  # ID will be set for updates
                type=dns_policy_type,
                domain=domain,
                ipv4_address=ipv4_address,
                ttl_seconds=ttl_seconds,
                enabled=enabled
            )
            
            if existing_policy:
                dns_policy.id = existing_policy.id  # set ID for update operation

                # Check if policy needs to be updated
                needs_update = (
                    existing_policy.type != dns_policy_type or
                    existing_policy.ipv4_address != ipv4_address or
                    existing_policy.ttl_seconds != ttl_seconds or
                    existing_policy.enabled != enabled
                )
                
                if needs_update:
                    if not module.check_mode:
                        result = client.create_or_update_dns_policy(site_id, dns_policy)
                    module.exit_json(
                        changed=True,
                        msg=f"DNS policy for domain {domain} updated",
                        dns_policy=dns_policy.to_dict()
                    )
                else:
                    module.exit_json(
                        changed=False,
                        msg=f"DNS policy for domain {domain} already exists with correct configuration",
                        dns_policy=dns_policy.to_dict()
                    )
            else:
                # Create new DNS policy
                if not module.check_mode:
                    result = client.create_or_update_dns_policy(site_id, dns_policy)
                module.exit_json(
                    changed=True,
                    msg=f"DNS policy for domain {domain} created",
                    dns_policy=dns_policy.to_dict()
                )
                
    except Exception as e:
        # also log stack trace for easier debugging
        import traceback
        traceback_str = traceback.format_exc()
        module.fail_json(msg=f"Failed to manage DNS policy: {str(e)}, {traceback_str}", exception=traceback_str)

if __name__ == "__main__":
    main()
