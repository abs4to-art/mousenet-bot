import asyncio
import logging
import sys

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PORT
from database import init_db
from handlers import start, tariffs, trial, servers, referral, support, admin, payment
from webhook import routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting Mouse.NET bot...")

    try:
        init_db()
    except Exception as e:
        logger.error("Database init failed: %s", e)
        sys.exit(1)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

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
    app.router.add_routes(routes)

    async def start_polling() -> None:
        logger.info("Bot started polling")
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logger.error("Polling error: %s", e)
            sys.exit(1)

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

    try:
        await asyncio.gather(start_polling(), start_webhook())
    except Exception as e:
        logger.error("Fatal error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    except Exception as e:
        logger.error("Unhandled exception: %s", e, exc_info=True)
        sys.exit(1)
