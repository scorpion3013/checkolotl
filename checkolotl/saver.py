import sys

from checkolotl.values import combos, other
from checkolotl.settings import settings
import threading
import time
import os
from pathlib import Path


def save(checker, account):
    combos.results[checker].append(account)
    other.saver_queue.put([checker, account])
    if settings.checker_general.print_hits:
        other.status_bar.write(f"[{checker}] {account}")


def saver():
    if getattr(sys, 'frozen', False):
        save_path = str(Path(os.path.dirname(sys.executable)))
    else:
        save_path = str(os.path.dirname(os.path.abspath(Path(__file__).parent)))
    replace_dict = {
        "current": save_path,
        "unix": str(int(time.mktime(other.start_time.timetuple())))
    }
    path = str(settings.checker_general.path).format(**replace_dict)
    path = other.start_time.strftime(path)
    settings.paths.save = path
    if not os.path.exists(path):
        os.makedirs(path)
    while True:
        if other.finished and other.saver_queue.empty():
            break
        elif not other.saver_queue.empty():
            checker, account = other.saver_queue.get()
            replace_dict = {
                "checkername": str(checker),
                "unix": str(int(time.mktime(other.start_time.timetuple())))
            }

            output_format = str(settings.checkers.minecraft.outputname).format(**replace_dict)
            with open(f"{path}/{output_format}", "a") as file:
                file.write(f"{account}\n")
                file.close()
    print("Finished checking")


def start():
    t = threading.Thread(target=saver, args=[])
    t.daemon = False
    t.start()
