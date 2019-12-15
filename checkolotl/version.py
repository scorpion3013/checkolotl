import requests
import time

version = "v2.0.0"


def update_check():
    try:
        r = requests.get(url="https://api.github.com/repos/scorpion3013/checkolotl/releases", timeout=5).json()
        latest = r[0].get("tag_name")
        if latest != version:
            print(f"It looks like your checkolotl version is outdated.\nYour checkolotl is on version {version}, but the latest version is {latest}.")
            time.sleep(5)
    except:
        print("Could not check for updates.")
        time.sleep(5)
