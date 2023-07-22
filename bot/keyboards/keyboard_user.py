from aiogram import types


def get_keyboard_choose_cake(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="Готовый торт",
                                   callback_data=callback_keyboard.new(action="ready_cake", value="", info="")),
        types.InlineKeyboardButton(text="Создать свой",
                                   callback_data=callback_keyboard.new(
                                       action="castom_cake", value="", info="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
