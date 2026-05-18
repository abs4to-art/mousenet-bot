import logging

from aiogram import Router, types
from aiogram.types import CallbackQuery

from keyboards import main_menu
from database import has_trial_used, use_trial, add_order

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "trial")
async def trial_request(callback: CallbackQuery):
    user_id = callback.from_user.id

    if has_trial_used(user_id):
        await callback.message.edit_text(
            "😔 Вы уже использовали пробный период.\n\n"
            "Пробный период можно получить только один раз.\n"
            "Приобретите тариф, чтобы продолжить пользоваться Mouse.NET.",
            reply_markup=main_menu(),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        "🎁 <b>Пробный период на 3 дня</b>\n\n"
        "Вы можете бесплатно попробовать Mouse.NET в течение 3 дней.\n"
        "Доступны все возможности обычного тарифа.\n\n"
        "Пробный период предоставляется только один раз.",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="✅ Активировать пробный",
                        callback_data="trial_activate",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="back_main",
                    )
                ],
            ]
        ),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "trial_activate")
async def trial_activate(callback: CallbackQuery):
    user_id = callback.from_user.id

    if has_trial_used(user_id):
        await callback.message.edit_text(
            "😔 Вы уже использовали пробный период.",
            reply_markup=main_menu(),
        )
        await callback.answer()
        return

    use_trial(user_id)
    add_order(user_id, "Пробный период 3 дня")

    await callback.message.edit_text(
        "✅ <b>Заявка на пробный период отправлена!</b>\n\n"
        "Администратор свяжется с вами в ближайшее время.",
        reply_markup=main_menu(),
    )
    await callback.answer("Пробный период активирован!")
