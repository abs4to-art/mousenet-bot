import asyncio
import logging
import sys

from vkbottle.bot import Bot

from database import init_db
from vk_bot.config import VK_TOKEN
from vk_bot.handlers import (
    start,
    tariffs,
    trial,
    servers,
    referral,
    support,
    payment,
    admin,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting Mouse.NET VK bot...")

    try:
        init_db()
    except Exception as e:
        logger.error("Database init failed: %s", e)
        sys.exit(1)

    bot = Bot(VK_TOKEN)

    for bp in [
        start.bp,
        tariffs.bp,
        trial.bp,
        servers.bp,
        referral.bp,
        support.bp,
        payment.bp,
        admin.bp,
    ]:
        bot.labeler.load(bp)

    logger.info("VK bot started polling")
    await bot.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("VK bot stopped")
    except Exception as e:
        logger.error("Unhandled exception: %s", e, exc_info=True)
        sys.exit(1)
