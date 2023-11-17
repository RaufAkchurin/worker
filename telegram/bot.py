import logging
import sys

from aiogram.enums import ParseMode
import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

import keyboards
from telegram.API import get_object_list
from telegram.objects_kb import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard

# TODO: Добавить проверку пользователя по ТГ-айди в БД
# TODO: Добавить проверку пароля

BOT_LINK = "t.me/stroyka_worker_bot"
TOKEN_API = "6769629902:AAGJf0olx2jc3hDADb-HFVYJzWgXFPLNGB8"
HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(TOKEN_API)
dp = Dispatcher()

#############################################################################################


#############################################################################################
smiles = [
    ["🥑", "Я люблю авокадо!"],
    ["🍓", "Клубника - это орех"],
    ["💭", "Ох.. как много идей!"],
    ["🙃", "У тебя всё получится!"]
]


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello, AIOgram 3.x", reply_markup=keyboards.main_kb)


@dp.callback_query(keyboards.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: keyboards.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(smiles) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{smiles[page][0]} <b>{smiles[page][1]}</b>",
            reply_markup=keyboards.paginator(page)
        )
    await call.answer()


#
#
@dp.message(F.text.lower().in_(["хай", "хелоу", "привет"]))
async def greetings(message: Message):
    await message.reply("Привееееть!")


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "ссылки":
        await message.answer("Вот ваши ссылки:", reply_markup=keyboards.links_kb)
    elif msg == "спец. кнопки":
        await message.answer("Спец. кнопки:", reply_markup=keyboards.spec_kb)
    elif msg == "отпр. отчёт":
        await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
    elif msg == "смайлики":
        await message.answer(f"{smiles[0][0]} <b>{smiles[0][1]}</b>", reply_markup=keyboards.paginator())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=keyboards.main_kb)

    #############################################################################################


async def on_startup():
    print("Я был запущен")


# @dp.message(aiogram.filters.CommandStart())
# async def help_command(message: types.Message):
#     await message.answer(text="Добро пожаловать в наш телеграмм Бот")
#     await message.delete()
#
#
# @dp.message(aiogram.filters.Command(commands=['help']))
# async def help_command(message: types.Message):
#     await message.reply(text=HELP_COMMAND)
#
#
# @dp.message(aiogram.filters.Command(commands=['description']))
# async def description_command(message: types.Message):
#     await message.reply(text="Данный бот собирает отчёты о вашей рабочей смене")
#
#
# @dp.message()
# async def echo_capitalize(message: types.Message):
#     await message.answer(text=message.text.capitalize())

# Создаем объекты инлайн-кнопок
big_button_1 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed'
)

big_button_2 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed'
)


# Создаем свой класс фабрики коллбэков, указывая префикс
# и структуру callback_data
class GoodsCallbackFactory(CallbackData, prefix="goods"):
    object_id: int
    category_id: int
    work_type_id: int


# Создаем объекты кнопок, с применением фабрики коллбэков
button_1 = InlineKeyboardButton(
    text='Категория 1',  # name от категории тут должен быть
    callback_data=GoodsCallbackFactory(
        object_id=1,  # id от категории
        category_id=0,
        work_type_id=0
    ).pack()
)

button_2 = InlineKeyboardButton(
    text='Категория 2',
    callback_data=GoodsCallbackFactory(
        object_id=2,
        category_id=0,
        work_type_id=0
    ).pack()
)

# Создаем объект клавиатуры, добавляя в список списки с кнопками
markup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1], [button_2]]
)


# Этот хэндлер будет срабатывать на команду /start
# и отправлять пользователю сообщение с клавиатурой
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Вот такая клавиатура',
        reply_markup=markup
    )


######################################################################################################################
@dp.callback_query(GoodsCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: GoodsCallbackFactory):
    await callback.message.answer(
        text=f'Объект: {callback_data.object_id}\n' \
             f'Категория: {callback_data.category_id}\n' \
             f'Тип работ: {callback_data.work_type_id}'
    )
    await callback.answer()


######################################################################################################################
@dp.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory):
    await callback.message.answer(
        text=f'Айди объекта: {callback_data.id}\n' \
             f'Название объекта: {callback_data.name}\n',
        reply_markup=CategoryInlineKeyboard(callback_data.id)
    )
    await callback.answer()


#################################################################3###################################################

async def main() -> None:
    dp.startup.register(on_startup)
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    asyncio.get_event_loop().run_forever()
