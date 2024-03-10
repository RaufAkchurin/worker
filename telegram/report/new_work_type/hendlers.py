from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, CallbackQuery
from magic_filter import F

from telegram.cleaner.cleaner import Cleaner
from telegram.report.report_kb import PaginationCallbackFactory, ObjectInlineKeyboard

router = Router()


class NewTypeState(StatesGroup):
    name_input = State()
    measurement_choice = State()


# FUNCTIONS




@router.callback_query(PaginationCallbackFactory.filter(F.action == "add_new_work_type"))
async def new_type_name_input(callback: CallbackQuery,
                              callback_data: PaginationCallbackFactory,
                              state: FSMContext,
                              cleaner: Cleaner):
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text="Введите название нового типа работ",)
    await state.set_state(NewTypeState.name_input)
    await cleaner.add(msg.message_id)
