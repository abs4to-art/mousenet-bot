import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN: str = os.getenv("VK_TOKEN", "")
ADMIN_VK_IDS: list[int] = [int(x.strip()) for x in os.getenv("ADMIN_VK_IDS", "").split(",") if x.strip()]

if not VK_TOKEN:
    raise ValueError("VK_TOKEN is not set in .env or environment variables")
