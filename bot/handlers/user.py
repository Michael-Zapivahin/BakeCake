import os
import time
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from asgiref.sync import sync_to_async

from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from bot.handlers.common import USERS_DATA
from bot.keyboards.keyboard_admin import get_keyboard_none, get_keyboard_admin, get_keyboard_sender_client
# from bot.management.commands.bot import *
from bot.keyboards.keyboard_start import get_keyboard_back, get_keyboard_for_start
from bot.keyboards.keyboard_user import get_keyboard_choose_cake
from shop.models import Client

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

callback_keyboard = CallbackData("procedures", "action", "value", "info")


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard), parse_mode="Markdown")


ITEM_PRICE = """
*Уровни торта:*
Один + 400₽; Два + 750₽; Три + 1100₽
___________________________________________________
*Форма тора:*
Круг +600₽; Квадрат + 400₽; Прямоугольник + 1000₽
___________________________________________________
*Топинг:*
Белый соус + 200₽; Карамельный + 180₽;
Кленовый + 200₽; Черничный + 300₽;
Молочный шоколад + 350₽; Клубничный +200₽
___________________________________________________
*Ягоды:*
Ежевика + 400₽; Малина +300₽;
Голубика + 450₽; Клубника + 500₽
___________________________________________________
*Декор:*
Фисташки + 300₽; Безе + 450₽;
Фундук + 350₽; Пекан + 300₽;
Маршмеллоу + 200₽; Марципан + 280₽
___________________________________________________
*Добавить фразу на торт:*
Слово/фраза + 500₽
"""


async def make_newsletter(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "view_price":
        await update_text(call.message, ITEM_PRICE, get_keyboard_back)

    elif action == "back":
        text = 'Вас приветствует Сервис BakeCake'
        await update_text(call.message, text, get_keyboard_for_start)

    elif action == "order_cake":
        text = 'Какой торт хотите заказать?'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_choose_cake)
    elif action == "order_cake":
        text = 'Какой торт хотите заказать?'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_choose_cake)
    await call.answer()
