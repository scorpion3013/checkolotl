from checkolotl.settings import settings
import threading
import os
import time


def timeouter():
    timer = 0
    while True:
        time.sleep(1)
        timer = timer + 1
        if timer >= settings.checker_general.timeout * 60:
            os._exit(0)


def start():
    t = threading.Thread(target=timeouter, args=[])
    t.daemon = True
    t.start()
