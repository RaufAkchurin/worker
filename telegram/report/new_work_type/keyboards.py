from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.API import get_measurement_list
from telegram.report.new_work_type.factory import MeasurementCallbackFactory


def MeasurementInlineKeyboard():
    query_from_api = get_measurement_list()  # we need only 10 ITEMS IN PAGE
    inline_keyboard = []

    for item in query_from_api["results"]:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=item["name"],
                callback_data=MeasurementCallbackFactory(
                    id=str(item["id"]),
                    name=item["name"][:20],
                ).pack()
            )])

    from telegram.report.report_kb import pagination_bottoms_adding
    inline_keyboard = pagination_bottoms_adding(query_from_api, inline_keyboard)
    type_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return type_inline_markup
