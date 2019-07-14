[![star this repo](http://githubbadges.com/star.svg?user=scorpion3013&repo=checkolotl&style=flat)](https://github.com/scorpion3013/checkolotl)
[![fork this repo](http://githubbadges.com/fork.svg?user=scorpion3013&repo=checkolotl&style=flat)](https://github.com/scorpion3013/checkolotl/fork)
[![test](https://img.shields.io/github/last-commit/scorpion3013/checkolotl.svg?style=flat)](https://github.com/scorpion3013/checkolotl/commits/master)
[![test](https://img.shields.io/github/release-date/scorpion3013/checkolotl.svg?style=flat)](https://github.com/scorpion3013/checkolotl/releases/latest)
[![test](https://img.shields.io/github/commits-since/scorpion3013/checkolotl/latest.svg?style=flat)](https://github.com/scorpion3013/checkolotl/releases/latest)
# checkolotl
# ![checkolotl](logo.png)
checkolotl is an account checker made with python 3.6.

Warning: This checker has no WINDOWS support yet (The checker uses the reprint libary which has no windows support, I will add a Windows mode sooner or later. (You can run it on Windows using WSL)

## Installation and Running
```bash
git clone https://github.com/scorpion3013/checkolotl
```
```bash
cd checkolotl/
```
Update it with
```bash
git pull
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the all the external libs that are used within this checker.

```bash
pip install -r requirements.txt
```

Supply the combos.txt with accounts in the format `email:password`

Supply the proxies_http/socks4/socks4.txt with proxies in the format of `ip:port`

Edit the config.yml so it fits your desire and your proxies.

Run main.py to start.
```bash
python main.py
```
We also support optional arguments

`--combos` is used to change the combo path.

`--proxieshttp` is used to change the http proxy path.

`--proxiessocks4` is used to change the socks4 proxy path.

`--proxiessocks5` is used to change the socks5 proxy path.

`--config` is used to change the path of the config that should be used.
```bash
python main.py --combos "combos-1.txt" --config "otherconfig.yml"
```

## Tutorial
Will be added soon.

https://streamable.com/6x2sl

bad but yeah

## Support
Discord link: Will be added soon.

# Terms and conditions
- This repository is for educational purposes only
- You won't use this application/code to attempt to obtain accounts which are NOT yours (bruteforcing, etc...)
- You won't use this application/code to do anything unlawful or commit crimes
- I am not responsible for any actions done by people who use this code


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure that the checker still works.

## License
Not set yet.
