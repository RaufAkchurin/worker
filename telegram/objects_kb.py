from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.API import get_object_list, get_category_list_by_object_id


class ObjectCallbackFactory(CallbackData, prefix="object"):
    id: str
    name: str


def ObjectInlineKeyboard():
    objects = get_object_list()
    inline_keyboard = []

    for object in objects:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=object["name"],
                callback_data=ObjectCallbackFactory(
                    id=str(object["id"]),
                    name=object["name"]
                ).pack()
            )])
    object_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return object_inline_markup

######################################################################################


class CategoryCallbackFactory(CallbackData, prefix="category"):
    id: str
    name: str


def CategoryInlineKeyboard(object_id):

    categories = get_category_list_by_object_id(object_id)
    inline_keyboard = []

    for category in categories:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=category["name"],
                callback_data=CategoryCallbackFactory(
                    id=str(category["id"]),
                    name=category["name"]
                ).pack()
            )])
    object_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return object_inline_markup

######################################################################################


