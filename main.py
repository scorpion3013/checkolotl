#! /bin/python
import importlib
import random
import string
import time
from multiprocessing.dummy import Pool as ThreadPool
import threading
import sys
import os
import inspect
from reprint import output
import utils.welcome
time.sleep(5)
from utils.values import Proxies, registered_checkers, accounts, settings
import checkers.proxies as pro
pro.run()
import utils.utilities as u
start_unix = time.time()

wanted_path = settings.general.results
location_path = os.path.dirname(os.path.abspath(__file__))

replacer_path = {"current": str(location_path), "unix": str(int(start_unix))}

save_path = (time.strftime(wanted_path)).format(**replacer_path)
if not os.path.exists(save_path):
    os.makedirs(save_path)

class senpai:
    p = 0


for checker in registered_checkers:

    locals()[checker] = importlib.import_module('checkers.' + checker)

    globals().update(
        {n: getattr(locals()[checker], n) for n in locals()[checker].__all__} if hasattr(locals()[checker], '__all__')
        else
        {k: v for (k, v) in locals()[checker].__dict__.items() if not k.startswith('_')
         })



def thread_starter(numbers, threads=1, name=""):
    pool = ThreadPool(threads)
    results = pool.map(eval(name).check, numbers)
    pool.close()
    pool.join()
    return results

def checker_thread_starter(x):
    thread_number_list = []
    for i in range(0, len(accounts.combos)):
        thread_number_list.append(int(i))
    the_focking_threads = thread_starter(numbers=thread_number_list, threads=int(settings.general.total_threads), name=x)
    senpai.p = senpai.p + 1


for checker in registered_checkers:
    t1 = threading.Thread(target=checker_thread_starter, args=[checker])
    t1.daemon = True
    t1.start()

o = 0
with output(output_type='dict') as output_lines:
    while True:
        if o == int(settings.general.timeout) * 60:
            break
        time.sleep(0.5)
        o = o + 1
        for che in registered_checkers:
            output_lines["[Checker] " + che] = str(len(eval("accounts.valid_" + che)) + len(eval("accounts.invalid_" + che))) + " / " + str(len(accounts.combos)) + " Hits: " + str(len(eval("accounts.valid_" + che)))
            if len(eval("accounts.valid_" + che)) > 0:
                replacer = {"checkername" : str(che), "unix": str(int(start_unix))}
                with open(save_path + eval("settings." + che + ".outputname").format(**replacer), mode="wt", encoding="utf-8") as result_file:
                    result_file.write('\n'.join(eval("accounts.valid_" + che)))
        if senpai.p == len(registered_checkers):
            break

        time.sleep(0.5)
time.sleep(1)
if o == int(settings.general.timeout) * 60:
    print("[Checker] reached timeout value. Closing...")
else:
    print("[Checker] All combos has been checked. Closing...")
