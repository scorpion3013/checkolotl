from typing import List, Any
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import time
import threading
from utils.values import settings, Proxies, registered_checkers
url = "http://api.ipify.org/"
def run():

    def add_to_working(proxy, proxytype, exitip="Unknown"):
        Proxies.checked_json[proxy] = {}
        Proxies.checked_json[proxy]["ip"] = proxy.split(":")[0]
        Proxies.checked_json[proxy]["port"] = proxy.split(":")[1]
        Proxies.checked_json[proxy]["type"] = proxytype
        Proxies.checked_json[proxy]["exitip"] = exitip.strip()
        Proxies.checked_json[proxy]["bans"] = {}
        for checker in registered_checkers:
            Proxies.checked_json[proxy]["bans"][checker] = False

    def check(number):
        ip = "Unknown"
        proxy = list(Proxies.raw_proxies)[number].strip()
        type = Proxies.raw_proxies[proxy]
        if type == "http":
            if not settings.proxies.check_http:
                Proxies.checked_counter += 1
                add_to_working(proxy=proxy, proxytype=type, exitip=ip)
                return
            proxy_dict = {
                'http': "http://" + proxy,
                'https': "https://" + proxy
            }
        elif type == "socks4":
            if not settings.proxies.check_socks4:
                Proxies.checked_counter += 1
                add_to_working(proxy=proxy, proxytype=type, exitip=ip)
                return
            proxy_dict = {
                'http': "socks4://" + proxy,
                'https': "socks4://" + proxy
            }
        elif type == "socks5":  # socks5
            if not settings.proxies.check_socks5:
                Proxies.checked_counter += 1
                add_to_working(proxy=proxy, proxytype=type, exitip=ip)
                return
            proxy_dict = {
                'http': "socks5://" + proxy,
                'https': "socks5://" + proxy
            }
        else:
            print("WTF")
            proxy_dict = {
                'http': "socks5://" + proxy,
                'https': "socks5://" + proxy
            }
        try:
            r = requests.get(url=url, timeout=float(settings.proxies.timeout), proxies=proxy_dict, stream=False)
            if len(r.text) > 20:
                raise Exception
        except Exception as e:
            pass
        else:
            add_to_working(proxy=proxy, proxytype=type, exitip=ip)
        finally:
            Proxies.checked_counter = Proxies.checked_counter + 1


    def thread_starter(numbers, threads=1):
        pool = ThreadPool(threads)
        results = pool.map(check, numbers)
        pool.close()
        pool.join()
        return results

    if __name__ == "checkers.proxies":
        running = True

        def status_thread_combos():
            time.sleep(1)
            while running:
                print(f"[Checker] Proxies: {Proxies.checked_counter}/{len(Proxies.raw_proxies)} Working: {len(Proxies.checked_json)}", end="\r")
                time.sleep(0.1)

        t1 = threading.Thread(target=status_thread_combos, args=[])
        t1.daemon = True
        t1.start()
        thread_number_list = []
        for x in range(0, len(Proxies.raw_proxies)):
            thread_number_list.append(int(x))
        the_focking_threads = thread_starter(thread_number_list, int(settings.proxies.threads))
        running = False
        time.sleep(1)
        print(f"[Checker] Proxies: {Proxies.checked_counter}/{len(Proxies.raw_proxies)} Working: {len(Proxies.checked_json)} " + u"\u2713")
        time.sleep(0.5)
