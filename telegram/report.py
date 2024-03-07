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


async def message_to_confirmation(message: Message, state: FSMContext,
                                  bot: Bot):  # ЭТО ПРОСТО СООБЩЕНИЕ БЕЗ ВСЯКОЙ ЛОГИКИ
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
                    "Подтверждаете введённые данные? (да/нет)"
                    )

    msg = await bot.send_message(
        message.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=bot_kb.yes_or_no_kb
    )


async def report_value_input(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        await state.update_data(report_value=message.text)
        await message_to_confirmation(message, state, bot)
        await state.set_state(ReportState.confirmation)
    else:
        await bot.send_message(message.from_user.id, text="⚠️ Введите пожалуйста число⚠️ ")


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


