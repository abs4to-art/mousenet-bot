import logging

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_IDS
from keyboards import admin_menu, admin_order_action
from database import get_pending_orders, confirm_order, reject_order, get_all_users

logger = logging.getLogger(__name__)

router = Router()


class BroadcastStates(StatesGroup):
    waiting_for_message = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к админ-панели.")
        return

    await message.answer(
        "🔐 <b>Админ-панель Mouse.NET</b>\n\n"
        "Выберите действие:",
        reply_markup=admin_menu(),
    )


@router.callback_query(lambda c: c.data == "admin_orders")
async def admin_orders(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    orders = get_pending_orders()
    if not orders:
        await callback.message.edit_text(
            "📋 Нет новых заявок.",
            reply_markup=admin_menu(),
        )
        await callback.answer()
        return

    for order in orders:
        text = (
            f"📋 <b>Заявка #{order['id']}</b>\n"
            f"👤 Пользователь: <code>{order['user_id']}</code>\n"
            f"📦 Тариф: {order['tariff']}\n"
            f"🕐 Создана: {order['created_at']}"
        )
        await callback.message.answer(
            text,
            reply_markup=admin_order_action(order["id"]),
        )

    await callback.message.delete()
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("admin_confirm_"))
async def admin_confirm(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.replace("admin_confirm_", ""))
    confirm_order(order_id)
    await callback.message.edit_text(
        f"✅ Заявка #{order_id} подтверждена.",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("admin_reject_"))
async def admin_reject(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.replace("admin_reject_", ""))
    reject_order(order_id)
    await callback.message.edit_text(
        f"❌ Заявка #{order_id} отклонена.",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "admin_broadcast")
async def admin_broadcast_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await callback.message.edit_text(
        "📨 <b>Рассылка</b>\n\n"
        "Отправьте сообщение, которое хотите разослать всем пользователям.\n"
        "Поддерживается форматирование и медиафайлы.\n\n"
        "Для отмены отправьте /cancel",
    )
    await state.set_state(BroadcastStates.waiting_for_message)
    await callback.answer()


@router.message(Command("cancel"), StateFilter(BroadcastStates.waiting_for_message))
async def broadcast_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Рассылка отменена.")


@router.message(BroadcastStates.waiting_for_message)
async def broadcast_send(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return

    users = get_all_users()
    sent = 0
    failed = 0

    await message.answer(f"📨 Начинаю рассылку {len(users)} пользователям...")

    for user in users:
        try:
            await message.send_copy(chat_id=user["id"])
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send to user {user['id']}: {e}")
            failed += 1

    await message.answer(
        f"✅ Рассылка завершена.\n"
        f"📨 Отправлено: {sent}\n"
        f"❌ Ошибок: {failed}"
    )
    await state.clear()


@router.callback_query(lambda c: c.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    from keyboards import main_menu

    await callback.message.edit_text(
        "🐭 <b>Mouse.NET</b>\n\nГлавное меню:",
        reply_markup=main_menu(),
    )
    await callback.answer()
