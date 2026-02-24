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
        default: 3600
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
    type: A_RECORD
    domain: my-server.example.com
    ipv4_address: 192.168.0.23
    ttl_seconds: 3600
    enabled: true
    state: present
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
                type={"type": "str"},
                domain={"type": "str"},
                ipv4_address={"type": "str"},
                ttl_seconds={"type": "int", "default": 3600},
                enabled={"type": "bool", "default": True},
                state={"type": "str", "default": "present", "choices": ["present", "absent"]}
            ),
            supports_check_mode=True
        )

from ansible.module_utils.basic import AnsibleModule

def main():
    module = DnsPolicy.define_module()

    state = module.params.get("state")
    
    # Get module parameters
    dns_policy_type = module.params.get("type")
    domain = module.params.get("domain")
    ipv4_address = module.params.get("ipv4_address")
    ttl_seconds = module.params.get("ttl_seconds")
    enabled = module.params.get("enabled")
    
    try:
        if state == "absent":
            # Delete DNS policy logic would go here
            module.exit_json(
                changed=True,
                msg="DNS policy deleted",
                dns_policy={
                    "domain": domain,
                    "state": "absent"
                }
            )
        elif state == "present":
            # Create or update DNS policy logic would go here
            module.exit_json(
                changed=True,
                msg="DNS policy created or updated",
                dns_policy={
                    "type": dns_policy_type,
                    "domain": domain,
                    "ipv4_address": ipv4_address,
                    "ttl_seconds": ttl_seconds,
                    "enabled": enabled,
                    "state": "present"
                }
            )
    except Exception as e:
        module.fail_json(msg=f"Failed to manage DNS policy: {str(e)}")

if __name__ == "__main__":
    main()
