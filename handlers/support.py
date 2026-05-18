import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards import main_menu

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "support")
async def support_info(callback: CallbackQuery):
    text = (
        "🆘 <b>Поддержка Mouse.NET</b>\n\n"
        "Если у вас возникли вопросы или проблемы, свяжитесь с нами:\n\n"
        "✉️ <b>Написать администратору:</b>\n"
        "Напишите сюда — @mousenet_support\n\n"
        "📧 <b>Email:</b>\n"
        "support@mousenet.example\n\n"
        "💬 <b>Ответы на частые вопросы:</b>\n"
        "• Что делать, если не работает подключение?\n"
        "  Проверьте интернет-соединение и переподключитесь.\n"
        "• Как сменить тариф?\n"
        "  Напишите в поддержку.\n"
        "• Сколько устройств можно подключить?\n"
        "  Это зависит от тарифа."
    )
    await callback.message.edit_text(text, reply_markup=main_menu())
    await callback.answer()
