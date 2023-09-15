import json
from cloudflare import CloudflareDNSManager
from ConfigUpdater import ConfigUpdater
from AppSettings import AppSettings
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
        "IPPath": path_to_ips.replace("'", "").replace('"', '')
    }
    with open(ip_file_path, "w") as file:
        json.dump(content, file)
    return path_to_ips


def get_save_location(save_file_path):
    path_to_save = input("Where do you want the Results to be saved at?Enter full Directory\n   e.g:D:/IPs\n ").strip()
    print("You can change This Address in Paths.json")
    with open(save_file_path, "r+") as file:
        content = json.load(file)
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    content["SaveLocation"] = path_to_save.replace("'", "").replace('"', '')
    with open(save_file_path, "w") as file:
        json.dump(content, file)
    return path_to_save


def split_the_i_ps(listofip):
    output = []
    for ip in listofip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


processDone = False
wehavedata = (os.path.isfile(os.path.join(os.getcwd(), 'Credentials.json')) and
              os.path.isfile(os.path.join(os.getcwd(), 'Paths.json')))
while not processDone:
    choice = input(f"What do you want to do? \n    1_ Update V2ray Config\n    2_ Change Cloudflare DNS Record IP\n" +
                   f"{'    3_ Manage Settings' if wehavedata else ''}\n"
                   +
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

    elif choice == "2":
        cf_manager = CloudflareDNSManager()
        cf_manager.load_credentials()
        cf_manager.load_dns_records()
        cf_manager.display_dns_records()
        cf_manager.choose_dns_record()
        cf_manager.change_dns_record_ip()

    elif choice == "3":
        settings = AppSettings()

    else:
        print("Please Enter Valid Input")
