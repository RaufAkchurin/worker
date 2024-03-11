from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from telegram.API import post_work_type_create, get_worker_by_telegram
from telegram.cleaner.cleaner import Cleaner
from telegram.report.new_work_type.factory import MeasurementCallbackFactory
from telegram.report.new_work_type.keyboards import MeasurementInlineKeyboard
from telegram.report.report_kb import PaginationCallbackFactory, TypeInlineKeyboard

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
    msg = await message.answer(text="Теперь выберите еденицу измерения",
                               reply_markup=MeasurementInlineKeyboard())
    await cleaner.add(msg.message_id)


@router.callback_query(MeasurementCallbackFactory.filter())
async def new_type_measurement_choice(callback: CallbackQuery,
                                      callback_data: MeasurementCallbackFactory,
                                      state: FSMContext,
                                      bot: Bot,
                                      cleaner: Cleaner):
    await state.update_data(new_type_measurement_id=callback_data.id)
    data = await state.get_data()

    created = await post_work_type_create(
        name=data["new_type_name"],
        category=data['selected_category_id'],
        measurement=data['new_type_measurement_id'],
        created_by=get_worker_by_telegram(callback.from_user.id)["worker"],
        worker_tg=callback.from_user.id,
        bot=bot,
    )

    if created:
        msg = await callback.bot.send_message(callback.message.chat.id,
                                              text="🏆Новый тип добавлен, можно перейти к отчёту🏆",
                                              reply_markup=TypeInlineKeyboard(category_id=data['selected_category_id']))
    else:
        msg = await callback.bot.send_message(callback.message.chat.id,
                                              text="😕Не удалось добавить новый тип работ.😕")
    await cleaner.add(msg.message_id)
    await state.clear()
