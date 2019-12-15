import argparse
import os
from pathlib import Path
parser = argparse.ArgumentParser()
import sys, os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    combo_path = str(Path(os.path.dirname(sys.executable))) + "/combos.txt"
    proxy_path = str(Path(os.path.dirname(sys.executable))) + "/proxies.txt"
    config_path = str(Path(os.path.dirname(sys.executable))) + "/config.yml"
else:
    combo_path = str(os.path.dirname(os.path.abspath(Path(__file__).parent.parent))) + "/combos.txt"
    proxy_path = str(os.path.dirname(os.path.abspath(Path(__file__).parent.parent))) + "/proxies.txt"
    config_path = str(os.path.dirname(os.path.abspath(Path(__file__).parent.parent))) + "/config.yml"

parser.add_argument("--combos", help="changes the combo file", type=str, default=combo_path)
parser.add_argument("--proxies", help="changes the proxy file", type=str, default=proxy_path)
parser.add_argument("--config", help="changes the config", type=str, default=config_path)
arguments = parser.parse_args()
