import base64
import json


def Split_The_IPs(listofip):
    output = []
    for ip in listofip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


# Read the IP addresses from the file
with open('D:/ips.txt', 'r') as f:
    ips = Split_The_IPs([line.strip() for line in f])

# ips = ['104.16.209.44', '104.16.242.31', '104.16.224.70', '104.19.179.61', '104.16.26.64', '104.17.216.74',
# '104.16.47.47', '104.16.129.85', '104.16.221.100', '104.18.43.83', '104.18.47.178', '104.18.247.86',
# '104.17.65.246', '104.17.199.54', '104.17.234.87', '104.17.234.165', '104.19.14.211'] Decode the configuration string
config_str = input("Enter Config: ")
config_bytes = base64.urlsafe_b64decode(config_str.split('//', 1)[1] + '=' * 3)

# Decode the original configuration
config_json = config_bytes.decode('utf-8')

# Parse the original configuration JSON
config = json.loads(config_json)

# Update the "add" field with each IP address in the file
configs = []
for ip in ips:
    # Make a copy of the configuration for each IP address
    config_copy = config.copy()

    # Update the "add" field with the IP address
    config_copy['add'] = ip

    # Encode the updated configuration to base64 and append to the list of configs
    config_json = json.dumps(config_copy)
    config_bytes = config_json.encode('utf-8')
    encoded_config = base64.urlsafe_b64encode(config_bytes).decode().rstrip('=')
    # res = base64.b64encode(f'vmess://{encoded_config}'.encode()).decode()
    configs.append(f'vmess://{encoded_config}')

# Write the updated configurations to file
with open('D:/jvb.txt', 'w') as f:
    for config in configs:
        f.write(config + '\n')
