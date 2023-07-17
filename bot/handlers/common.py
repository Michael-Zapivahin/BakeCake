from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.keyboards.keyboard_admin import get_keyboard_admin
from bot.keyboards.keyboard_start import get_keyboard_for_start

from shop.models import Client

callback_keyboard = CallbackData("procedures", "action", "value", "info")
START_TEXT = "Вас приветствует Сервис BakeCake"
USERS_DATA = {}


@sync_to_async()
def get_and_create_client(telegram_id):
    client, _ = Client.objects.update_or_create(
        telegram_id=USERS_DATA[f'{telegram_id}']['telegram_id'],
        defaults={
            'nik_name': USERS_DATA[f'{telegram_id}']['nikname'],
        }
    )
    return client


# Хэндлер на команду /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    telegram_id = message.from_id
    nikname = message.from_user.username
    USERS_DATA[f'{telegram_id}'] = {'telegram_id': telegram_id,
                                    'nikname': nikname
                                    }
    await get_and_create_client(telegram_id)
    text = START_TEXT  # await get_start_text()
    keyboard = get_keyboard_for_start(callback_keyboard)
    await message.answer(
        text,
        reply_markup=keyboard
    )


# Хэндлер на команду /cancel
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


# Хэндлер на команду /admin
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.finish()
    text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
    await message.answer(
        text,
        reply_markup=get_keyboard_admin(callback_keyboard)
    )


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_admin, IDFilter(user_id=admin_id), commands="admin", state="*")
