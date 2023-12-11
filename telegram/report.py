from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


class ReportState(StatesGroup):
    volume = State()

message_text = (f'<u><b>Объект:</b></u> {selected_object_name}   \n' \
                 f'<u><b>Категория:</b></u> {selected_type_name} \n' \
                 f'<u><b>Тип работ:</b></u> {callback_data.name} \n' \
                 f'<u><b>тип изм.:</b></u> {callback_data.measurement} \n' \
                 f'                                              \n' \
                 f"Введите пожалуйста объём выполниненных работ в <u><b>{callback_data.measurement}</b></u>\n"
                )
await callback.message.answer(
    text=message_text,
    parse_mode=ParseMode.HTML,
)

async def report_volume(message: Message, state: FSMContext):
    worker = get_worker_by_telegram(message.from_user.id)
    if worker:
        await answer_for_registered_user(message=message, worker=worker)
    else:
        await message.answer(f'⭐ Давайте начнём регистрацию \n Для начала скажите, как к вас зовут? ⭐')
        await state.set_state(RegisterState.regName)