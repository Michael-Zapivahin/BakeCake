from aiogram import types


def get_keyboard_for_start(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="Заказать торт",
                                   callback_data=callback_keyboard.new(action="order_cake", value="", info="")),
        types.InlineKeyboardButton(text="Посмотреть прайс",
                                   callback_data=callback_keyboard.new(
                                       action="view_price", value="", info="")),
        types.InlineKeyboardButton(text="Что умеет бот",
                                   callback_data=callback_keyboard.new(action="FAQ", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
