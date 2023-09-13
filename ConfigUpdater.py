import base64
import json
import os.path
import re


class Config:
    def __init__(self, link, configtype):
        self.link: str = link
        self.configtype: str = configtype


class ConfigUpdater:
    def __init__(self, ips_location: str, save_location: str):
        self.IPlocation = ips_location
        self.SaveLocation = save_location
        self.vless_pattern = r'^(vless://)?([\w-]+)@([\d.]+):(\d+)\?([^#]*)#(.*)$'

    @staticmethod
    def split_the_ips(list_of_ips: list) -> list:
        return [ip.split(":")[0] for ip in list_of_ips if ":" in ip]

    @staticmethod
    def detect_config_protocol(config_link: str) -> str:
        return "vmess" if config_link.lower().startswith("vmess") else "vless"

    @staticmethod
    def update_vmess_config(config: dict, ip: str) -> dict:
        config_copy = config.copy()
        config_copy['add'] = ip
        return config_copy

    def update_vless_config(self, config: Config, new_ip: str) -> str:
        match = re.search(self.vless_pattern, config.link)
        if match:
            prefix = match.group(1) if match.group(1) else ''
            username = match.group(2)
            port = match.group(4)
            fragment_identifier = match.group(6)

            new_config = f'{prefix}{username}@{new_ip}:{port}?{fragment_identifier}'
            return new_config
        else:
            raise ValueError("Invalid VLESS URL format")

    def write_config_to_disk(self, config: Config, encoded_configs: list):
        output_file = os.path.join(self.SaveLocation, f"{config.configtype.capitalize()}final.txt")
        # Write the updated configurations to the respective output file
        with open(output_file, 'w') as f:
            for config in encoded_configs:
                f.write(config + '\n')
        print(f"Updated configurations saved to {output_file}")
        return True

    def update_config(self, configstr: str):
        with open(self.IPlocation.strip('"\''), "r+") as ipfile:
            ips = self.split_the_ips([line.strip() for line in ipfile])

        config = Config(configstr, self.detect_config_protocol(configstr))

        if config.configtype == "vmess":
            config_bytes = base64.urlsafe_b64decode(config.link.split('//', 1)[1] + '=' * 3)
            config_json = config_bytes.decode('utf-8')
            decoded_config = json.loads(config_json)
            updated_configs = [self.update_vmess_config(decoded_config, ip) for ip in ips]
            encoded_configs = [
                f'vmess://{base64.urlsafe_b64encode(json.dumps(updated_config).encode()).decode().rstrip("=")}'
                for updated_config in updated_configs]

        elif config.configtype == "vless":
            query_and_fragment = config.link.split('?', 1)[1]
            updated_configs = [self.update_vless_config(config, ip) for ip in ips]

            # Check if the prefix is already present and add it accordingly
            encoded_configs = [
                f'{updated_config}?{query_and_fragment}' if updated_config.startswith('vless://') else
                f'vless://{updated_config}?{query_and_fragment}' for updated_config in updated_configs]

        else:
            raise ValueError("Value Not Assessed")

        self.write_config_to_disk(config, encoded_configs)
