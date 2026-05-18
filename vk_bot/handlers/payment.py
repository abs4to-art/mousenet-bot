import logging

from vkbottle.bot import Message, Blueprint

from database import get_order
from vk_bot.keyboards import back_keyboard

logger = logging.getLogger(__name__)

bp = Blueprint("payment")


@bp.on.message(text=lambda text: text and text.startswith("Статус "))
async def check_payment(message: Message):
    try:
        order_id = int(message.text.replace("Статус ", ""))
    except ValueError:
        await message.answer("Неверный формат. Напишите: Статус {номер_заказа}")
        return

    order = get_order(order_id)
    if not order:
        await message.answer("Заказ не найден.", keyboard=back_keyboard().get_json())
        return

    if order["status"] == "confirmed":
        await message.answer(
            "✅ Оплата подтверждена!\n\n"
            "Администратор скоро свяжется с вами для настройки.",
            keyboard=back_keyboard().get_json(),
        )
    elif order["status"] == "rejected":
        await message.answer("❌ Заказ отклонён.", keyboard=back_keyboard().get_json())
    else:
        await message.answer(
            "⏳ Оплата ещё не поступила. Попробуйте позже.",
            keyboard=back_keyboard().get_json(),
        )
