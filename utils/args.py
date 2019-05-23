import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--combos", help="changes the combo file", type=str, default="combos.txt")
parser.add_argument("--proxieshttp", help="changes the http proxy file", type=str, default="proxies_http.txt")
parser.add_argument("--proxiessocks4", help="changes the socks4 proxy file", type=str, default="proxies_socks4.txt")
parser.add_argument("--proxiessocks5", help="changes the socks5 proxy file", type=str, default="proxies_socks5.txt")
parser.add_argument("--config", help="changes the config", type=str, default="config.yml")

arguments = parser.parse_args()
