from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from telegram import keyboards
from telegram.API import post_work_type_create, get_worker_by_telegram
from telegram.cleaner.cleaner import Cleaner
from telegram.report.new_work_type.factory import MeasurementCallbackFactory
from telegram.report.new_work_type.keyboards import MeasurementInlineKeyboard
from telegram.report.new_work_type.utils import info_about_new_type_choices
from telegram.report.report_kb import PaginationCallbackFactory, TypeInlineKeyboard

router = Router()


class NewTypeState(StatesGroup):
    name_input = State()
    measurement_choice = State()
    confirmation = State()


@router.callback_query(PaginationCallbackFactory.filter(F.action == "add_new_work_type"))
async def new_type_name_input(callback: CallbackQuery,
                              state: FSMContext,
                              cleaner: Cleaner):
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text="Введите название нового типа работ", )
    await state.set_state(NewTypeState.name_input)
    await cleaner.add(msg.message_id)


async def new_type_name_measurement(message: types.Message, cleaner: Cleaner, state: FSMContext):
    await state.update_data(new_type_name=message.text)
    msg = await message.answer(text="Теперь выберите еденицу измерения",
                               reply_markup=MeasurementInlineKeyboard())
    await cleaner.add(msg.message_id)


@router.callback_query(MeasurementCallbackFactory.filter())
async def new_type_measurement_choice(callback: CallbackQuery,
                                      callback_data: MeasurementCallbackFactory,
                                      state: FSMContext,
                                      bot: Bot,
                                      ):
    await state.update_data(new_type_measurement_id=callback_data.id)
    await state.update_data(new_type_measurement_name=callback_data.name)

    await info_about_new_type_choices(callback=callback, state=state, bot=bot)
    await callback.bot.send_message(
        callback.message.chat.id,
        text="Всё верно?",
        reply_markup=keyboards.yes_or_no_kb
    )
    await state.set_state(NewTypeState.confirmation)


async def new_type_create_confirmation(message: types.Message,
                                       state: FSMContext, bot: Bot,
                                       cleaner: Cleaner):
    if message.text == "да":
        data = await state.get_data()
        created = await post_work_type_create(
            name=data["new_type_name"],
            category=data['selected_category_id'],
            measurement=data['new_type_measurement_id'],
            created_by=get_worker_by_telegram(message.from_user.id)["worker"]["id"],
            worker_tg=message.from_user.id,
            bot=bot,
        )

        if created:
            msg = await message.answer(
                text="🏆Новый тип добавлен, можно перейти к отчёту🏆",
                reply_markup=TypeInlineKeyboard(
                    category_id=data['selected_category_id']))
        else:
            msg = await message.answer(text="😕Не удалось добавить новый тип работ.😕")
        await cleaner.add(msg.message_id)
        await state.clear()

    else:
        await message.answer(text="Введите название нового типа работ")
        await state.set_state(NewTypeState.name_input)
