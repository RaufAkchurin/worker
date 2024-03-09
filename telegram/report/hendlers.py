from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from magic_filter import F

from telegram.API import get_worker_by_telegram, post_shift_creation
from telegram.cleaner.cleaner import Cleaner
from telegram.main_kb import main_kb
from telegram.report.report_kb import DateInlineKeyboard, DateCallbackFactory, ObjectInlineKeyboard, ObjectCallbackFactory, \
    CategoryInlineKeyboard, CategoryCallbackFactory, TypeInlineKeyboard, TypeCallbackFactory, PaginationCallbackFactory

router = Router()


class ReportState(StatesGroup):
    type_choice = State()
    value = State()
    confirmation = State()
    need_to_add_more = State()


@router.callback_query(DateCallbackFactory.filter())
async def process_data_press(callback: CallbackQuery,
                             callback_data: DateCallbackFactory,
                             state: FSMContext,
                             cleaner: Cleaner):
    await state.update_data(selected_date=callback_data.date)
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=f'Дата: {callback_data.date}\n' \
                                               f'Выберите объект',
                                          reply_markup=ObjectInlineKeyboard()
                                          )
    await cleaner.add(msg.message_id)


@router.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory,
                               state: FSMContext,
                               cleaner: Cleaner):
    await state.update_data(selected_object_id=callback_data.id)
    await state.update_data(selected_object_name=callback_data.name)
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=f'Название объекта: {callback_data.name}\n',
                                          reply_markup=CategoryInlineKeyboard(callback_data.id)
                                          )
    await cleaner.add(msg.message_id)


@router.callback_query(CategoryCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: CategoryCallbackFactory,
                                 state: FSMContext):
    await state.update_data(selected_category_id=callback_data.id)
    await state.update_data(selected_category_name=callback_data.name)
    await callback.bot.send_message(callback.message.chat.id,
                                    text=f'Название категории: {callback_data.name}\n',
                                    reply_markup=TypeInlineKeyboard(category_id=callback_data.id)
                                    )
    await state.set_state(ReportState.type_choice)


@router.callback_query(TypeCallbackFactory.filter())
async def process_type_press(callback: CallbackQuery,
                             callback_data: TypeCallbackFactory,
                             state: FSMContext,
                             cleaner: Cleaner
                             ):
    await state.update_data(selected_type_id=callback_data.id)  # Для пост запроса на создание смены
    await state.update_data(selected_type_name=callback_data.name)
    await state.update_data(selected_type_measurement=callback_data.measurement)

    message_text = (f'Тип работ: {callback_data.name} \n' \
                    f"Введите пожалуйста объём выполниненных работ в <u><b>{callback_data.measurement}</b></u>\n"
                    )
    msg = await callback.bot.send_message(callback.message.chat.id,
                                          text=message_text,
                                          parse_mode=ParseMode.HTML,
                                          )
    await state.set_state(ReportState.value)
    await cleaner.add(msg.message_id)


