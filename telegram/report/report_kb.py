import math
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telegram.API import get_object_list, get_category_list_by_object_id, \
    get_work_type_list_by_category_id, get_work_type_list_by_paginated_url, get_object_by_paginated_url, \
    get_category_list_by_paginated_url
from datetime import datetime, timedelta
from telegram.report.factory import ObjectCallbackFactory, CategoryCallbackFactory, TypeCallbackFactory, \
    DateCallbackFactory, PaginationCallbackFactory

localhost = os.getenv('LOCALHOST_IP')


def ObjectInlineKeyboard(url: str = None):
    if url:
        query_from_api = get_object_by_paginated_url(f"http://{localhost}/" + url)
    else:
        query_from_api = get_object_list()

    inline_keyboard = []

    for object in query_from_api["results"]:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=object["name"],
                callback_data=ObjectCallbackFactory(
                    id=str(object["id"]),
                    name=object["name"][:20]
                ).pack()
            )])
    inline_keyboard = pagination_bottoms_adding(query_from_api, inline_keyboard)
    object_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return object_inline_markup


# CATEGORY ITEMS


def CategoryInlineKeyboard(object_id, url=None):
    if url:
        query_from_api = get_category_list_by_paginated_url(f"http://{localhost}/" + url)
    else:
        query_from_api = get_category_list_by_object_id(object_id)
    inline_keyboard = []

    for category in query_from_api["results"]:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=category["name"],
                callback_data=CategoryCallbackFactory(
                    id=str(category["id"]),
                    name=category["name"][:20],
                    action="change_category"
                ).pack()
            )])
    inline_keyboard = pagination_bottoms_adding(query_from_api, inline_keyboard)
    category_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return category_inline_markup


# TYPE ITEMS


def TypeInlineKeyboard(category_id, url=None):
    if url:
        query_from_api = get_work_type_list_by_paginated_url(f"http://{localhost}/" + url)
    else:
        query_from_api = get_work_type_list_by_category_id(category_id)  # we need only 10 ITEMS IN PAGE
    inline_keyboard = []

    for item in query_from_api["results"]:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=item["name"],
                callback_data=TypeCallbackFactory(
                    id=str(item["id"]),
                    name=item["name"][:20],
                    measurement=item["measurement"]["name"],
                ).pack()
            )])

    from telegram.report.new_work_type.utils import new_work_type_bottom_adding
    inline_keyboard = new_work_type_bottom_adding(query_from_api, inline_keyboard)
    inline_keyboard = pagination_bottoms_adding(query_from_api, inline_keyboard)
    type_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return type_inline_markup


# DATE ITEMS


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


# PAGINATION ITEMS


def pagination_bottoms_adding(query_from_api, inline_keyboard):
    try:
        pages_count = math.ceil(query_from_api["count"] / 10)
        if query_from_api["next"]:
            current_page = int(query_from_api["next"][-1]) - 1
        else:
            current_page = pages_count
    except ZeroDivisionError:
        pages_count = 0
        current_page = 0

    progress_bottom = InlineKeyboardButton(
        text=f"{current_page} из {pages_count}",
        callback_data=PaginationCallbackFactory(
            action="counter",
            url="counter"
        ).pack()
    )

    if query_from_api["next"]:
        next_bottom = InlineKeyboardButton(
            text="▶️",
            callback_data=PaginationCallbackFactory(
                action="next",
                url=query_from_api["next"],
            ).pack()
        )

    if query_from_api["previous"]:
        previous_bottom = InlineKeyboardButton(
            text="⬅️",
            callback_data=PaginationCallbackFactory(
                action="previous",
                url=query_from_api["previous"]
            ).pack()
        )
    if query_from_api["next"] and not query_from_api["previous"]:
        inline_keyboard.append([progress_bottom, next_bottom])

    if query_from_api["previous"] and not query_from_api["next"]:
        inline_keyboard.append([previous_bottom, progress_bottom])

    if query_from_api["next"] and query_from_api["previous"]:
        inline_keyboard.append([previous_bottom, progress_bottom, next_bottom])

    return inline_keyboard


def profile_kb(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
