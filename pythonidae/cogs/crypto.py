# coding=utf-8


# third-party modules
import aiohttp

# third-party modules - discord and related
#import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class CryptoCog(commands.Cog, name='crypto'):
    """crypto currency cog"""

    def __init__(self, bot: PythonBot) -> None:
        self.bot = bot

    @commands.command(aliases=['crypto_price', 'price'])
    @commands.is_owner()
    @commands.guild_only()
    @print_context
    async def crypto(self, ctx: commands.Context, *coins: str) -> None:
        """displays the prices of all or a specific crypto currency"""

        if coins:
            coins = [coin.upper() for coin in coins]

        # crypto names and aliases
        crypto_types = {
            'ADA': ['CARDANO',],
            'BCH': ['BITCOIN CASH', 'BITCOINCASH',],
            'BSV': ['BITCOIN SV', 'BITCOINSV',],
            'BTC': ['BITCOIN',],
            'BTG': ['BITCOIN GOLD', 'BITCOINGOLD',],
            'DASH': ['DASH',],
            'DCR': ['DECRED',],
            'DOGE': ['DOGECOIN',],
            'EOS': ['EOS',],
            'ETC': ['ETHEREUM CLASSIC', 'ETHEREUMCLASSIC',],
            'ETH': ['ETHEREUM',],
            'IOTA': ['IOTA',],
            'LSK': ['LISK',],
            'LTC': ['LITECOIN',],
            'NEO': ['NEO',],
            'QTUM': ['QTUM',],
            'TRX': ['TRON',],
            'XEM': ['NEM',],
            'XLM': ['STELLAR',],
            'XMR': ['MONERO',],
            'XRP': ['XRP',],
            'ZEC': ['ZCASH',],
        }

        # check for valid coins argument
        if coins:
            crypto_targets = []
            unsupported = []
            for coin in coins:
                if coin in crypto_types:
                    if coin not in crypto_targets:
                        crypto_targets.append(coin)
                else:
                    for crypto_type, aliases in crypto_types.items():
                        if coin in aliases:
                            if crypto_type not in crypto_targets:
                                crypto_targets.append(crypto_type)
                            break
                    else:
                        unsupported.append(coin)
            if unsupported:
                unsupported = ', '.join(unsupported)
                msg = f"**`Error: crypto type(s): '{unsupported}' are unsupported`**"
                await ctx.send(msg)
                if not crypto_targets:
                    return
            crypto_targets.sort()
        else:
            crypto_targets = list(crypto_types)

        # create url to retrieve crypto data from
        url = 'https://production.api.coindesk.com/v2/price/ticker?assets='
        url += ','.join(crypto_targets)

        # retrieve crypto data
        crypto_data = await self.get_json(url)

        # create message
        padding = max(len(crypto_data['data'][target]['name']) for target in crypto_targets) + 1
        values = []
        for target in crypto_targets:
            name = crypto_data['data'][target]['name']
            value = crypto_data['data'][target]['ohlc']['c']
            values.append(f"{name + ':':<{padding}} {value}")
        msg = '```\n' + '\n'.join(values) + '```'

        # send message
        await ctx.send(msg)

    async def get_json(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_dict = await resp.json()
                return resp_dict


def setup(bot: PythonBot) -> None:
    bot.add_cog(CryptoCog(bot))
