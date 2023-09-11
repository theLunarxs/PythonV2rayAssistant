import json
from cloudflare import CloudflareDNSManager
from ConfigUpdater import V2RayConfigUpdater
import os


def IPListLoader(file_path):
    ips = []
    with open(file_path, "r+") as file:
        user_data = json.load(file)
    path_to_ips = user_data.get("IPPath") if "IPPath" in user_data else GetIPPath(file_path)
    with open(path_to_ips, "r+") as IPFile:
        ips.append(Split_The_IPs([line.strip() for line in IPFile]))
    return ips


def DestinationPathLoader(file_path):
    with open(file_path, "r+") as file:
        user_data = json.load(file)
    path_to_save = user_data.get("SaveLocation") if "SaveLocation" in user_data else GetSaveLocation(file_path)
    return path_to_save


def GetIPPath(file_path):
    path_to_ips = input("Where is the IP file?Enter full directory \n   e.g:D:/IPs/IPList.txt\n ")
    print("You can change This Address in Paths.json")
    content = {
        "IPPath": path_to_ips
    }
    with open(file_path, "w") as file:
        json.dump(content, file)
    return path_to_ips


def GetSaveLocation(file_path):
    path_to_save = input("Where do you want the Results to be saved at?Enter full Directory\n   e.g:D:/IPs\n ")
    print("You can change This Address in Paths.json")
    with open(file_path, "r+") as file:
        content = json.load(file)
    content["SaveLocation"] = path_to_save
    with open(file_path, "w") as file:
        json.dump(content, file)
    return path_to_save


def Split_The_IPs(listofip):
    output = []
    for ip in listofip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


choice = input("What do you intend to do? \n    1_ Update V2ray Config\n    2_Change Cloudflare DNS Record IP\n"
               "    Enter Here: ")
processDone = False
while not processDone:
    if choice == "1":
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "Paths.json")
        if not os.path.isfile(file_path):
            GetIPPath(file_path)
            GetSaveLocation(file_path)
        ips = IPListLoader(file_path)
        dest = DestinationPathLoader(file_path)
        configUpdater = V2RayConfigUpdater(ips)
        config = input("Please Enter Your Vmess/Vless Config:\n ")
        updatedconfigs = configUpdater.update_configs([config])
        with open(dest + "result.txt", "w") as file:
            for updated_config in updatedconfigs:
                file.write("\n".join(updated_config))
        processDone = True

    elif choice == "2":
        cf_manager = CloudflareDNSManager()
        cf_manager.load_credentials()
        cf_manager.load_dns_records()
        cf_manager.display_dns_records()
        cf_manager.choose_dns_record()
        cf_manager.change_dns_record_ip()
        processDone = True
