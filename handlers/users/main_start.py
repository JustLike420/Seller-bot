from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from data.messages_text import message_text
from data import config
from loader import dp, bot
from utils.work_with_db import SQLite

db = SQLite()


@dp.message_handler(state='*', commands='start')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, str(message.from_user.username))
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(InlineKeyboardButton(message_text['dagree'], callback_data='dagree'), InlineKeyboardButton(message_text['agree'], callback_data='agree'))
    with open('start.gif', 'rb') as gif:

        await bot.send_animation(message.from_user.id, gif)
    await message.answer(message_text['starting message'],
                         reply_markup=markup)
