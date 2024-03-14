from aiogram.filters.callback_data import CallbackData


class ObjectCallbackFactory(CallbackData, prefix="object"):
    id: str
    name: str


class CategoryCallbackFactory(CallbackData, prefix="category"):
    id: str
    name: str


class TypeCallbackFactory(CallbackData, prefix="type"):
    id: str
    name: str
    measurement: str


class DateCallbackFactory(CallbackData, prefix="date"):
    date: str


class PaginationCallbackFactory(CallbackData, prefix="pagination"):
    url: str
    action: str
