import logging

from vkbottle.bot import Message, Blueprint

from vk_bot.keyboards import main_menu

logger = logging.getLogger(__name__)

bp = Blueprint("support")


@bp.on.message(text="🆘 Поддержка")
async def support_info(message: Message):
    text = (
        "🆘 Поддержка Mouse.NET\n\n"
        "Если у вас возникли вопросы или проблемы, свяжитесь с нами:\n\n"
        "✉️ Написать администратору:\n"
        "Напишите сюда — @jolkj\n\n"
        "💬 Ответы на частые вопросы:\n"
        "• Что делать, если не работает подключение?\n"
        "  Проверьте интернет-соединение и переподключитесь.\n"
        "• Как сменить тариф?\n"
        "  Напишите в поддержку.\n"
        "• Сколько устройств можно подключить?\n"
        "  Это зависит от тарифа."
    )
    await message.answer(text, keyboard=main_menu().get_json())
