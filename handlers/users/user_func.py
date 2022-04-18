from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, ParseMode
from loader import dp
from loader import bot
from data.messages_text import message_text, payment_links, buttons_text, choice_mes
from states.user_form import UserForm
import aiogram.utils.markdown as md

from utils import send_all_admin
from utils.send_email import send_email


@dp.callback_query_handler(text="agree")
async def agree(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(InlineKeyboardButton(buttons_text['1'], callback_data='choice_1'),
               InlineKeyboardButton(buttons_text['2'], callback_data='choice_2'),
               InlineKeyboardButton(buttons_text['3'], callback_data='choice_3'))
    markup.add(InlineKeyboardButton(buttons_text['4'], callback_data='choice_4'),
               InlineKeyboardButton(buttons_text['5'], callback_data='choice_5'))
    await call.message.edit_text(message_text['agree_mes'], reply_markup=markup)


@dp.callback_query_handler(state='*', text_startswith="choice")
async def one(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await state.finish()
    choice = call.data.split("_")[1]
    async with state.proxy() as data:
        data['choice'] = choice
    await UserForm.name.set()
    await bot.send_message(call.message.chat.id, choice_mes[choice])
    await bot.send_message(call.message.chat.id, message_text['full name'])


@dp.message_handler(state=UserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await UserForm.next()
    await bot.send_message(message.chat.id, message_text['phone number'])


@dp.message_handler(state=UserForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await UserForm.next()
    await bot.send_message(message.chat.id, message_text['email'])


@dp.message_handler(state=UserForm.email)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(InlineKeyboardButton('כל הפרטים נכונים', callback_data='correct'),
                   InlineKeyboardButton('עשיתי טעות צריך לתקן', callback_data=f"choice_{data['choice']}"))
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('הבוט שואל האם כל הפרטים נכונים?'),
                md.text(message_text['full name'], md.bold(data['name'])),
                md.text(message_text['phone number'], md.code(data['phone'])),
                md.text(message_text['email'], md.code(data['email'])),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )


@dp.callback_query_handler(state='*', text='correct')
async def correct(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        print(data['choice'])
        if data['choice'] == '1':
            await bot.send_message(call.message.chat.id, message_text['request_1'])
        else:
            await bot.send_message(call.message.chat.id, 'הבוט ישלח לינק לPAYBOX לפי מנוי')
            await bot.send_message(call.message.chat.id, payment_links[data['choice']])
        await send_all_admin(md.text(
            md.text('Username:', md.bold('@' + call.from_user.username),
                    md.text(md.bold(buttons_text[data['choice']])),
                    md.text(message_text['full name'], md.bold(data['name'])),
                    md.text(message_text['phone number'], md.code(data['phone'].replace("\\", ""))),
                    md.text(message_text['email'], md.code(data['email'])),
                    sep='\n',
                    )))

        # await send_email(f"@{call.from_user.username}\n"
        #                  f"{buttons_text[data['choice']]}"
        #                  f"{message_text['full name']} {data['name']}\n"
        #                  f"{message_text['phone number']} {data['phone']}\n"
        #                  f"{message_text['email']} {data['email']}\n")
        await send_email(f"{data['name']}\n{data['name']}\n{data['phone']}\n{data['email']}\n")
        await state.finish()


@dp.callback_query_handler(text="dagree")
async def dagree(message: types.Message):
    await bot.send_message(message.from_user.id, message_text['dagree_mes'])
