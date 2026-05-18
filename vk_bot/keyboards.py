from vkbottle import Keyboard, KeyboardButtonColor, Text


def main_menu() -> Keyboard:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🐭 Купить VPN"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("🎁 Пробный период 3 дня"), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("📍 Серверы"), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    kb.add(Text("👥 Реферальная программа"), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    kb.add(Text("🆘 Поддержка"), color=KeyboardButtonColor.SECONDARY)
    return kb


def tariffs_keyboard() -> Keyboard:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🌐 Обычный VPN — 120₽"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("🚀 Обычный + обход — 220₽"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("🔓 Только обход — 160₽"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("⬅️ Главное меню"), color=KeyboardButtonColor.SECONDARY)
    return kb


def servers_keyboard() -> Keyboard:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("Литва 🇱🇹"), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    kb.add(Text("Казахстан 🇰🇿"), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    kb.add(Text("Сербия 🇷🇸"), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    kb.add(Text("⬅️ Главное меню"), color=KeyboardButtonColor.SECONDARY)
    return kb


def admin_menu() -> Keyboard:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("📋 Заявки"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("📨 Рассылка"), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("⬅️ Главное меню"), color=KeyboardButtonColor.SECONDARY)
    return kb


def back_keyboard() -> Keyboard:
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("⬅️ Главное меню"), color=KeyboardButtonColor.SECONDARY)
    return kb
