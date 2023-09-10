import base64
import json
import re


def Split_The_IPs(listofip):
    output = []
    for ip in listofip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


def update_vmess_address(config, ip):
    config_copy = config.copy()
    config_copy['add'] = ip
    return config_copy


def update_vless_address(vless_config, new_ip):
    # Define a regular expression pattern to match the VLESS URL structure
    vless_pattern = r'^(vless://)?([\w-]+)@([\d.]+):(\d+)\?([^#]*)#(.*)$'

    # Use re.search to find the VLESS URL components
    match = re.search(vless_pattern, vless_config)

    if match:
        prefix = match.group(1) if match.group(1) else ''
        username = match.group(2)
        port = match.group(4)
        fragment_identifier = match.group(6)

        new_config = f'{prefix}{username}@{new_ip}:{port}?{fragment_identifier}'
        return new_config
    else:
        print("Invalid VLESS URL format")
        return vless_config


def update_configs(config_str, ips):
    if config_str.startswith('vmess://'):
        config_bytes = base64.urlsafe_b64decode(config_str.split('//', 1)[1] + '=' * 3)
        config_json = config_bytes.decode('utf-8')
        config = json.loads(config_json)
        updated_configs = [update_vmess_address(config, ip) for ip in ips]
        encoded_configs = [
            f'vmess://{base64.urlsafe_b64encode(json.dumps(updated_config).encode()).decode().rstrip("=")}'
            for updated_config in updated_configs]
        output_file = 'D:/v2rayfolder/Vmessfinals.txt'

    elif config_str.startswith('vless://'):
        query_and_fragment = config_str.split('?', 1)[1]
        updated_configs = [update_vless_address(config_str, ip) for ip in ips]

        # Check if the prefix is already present and add it accordingly
        encoded_configs = [f'{updated_config}?{query_and_fragment}' if updated_config.startswith('vless://') else
                           f'vless://{updated_config}?{query_and_fragment}' for updated_config in updated_configs]

        output_file = 'D:/v2rayfolder/Vlessfinals.txt'
    else:
        print("Unsupported configuration type")
        return

    # Write the updated configurations to the respective output file
    with open(output_file, 'w') as f:
        for config in encoded_configs:
            f.write(config + '\n')

    print(f"Updated configurations saved to {output_file}")


# Read the IP addresses from the file
with open('D:/v2rayfolder/ips.txt', 'r') as f:
    ips = Split_The_IPs([line.strip() for line in f])

# Decode the configuration string
config_str = input("Enter Config: ")

# Call the function to update and save configurations
update_configs(config_str, ips)
