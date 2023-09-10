import json
import re
import requests
import os


class DNSRecord:
    def __init__(self, RecordId, content, name, recordtype):
        self.id = RecordId
        self.content = content
        self.name = name
        self.type = recordtype


def ip_validator(ip):
    return bool(re.match(ipv4_pattern, ip))


# Pattern to Validate IPV4 IP Address
ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

# Check Whether we have User's API Address or other stuff or not
current_directory = os.getcwd()
file_path = os.path.join(current_directory, "Credentials.json")

# If no Data is present, we ask the user about their data.
if not os.path.isfile(file_path):
    apikey = input("Enter API Key: ").strip()
    EmailAddress = input("Enter your Email Address: ").strip()
    ZoneID = input("Enter ZoneID: ").strip()
    UserCredentials = {
        "apikey": f"{apikey}",
        "EmailAddress": f"{EmailAddress}",
        "ZoneID": f"{ZoneID}",
    }
    # We write their data to the disk
    with open(file_path, "w") as file:
        json.dump(UserCredentials, file_path)

# Data is loaded
UserData = json.load(file_path)

# Each Variable is read from disk and prepared to be used
apikey = UserData["apikey"]
EmailAddress = UserData["EmailAddress"]
ZoneID = UserData["ZoneID"]

geturl = f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records"
PatchURL = f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/"

header = {
    "Content-Type": "application/json",
    "X-Auth-Email": EmailAddress,
    "X-Auth-Key": apikey
}
dns_records = []
# We Get the List of User's Records from Cloudflare GET Endpoint
apiget = requests.get(geturl, headers=header).text
api_data = json.loads(apiget)["result"]

# We make DNSRecord Objects from the data received based on the info we need
for record in api_data:
    record_id = record["id"]
    content = record["content"]
    name = record["name"]
    recordtype = record["type"]

    # Create new DNS Record Object
    dns_record = DNSRecord(record_id, content, name, recordtype)
    dns_records.append(dns_record)

counter = 1
print("Here's a List of your DNS Records:")
# Displaying User's DNS Records
for record in dns_records:
    print(f"    {counter}_ name: {record.name} \n       Current IP Address: {record.content} \n "
          f"            -----------------")
    counter += 1
# Asking user which Record He ( Yes I'm misogynistic, women can't do stuff like this) wants to change.
RecordToChangeIndex = int(input("Enter the Number(Index) of the Record you wish to change, e.g: '1': \n")) - 1
RecordToChange = dns_records[RecordToChangeIndex]

ip_received = False

while not ip_received:
    new_ip = input("Enter the new IP Address: ").strip()

    if ip_validator(new_ip):
        print(f"Valid IPv4 address received: {new_ip}\n")
        ip_received = True
    else:
        print(f"Invalid IPv4 address format. Please try again.")

new_info = {
    "content": f"{new_ip}",
    "name": f"{RecordToChange.name}",
    "type": f"{RecordToChange.type}",
}
# Sending PATCH request to cloudflare to change DNS Record's Info
response = requests.request("PATCH", f"{PatchURL + RecordToChange.id}"
                            , json=new_info, headers=header)

if response.status_code == 200:
    print(f"**DNS Record {RecordToChange.name}'s IP Changed to {new_ip} Successfully **")
else:
    print(response.text)
