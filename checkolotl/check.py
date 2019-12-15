from checkolotl.settings import settings, toggled_checkers
from checkolotl.values import combos, other
from checkolotl.status import create_bar
from checkolotl.checkers import minecraft, nordvpn, vyprvpn


from multiprocessing.dummy import Pool as ThreadPool
import threading
from datetime import datetime


def start():
    if settings.checker_general.order == "all":
        def check2(combo):
            threads = []
            for check in toggled_checkers:
                t = threading.Thread(target=eval(check + ".check"), args=[combo])
                t.daemon = True
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()
            other.status_bar.update(1)
            hits = []
            for check in toggled_checkers:
                hits.append(check[:2] + ": " + str(len(combos.results[check])))
            other.status_bar.set_postfix_str(" | ".join(hits))

        other.status_bar = create_bar(len(combos.raw), "Combos", "")
        pool = ThreadPool(settings.checker_general.threads)
        pool.map(check2, combos.raw)
        pool.close()
        pool.join()
        other.status_bar.close()
        other.end_time = datetime.now()
        other.finished = True
    elif settings.checker_general.order == "one":

        for check in toggled_checkers:
            def check2(combo):
                eval(check + ".check(combo)")
                other.status_bar.update(1)
                other.status_bar.set_postfix_str(check[:2] + ": " + str(len(combos.results[check])))

            other.status_bar = create_bar(len(combos.raw), check, "")
            pool = ThreadPool(settings.checker_general.threads)
            pool.map(check2, combos.raw)
            pool.close()
            pool.join()
            other.status_bar.close()
            hit_amount = str(len(combos.results[check]))
            print(f"Finished {check} with {hit_amount} hits")
        other.end_time = datetime.now()
        other.finished = True
