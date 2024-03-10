from aiogram.filters.callback_data import CallbackData


class MeasurementCallbackFactory(CallbackData, prefix="measurement"):
    id: str
    name: str
