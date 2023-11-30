from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from API import get_worker_list


class WorkerCallbackFactory(CallbackData, prefix="worker"):
    id: str
    name: str


def WorkerInlineKeyboard():
    items = get_worker_list()
    inline_keyboard = []

    for item in items:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=item["name"],
                callback_data=WorkerCallbackFactory(
                    id=str(item["id"]),
                    name=item["name"]
                ).pack()
            )])
    worker_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return worker_inline_markup