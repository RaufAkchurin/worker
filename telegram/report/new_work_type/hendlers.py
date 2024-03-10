from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import Message
from telegram.API import post_work_type_create, get_worker_by_telegram
from telegram.cleaner.cleaner import Cleaner
from telegram.report.new_work_type.factory import MeasurementCallbackFactory
from telegram.report.new_work_type.keyboards import MeasurementInlineKeyboard
from telegram.report.report_kb import PaginationCallbackFactory, ObjectInlineKeyboard

router = Router()


class NewTypeState(StatesGroup):
    name_input = State()
    measurement_choice = State()


@router.callback_query(PaginationCallbackFactory.filter(F.action == "add_new_work_type"))
async def new_type_name_input(callback: CallbackQuery,
                              state: FSMContext,
                              cleaner: Cleaner):
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text="Введите название нового типа работ", )
    await state.set_state(NewTypeState.name_input)
    await cleaner.add(msg.message_id)


async def new_type_name_hendler(message: types.Message, cleaner: Cleaner, state: FSMContext):
    await state.update_data(new_type_name=message.text)
    await state.update_data(new_type_name=message.text)
    msg = await message.answer(text="Теперь выберите еденицу измерения",
                               reply_markup=MeasurementInlineKeyboard())
    await cleaner.add(msg.message_id)


@router.callback_query(MeasurementCallbackFactory.filter())
async def new_type_measurement_choice(callback: MeasurementCallbackFactory,
                                      state: FSMContext,
                                      bot: Bot, ):
    await state.update_data(new_type_measurement_id=callback.id)

    # Fetching data
    data = await state.get_data()
    created_by = get_worker_by_telegram(callback.from_user.id)["worker"]
    selected_category_id = data['selected_category_id']
    new_type_measurement_id = data['new_type_measurement_id']

    print(await post_work_type_create(
        name=callback.id,
        category=selected_category_id,
        measurement=new_type_measurement_id,
        created_by=created_by["id"],
        worker_tg=callback.from_user.id,
        bot=bot,
    ))
