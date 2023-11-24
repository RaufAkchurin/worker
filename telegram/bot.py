import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, state, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import test_kb
from telegram.keyboards import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, profile_kb
from telegram.log.workers_kb import WorkerInlineKeyboard, WorkerCallbackFactory
from telegram.utils.states import Form

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


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.username
    await message.answer(f"Hello, AIOgram 3.x! Your user ID is {user_id}", reply_markup=test_kb.main_kb)


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "авторизоваться":
        await message.answer("Выберите своё имя:", reply_markup=WorkerInlineKeyboard())
    elif msg == "отпр. отчёт":
        await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=test_kb.main_kb)

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
async def process_worker_name_press(callback: CallbackQuery,
                                    callback_data: WorkerCallbackFactory,
                                    state: FSMContext):
    await state.set_state(Form.password)
    await callback.message.answer(
        text=f'Айди рабочего: {callback_data.id}\n' \
             f'Выбрано имя: {callback_data.name}\n' \
             'Введите пожалуйста пароль',
    )


@dp.message(F.text.lower().in_(["zw", "wz"]))
async def form_password(message: Message, state: FSMContext):
    await message.reply("PAAAAAAAAAAAAAAAASSSSSSSSSS")
    print("HEREEEEEEEEEEEEEEEEEEE")


#################################################################3###################################################

# async def login(message: types.Message):
#     # Запрашиваем пароль у пользователя
#     await message.answer("Введите пароль:")
#     # Ожидаем ответ пользователя
#     response = await bot.wait_for('message')
#
#     # Получаем введенный пароль
#     entered_password = response.text
#
#     # Здесь вы можете сравнить введенный пароль с оригиналом
#     original_password = "your_original_password"
#
#     if entered_password == original_password:
#         await message.answer("Пароль верный, доступ разрешен.")
#     else:
#         await message.answer("Неверный пароль, доступ запрещен.")


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
