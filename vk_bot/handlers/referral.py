import logging

from vkbottle.bot import Message, Blueprint

from database import get_referral_count
from vk_bot.keyboards import back_keyboard

logger = logging.getLogger(__name__)

bp = Blueprint("referral")


@bp.on.message(text="👥 Реферальная программа")
async def referral_info(message: Message):
    user_id = message.from_id
    count = get_referral_count(user_id)
    # VK uses domain-based links, can't do deep links easily
    ref_link = f"https://vk.com/im?sel={user_id}"

    text = (
        "👥 Реферальная программа\n\n"
        "Приглашайте друзей и получайте бонусы!\n\n"
        f"🔗 Ваша реферальная ссылка:\n{ref_link}\n\n"
        f"📊 Приглашено пользователей: {count}\n\n"
        "За каждые 5 приглашённых друзей — месяц VPN в подарок!"
    )
    await message.answer(text, keyboard=back_keyboard().get_json())
