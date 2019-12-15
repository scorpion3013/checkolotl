from datetime import datetime
from checkolotl.settings import settings, config
from checkolotl.values import proxies, combos, other
from discord_webhook import DiscordWebhook, DiscordEmbed
from os import walk


def start():
    checkers = []
    for check in config["checkers"].keys():
        string = check
        if config["checkers"][check]["enabled"]:
            string = "✅ " + string
        else:
            string = "❌ " + string
        checkers.append(string)
    checkers = "\n".join(checkers)
    combo_amount = len(combos.raw)
    proxy_amount = len(proxies.raw)
    webhook = DiscordWebhook(url=settings.announcer.discord_webhook_url)
    embed = DiscordEmbed(title='Checkolotl Started', color=0x06bd22)
    embed.set_footer(text='Checkolotl by scorpion3013')
    embed.set_timestamp()
    embed.add_embed_field(name='Combos:', value=combo_amount)
    embed.add_embed_field(name='Proxies:', value=proxy_amount)
    embed.add_embed_field(name='Server Timestamp:', value=str(datetime.now()), inline=False)
    embed.add_embed_field(name='Checkers:', value=checkers)
    webhook.add_embed(embed)
    webhook.execute()

    if settings.announcer.on_start.discord.post_combos:
        webhook = DiscordWebhook(url=settings.announcer.discord_webhook_url)
        with open(settings.paths.combos, "rb") as f:
            webhook.add_file(file=f.read(), filename='combos.txt')
        webhook.execute()


def end():
    results = []
    for check in combos.results.keys():
        string = check + ": " + str(len(combos.results[check]))
        results.append(string)
    results = "\n".join(results)
    combo_amount = len(combos.raw)
    proxy_amount = str(proxies.working_count)

    webhook = DiscordWebhook(url=settings.announcer.discord_webhook_url)
    embed = DiscordEmbed(title='Checkolotl Finished', color=13369344)
    embed.set_footer(text='Checkolotl by scorpion3013')
    embed.set_timestamp()
    embed.add_embed_field(name='Combos:', value=combo_amount)
    embed.add_embed_field(name='Proxies:', value=proxy_amount)
    embed.add_embed_field(name='Server Timestamp:', value=str(datetime.now()), inline=False)
    embed.add_embed_field(name='Results:', value=results)
    webhook.add_embed(embed)
    webhook.execute()

    if settings.announcer.on_end.discord.post_results:
        webhook = DiscordWebhook(url=settings.announcer.discord_webhook_url)
        existing = False
        for (dirpath, dirnames, filenames) in walk(settings.paths.save):
            for filename in filenames:
                existing = True
                with open(settings.paths.save + "/" + filename, "rb") as f:
                    webhook.add_file(file=f.read(), filename=f'{filename}')
        if existing:
            webhook.execute()