async def info_about_choices(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    selected_date = data.get('selected_date')
    selected_object = data.get('selected_object_name')
    selected_category = data.get('selected_category_name')
    selected_type = data.get('selected_type_name')
    selected_measurement = data.get('selected_type_measurement')
    selected_value = data.get('report_value')

    message_text = (f'<u><b>Дата:</b></u> {selected_date}   \n' \
                    f'<u><b>Объект:</b></u> {selected_object}   \n' \
                    f'<u><b>Категория:</b></u> {selected_category} \n' \
                    f'<u><b>Тип работ:</b></u> {selected_type} \n' \
                    f'<u><b>тип изм.:</b></u> {selected_measurement} \n' \
                    f"<u><b>Объём:</b></u> {selected_value}\n" \
                    )

    msg = await bot.send_message(
        message.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
    )
    return msg


async def info_about_added_report(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    selected_date = data.get('selected_date')
    selected_object = data.get('selected_object_name')
    selected_category = data.get('selected_category_name')
    selected_type = data.get('selected_type_name')
    selected_measurement = data.get('selected_type_measurement')
    selected_value = data.get('report_value')

    message_text = (f'<u><b>Дата:</b></u> {selected_date}   \n' \
                    f'<u><b>Объект:</b></u> {selected_object}   \n' \
                    f'<u><b>Категория:</b></u> {selected_category} \n' \
                    f'<u><b>Тип работ:</b></u> {selected_type} \n' \
                    f'<u><b>тип изм.:</b></u> {selected_measurement} \n' \
                    f"<u><b>Объём:</b></u> {selected_value}\n" \
                    )

    msg = await bot.send_message(
        message.from_user.id, text=message_text,
        parse_mode=ParseMode.HTML,
    )
    return msg


async def shift_creation(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    worker_id = get_worker_by_telegram(message.from_user.id)["worker"]["id"]
    date = data.get('selected_date')
    work_type_id = data.get('selected_type_id')
    value = data.get('report_value')
    response = await post_shift_creation(date=date,
                                         worker_id=worker_id,
                                         worker_tg=message.from_user.id,
                                         work_type_id=work_type_id,
                                         value=value,
                                         bot=bot)
    return response


async def report_value_input(message: Message,
                             state: FSMContext,
                             bot: Bot,
                             cleaner: Cleaner):
    messages = []
    if message.text.isdigit():
        await state.update_data(report_value=message.text)
        messages.append(message)
        messages.append(await info_about_choices(message, state, bot))
        messages.append(await bot.send_message(message.from_user.id,
                                               text="Подтверждаете введённые данные? (да/нет)",
                                               reply_markup=main_kb.yes_or_no_kb
                                               ))
        [await cleaner.add(message.message_id) for message in messages]
        await state.set_state(ReportState.confirmation)

    else:
        msg = await bot.send_message(message.from_user.id, text="⚠️ Введите пожалуйста число⚠️ ")
        await cleaner.add(msg.message_id)


async def report_confirmation(message: Message, state: FSMContext, bot: Bot, cleaner: Cleaner):
    messages = [message, ]
    if message.text == "да":
        result = await shift_creation(message=message, state=state, bot=bot)
        if result:
            await info_about_choices(message, state, bot)
            await bot.send_message(message.from_user.id,
                                   text="🏆Отчёт успешно добавлен, продолжим?🏆",
                                   reply_markup=main_kb.yes_or_no_kb)
            await state.set_state(ReportState.need_to_add_more)
        else:
            messages.append(await bot.send_message(message.from_user.id,
                                                   text="😕Отчёт не прошёл, повторите пожалуйста занова😕",
                                                   reply_markup=main_kb.main_kb
                                                   ))
            await state.clear()

    elif message.text == "нет":
        await state.clear()
        messages.append(await bot.send_message(message.from_user.id,
                                               text="Выберите дату для отчёта занова:",
                                               reply_markup=DateInlineKeyboard()))
    else:
        messages.append(await bot.send_message(message.from_user.id,
                                               text="⚠️ Ответить можно только да или нет⚠️"))

    [await cleaner.add(message.message_id) for message in messages]


async def add_more(message: Message, bot: Bot, state: FSMContext, cleaner: Cleaner) -> None:
    messages = [message, ]
    data = await state.get_data()
    selected_category_id = data.get("selected_category_id")
    if message.text == "да":
        await state.set_state(ReportState.type_choice)
        await bot.send_message(message.from_user.id,
                               text=f'В таком случае выберите тип работ из списка',
                               reply_markup=TypeInlineKeyboard(category_id=selected_category_id))
        [await cleaner.add(message.message_id) for message in messages]

    else:
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо большое, скоро вам придёт ексель файл'
                                    f'\nДля добавления нового отчёта нажмите в меню ОТПАРВИТЬ ОТЧЁТ',
                               reply_markup=main_kb.main_kb)
        # TODO добавить здесь отправку ексель файла юзеру
        await state.clear()

    [await cleaner.add(m.message_id) for m in messages]
    await cleaner.purge()


@router.callback_query(PaginationCallbackFactory.filter(F.action.in_(["next", "previous"])))
async def paginator(query: CallbackQuery, callback_data: PaginationCallbackFactory):
    if "objects" in query.data:
        await query.message.edit_text(
            text="Выберите объект",
            reply_markup=ObjectInlineKeyboard(url=callback_data.url)
        )
    elif "categories" in query.data:
        await query.message.edit_text(
            text="Выберите категорию",
            reply_markup=CategoryInlineKeyboard(url=callback_data.url, object_id=None)
        )

    elif "work_types" in query.data:
        await query.message.edit_text(
            text="Выберите тип работ",
            reply_markup=TypeInlineKeyboard(url=callback_data.url, category_id=None)
        )