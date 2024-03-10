from aiogram.types import InlineKeyboardButton

from telegram.API import get_work_type_list_by_category_id
from telegram.report.factory import TypeCallbackFactory


def TypeInlineKeyboard(category_id, url=None):
    query_from_api = get_work_type_list_by_category_id(category_id)  # we need only 10 ITEMS IN PAGE
    inline_keyboard = []

    # for item in query_from_api["results"]:
    #     inline_keyboard.append(
    #         [InlineKeyboardButton(
    #             text=item["name"],
    #             callback_data=TypeCallbackFactory(
    #                 id=str(item["id"]),
    #                 name=item["name"][:20],
    #                 measurement=item["measurement"]["name"],
    #             ).pack()
    #         )])
    #
    # inline_keyboard = new_work_type_bottom_adding(query_from_api, inline_keyboard)
    # inline_keyboard = pagination_bottoms_adding(query_from_api, inline_keyboard)
    # type_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    # return type_inline_markup