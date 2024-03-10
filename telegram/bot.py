import logging
import sys
import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.filters import CommandStart

from telegram import keyboards, report
from registration.registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from report.report_kb import DateInlineKeyboard
import os
from dotenv import load_dotenv

from cleaner.cleaner import Cleaner
from cleaner.cleaner_middleware import CleanerMiddleware

from aiogram import Bot
from aiogram.types import Message

from API import get_worker_by_telegram
from report.hendlers import report_value_input, ReportState, report_confirmation, add_more
from telegram.report.new_work_type.hendlers import new_type_name_hendler, NewTypeState

load_dotenv()
router = Router()

# Регистрируем хендлеры регистрации нового пользователя
router.message.register(register_start, F.text == 'Регистрация/Профиль')
router.message.register(register_name, RegisterState.regName)
router.message.register(register_surname, RegisterState.regSurname)
router.message.register(register_phone, RegisterState.regPhone)
router.message.register(register_confirmation, RegisterState.confirmation)

# Регистрируем хендлеры отчётов
router.message.register(report_value_input, ReportState.value)
router.message.register(report_confirmation, ReportState.confirmation)
router.message.register(add_more, ReportState.need_to_add_more)

# Регистрируем хендлеры добавления нового типа работ
router.message.register(new_type_name_hendler, NewTypeState.name_input)

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    if get_worker_by_telegram(message.from_user.id):
        await bot.send_message(message.from_user.id, text=f"Привет, бот запустился \n" \
                                                          "Перезапустить бота - /start"
                               , reply_markup=keyboards.main_kb)
    else:
        await bot.send_message(message.from_user.id, text="Пожалуйста пройдите регистрацию.",
                               reply_markup=keyboards.main_kb)


@router.message()
async def echo(message: Message, cleaner):
    messages = []
    msg = message.text.lower()
    if msg == "отправить отчёт":
        if get_worker_by_telegram(message.from_user.id):  # Проверяем зарегистрирован ли пользователь
            messages.append(await message.answer(text="Выберите дату для отчёта:",
                                                 reply_markup=DateInlineKeyboard()))

        else:
            messages.append(await message.answer(text="⚠️ Вы не можете отправлять отчёты,"
                                                      " вам необходимо пройти регистрацию. ⚠️"))

    elif msg == "перезагрузить бота":
        await message.answer(text="Вы перешли в главное меню!", reply_markup=keyboards.main_kb)

    [await cleaner.add(message.message_id) for message in messages]


async def main() -> None:
    bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()

    # ROUTERS
    dp.include_router(router)
    dp.include_router(report.hendlers.router)
    dp.include_router(report.new_work_type.hendlers.router)
    ###################################

    cleaner = Cleaner(limit=100)
    dp.update.middleware(CleanerMiddleware(cleaner))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
