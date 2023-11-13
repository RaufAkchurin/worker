import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import aiogram.filters
from django import setup

from worker_app.django_models import Category

#TODO: Добавить проверку пользователя по ТГ-айди в БД
#TODO: Добавить проверку пароля

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
setup()

BOT_LINK = "t.me/stroyka_worker_bot"
TOKEN_API = "6769629902:AAGJf0olx2jc3hDADb-HFVYJzWgXFPLNGB8"
HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом

"""

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message(aiogram.filters.Command(commands=['help']))
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)
    new_object = Category.objects.create(name="FROM_AIOGRAM")
    new_object.save()


@dp.message(aiogram.filters.Command(commands=['description']))
async def description_command(message: types.Message):
    await message.reply(text="Данный бот собирает отчёты о вашей рабочей смене")


@dp.message(aiogram.filters.CommandStart())
async def help_command(message: types.Message):
    await message.answer(text="Добро пожаловать в наш телеграмм Бот")
    await message.delete()


@dp.message()
async def echo_capitalize(message: types.Message):
    await message.answer(text=message.text.capitalize())


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())