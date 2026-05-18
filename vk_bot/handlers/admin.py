import logging

from vkbottle.bot import Message, Blueprint
from vkbottle import Keyboard, KeyboardButtonColor, Text

from config import YOOMONEY_RECEIVER
from vk_bot.config import ADMIN_VK_IDS
from vk_bot.keyboards import admin_menu, back_keyboard
from database import get_pending_orders, confirm_order, reject_order, get_all_users

logger = logging.getLogger(__name__)

bp = Blueprint("admin")


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_VK_IDS


def order_action_keyboard(order_id: int) -> str:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text(f"✅ Подтвердить #{order_id}"), color=KeyboardButtonColor.POSITIVE)
    kb.add(Text(f"❌ Отклонить #{order_id}"), color=KeyboardButtonColor.NEGATIVE)
    kb.row()
    kb.add(Text("⬅️ Главное меню"), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()


@bp.on.message(text="!admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_id):
        await message.answer("⛔ У вас нет доступа к админ-панели.")
        return

    yoomoney_status = "✅ Подключена" if YOOMONEY_RECEIVER else "❌ Не настроена"
    await message.answer(
        f"🔐 Админ-панель Mouse.NET\n\n"
        f"💰 ЮMoney: {yoomoney_status}\n\n"
        f"Выберите действие:",
        keyboard=admin_menu().get_json(),
    )


@bp.on.message(text="📋 Заявки")
async def admin_orders(message: Message):
    if not is_admin(message.from_id):
        return

    orders = get_pending_orders()
    if not orders:
        await message.answer("📋 Нет новых заявок.", keyboard=admin_menu().get_json())
        return

    for order in orders:
        text = (
            f"📋 Заявка #{order['id']}\n"
            f"👤 Пользователь: {order['user_id']}\n"
            f"📦 Тариф: {order['tariff']}\n"
            f"🕐 Создана: {order['created_at']}"
        )
        await message.answer(text, keyboard=order_action_keyboard(order["id"]))


@bp.on.message(text=lambda text: text and text.startswith("✅ Подтвердить #"))
async def admin_confirm(message: Message):
    if not is_admin(message.from_id):
        return
    try:
        order_id = int(message.text.replace("✅ Подтвердить #", ""))
    except ValueError:
        return
    confirm_order(order_id)
    await message.answer(f"✅ Заявка #{order_id} подтверждена.", keyboard=admin_menu().get_json())


@bp.on.message(text=lambda text: text and text.startswith("❌ Отклонить #"))
async def admin_reject(message: Message):
    if not is_admin(message.from_id):
        return
    try:
        order_id = int(message.text.replace("❌ Отклонить #", ""))
    except ValueError:
        return
    reject_order(order_id)
    await message.answer(f"❌ Заявка #{order_id} отклонена.", keyboard=admin_menu().get_json())


@bp.on.message(text="📨 Рассылка")
async def admin_broadcast_help(message: Message):
    if not is_admin(message.from_id):
        return
    await message.answer(
        "📨 Рассылка\n\n"
        "Чтобы разослать сообщение, напишите:\n"
        "!broadcast Текст сообщения\n\n"
        "Например:\n"
        "!broadcast Привет! У нас акция!"
    )


@bp.on.message(text=lambda text: text and text.startswith("!broadcast "))
async def admin_broadcast_send(message: Message):
    if not is_admin(message.from_id):
        return

    text = message.text[len("!broadcast "):]
    if not text:
        await message.answer("Напишите текст после !broadcast")
        return

    users = get_all_users()
    sent = 0
    failed = 0

    await message.answer(f"📨 Начинаю рассылку {len(users)} пользователям...")

    api = message.ctx_api
    for user in users:
        try:
            await api.messages.send(
                user_id=user["id"],
                message=text,
                random_id=0,
            )
            sent += 1
        except Exception as e:
            logger.warning("Failed to send to user %s: %s", user["id"], e)
            failed += 1

    await message.answer(
        f"✅ Рассылка завершена.\n"
        f"📨 Отправлено: {sent}\n"
        f"❌ Ошибок: {failed}",
        keyboard=admin_menu().get_json(),
    )
