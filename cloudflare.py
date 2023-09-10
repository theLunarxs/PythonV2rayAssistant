import requests

# Fixed Datas
apikey = "49a5063c989190bb5381d7a06354944e7f54c"
EmailAddress = "aryanesmailiea@gmail.com"
zoneid = "54329bed49dbb8f5d56ee404eafea29c"
geturl = f"https://api.cloudflare.com/client/v4/zones/{zoneid}/dns_records"
patchurl = f"https://api.cloudflare.com/client/v4/zones/{zoneid}/dns_records/"

# Dynamic Datas
DNS_record_ID = "70eedf1213e637488d52a487bdd3cc0d"
new_ip = "185.220.204.225"


header = {
    "Content-Type": "application/json",
    "X-Auth-Email": EmailAddress,
    "X-Auth-Key": apikey
}

new_info = {
    "content": f"{new_ip}",
    "name": "escp.pexita.store",
    "type": "A",
}

response = requests.request("PATCH", f"{patchurl + DNS_record_ID}"
                            , json=new_info, headers=header)
print(response.text)

