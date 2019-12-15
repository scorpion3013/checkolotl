import threading
import os


def start():
    def commands():
        while True:
            userinput = input()
            if userinput.lower().strip() == "exit":
                os._exit(0)

    t1 = threading.Thread(target=commands, args=[])
    t1.daemon = True
    t1.start()