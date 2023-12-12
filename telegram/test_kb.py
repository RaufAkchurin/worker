from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить отчёт"),
        ],
        [
            KeyboardButton(text="Регистрация/Профиль"),
        ],
        [
            KeyboardButton(text="Перезагрузить бота"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)
