import asyncio

from signal import signal as signal_fn, SIGINT, SIGTERM, SIGABRT

from src.app import web
from src.bot import bot
from src.logs import logs


async def idle():
    task = None

    def signal_handler(_, __):
        if web.web_server_task:
            web.web_server_task.cancel()
        task.cancel()

    for s in (SIGINT, SIGTERM, SIGABRT):
        signal_fn(s, signal_handler)

    while True:
        task = asyncio.create_task(asyncio.sleep(600))
        web.bot_main_task = task
        try:
            await task
        except asyncio.CancelledError:
            break


async def main():
    logs.info("正在启动 Web Server")
    await web.start()
    logs.info("正在启动 Bot")
    await bot.start()
    try:
        logs.info("正在运行")
        await idle()
    finally:
        try:
            await bot.stop()
        except ConnectionError:
            pass
        if web.web_server:
            try:
                await web.web_server.shutdown()
            except AttributeError:
                pass


if __name__ == "__main__":
    bot.run(main())
