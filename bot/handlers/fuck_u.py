from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from bot.keyboards.keyboard_start import get_keyboard_back

callback_keyboard = CallbackData("procedures", "action", "value", "info")
FAQ = """
Уважаемые пользователи❗️
ВПЕРВЫЕ‼️
Представляем вашему вниманию нашего бота❗️
Хотите спросить что он умеет⁉️
- Возможность заказать торт.
- Возможность собрать кастомный торт.
- Посмотреть свои заказы !
- Узнать стоимость ингредиентов для кастомного торта.
- Для администратора: возможность делать рассылку пользователям по акциям/скидкам/делам.
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
/admin - Меню администратора.
/start - Начать работу с ботом для пользователя.
ОСТОРОЖНО‼️
БОТ УМЕЕТ КАКАТЬ‼️
"""


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


async def fuck_u(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "FAQ":
        await update_text(call.message, FAQ, get_keyboard_back)

    await call.answer()


def register_handlers_fuck_u(dp: Dispatcher):
    dp.register_callback_query_handler(
        fuck_u,
        callback_keyboard.filter(action=[
            "FAQ",
        ]),
        state="*", )
