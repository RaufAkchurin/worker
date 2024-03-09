import logging
import sys
import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.filters import CommandStart
from telegram.registration.registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from telegram.report.report_kb import DateInlineKeyboard
import os
from dotenv import load_dotenv

from telegram.cleaner.cleaner import Cleaner
from telegram.cleaner.cleaner_middleware import CleanerMiddleware

from aiogram import Bot
from aiogram.types import Message

from API import get_worker_by_telegram
from telegram.report import hendlers
from telegram.report.hendlers import report_value_input, ReportState, report_confirmation, add_more

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


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    if get_worker_by_telegram(message.from_user.id):
        await bot.send_message(message.from_user.id, text=f"Привет, бот запустился \n" \
                                                          "Перезапустить бота - /start"
                               , reply_markup=bot_kb.main_kb)
    else:
        await bot.send_message(message.from_user.id, text="Пожалуйста пройдите регистрацию.",
                               reply_markup=bot_kb.main_kb)


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
        await message.answer(text="Вы перешли в главное меню!", reply_markup=bot_kb.main_kb)

    [await cleaner.add(message.message_id) for message in messages]


async def main() -> None:
    bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()

    # ROUTERS
    dp.include_router(router)
    dp.include_router(hendlers.router)
    ###################################

    cleaner = Cleaner(limit=100)
    dp.update.middleware(CleanerMiddleware(cleaner))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
