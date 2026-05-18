import logging

from aiogram import Router, types
from aiogram.filters import CommandStart

from database import add_user, user_exists
from keyboards import main_menu

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_ref(message: types.Message):
    args = message.text.split()
    ref_id = None
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            ref_id = int(args[1].replace("ref_", ""))
        except ValueError:
            pass

    user_id = message.from_user.id
    username = message.from_user.username

    if not user_exists(user_id):
        if ref_id and ref_id != user_id:
            add_user(user_id, username, referred_by=ref_id)
            logger.info(f"User {user_id} registered with referral {ref_id}")
        else:
            add_user(user_id, username)

    welcome_text = (
        "🐭 Добро пожаловать в <b>Mouse.NET</b>!\n\n"
        "Быстрый и надёжный VPN-сервис для ежедневного использования.\n"
        "Выбирай тариф, получай доступ и наслаждайся свободой в интернете."
    )
    await message.answer(welcome_text, reply_markup=main_menu())


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if not user_exists(user_id):
        add_user(user_id, username)

    welcome_text = (
        "🐭 Добро пожаловать в <b>Mouse.NET</b>!\n\n"
        "Быстрый и надёжный VPN-сервис для ежедневного использования.\n"
        "Выбирай тариф, получай доступ и наслаждайся свободой в интернете."
    )
    await message.answer(welcome_text, reply_markup=main_menu())
