from checkolotl.values import proxies
from checkolotl.settings import settings, toggled_checkers
from checkolotl.status import create_bar

import re
import requests
from multiprocessing.dummy import Pool as ThreadPool


def start():
    status_bar = create_bar(len(proxies.raw), "Proxies", "Working: 0")

    def check(proxy):
        if settings.proxies_checker.skipCheck:
            for checker in toggled_checkers:
                proxies.results[checker][proxy] = {
                    "outgoing_ip": "127.0.0.1"
                }
            proxies.working_count += 1
            status_bar.set_postfix_str("Working: " + str(proxies.working_count))
        else:
            try:
                r = requests.get(url=settings.proxies_checker.judge_url, proxies={
                    "http": proxy,
                    "https": proxy
                }, timeout=settings.proxies_checker.timeout)
                if r.status_code == 200:
                    for checker in toggled_checkers:
                        proxies.results[checker][proxy] = {
                                "outgoing_ip": re.findall(settings.proxies_checker.ip_regex, r.text)[0]
                        }
                    proxies.working_count += 1
                    status_bar.set_postfix_str("Working: " + str(proxies.working_count))
            except Exception as e:
                pass

        status_bar.update(1)
        status_bar.refresh()

    pool = ThreadPool(settings.proxies_checker.threads)
    pool.map(check, proxies.raw)
    pool.close()
    pool.join()
    status_bar.close()
