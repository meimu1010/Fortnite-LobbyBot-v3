# -*- coding: utf-8 -*-
import asyncio
import importlib
import platform
import sys
import traceback

try:
    import aiohttp
    import colorama
    import jaconv
    import sanic

    discord = importlib.import_module('discord')
    rebootpy = importlib.import_module('rebootpy')
    pykakasi = importlib.import_module('pykakasi')
except ModuleNotFoundError:
    print(traceback.format_exc())
    print(f'Python {platform.python_version()}\n')
    print(
        'Failed to load third party library. Please install the dependencies\n'
        'Discord: @meimu69\n'
        'Or please join support Discord server\n'
        'https://github.com/meimu1010/Fortnite-LobbyBot-v3'
    )
    sys.exit(1)

try:
    import modules
except ModuleNotFoundError:
    print(traceback.format_exc())
    print(f'Python {platform.python_version()}\n')
    print(
        'Failed to load third party library. Please install the dependencies\n'
        'Discord: @meimu69\n'
        'Or please join support Discord server\n'
        'https://github.com/meimu1010/Fortnite-LobbyBot-v3'
    )
    sys.exit(1)


# =========================
# Event loop policy（Windows対応修正版）
# =========================
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        import uvloop
    except ModuleNotFoundError:
        pass
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


# =========================
# main async entrypoint
# =========================
async def main():
    mode = 'pc'
    loop = asyncio.get_running_loop()

    print(modules.colors.green(
        f'V{modules.__version__}\n'
        f'Python {platform.python_version()}\n'
        f'rebootpy {rebootpy.__version__}\n'
        f'discord.py {discord.__version__}\n'
        f'Sanic {sanic.__version__}'
    ))

    bot = modules.Bot(
        mode,
        loop=loop,
        dev='-dev' in sys.argv,
        use_device_code='-use-device-code' in sys.argv,
        use_device_auth='-use-device-auth' in sys.argv,
        use_authorization_code='-use-authorization-code' in sys.argv
    )

    # ★旧コードの bot.setup() は同期でもOKだが問題があるなら async化推奨
    bot.setup()

    await bot.start()


# =========================
# entry
# =========================
if __name__ == '__main__':
    asyncio.run(main())