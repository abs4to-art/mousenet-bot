from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🐭 Купить VPN", callback_data="tariffs")
    builder.button(text="🎁 Пробный период 3 дня", callback_data="trial")
    builder.button(text="📍 Серверы", callback_data="servers")
    builder.button(text="👥 Реферальная программа", callback_data="referral")
    builder.button(text="🆘 Поддержка", callback_data="support")
    builder.adjust(1)
    return builder.as_markup()


def tariffs_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Обычный VPN — 120₽", callback_data="tariff_regular")
    builder.button(text="🚀 Обычный + обход — 220₽", callback_data="tariff_combined")
    builder.button(text="🔓 Только обход — 160₽", callback_data="tariff_bypass")
    builder.button(text="⬅️ Назад", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


def tariff_action_keyboard(tariff_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатить", callback_data=f"pay_{tariff_key}")
    builder.button(text="⬅️ Назад к тарифам", callback_data="tariffs")
    builder.adjust(1)
    return builder.as_markup()


def servers_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Литва 🇱🇹", callback_data="server_lithuania")
    builder.button(text="Казахстан 🇰🇿", callback_data="server_kazakhstan")
    builder.button(text="Сербия 🇷🇸", callback_data="server_serbia")
    builder.button(text="⬅️ Назад", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


def admin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Заявки", callback_data="admin_orders")
    builder.button(text="📨 Рассылка", callback_data="admin_broadcast")
    builder.adjust(1)
    return builder.as_markup()


def admin_order_action(order_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data=f"admin_confirm_{order_id}")
    builder.button(text="❌ Отклонить", callback_data=f"admin_reject_{order_id}")
    builder.adjust(2)
    return builder.as_markup()
