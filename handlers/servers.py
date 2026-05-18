import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards import servers_keyboard

logger = logging.getLogger(__name__)

router = Router()

SERVER_INFO = {
    "server_lithuania": (
        "📍 <b>Литва 🇱🇹</b>\n\n"
        "• Город: Вильнюс\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 30 мс\n"
        "• Статус: ✅ Online"
    ),
    "server_kazakhstan": (
        "📍 <b>Казахстан 🇰🇿</b>\n\n"
        "• Город: Алматы\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 50 мс\n"
        "• Статус: ✅ Online"
    ),
    "server_serbia": (
        "📍 <b>Сербия 🇷🇸</b>\n\n"
        "• Город: Белград\n"
        "• Протоколы: WireGuard, OpenVPN\n"
        "• Пинг: от 40 мс\n"
        "• Статус: ✅ Online"
    ),
}


@router.callback_query(lambda c: c.data == "servers")
async def show_servers(callback: CallbackQuery):
    await callback.message.edit_text(
        "📍 <b>Наши серверы</b>\n\nВыберите сервер для подключения:",
        reply_markup=servers_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("server_"))
async def show_server_detail(callback: CallbackQuery):
    info = SERVER_INFO.get(callback.data)
    if not info:
        await callback.answer("Неизвестный сервер")
        return

    await callback.message.edit_text(
        info + "\n\nДоступно по всем активным тарифам.",
        reply_markup=servers_keyboard(),
    )
    await callback.answer()
