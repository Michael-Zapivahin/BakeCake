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
from shop.models import Client

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

callback_keyboard = CallbackData("procedures", "action", "value", "info")

TEXT_NEWSLETTER = 'Запишите сообщение которое хотите разослать. \n' \
                  'Сообщение поддерживает форматирование текста\n'


class PersonalData(StatesGroup):
    waiting_make_newsletter_for_all = State()


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard), parse_mode="Markdown")


@sync_to_async()
def get_all():
    return list(Client.objects.all())


async def make_newsletter(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "make_newsletter":
        await update_text(call.message, TEXT_NEWSLETTER, get_keyboard_none)
        await state.set_state(PersonalData.waiting_make_newsletter_for_all.state)

    elif action == "send_clients":
        newsletter = USERS_DATA.get('newsletter')
        clients = await get_all()
        for client in clients:
            await update_text(call.message, 'wait', get_keyboard_none)
            time.sleep(1)
            try:
                await call.message.bot.send_message(chat_id=int(client.telegram_id), text=newsletter)
            except:
                continue
            time.sleep(0.2)
        await update_text(call.message, 'ok', get_keyboard_none)

    elif action == "cancel":
        text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


async def make_newsletter_for_all(message: types.Message, state: FSMContext):
    newsletter = message.text
    USERS_DATA['newsletter'] = newsletter
    await message.answer(f"Ваше сообщение:\n{newsletter}", reply_markup=get_keyboard_sender_client(callback_keyboard))
    await state.finish()


# @sync_to_async()
# def view_cake_orders():
#     orders = Order.objects.filter(is_active=True)
#
#     return ''


async def admin_view_orders(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "view_speakers":
        text = '*Заявки:*\n'
        # text = text + await view_cake_applications()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


async def admin_callbacks_back(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "admin_back":
        text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_newsletter_for_all, state=PersonalData.waiting_make_newsletter_for_all)
    dp.register_callback_query_handler(
        make_newsletter,
        callback_keyboard.filter(action=[
            "make_newsletter",
            "make_newsletter_for_all",
            "send_clients",
            "cancel",
        ]
        ),
        state="*", )

    dp.register_callback_query_handler(
        admin_callbacks_back,
        callback_keyboard.filter(action=[
            "admin_back",
        ]
        ),
        state="*", )
