import yaml
import sys
from utils.args import arguments
class paths:
    combos = arguments.combos
    http = arguments.proxieshttp
    socks4 = arguments.proxiessocks4
    socks5 = arguments.proxiessocks5
    config = arguments.config

config = yaml.load(open(paths.config, 'r', encoding="utf8", errors='ignore'), Loader=yaml.Loader)

registered_checkers = []

class settings:
    for key in config.keys():
        if key != "proxies" and key != "general" and config[key]["enabled"]:
            registered_checkers.append(key)
        class A(object):
            pass
        locals()[key] = A()
        for underkey in config[key]:
            setattr(locals()[key], underkey, config[key][underkey])




class Proxies:
    raw_proxies = {}
    checked_counter = 0
    if settings.proxies.use_http:
        try:
            http_raw = [x.strip() for x in open(paths.http, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]
            http_raw = list(dict.fromkeys(http_raw))
            for proxy in http_raw:
                raw_proxies[proxy] = "http"
        except:
            http_raw = []
            print("You had http proxies enabled, but I could not load them!")
        print(f"Loaded {len(http_raw)} http proxies.")
    else:
        http_raw = []
    if settings.proxies.use_socks4:
        try:
            socks4_raw = [x.strip() for x in open(paths.socks4, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]
            socks4_raw = list(dict.fromkeys(socks4_raw))
            for proxy in socks4_raw:
                raw_proxies[proxy] = "socks4"
        except:
            socks4_raw = []
            print("You had socks4 proxies enabled, but I could not load them!")
        print(f"Loaded {len(socks4_raw)} socks4 proxies.")
    else:
        socks4_raw = []
    if settings.proxies.use_socks5:
        try:
            socks5_raw = [x.strip() for x in open(paths.socks5, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]
            socks5_raw = list(dict.fromkeys(socks5_raw))
            for proxy in socks5_raw:
                raw_proxies[proxy] = "socks5"
        except:
            socks5_raw = []
            print("You had socks5 proxies enabled, but I could not load them!")
        print(f"Loaded {len(socks5_raw)} socks5 proxies.")
    else:
        socks5_raw = []

    checked_json = {}


class accounts:
    combos = [x.strip() for x in open(paths.combos, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]
    combos = list(dict.fromkeys(combos))
    if len(combos) == 0:
        print("Error: 0 Combos loaded")
        sys.exit()
    else:
        print(f"Loaded {len(combos)} combos.")
    for checker in registered_checkers:
        locals()["valid_" + checker] = []
        locals()["invalid_" + checker] = []
