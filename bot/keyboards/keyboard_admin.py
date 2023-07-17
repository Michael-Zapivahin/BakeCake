from aiogram import types


def get_keyboard_admin(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Заявки",
            callback_data=callback_keyboard.new(action="applications", value="", info="")),
        types.InlineKeyboardButton(
            text="Сделать рассылку",
            callback_data=callback_keyboard.new(action="make_newsletter", value="", info="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_admin_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_none(callback_keyboard):
    buttons = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_sender_client(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Отправить",
            callback_data=callback_keyboard.new(action="send_clients", value="", info="")),
        types.InlineKeyboardButton(
            text="Отменить",
            callback_data=callback_keyboard.new(action="cancel", value="", info="")),

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
