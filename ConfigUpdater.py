import json
import base64
import re


class V2RayConfigUpdater:

    def __init__(self, ip_addresses):
        self.ip_addresses = ip_addresses

    def detect_config(self, config):
        if config.startswith('vmess://'):
            return 'vmess'
        elif config.startswith('vless://'):
            return 'vless'
        else:
            raise ValueError('Unknown config type')

    def update_vmess(self, config):
        updated_configs = [self.update_vmess_address(config, ip) for ip in self.ip_addresses]
        encoded_configs = [self.encode_vmess(c) for c in updated_configs]
        return encoded_configs

    def update_vmess_address(self, config, ip):
        config['add'] = ip
        return config

    def encode_vmess(self, config):
        data = json.dumps(config).encode()
        encoded = base64.urlsafe_b64encode(data).decode().rstrip('=')
        return f'vmess://{encoded}'

    def update_vless(self, config):
        updated_configs = [self.update_vless_address(config, ip) for ip in self.ip_addresses]
        encoded_configs = [self.format_vless(c) for c in updated_configs]
        return encoded_configs

    def update_vless_address(self, config, ip):
        pattern = r'^(vless://)?([\w-]+)@([\d.]+):(\d+)\?([^#]*)#(.*)$'
        match = re.search(pattern, config)
        if match:
            # Extract components
            prefix = match.group(1) if match.group(1) else ''
            username = match.group(2)
            port = match.group(4)
            params = match.group(5)
            fragment = match.group(6)

            return f'{prefix}{username}@{ip}:{port}?{params}#{fragment}'
        else:
            raise ValueError('Invalid VLESS config format')

    def format_vless(self, config):
        if config.startswith('vless://'):
            return config
        else:
            return f'vless://{config}'

    def update_configs(self, configs):
        updated = []

        for config in configs:
            config_type = self.detect_config(config)

            if config_type == 'vmess':
                updated.append(self.update_vmess(config))
            elif config_type == 'vless':
                updated.append(self.update_vless(config))

        return updated
