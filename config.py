import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_IDS: list[int] = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

YOOMONEY_RECEIVER: str = os.getenv("YOOMONEY_RECEIVER", "")
YOOMONEY_REDIRECT_URI: str = os.getenv("YOOMONEY_REDIRECT_URI", "")
YOOMONEY_NOTIFICATION_SECRET: str = os.getenv("YOOMONEY_NOTIFICATION_SECRET", "")

WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", os.getenv("PORT", "8080")))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env or environment variables")
