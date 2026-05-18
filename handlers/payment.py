import logging
import uuid

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import add_order, get_order
from config import YOOMONEY_RECEIVER

logger = logging.getLogger(__name__)

router = Router()

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

yoomoney_enabled = bool(YOOMONEY_RECEIVER)
if yoomoney_enabled:
    from yoomoney_client import YooMoneyClient
    yoomoney = YooMoneyClient()
    logger.info("YooMoney payments enabled")
else:
    yoomoney = None
    logger.info("YooMoney not configured — manual orders only")


def payment_keyboard(order_id: int, pay_link: str | None = None) -> InlineKeyboardMarkup:
    buttons = []
    if pay_link:
        buttons.append([InlineKeyboardButton(text="💳 Оплатить", url=pay_link)])
    buttons.append(
        [InlineKeyboardButton(text="✅ Проверить статус", callback_data=f"check_{order_id}")]
    )
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Назад к тарифам", callback_data="tariffs")]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
    order_id = add_order(user_id, tariff_name, payment_label=label)

    pay_link = None
    if yoomoney_enabled and amount:
        try:
            pay_link = yoomoney.create_payment_link(amount, label, tariff_name)
        except Exception as e:
            logger.error("Failed to create payment link: %s", e)

    if pay_link:
        text = (
            f"📦 <b>{tariff_name}</b>\n\n"
            f"💰 Сумма: <b>{amount}₽</b>\n\n"
            f"Нажмите «Оплатить» для перехода на сайт ЮMoney.\n"
            f"После оплаты нажмите «Проверить статус»."
        )
    else:
        text = (
            f"✅ <b>Заявка на тариф «{tariff_name}» передана администратору!</b>\n\n"
            "Ожидайте, скоро с вами свяжутся для оплаты и настройки."
        )

    await callback.message.edit_text(text, reply_markup=payment_keyboard(order_id, pay_link))
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
                    [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_main")]
                ]
            ),
        )
    elif order["status"] == "rejected":
        await callback.answer("Заказ отклонён", show_alert=True)
    else:
        await callback.answer("⏳ Оплата ещё не поступила. Попробуйте позже.", show_alert=True)
