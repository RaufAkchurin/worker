import logging
import sys
import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from report_kb import ObjectInlineKeyboard, CategoryInlineKeyboard, TypeInlineKeyboard, PaginationCallbackFactory
import os
from dotenv import load_dotenv

from cleaner import Cleaner
from cleaner_middleware import CleanerMiddleware

from aiogram import Bot
from aiogram.types import Message

from API import  get_worker_by_telegram
import bot_kb
from telegram.report import hendlers
from telegram.report.hendlers import report_value_input, ReportState, report_confirmation, add_more

load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

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


@router.callback_query(PaginationCallbackFactory.filter(F.action.in_(["next", "previous"])))
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
