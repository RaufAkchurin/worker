import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import bot_kb
from API import get_worker_by_telegram
from registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from report import ReportState, report_value_input, shift_creation
from report_kb import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, TypeCallbackFactory, DateCallbackFactory, DateInlineKeyboard, \
    PaginationCallbackFactory
import os
from dotenv import load_dotenv

from telegram.cleaner import Cleaner
from telegram.middleware.cleaner import CleanerMiddleware

load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

cleaner = Cleaner(limit=100)
dp.update.middleware(CleanerMiddleware(cleaner))


async def report_confirmation(message: Message, state: FSMContext, bot: Bot):
    if message.text == "да":
        result = await shift_creation(message=message, state=state, bot=bot)
        if result:
            await bot.send_message(message.from_user.id,
                                   text="🏆Отчёт успешно добавлен🏆",
                                   reply_markup=bot_kb.main_kb
                                   )
            await cleaner.purge()
        else:
            await bot.send_message(message.from_user.id,
                                   text="😕Отчёт не прошёл, повторите пожалуйста занова😕",
                                   reply_markup=bot_kb.main_kb
                                   )
        await state.set_state(ReportState.type_choice)
        # await state.clear()

        # confirmation to continue adding report

        # await bot.send_message(message.from_user.id, text="Желаете добавить еще работы по данному объекту?",
        #                        reply_markup=bot_kb.yes_or_no_kb)
        # if message.text == "да":
        #     await state.set_state(ReportState.adding_continue)
        # else:
        #     await state.clear()
        #     await bot.send_message(message.from_user.id, text="Спасибо за отчёт!")



    elif message.text == "нет":
        await state.clear()
        await bot.send_message(message.from_user.id, text="Выберите дату для отчёта занова:",
                               reply_markup=DateInlineKeyboard())
    else:
        await bot.send_message(message.from_user.id, text="⚠️ Ответить можно только да или нет⚠️")


# Регистрируем хендлеры регистрации нового пользователя
dp.message.register(register_start, F.text == 'Регистрация/Профиль')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_surname, RegisterState.regSurname)
dp.message.register(register_phone, RegisterState.regPhone)
dp.message.register(register_confirmation, RegisterState.confirmation)

# Регистрируем хендлеры отчётов
dp.message.register(report_value_input, ReportState.value)
dp.message.register(report_confirmation, ReportState.confirmation)


@dp.message(CommandStart())
async def start(message: Message):
    if get_worker_by_telegram(message.from_user.id):
        await bot.send_message(message.from_user.id, text=f"Привет, бот запустился \n" \
                                                          "Перезапустить бота - /start"
                               , reply_markup=bot_kb.main_kb)
    else:
        await bot.send_message(message.from_user.id, text="Пожалуйста пройдите регистрацию.",
                               reply_markup=bot_kb.main_kb)


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()
    if msg == "отправить отчёт":
        if get_worker_by_telegram(message.from_user.id):  # Проверяем зарегистрирован ли пользователь
            msg = await bot.send_message(message.from_user.id, text="Выберите дату для отчёта:",
                                         reply_markup=DateInlineKeyboard())
        else:
            msg = await bot.send_message(message.from_user.id,
                                         text="⚠️ Вы не можете отправлять отчёты, вам необходимо пройти регистрацию. ⚠️")
    elif msg == "перезагрузить бота":
        msg = await bot.send_message(message.from_user.id, text="Вы перешли в главное меню!",
                                     reply_markup=bot_kb.main_kb)
    await cleaner.add(msg.message_id)


@dp.callback_query(PaginationCallbackFactory.filter(F.action.in_(["next", "previous"])))
async def paginator(query: CallbackQuery, callback_data: PaginationCallbackFactory):
    if "objects" in query.data:
        await query.message.edit_text(
            text="Выберите объект",
            reply_markup=ObjectInlineKeyboard(url=callback_data.url)
        )
    elif "categories" in query.data:
        await query.message.edit_text(
            text="Выберите категорию",
            reply_markup=CategoryInlineKeyboard(url=callback_data.url, object_id=None)
        )

    elif "work_types" in query.data:
        await query.message.edit_text(
            text="Выберите тип работ",
            reply_markup=TypeInlineKeyboard(url=callback_data.url, category_id=None)
        )


@dp.callback_query(DateCallbackFactory.filter())
async def process_data_press(callback: CallbackQuery,
                             callback_data: DateCallbackFactory,
                             state: FSMContext):
    await state.update_data(selected_date=callback_data.date)
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=f'Дата: {callback_data.date}\n' \
                                               f'Выберите объект',
                                          reply_markup=ObjectInlineKeyboard()
                                          )
    await cleaner.add(msg.message_id)


@dp.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory,
                               state: FSMContext):
    await state.update_data(selected_object_name=callback_data.name)
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=f'Название объекта: {callback_data.name}\n',
                                          reply_markup=CategoryInlineKeyboard(callback_data.id)
                                          )
    await cleaner.add(msg.message_id)


@dp.callback_query(CategoryCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: CategoryCallbackFactory,
                                 state: FSMContext):
    await state.update_data(selected_category_id=callback_data.id)
    await state.update_data(selected_category_name=callback_data.name)
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=f'Название категории: {callback_data.name}\n',
                                          reply_markup=TypeInlineKeyboard(category_id=callback_data.id)
                                          )
    await state.set_state(ReportState.type_choice)


@dp.callback_query(TypeCallbackFactory.filter())
async def process_type_press(callback: CallbackQuery,
                             callback_data: TypeCallbackFactory,
                             state: FSMContext,
                             ):
    await state.update_data(selected_type_id=callback_data.id)  # Для пост запроса на создание смены
    await state.update_data(selected_type_name=callback_data.name)
    await state.update_data(selected_type_measurement=callback_data.measurement)

    message_text = (f'Тип работ: {callback_data.name} \n' \
                    f'                                              \n' \
                    f"Введите пожалуйста объём выполниненных работ в <u><b>{callback_data.measurement}</b></u>\n"
                    )
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=message_text,
                                          parse_mode=ParseMode.HTML,
                                          )
    await state.set_state(ReportState.value)
    await cleaner.add(msg.message_id)


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
