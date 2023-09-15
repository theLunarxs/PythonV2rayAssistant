import json
from cloudflare import CloudflareDNSManager
from ConfigUpdater import ConfigUpdater
from AppSettings import AppSettings
import os


def ip_list_loader(ip_file_path):
    with open(ip_file_path, "r+") as file:
        user_data = json.load(file)
    return user_data.get("IPPath") if "IPPath" in user_data else get_ip_path(ip_file_path)


def destination_path_loader(destination_file_path):
    with open(destination_file_path, "r+") as file:
        user_data = json.load(file)
    path_to_save = user_data.get("SaveLocation") if "SaveLocation" in user_data else get_save_location(destination_file_path)
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


def split_the_i_ps(list_of_ip):
    output = []
    for ip in list_of_ip:
        if ":" in ip:
            output.append(ip.split(":")[0])
    return output


processDone = False
while not processDone:
    we_have_data = (os.path.isfile(os.path.join(os.getcwd(), 'Credentials.json')) and
                    os.path.isfile(os.path.join(os.getcwd(), 'Paths.json')))

    choice = input(f"What do you want to do? \n    1_ Update V2ray Config\n    2_ Change Cloudflare DNS Record IP\n" +
                   f"{'    3_ Manage Settings' if we_have_data else ''}\n"
                   f"{'    4_ Show your Info' if we_have_data else ''}\n"
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
        setting_choice = input("what changes do you want to make?\n"
                               "    1_ Change IPFile Location\n"
                               "    2_ Change Save Destination Location\n"
                               "    3_ Change Credentials(API Key, Email Address,Zone ID)\n"
                               "    Enter Here: ")

        if setting_choice == "1" or setting_choice == "2":
            new_location = input("Please Enter New Location as Directory path\n"
                                 "Enter Here: ")
            if setting_choice == "1":
                settings.change_ips_location(new_location)

            elif setting_choice == "2":
                settings.change_save_location(new_location)

        elif setting_choice == "3":
            credential_choice = input("What Do you want to change?\n"
                                      "     1_ API Key\n"
                                      "     2_ Email Address\n"
                                      "     3_ Zone ID\n"
                                      " Enter Here: ")
            new_value = input("Enter the new value: ")
            settings.change_credentials(int(credential_choice), new_value)
        print("Value Changed Successfully")
    elif choice == "4":
        settings = AppSettings()
        user_info = settings.show_user_info()
        print("Your Info looks like this:\n"
              f"IP File Path: {user_info.IPPath}\n"
              f"Save Destination: {user_info.Save_Destination}\n"
              f"API Key: {user_info.apikey}\n"
              f"Zone ID: {user_info.ZoneID}\n"
              f"Email Address: {user_info.EmailAddress}\n")
    else:
        print("Please Enter Valid Input")
