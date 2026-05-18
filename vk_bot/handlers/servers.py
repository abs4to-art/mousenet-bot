import logging

from vkbottle.bot import Message, Blueprint

from vk_bot.keyboards import servers_keyboard

logger = logging.getLogger(__name__)

bp = Blueprint("servers")

SERVER_INFO = {
    "Литва": (
        "📍 Литва 🇱🇹\n\n"
        "• Город: Вильнюс\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 30 мс\n"
        "• Статус: ✅ Online"
    ),
    "Казахстан": (
        "📍 Казахстан 🇰🇿\n\n"
        "• Город: Алматы\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 50 мс\n"
        "• Статус: ✅ Online"
    ),
    "Сербия": (
        "📍 Сербия 🇷🇸\n\n"
        "• Город: Белград\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 40 мс\n"
        "• Статус: ✅ Online"
    ),
}


@bp.on.message(text="📍 Серверы")
async def show_servers(message: Message):
    text = "📍 Наши серверы:\n\n" + "\n\n".join(
        f"• {name}" for name in SERVER_INFO
    )
    await message.answer(
        text + "\n\nНапишите название страны для подробной информации.",
        keyboard=servers_keyboard().get_json(),
    )


@bp.on.message(text=["Литва 🇱🇹", "Литва"])
async def server_lithuania(message: Message):
    await message.answer(
        SERVER_INFO["Литва"] + "\n\nДоступно по всем активным тарифам.",
        keyboard=servers_keyboard().get_json(),
    )


@bp.on.message(text=["Казахстан 🇰🇿", "Казахстан"])
async def server_kazakhstan(message: Message):
    await message.answer(
        SERVER_INFO["Казахстан"] + "\n\nДоступно по всем активным тарифам.",
        keyboard=servers_keyboard().get_json(),
    )


@bp.on.message(text=["Сербия 🇷🇸", "Сербия"])
async def server_serbia(message: Message):
    await message.answer(
        SERVER_INFO["Сербия"] + "\n\nДоступно по всем активным тарифам.",
        keyboard=servers_keyboard().get_json(),
    )
