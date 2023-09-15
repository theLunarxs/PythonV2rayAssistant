import json
import os


class UserInfo:
    def __init__(self, apikey, email, zoneid, save_dest, ippath):
        self.Save_Destination = save_dest
        self.ZoneID = zoneid
        self.IPPath = ippath
        self.EmailAddress = email
        self.apikey = apikey


class AppSettings:
    def __init__(self):
        self.locations = {
            "Credentials": os.path.join(os.getcwd(), "Credentials.json"),
            "Paths": os.path.join(os.getcwd(), "Paths.json")
        }

    def change_ips_location(self, new_ip_location: str):
        with open(self.locations['Paths'], "r+") as f:
            file = json.load(f)
        file['IPPath'] = new_ip_location.replace("'", "").replace('"', '')

        # Write the updated JSON data back to the file
        with open(self.locations['Paths'], 'w') as f:
            json.dump(file, f)

    def change_save_location(self, new_save_location):
        with open(self.locations['Paths']) as f:
            file = json.load(f)
        file['SaveLocation'] = new_save_location.replace("'", "").replace('"', '')

        # Write the updated JSON data back to the file
        with open(self.locations['Paths'], 'w') as f:
            json.dump(file, f)

    def change_credentials(self, credential: int, new_value: str):
        with open(self.locations['Credentials'], "r+") as f:
            file = json.load(f)
        if credential == 1:
            file['apikey'] = new_value
        elif credential == 2:
            file['EmailAddress'] = new_value
        elif credential == 3:
            file['ZoneID'] = new_value
        with open(self.locations['Credentials'], "w") as f:
            json.dump(file, f)

    def show_user_info(self):
        with open(self.locations["Credentials"], "r") as f:
            credentials = json.load(f)
        with open(self.locations["Paths"], "r") as f:
            paths = json.load(f)

        return UserInfo(credentials['apikey'], credentials['EmailAddress'], credentials['ZoneID']
                        , paths['SaveLocation'], paths['IPPath'])
