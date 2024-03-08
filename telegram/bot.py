import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from report_kb import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, TypeCallbackFactory, DateCallbackFactory, DateInlineKeyboard, \
    PaginationCallbackFactory
import os
from dotenv import load_dotenv

from telegram.cleaner import Cleaner
from telegram.middleware.cleaner import CleanerMiddleware

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from API import post_shift_creation, get_worker_by_telegram
from report_kb import DateInlineKeyboard
import bot_kb


# TODO добавить передачу бота чтобы не путались сообщения между разными пользователями


class ReportState(StatesGroup):
    type_choice = State()
    value = State()
    confirmation = State()


async def info_about_choices(message: Message, state: FSMContext,
                             bot: Bot):
    data = await state.get_data()
    selected_date = data.get('selected_date')
    selected_object = data.get('selected_object_name')
    selected_category = data.get('selected_category_name')
    selected_type = data.get('selected_type_name')
    selected_measurement = data.get('selected_type_measurement')
    selected_value = data.get('report_value')

    message_text = (f'<u><b>Дата:</b></u> {selected_date}   \n' \
                    f'<u><b>Объект:</b></u> {selected_object}   \n' \
                    f'<u><b>Категория:</b></u> {selected_category} \n' \
                    f'<u><b>Тип работ:</b></u> {selected_type} \n' \
                    f'<u><b>тип изм.:</b></u> {selected_measurement} \n' \
                    f"<u><b>Объём:</b></u> {selected_value}\n" \
                    )

    msg = await bot.send_message(
        message.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
    )
    return msg


async def info_about_added_report(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    selected_date = data.get('selected_date')
    selected_object = data.get('selected_object_name')
    selected_category = data.get('selected_category_name')
    selected_type = data.get('selected_type_name')
    selected_measurement = data.get('selected_type_measurement')
    selected_value = data.get('report_value')

    message_text = (f'<u><b>Дата:</b></u> {selected_date}   \n' \
                    f'<u><b>Объект:</b></u> {selected_object}   \n' \
                    f'<u><b>Категория:</b></u> {selected_category} \n' \
                    f'<u><b>Тип работ:</b></u> {selected_type} \n' \
                    f'<u><b>тип изм.:</b></u> {selected_measurement} \n' \
                    f"<u><b>Объём:</b></u> {selected_value}\n" \
                    )

    msg = await bot.send_message(
        message.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
    )
    return msg


async def report_value_input(message: Message, state: FSMContext, bot: Bot):
    messages = []
    if message.text.isdigit():
        await state.update_data(report_value=message.text)
        messages.append(message)
        messages.append(await info_about_choices(message, state, bot))
        messages.append(await bot.send_message(message.from_user.id,
                                               text="Подтверждаете введённые данные? (да/нет)",
                                               reply_markup=bot_kb.yes_or_no_kb
                                               ))
        [await cleaner.add(message.message_id) for message in messages]
        await state.set_state(ReportState.confirmation)

    else:
        msg = await bot.send_message(message.from_user.id, text="⚠️ Введите пожалуйста число⚠️ ")
        await cleaner.add(msg.message_id)


async def shift_creation(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    worker_id = get_worker_by_telegram(message.from_user.id)["worker"]["id"]
    date = data.get('selected_date')
    work_type_id = data.get('selected_type_id')
    value = data.get('report_value')
    response = await post_shift_creation(date=date,
                                         worker_id=worker_id,
                                         worker_tg=message.from_user.id,
                                         work_type_id=work_type_id,
                                         value=value,
                                         bot=bot)
    return response


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
    messages = [message,]
    if message.text == "да":
        result = await shift_creation(message=message, state=state, bot=bot)
        if result:
            await info_about_choices(message, state, bot)
            await bot.send_message(message.from_user.id,
                                   text="🏆Отчёт успешно добавлен🏆",
                                   reply_markup=bot_kb.main_kb)
        else:
            messages.append(await bot.send_message(message.from_user.id,
                                                   text="😕Отчёт не прошёл, повторите пожалуйста занова😕",
                                                   reply_markup=bot_kb.main_kb
                                                   ))

        await state.set_state(ReportState.type_choice)

    elif message.text == "нет":
        await state.clear()
        messages.append(await bot.send_message(message.from_user.id,
                                               text="Выберите дату для отчёта занова:",
                                               reply_markup=DateInlineKeyboard()))
    else:
        messages.append(await bot.send_message(message.from_user.id,
                                               text="⚠️ Ответить можно только да или нет⚠️"))

    [await cleaner.add(message.message_id) for message in messages]
    await cleaner.purge()


async def report_continue(state: FSMContext, message: Message, bot: Bot):
    if message.text == "да":
        data = await state.get_data()
        selected_object_id = data.get("selected_object_id")
        await bot.send_message(message.from_user.id,
                               text=f'Выберите категорию для следующего добавления',
                               reply_markup=CategoryInlineKeyboard(selected_object_id))
    else:
        await bot.send_message(message.from_user.id, text="Спасибо за отчёт!")
        await state.clear()


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
    messages = []
    msg = message.text.lower()
    if msg == "отправить отчёт":
        if get_worker_by_telegram(message.from_user.id):  # Проверяем зарегистрирован ли пользователь
            messages.append(await bot.send_message(message.from_user.id,
                                                   text="Выберите дату для отчёта:",
                                                   reply_markup=DateInlineKeyboard()))

        else:
            messages.append(await bot.send_message(message.from_user.id,
                                                   text="⚠️ Вы не можете отправлять отчёты,"
                                                        " вам необходимо пройти регистрацию. ⚠️"))

    elif msg == "перезагрузить бота":
        await bot.send_message(message.from_user.id, text="Вы перешли в главное меню!",
                               reply_markup=bot_kb.main_kb)

    [await cleaner.add(message.message_id) for message in messages]


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
    await state.update_data(selected_object_id=callback_data.id)
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
