import json
import re
import requests
import os


class CloudflareDNSManager:
    def __init__(self):
        self.apikey = None
        self.EmailAddress = None
        self.ZoneID = None
        self.header = None
        self.dns_records = []
        self.RecordToChange = None

    @staticmethod
    def ip_validator(ip):
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        return bool(re.match(ipv4_pattern, ip))

    def load_credentials(self):
        # Load user credentials from the "Credentials.json" file
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "Credentials.json")

        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                user_data = json.load(file)

            self.apikey = user_data.get("apikey")
            self.EmailAddress = user_data.get("EmailAddress")
            self.ZoneID = user_data.get("ZoneID")
        else:
            # If the file doesn't exist, ask the user for the data
            self.apikey = input("Enter API Key: ").strip()
            self.EmailAddress = input("Enter your Email Address: ").strip()
            self.ZoneID = input("Enter ZoneID: ").strip()

            UserCredentials = {
                "apikey": f"{self.apikey}",
                "EmailAddress": f"{self.EmailAddress}",
                "ZoneID": f"{self.ZoneID}",
            }

            # Write the user's data to the "Credentials.json" file
            with open(file_path, "w") as file:
                json.dump(UserCredentials, file)

    def load_dns_records(self):
        # Load DNS records from Cloudflare API
        geturl = f"https://api.cloudflare.com/client/v4/zones/{self.ZoneID}/dns_records"
        self.header = {
            "Content-Type": "application/json",
            "X-Auth-Email": self.EmailAddress,
            "X-Auth-Key": self.apikey
        }

        apiget = requests.get(geturl, headers=self.header).text
        api_data = json.loads(apiget)["result"]

        for record in api_data:
            record_id = record["id"]
            content = record["content"]
            name = record["name"]
            recordtype = record["type"]

            self.dns_records.append(DNSRecord(record_id, content, name, recordtype))

    def display_dns_records(self):
        # Display DNS records
        counter = 1
        print("Here's a List of your DNS Records:")
        for record in self.dns_records:
            print(f"    {counter}_ name: {record.name} \n       Current IP Address: {record.content} \n "
                  f"            -----------------")
            counter += 1

    def choose_dns_record(self):
        # Choose a DNS record to change
        RecordToChangeIndex = int(input("Enter the Number(Index) of the Record you wish to change, e.g: '1': \n")) - 1
        self.RecordToChange = self.dns_records[RecordToChangeIndex]

    def change_dns_record_ip(self):
        ip_received = False
        while not ip_received:
            new_ip = input("Enter the new IP Address: ").strip()
            if self.ip_validator(new_ip):
                print(f"Valid IPv4 address received: {new_ip}\n")
                ip_received = True
            else:
                print(f"Invalid IPv4 address format. Please try again.")

        new_info = {
            "content": f"{new_ip}",
            "name": f"{self.RecordToChange.name}",
            "type": f"{self.RecordToChange.type}",
        }

        PatchURL = f"https://api.cloudflare.com/client/v4/zones/{self.ZoneID}/dns_records/{self.RecordToChange.id}"
        response = requests.request("PATCH", PatchURL, json=new_info, headers=self.header)

        if response.status_code == 200:
            print(f"**DNS Record {self.RecordToChange.name}'s IP Changed to {new_ip} Successfully **")
        else:
            print(response.text)


class DNSRecord:
    def __init__(self, RecordId, content, name, recordtype):
        self.id = RecordId
        self.content = content
        self.name = name
        self.type = recordtype


if __name__ == "__main__":
    # Create an instance of CloudflareDNSManager
    cf_dns_manager = CloudflareDNSManager()

    # Load user credentials from "Credentials.json"
    cf_dns_manager.load_credentials()

    # Load DNS records from Cloudflare API
    cf_dns_manager.load_dns_records()

    # Display DNS records
    cf_dns_manager.display_dns_records()

    # Choose a DNS record to change
    cf_dns_manager.choose_dns_record()

    # Change DNS record IP
    cf_dns_manager.change_dns_record_ip()
