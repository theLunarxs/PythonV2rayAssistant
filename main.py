import json
from cloudflare import CloudflareDNSManager
from ConfigUpdater import ConfigUpdater
import os


def ip_list_loader(ip_file_path):
    with open(ip_file_path, "r+") as file:
        user_data = json.load(file)
    return user_data.get("IPPath") if "IPPath" in user_data else get_ip_path(ip_file_path)


def destination_path_loader(dest_file_path):
    with open(dest_file_path, "r+") as file:
        user_data = json.load(file)
    path_to_save = user_data.get("SaveLocation") if "SaveLocation" in user_data else get_save_location(dest_file_path)
    return path_to_save


def get_ip_path(ip_file_path):
    path_to_ips = input("Where is the IP file? Enter full directory \n   e.g:D:/IPs/IPList.txt\n ").strip()
    print("You can change This Address in Paths.json")
    content = {
        "IPPath": path_to_ips
    }
    with open(ip_file_path, "w") as file:
        json.dump(content, file)
    return path_to_ips


def get_save_location(file_path):
    path_to_save = input("Where do you want the Results to be saved at?Enter full Directory\n   e.g:D:/IPs\n ").strip()
    print("You can change This Address in Paths.json")
    with open(file_path, "r+") as file:
        content = json.load(file)
    content["SaveLocation"] = path_to_save
    with open(file_path, "w") as file:
        json.dump(content, file)
    return path_to_save


def split_the_i_ps(listofip):
    output = []
    for ip in listofip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


processDone = False

while not processDone:
    choice = input("What do you intend to do? \n    1_ Update V2ray Config\n    2_Change Cloudflare DNS Record IP\n"
                   "    Enter Here: ").strip()

    if choice == "1":
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "Paths.json")

        if not os.path.isfile(file_path):
            get_ip_path(file_path)
            get_save_location(file_path)

        ips = ip_list_loader(file_path)
        destination_path = destination_path_loader(file_path)

        config = input("Please Enter Your Vmess/Vless Config:\n ").strip()
        configUpdater = ConfigUpdater(ips, destination_path)
        configUpdater.update_config(config)
        processDone = True

    elif choice == "2":
        cf_manager = CloudflareDNSManager()
        cf_manager.load_credentials()
        cf_manager.load_dns_records()
        cf_manager.display_dns_records()
        cf_manager.choose_dns_record()
        cf_manager.change_dns_record_ip()
        processDone = True
