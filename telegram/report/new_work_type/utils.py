from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from telegram.report.factory import PaginationCallbackFactory


def new_work_type_bottom_adding(query_from_api, inline_keyboard):
    if (query_from_api["previous"] and not query_from_api["next"]) \
            or (not query_from_api["next"] and not query_from_api["previous"]):
        add_new_work_type_bottom = InlineKeyboardButton(
            text=f"Добавить новый тип работ",
            callback_data=PaginationCallbackFactory(
                action="add_new_work_type",
                url="telegram.com"
            ).pack()
        )
        inline_keyboard.append([add_new_work_type_bottom])

    return inline_keyboard

async def info_about_new_type_choices(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

    selected_category = data.get('selected_category_name')
    new_type_measurement_name = data.get('new_type_measurement_name')
    new_type_name = data.get('new_type_name')

    message_text = (
        f'<u><b>Категория:</b></u> {selected_category} \n' \
        f'<u><b>Название типа работ:</b></u> {new_type_name} \n' \
        f'<u><b>тип изм.:</b></u> {new_type_measurement_name} \n' \
        )

    msg = await bot.send_message(
        callback.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
    )
    return msg
