import logging
import uuid

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import add_order, get_order
from yoomoney_client import YooMoneyClient

logger = logging.getLogger(__name__)

router = Router()
yoomoney = YooMoneyClient()

TARIFF_PRICES: dict[str, float] = {
    "pay_regular": 120,
    "pay_combined": 220,
    "pay_bypass": 160,
}

TARIFF_NAMES: dict[str, str] = {
    "pay_regular": "Обычный VPN",
    "pay_combined": "Обычный + обход",
    "pay_bypass": "Только обход",
}


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_tariff(callback: CallbackQuery):
    tariff_key = callback.data
    amount = TARIFF_PRICES.get(tariff_key)
    tariff_name = TARIFF_NAMES.get(tariff_key)
    if not tariff_name:
        await callback.answer("Неизвестный тариф")
        return

    user_id = callback.from_user.id
    label = f"mouse_{user_id}_{uuid.uuid4().hex[:6]}"

    if amount and amount > 0:
        pay_link = yoomoney.create_payment_link(amount, label, tariff_name)
        order_id = add_order(user_id, tariff_name, payment_label=label)

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=pay_link)],
                [
                    InlineKeyboardButton(
                        text="✅ Проверить оплату", callback_data=f"check_{order_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад к тарифам", callback_data="tariffs"
                    )
                ],
            ]
        )
        await callback.message.edit_text(
            f"📦 <b>{tariff_name}</b>\n\n"
            f"💰 Сумма: <b>{amount}₽</b>\n\n"
            f"Нажмите «Оплатить» для перехода на сайт ЮMoney.\n"
            f"После оплаты нажмите «Проверить оплату».",
            reply_markup=kb,
        )
    else:
        order_id = add_order(user_id, tariff_name)
        await callback.message.edit_text(
            f"✅ <b>Заявка на тариф «{tariff_name}» передана администратору!</b>\n\n"
            "Ожидайте, скоро с вами свяжутся.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="⬅️ Назад к тарифам", callback_data="tariffs"
                        )
                    ]
                ]
            ),
        )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("check_"))
async def check_payment(callback: CallbackQuery):
    try:
        order_id = int(callback.data.replace("check_", ""))
    except ValueError:
        await callback.answer("Ошибка")
        return

    order = get_order(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    if order["status"] == "confirmed":
        await callback.message.edit_text(
            "✅ <b>Оплата подтверждена!</b>\n\n"
            "Администратор скоро свяжется с вами для настройки.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="⬅️ Главное меню", callback_data="back_main"
                        )
                    ]
                ]
            ),
        )
    elif order["status"] == "rejected":
        await callback.answer("Заказ отклонён", show_alert=True)
    else:
        await callback.answer(
            "⏳ Оплата ещё не поступила. Попробуйте позже.", show_alert=True
        )
