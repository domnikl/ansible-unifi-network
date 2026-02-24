# Ansible Collection - domnikl.unifi_network

A comprehensive Ansible collection for managing UniFi Network resources through the UniFi Network Integration API.

[![GitHub release](https://img.shields.io/github/release/domnikl/ansible-unifi-network.svg)](https://github.com/domnikl/ansible-unifi-network/releases)
[![License](https://img.shields.io/github/license/domnikl/ansible-unifi-network.svg)](https://github.com/domnikl/ansible-unifi-network/blob/main/LICENSE)

## Description

This collection provides Ansible modules for automating UniFi Network management tasks, including DNS policy management. It communicates directly with the UniFi Network controller through its Integration API, enabling Infrastructure as Code approaches for network configurations.

## Requirements

- **Ansible**: `>= 2.16.0`
- **Python**: `>= 3.9`
- **UniFi Network Controller**: Access to a UniFi Network controller with Integration API enabled
- **API Key**: Valid API key for the UniFi Network controller

### Python Dependencies

The collection requires the following Python packages:

```text
requests >= 2.25.0
certifi
```

## Installation

### From Git (Recommended)

Clone the repository directly to your Ansible collections path:

```bash
# Create collections directory if it doesn't exist
mkdir -p ~/.ansible/collections/ansible_collections/domnikl

# Clone the repository
git clone https://github.com/domnikl/ansible-unifi-network.git ~/.ansible/collections/ansible_collections/domnikl/unifi_network
```

### Build from Source

1. Clone the repository:
```bash
git clone https://github.com/domnikl/ansible-unifi-network.git
cd ansible-unifi-network
```

2. Build and install the collection:
```bash
ansible-galaxy collection build .
ansible-galaxy collection install domnikl-unifi_network-*.tar.gz
```

### Install Dependencies

After installing the collection, ensure the Python dependencies are available:

```bash
# System-wide installation
pip install requests certifi

# Or in a virtual environment
python -m venv ansible-env
source ansible-env/bin/activate  # On Windows: ansible-env\Scripts\activate
pip install requests certifi
```

## Quick Start

### Prerequisites

1. **UniFi Network Controller**: Ensure you have access to a UniFi Network controller
2. **API Key**: Generate an Integration API key in your UniFi Network controller:
   - Navigate to Settings → System → Integrations
   - Create a new Integration API key
   - Note the API key for use in your playbooks

### Basic Usage

Create a simple playbook to manage DNS policies:

```yaml
---
- name: Manage UniFi Network DNS Policies
  hosts: localhost
  gather_facts: false
  vars:
    unifi_controller: "your-controller.example.com"
    unifi_api_key: "{{ vault_unifi_api_key }}"  # Store securely with ansible-vault
    
  tasks:
    - name: Create A record for server
      domnikl.unifi_network.dns_policy:
        host: "{{ unifi_controller }}"
        api_key: "{{ unifi_api_key }}"
        site_name: "default"
        type: "A_RECORD"
        domain: "server.internal.example.com"
        ipv4_address: "192.168.1.100"
        ttl_seconds: 3600
        enabled: true
        state: present
        
    - name: Create CNAME record
      domnikl.unifi_network.dns_policy:
        host: "{{ unifi_controller }}"
        api_key: "{{ unifi_api_key }}"
        site_name: "default" 
        type: "CNAME_RECORD"
        domain: "app.internal.example.com"
        ipv4_address: "server.internal.example.com"
        state: present
        
    - name: Remove DNS policy
      domnikl.unifi_network.dns_policy:
        host: "{{ unifi_controller }}"
        api_key: "{{ unifi_api_key }}"
        site_name: "default"
        domain: "old-server.internal.example.com" 
        state: absent
```

### Secure API Key Management

Always store API keys securely using ansible-vault:

```bash
# Create encrypted variable file
ansible-vault create group_vars/all/vault.yml

# Add your API key
vault_unifi_api_key: "your-actual-api-key-here"
```

## Available Modules

### dns_policy

Manages DNS policies on UniFi Network controllers.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `host` | string | yes | | UniFi Network controller hostname/IP |
| `api_key` | string | yes | | Integration API key |
| `site_name` | string | no | "default" | Site name where policy should be managed |
| `verify_ssl` | boolean | no | `true` | Whether to verify SSL certificates |
| `type` | string | yes | | DNS record type (`A_RECORD`, `CNAME_RECORD`) |
| `domain` | string | yes | | Domain name for the DNS policy |
| `ipv4_address` | string | no | | IPv4 address or target domain |
| `ttl_seconds` | integer | no | `3600` | TTL in seconds |
| `enabled` | boolean | no | `true` | Whether the policy is enabled |
| `state` | string | no | "present" | Whether policy should exist (`present`, `absent`) |

**Examples:**

```yaml
# Create A record
- domnikl.unifi_network.dns_policy:
    host: controller.example.com
    api_key: "{{ unifi_api_key }}"
    type: A_RECORD
    domain: web.local
    ipv4_address: 192.168.1.10
    
# Create CNAME record
- domnikl.unifi_network.dns_policy:
    host: controller.example.com  
    api_key: "{{ unifi_api_key }}"
    type: CNAME_RECORD
    domain: www.local
    ipv4_address: web.local
    
# Delete DNS policy
- domnikl.unifi_network.dns_policy:
    host: controller.example.com
    api_key: "{{ unifi_api_key }}" 
    domain: old.local
    state: absent
```

## Testing

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/domnikl/ansible-unifi-network.git
cd ansible-unifi-network
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run tests:
```bash
# Syntax validation
ansible-test sanity --docker

# Unit tests (if available)
ansible-test units --docker
```

### Manual Testing

Create a test playbook and ensure you have:
- Access to a UniFi Network controller
- Valid API key
- Network connectivity to the controller

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'requests'**
```bash
# Install requests in your Python environment
pip install requests
```

**SSL Certificate Verification Errors** 
```yaml
# Disable SSL verification (not recommended for production)
- domnikl.unifi_network.dns_policy:
    verify_ssl: false
    # ... other parameters
```

**API Authentication Errors**
- Verify your API key is correct
- Ensure the API key has sufficient permissions
- Check that the Integration API is enabled on your controller

**Connection Timeout**
- Verify controller hostname/IP address
- Check network connectivity to the controller
- Ensure the controller is accessible on the network

### Debug Mode

Enable verbose output for troubleshooting:

```bash
ansible-playbook -vvv your-playbook.yml
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. **Code Style**: Follow Python PEP 8 and Ansible collection best practices
2. **Testing**: Add tests for new modules and features
3. **Documentation**: Update documentation for new features
4. **Commit Messages**: Use clear, descriptive commit messages

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`) 
5. Open a Pull Request

## License

This project is licensed under the GPL-3.0-or-later License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/domnikl/ansible-unifi-network/issues)
- **Documentation**: [Collection Documentation](https://github.com/domnikl/ansible-unifi-network)
- **Repository**: [GitHub Repository](https://github.com/domnikl/ansible-unifi-network)

---

**Author:** Dominik Liebler ([@domnikl](https://github.com/domnikl))
