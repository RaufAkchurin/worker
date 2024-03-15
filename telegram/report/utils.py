from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from magic_filter import F

from telegram import keyboards
from telegram.API import get_worker_by_telegram, post_shift_creation, get_report_individual
from telegram.cleaner.cleaner import Cleaner
from telegram.report.factory import DateCallbackFactory, ObjectCallbackFactory, CategoryCallbackFactory, \
    TypeCallbackFactory, PaginationCallbackFactory
from telegram.report.report_kb import ObjectInlineKeyboard, CategoryInlineKeyboard, TypeInlineKeyboard, \
    DateInlineKeyboard


async def get_report_worker_individual(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    selected_object_id = data.get("selected_object_id")
    worker_id = get_worker_by_telegram(message.from_user.id)

    updated_report = await get_report_individual(object_id=int(selected_object_id), worker_id=worker_id["worker"]["id"])
    if updated_report:
        from aiogram.types import FSInputFile
        excel_file = FSInputFile("/home/rauf/PycharmProjects/worker/report_worker.xlsx")
        await bot.send_document(
            message.from_user.id,
            document=excel_file,
        )
    else:
        await bot.send_message(message.from_user.id,
                               text=f'Обратитесь к разработчику бота,'
                                    f'\n Эксель файл не удалось получить с ендпоинта',
                               reply_markup=keyboards.main_kb)
