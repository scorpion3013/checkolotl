from utils.values import Proxies
import random

def proxy_getter(checker_name="Unknown.Unknown"):
    checker_name = str(checker_name).split(".")[1]
    while True:
        proxy = str(random.choice(list(Proxies.checked_json))).strip()
        type = Proxies.checked_json[proxy]["type"]
        bans = Proxies.checked_json[proxy]["bans"]
        if checker_name == "Unknown" or not bans[checker_name]:
            break
    if type == "http":
        proxy_dict = {
            'http': "http://" + proxy,
            'https': "https://" + proxy
        }
    elif type == "socks4":
        proxy_dict = {
            'http': "socks4://" + proxy,
            'https': "socks4://" + proxy
        }
    elif type == "socks5":  # socks5
        proxy_dict = {
            'http': "socks5://" + proxy,
            'https': "socks5://" + proxy
        }
    else:
        print("WTF")
        proxy_dict = {
            'http': "http://" + proxy,
            'https': "https://" + proxy
        }
    return [proxy, proxy_dict]