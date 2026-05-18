import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_referral_count

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "referral")
async def referral_info(callback: CallbackQuery):
    user_id = callback.from_user.id
    referral_count = get_referral_count(user_id)
    bot_username = (await callback.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    text = (
        "👥 <b>Реферальная программа</b>\n\n"
        "Приглашайте друзей и получайте бонусы!\n\n"
        "🔗 Ваша реферальная ссылка:\n"
        f"<code>{ref_link}</code>\n\n"
        f"📊 Приглашено пользователей: <b>{referral_count}</b>\n\n"
        "За каждые 5 приглашённых друзей — месяц VPN в подарок!"
    )

    await callback.message.edit_text(
        text,
        reply_markup=__import__("aiogram.types").types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    __import__("aiogram.types").types.InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="back_main",
                    )
                ],
            ]
        ),
    )
    await callback.answer()
