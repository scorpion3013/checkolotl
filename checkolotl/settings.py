import checkolotl.utils.args as args
import yaml


if __name__ == "checkolotl.settings":
    config = yaml.load(open(args.arguments.config, 'r', encoding="utf8", errors='ignore'), Loader=yaml.Loader)
    all_checkers = []
    for check in config["checkers"].keys():
        all_checkers.append(check)
    toggled_checkers = []
    for check in config["checkers"].keys():
        if config["checkers"][check]["enabled"]:
            toggled_checkers.append(check)
class settings:

    class paths:
        combos = args.arguments.combos
        proxies = args.arguments.proxies
        config = args.arguments.config
        save = ""

    class checker_general:
        _config = config["checker_general"]
        threads = _config["threads"]
        order = _config["order"]
        timeout = _config["timeout"]
        path = _config["path"]
        print_hits = _config["print_hits"]
        remove_duplicate_combos = _config["remove_duplicate_combos"]
        remove_duplicate_proxies = _config["remove_duplicate_proxies"]

    class proxies_checker:
        _config = config["proxies_checker"]
        threads = _config["threads"]
        timeout = _config["timeout"]
        judge_url = _config["judge_url"]
        ip_regex = _config["ip_regex"]

    class announcer:
        _config = config["announcer"]
        discord_webhook_url = _config["discord_webhook_url"]

        class on_start:
            _config = config["announcer"]["on_start"]
            class discord:
                _config = config["announcer"]["on_start"]["discord"]
                enabled = _config["enabled"]
                post_combos = _config["post_combos"]

        class on_end:
            _config = config["announcer"]["on_end"]
            class discord:
                _config = config["announcer"]["on_end"]["discord"]
                enabled = _config["enabled"]
                post_results = _config["post_results"]

    class checkers:
        _config = config["checkers"]

        class minecraft:
            _config = config["checkers"]["minecraft"]
            enabled = _config["enabled"]
            timeout = _config["timeout"]
            check_amount = _config["check_amount"]
            remove_banned_proxy = _config["remove_banned_proxy"]
            account_format = _config["account_format"]
            outputname = _config["outputname"]

        class nordvpn:
            _config = config["checkers"]["nordvpn"]
            enabled = _config["enabled"]
            timeout = _config["timeout"]
            check_amount = _config["check_amount"]
            remove_banned_proxy = _config["remove_banned_proxy"]
            account_format = _config["account_format"]
            outputname = _config["outputname"]

        class vyprvpn:
            _config = config["checkers"]["vyprvpn"]
            enabled = _config["enabled"]
            timeout = _config["timeout"]
            check_amount = _config["check_amount"]
            remove_banned_proxy = _config["remove_banned_proxy"]
            account_format = _config["account_format"]
            outputname = _config["outputname"]

