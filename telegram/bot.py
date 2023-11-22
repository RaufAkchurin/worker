import logging
import sys
from aiogram.enums import ParseMode
import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

import test_kb
from telegram.keyboards import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, CategoryCallbackFactory
from telegram.log.workers_kb import WorkerInlineKeyboard, WorkerCallbackFactory

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
    user_id = message.from_user.username
    await message.answer(f"Hello, AIOgram 3.x! Your user ID is {user_id}", reply_markup=test_kb.main_kb)


@dp.callback_query(test_kb.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: test_kb.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(smiles) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{smiles[page][0]} <b>{smiles[page][1]}</b>",
            reply_markup=test_kb.paginator(page)
        )
    await call.answer()


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "авторизоваться":
        await message.answer("Выберите своё имя:", reply_markup=WorkerInlineKeyboard())
    elif msg == "отпр. отчёт":
        await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=test_kb.main_kb)

    #############################################################################################


async def on_startup():
    print("Я был запущен")


######################################################################################################################
@dp.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory):
    await callback.message.answer(
        text=f'Айди объекта: {callback_data.id}\n' \
             f'Название объекта: {callback_data.name}\n',
        reply_markup=CategoryInlineKeyboard(callback_data.id)
    )


#################################################################3###################################################

@dp.callback_query(CategoryCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: CategoryCallbackFactory):
    await callback.message.answer(
        text=f'Айди категории: {callback_data.id}\n' \
             f'Название категории: {callback_data.name}\n',
        reply_markup=TypeInlineKeyboard(callback_data.id)
    )

#################################################################3###################################################


@dp.callback_query(WorkerCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: WorkerCallbackFactory):
    await callback.message.answer(
        text=f'Айди рабочего: {callback_data.id}\n' \
             f'Выбрано имя: {callback_data.name}\n'\
             'Введите пожалуйста пароль',
        # reply_markup=TypeInlineKeyboard(callback_data.id)
    )

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
