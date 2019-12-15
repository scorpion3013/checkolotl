from checkolotl.settings import settings, toggled_checkers
from datetime import datetime
import queue


class proxies:
    if settings.checker_general.remove_duplicate_proxies:
        raw = list(set([x.strip() for x in open(settings.paths.proxies, "r", encoding="utf8", errors='ignore').readlines() if
               ":" in x]))
    else:
        raw = [x.strip() for x in open(settings.paths.proxies, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]

    working_count = 0
    results = {}
    for checker in toggled_checkers:
        results[checker] = {}


class combos:
    if settings.checker_general.remove_duplicate_combos:
        raw = list(set([x.strip() for x in open(settings.paths.combos, "r", encoding="utf8", errors='ignore').readlines() if
               ":" in x]))
    else:
        raw = [x.strip() for x in open(settings.paths.combos, "r", encoding="utf8", errors='ignore').readlines() if ":" in x]
    results = {}
    for checker in toggled_checkers:
        results[checker] = []


class other:
    status_bar = None
    finished = False
    saver_queue = queue.Queue()
    start_time = datetime.now()
    end_time = None
