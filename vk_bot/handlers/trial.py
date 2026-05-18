import logging

from vkbottle.bot import Message, Blueprint

from database import has_trial_used, use_trial, add_order
from vk_bot.keyboards import main_menu, back_keyboard

logger = logging.getLogger(__name__)

bp = Blueprint("trial")


@bp.on.message(text="🎁 Пробный период 3 дня")
async def trial_info(message: Message):
    user_id = message.from_id

    if has_trial_used(user_id):
        await message.answer(
            "😔 Вы уже использовали пробный период.\n\n"
            "Пробный период можно получить только один раз.\n"
            "Приобретите тариф, чтобы продолжить пользоваться Mouse.NET.",
            keyboard=main_menu().get_json(),
        )
        return

    await message.answer(
        "🎁 Пробный период на 3 дня\n\n"
        "Вы можете бесплатно попробовать Mouse.NET в течение 3 дней.\n"
        "Доступны все возможности обычного тарифа.\n\n"
        "Напишите «Активировать пробный», чтобы получить доступ.",
        keyboard=back_keyboard().get_json(),
    )


@bp.on.message(text="Активировать пробный")
async def trial_activate(message: Message):
    user_id = message.from_id

    if has_trial_used(user_id):
        await message.answer(
            "😔 Вы уже использовали пробный период.",
            keyboard=main_menu().get_json(),
        )
        return

    use_trial(user_id)
    add_order(user_id, "Пробный период 3 дня")

    await message.answer(
        "✅ Заявка на пробный период отправлена!\n\n"
        "Администратор свяжется с вами в ближайшее время.",
        keyboard=main_menu().get_json(),
    )
