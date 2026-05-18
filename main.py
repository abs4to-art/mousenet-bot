import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PORT
from database import init_db
from handlers import start, tariffs, trial, servers, referral, support, admin, payment
from webhook import routes
from yoomoney_client import YooMoneyClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting Mouse.NET bot...")

    init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    yoomoney = YooMoneyClient()

    dp.include_routers(
        start.router,
        tariffs.router,
        trial.router,
        servers.router,
        referral.router,
        support.router,
        admin.router,
        payment.router,
    )

    app = web.Application()
    app["bot"] = bot
    app["yoomoney"] = yoomoney
    app.router.add_routes(routes)

    async def start_polling() -> None:
        logger.info("Bot started polling")
        await dp.start_polling(bot)

    async def start_webhook() -> None:
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, WEBHOOK_HOST, WEBHOOK_PORT)
        await site.start()
        logger.info("Webhook server on %s:%d", WEBHOOK_HOST, WEBHOOK_PORT)
        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()

    await asyncio.gather(start_polling(), start_webhook())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
