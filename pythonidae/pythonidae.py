#!/usr/bin/env python
# coding=utf-8


# standard library modules
import asyncio
from asyncio.events import AbstractEventLoop
import os
import signal

# third party modules
from dotenv import load_dotenv

# local modules
from pythonbot import PythonBot


async def handle_sigint(
        signal: signal.Signals,
        loop: AbstractEventLoop,
        bot: PythonBot
    ) -> None:
    print('\n' + '-' * 30)
    inp = input('Shutdown? [N/y] ').lower()
    if inp.lower() in ('y', 'yes'):
        msg = 'Shutting down, goodbye...'
        print(msg)
        # owner = await bot.get_owner()
        # await bot.send_info_msg(owner, msg)
        await bot.close()

def main() -> None:
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot = PythonBot()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(
        signal.SIGINT,
        lambda s=signal.SIGINT: asyncio.create_task(handle_sigint(s, loop, bot))
    )
    try:
        loop.run_until_complete(bot.start(token, bot=True, reconnect=True))
    except:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
