import logging

from vkbottle.bot import Message, Blueprint

from database import add_user, user_exists
from vk_bot.keyboards import main_menu

logger = logging.getLogger(__name__)

bp = Blueprint("start")


@bp.on.message(text=["start", "Начать", "/start"])
async def start_handler(message: Message):
    user_id = message.from_id
    username = f"vk{user_id}"

    if not user_exists(user_id):
        add_user(user_id, username)

    text = (
        "🐭 Добро пожаловать в Mouse.NET!\n\n"
        "Быстрый и надёжный VPN-сервис для ежедневного использования.\n"
        "Выбирай тариф, получай доступ и наслаждайся свободой в интернете."
    )
    await message.answer(text, keyboard=main_menu().get_json())


@bp.on.message(text="⬅️ Главное меню")
async def back_to_main(message: Message):
    text = (
        "🐭 Mouse.NET\n\nГлавное меню:"
    )
    await message.answer(text, keyboard=main_menu().get_json())
