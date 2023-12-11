from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


# TODO добавить очищение стейта
# TODO добавить передачу бота чтобы не путались сообщения между разными пользователями


class ReportState(StatesGroup):
    value = State()
    confirmation = State()


async def message_to_confirmation(message: Message, state: FSMContext): # ЭТО ПРОСТО СООБЩЕНИЕ БЕЗ ВСЯКОЙ ЛОГИКИ
    data = await state.get_data()
    selected_object = data.get('selected_object_name')
    selected_category = data.get('selected_category_name')
    selected_type = data.get('selected_type_name')
    selected_measurement = data.get('selected_type_measurement')
    selected_value = data.get('report_value')

    message_text = (f'<u><b>Объект:</b></u> {selected_object}   \n' \
                     f'<u><b>Категория:</b></u> {selected_category} \n' \
                     f'<u><b>Тип работ:</b></u> {selected_type} \n' \
                     f'<u><b>тип изм.:</b></u> {selected_measurement} \n' \
                     f"<u><b>Объём:</b></u> {selected_value}\n" \
                     "Подтверждаете введённые данные? (да/нет)"
                    )

    await message.answer(
        text=message_text,
        parse_mode=ParseMode.HTML,
    )


async def report_value_input(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(report_value=message.text)
        await message_to_confirmation(message, state)
        await state.set_state(ReportState.confirmation)
    else:
        await message.answer("⚠️ Введите пожалуйста число⚠️ ")


async def report_confirmation(message: Message, state: FSMContext):
    if message.text == "да":
        await message.answer("Вы выбрали да")
    elif message.text == "нет":
        await message.answer("Вы выбрали нет")
    else:
        await message.answer("⚠️ Ответить можно только да или нет⚠️")