import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards import contest_keyboard
from database import add_contest_participant, is_contest_participant

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "contest")
async def contest_info(callback: CallbackQuery):
    text = (
        "🏆 <b>Конкурс от Mouse.NET</b>\n\n"
        "Условия конкурса:\n"
        "1. Подпишись на наш канал\n"
        "2. Нажми кнопку «Участвую»\n"
        "3. Пригласи друзей по реферальной ссылке\n\n"
        "🎁 <b>Призы:</b>\n"
        "🥇 1 место — Годовой VPN (любой тариф)\n"
        "🥈 2 место — 6 месяцев VPN\n"
        "🥉 3 место — 3 месяца VPN\n\n"
        "Победители будут определены через 2 недели после старта.\n"
        "Количество приглашённых друзей увеличивает шансы!"
    )
    await callback.message.edit_text(text, reply_markup=contest_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "contest_join")
async def contest_join(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    if is_contest_participant(user_id):
        await callback.answer("Вы уже участвуете в конкурсе!", show_alert=True)
        return

    success = add_contest_participant(user_id, username)
    if success:
        await callback.answer("✅ Вы участвуете в конкурсе! Удачи!", show_alert=True)
    else:
        await callback.answer("Вы уже участвуете в конкурсе!", show_alert=True)
