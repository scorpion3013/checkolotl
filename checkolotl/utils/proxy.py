from checkolotl.values import proxies
import random


def get_proxy(checker):
    return random.choice(list(proxies.results[checker].keys()))


def remove_proxy(checker, proxy):
    proxies.results[checker].pop(proxy, None)
