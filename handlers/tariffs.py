import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards import tariffs_keyboard, tariff_action_keyboard

logger = logging.getLogger(__name__)

router = Router()

TARIFFS = {
    "regular": {
        "name": "🌐 Обычный VPN",
        "price": "120₽",
        "desc": (
            "🌐 <b>Обычный VPN</b>\n\n"
            "• Высокая скорость до 100 Мбит/с\n"
            "• Доступ к любым сайтам\n"
            "• Защита ваших данных\n"
            "• 1 устройство\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: <b>120₽</b>"
        ),
    },
    "combined": {
        "name": "🚀 Обычный + обход",
        "price": "220₽",
        "desc": (
            "🚀 <b>Обычный VPN + Обход блокировок</b>\n\n"
            "• Всё из обычного тарифа\n"
            "• Дополнительные протоколы обхода\n"
            "• Стабильное соединение в любых условиях\n"
            "• 2 устройства\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: <b>220₽</b>"
        ),
    },
    "bypass": {
        "name": "🔓 Только обход",
        "price": "160₽",
        "desc": (
            "🔓 <b>Только обход блокировок</b>\n\n"
            "• Специализированные протоколы\n"
            "• Обход глубокой фильтрации\n"
            "• Минимальная задержка\n"
            "• 1 устройство\n"
            "• Срок: 30 дней\n\n"
            "💰 Цена: <b>160₽</b>"
        ),
    },
}


@router.callback_query(lambda c: c.data == "tariffs")
async def show_tariffs(callback: CallbackQuery):
    await callback.message.edit_text(
        "🐭 <b>Выберите тариф</b>\n\nВыберите подходящий вариант:",
        reply_markup=tariffs_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("tariff_"))
async def show_tariff_detail(callback: CallbackQuery):
    tariff_map = {
        "tariff_regular": "regular",
        "tariff_combined": "combined",
        "tariff_bypass": "bypass",
    }
    key = tariff_map.get(callback.data)
    if not key:
        await callback.answer("Неизвестный тариф")
        return

    tariff = TARIFFS[key]
    await callback.message.edit_text(
        tariff["desc"],
        reply_markup=tariff_action_keyboard(key),
    )
    await callback.answer()
