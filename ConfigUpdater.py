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
        self.vless_pattern = r'vless://(?P<user_id>[^@]+)@(?P<address>[^:]+):(?P<port>\d+)\?(?P<parameters>[^#]+)#(?P<config_name>[^#]+)'

    @staticmethod
    def split_the_ips(list_of_ips: list) -> list:
        return [ip.split(":")[0] if ":" in ip else ip for ip in list_of_ips]

    @staticmethod
    def detect_config_protocol(config_link: str) -> str:
        return "vmess" if config_link.lower().startswith("vmess") else "vless"

    @staticmethod
    def update_vmess_config(config: dict, ip: str) -> dict:
        config_copy = config.copy()
        config_copy['add'] = ip
        return config_copy

    def update_vless_config(self, config: Config, new_ip: str) -> str:
        match = re.match(self.vless_pattern, config.link)
        if match:
            user_id = match.group('user_id')
            port = match.group('port')
            parameters = match.group('parameters')
            config_name = match.group('config_name')

            new_config = f'vless://{user_id}@{new_ip}:{port}?{parameters}#{config_name}'
            return new_config
        else:
            raise ValueError("Invalid VLESS URL format")

    def write_config_to_disk(self, config: Config, encoded_configs: list):
        # Construct the file path
        output_file = os.path.join(self.SaveLocation, f"{config.configtype.capitalize()}final.txt").replace("\\", "/")

        # Ensure the directory exists, including any necessary parent directories
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the updated configurations to the respective output file
        with open(output_file, 'w') as f:
            for config_line in encoded_configs:
                f.write(config_line + '\n')

        print(f"Updated configurations saved to {output_file}")
        return True

    def update_config(self, configstr: str):
        try:
            with open(self.IPlocation.strip('"\''), "r+") as ipfile:
                ips = self.split_the_ips([line.strip() for line in ipfile])

            config = Config(configstr, self.detect_config_protocol(configstr))

            try:
                if config.configtype == "vmess":
                    config_bytes = base64.urlsafe_b64decode(config.link.split('//', 1)[1] + '=' * 3)
                    config_json = config_bytes.decode('utf-8')
                    decoded_config = json.loads(config_json)
                    updated_configs = [self.update_vmess_config(decoded_config, ip) for ip in ips]
                    encoded_configs = [
                        f'vmess://{base64.urlsafe_b64encode(json.dumps(updated_config).encode()).decode().rstrip("=")}'
                        for updated_config in updated_configs]
                elif config.configtype == "vless":
                    updated_configs = [self.update_vless_config(config, ip) for ip in ips]
                    encoded_configs = [f'{updated_config}' for updated_config in updated_configs]
                else:
                    raise ValueError("Invalid config type")
            except Exception as config_error:
                print(f"Error updating config: {str(config_error)}")
                raise  # Reraise the exception to stop the process

            try:
                self.write_config_to_disk(config, encoded_configs)
            except Exception as write_error:
                print(f"Error writing config to disk: {str(write_error)}")

        except Exception as outer_error:
            print(f"Error during the update process: {str(outer_error)}")
# Example usage:
# updater = ConfigUpdater(ips_location='your_ips.txt', save_location='output_folder')
# updater.update_config('your_config_link_here')
