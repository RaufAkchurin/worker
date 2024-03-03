from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from API import get_object_list, get_category_list_by_object_id, get_work_type_list_by_object_id, \
    get_work_type_list_by_category_id, get_work_type_list_by_url
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


class PaginationCallbackFactory(CallbackData, prefix="pagination"):
    url: str
    action: str


def TypeInlineKeyboard(category_id, by_url=False, url=None):
    if by_url:
        url = "http://127.0.0.1:8000/" + url
        query_from_api = get_work_type_list_by_url(url)
    else:
        query_from_api = get_work_type_list_by_category_id(category_id)  # we need only 10 ITEMS IN PAGE
    inline_keyboard = []

    for item in query_from_api["results"]:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=item["name"],
                callback_data=TypeCallbackFactory(
                    id=str(item["id"]),
                    name=item["name"][:30],
                    measurement=item["measurement"]["name"][:30],
                ).pack()
            )])

    if query_from_api["next"]:
        inline_keyboard.append([InlineKeyboardButton(
                    text=">>>",
                    callback_data=PaginationCallbackFactory(
                        action="next",
                        url=query_from_api["next"],
                    ).pack()
        )])

    if query_from_api["previous"]:
        inline_keyboard.append([InlineKeyboardButton(
                    text="<<<",
                    callback_data=PaginationCallbackFactory(
                        action="previous",
                        url=query_from_api["previous"]
                    ).pack()
        )])

    type_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return type_inline_markup


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="▶️", callback_data=Pagination(action="next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


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
