import os

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from magic_filter import F

from telegram import keyboards
from telegram.API import get_worker_by_telegram, post_shift_creation, get_report_individual, post_log_create
from telegram.cleaner.cleaner import Cleaner
from telegram.report.factory import DateCallbackFactory, ObjectCallbackFactory, CategoryCallbackFactory, \
    TypeCallbackFactory, PaginationCallbackFactory
from telegram.report.report_kb import ObjectInlineKeyboard, CategoryInlineKeyboard, TypeInlineKeyboard, \
    DateInlineKeyboard
from aiogram.types import FSInputFile


async def get_report_worker_individual(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    selected_object_id = data.get("selected_object_id")
    worker_id = get_worker_by_telegram(message.from_user.id)["worker"]["id"]

    updated_report = await get_report_individual(object_id=selected_object_id, worker_id=worker_id)
    if updated_report:
        # generate file path
        current_directory = os.path.dirname(os.path.realpath(__file__))
        two_levels_up = os.path.normpath(os.path.join(current_directory, '../../'))
        excel_file_relative_path = os.path.join(two_levels_up, "report_worker.xlsx")

        excel_file = FSInputFile(excel_file_relative_path)
        await bot.send_document(
            message.from_user.id,
            document=excel_file,
        )
    else:
        await bot.send_message(message.from_user.id,
                               text=f'Обратитесь к разработчику бота,'
                                    f'\n Эксель файл не удалось сгенерировать с помощью'
                                    f'\n запроса на ендпоинт',
                               reply_markup=keyboards.main_kb)
        await post_log_create(
            func="def get_report_worker_individual",
            description=f"selected_object_id = {selected_object_id} \n"
                        f"worker_id = {worker_id}"
        )
