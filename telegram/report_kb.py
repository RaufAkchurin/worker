from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from API import get_object_list, get_category_list_by_object_id, get_work_type_list_by_object_id, \
    get_work_type_list_by_category_id, get_worker_list
from datetime import datetime, timedelta


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
                    name=category["name"],
                    action="change_category"
                ).pack()
            )])
    category_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return category_inline_markup


class TypeCallbackFactory(CallbackData, prefix="type"):
    id: str
    name: str
    measurement: str


def TypeInlineKeyboard(category_id):
    items = get_work_type_list_by_category_id(category_id)
    inline_keyboard = []

    for item in items:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=item["name"],
                callback_data=TypeCallbackFactory(
                    id=str(item["id"]),
                    name=item["name"],
                    measurement=item["measurement"]["name"],
                ).pack()
            )])
    type_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return type_inline_markup


def profile_kb(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


class DateCallbackFactory(CallbackData, prefix="date"):
    date: str


def date_buttons_text_generator():
    current_date = datetime.now().date()
    last_15_days = [current_date - timedelta(days=i) for i in range(14, -1, -1)]
    return last_15_days


def DateInlineKeyboard():
    items = date_buttons_text_generator()
    inline_keyboard = []

    row = []  # Список для хранения кнопок в текущей строке

    for item in items:
        # Создаем кнопку
        button = InlineKeyboardButton(
            text=str(item.strftime("%d.%m.%Y")),
            callback_data=DateCallbackFactory(
                date=str(item),
            ).pack()
        )

        row.append(button)  # Добавляем кнопку в текущую строку

        # Если в текущей строке уже 4 кнопки, добавляем строку в inline_keyboard и сбрасываем row
        if len(row) == 4:
            inline_keyboard.append(row)
            row = []

    # Если остались кнопки после завершения цикла, добавляем их в последнюю строку
    if row:
        inline_keyboard.append(row)

    inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return inline_markup