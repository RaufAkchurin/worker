from aiogram.types import InlineKeyboardButton

from telegram.report.report_kb import PaginationCallbackFactory


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