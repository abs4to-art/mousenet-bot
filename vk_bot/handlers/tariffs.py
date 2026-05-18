import logging
import uuid

from vkbottle.bot import Message, Blueprint

from database import add_order
from vk_bot.keyboards import tariffs_keyboard, back_keyboard
from config import YOOMONEY_RECEIVER

logger = logging.getLogger(__name__)

bp = Blueprint("tariffs")

TARIFFS = {
    "regular": {
        "name": "🌐 Обычный VPN",
        "price": "120₽",
        "amount": 120,
        "desc": (
            "🌐 Обычный VPN\n\n"
            "• Высокая скорость до 100 Мбит/с\n"
            "• Доступ к любым сайтам\n"
            "• Защита ваших данных\n"
            "• 1 устройство\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: 120₽"
        ),
    },
    "combined": {
        "name": "🚀 Обычный + обход",
        "price": "220₽",
        "amount": 220,
        "desc": (
            "🚀 Обычный VPN + Обход блокировок\n\n"
            "• Всё из обычного тарифа\n"
            "• Дополнительные протоколы обхода\n"
            "• Стабильное соединение в любых условиях\n"
            "• 2 устройства\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: 220₽"
        ),
    },
    "bypass": {
        "name": "🔓 Только обход",
        "price": "160₽",
        "amount": 160,
        "desc": (
            "🔓 Только обход блокировок\n\n"
            "• Специализированные протоколы\n"
            "• Обход глубокой фильтрации\n"
            "• Минимальная задержка\n"
            "• 1 устройство\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: 160₽"
        ),
    },
}

yoomoney_available = bool(YOOMONEY_RECEIVER)
if yoomoney_available:
    from yoomoney_client import YooMoneyClient
    yoomoney = YooMoneyClient()
else:
    yoomoney = None


@bp.on.message(text="🐭 Купить VPN")
async def show_tariffs(message: Message):
    await message.answer(
        "🐭 Выберите тариф:\n\n"
        "1. 🌐 Обычный VPN — 120₽\n"
        "2. 🚀 Обычный + обход — 220₽\n"
        "3. 🔓 Только обход — 160₽\n\n"
        "Напишите номер или название тарифа.",
        keyboard=tariffs_keyboard().get_json(),
    )


@bp.on.message(text=["🌐 Обычный VPN — 120₽", "1", "Обычный VPN"])
async def tariff_regular(message: Message):
    await show_tariff_detail(message, "regular")


@bp.on.message(text=["🚀 Обычный + обход — 220₽", "2", "Обычный + обход"])
async def tariff_combined(message: Message):
    await show_tariff_detail(message, "combined")


@bp.on.message(text=["🔓 Только обход — 160₽", "3", "Только обход"])
async def tariff_bypass(message: Message):
    await show_tariff_detail(message, "bypass")


async def show_tariff_detail(message: Message, key: str):
    t = TARIFFS[key]
    await message.answer(
        f"{t['desc']}\n\nНапишите «Оплатить», чтобы оформить заказ.",
        keyboard=back_keyboard().get_json(),
    )
    # store selected tariff in state — use simple approach: user message flow
    await message.answer(
        f"Чтобы оплатить тариф «{t['name']}», напишите: Оплатить {key}",
        keyboard=back_keyboard().get_json(),
    )


@bp.on.message(text=["Оплатить regular", "Оплатить combined", "Оплатить bypass"])
async def pay_tariff(message: Message):
    key_map = {
        "Оплатить regular": "regular",
        "Оплатить combined": "combined",
        "Оплатить bypass": "bypass",
    }
    key = key_map.get(message.text)
    if not key:
        return

    t = TARIFFS[key]
    user_id = message.from_id
    label = f"vk_{user_id}_{uuid.uuid4().hex[:6]}"
    order_id = add_order(user_id, t["name"], payment_label=label)

    pay_link = None
    if yoomoney_available and yoomoney and t["amount"]:
        try:
            pay_link = yoomoney.create_payment_link(t["amount"], label, t["name"])
        except Exception as e:
            logger.error("Payment link failed: %s", e)

    if pay_link:
        text = (
            f"📦 {t['name']}\n\n"
            f"💰 Сумма: {t['price']}\n\n"
            f"Ссылка для оплаты:\n{pay_link}\n\n"
            f"После оплаты напишите «Статус {order_id}» для проверки."
        )
    else:
        text = (
            f"✅ Заявка на тариф «{t['name']}» передана администратору!\n\n"
            "Ожидайте, скоро с вами свяжутся."
        )

    await message.answer(text, keyboard=back_keyboard().get_json())



