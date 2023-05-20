import datetime
import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandObject
import bot
from keyboards import key

router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    if message.chat.id not in key.user_id_work.keys():
        key.user_id_work[message.chat.id] = [key.User(message.chat.id, key.con.cursor()), message.chat.id, 1, 0]
    await message.answer("По умолчанию время первого вызова 01:00 по МСК.\nВызовите /time HH:MM чтобы изменить это")
    bot.set_new_user_jobs_morning(message.chat.id)


@router.message(Command("time"))  # [2]
async def cmd_time(message: Message, command: CommandObject):
    if message.chat.id in key.user_id_work.keys():
        if ":" in command.args and command.args.count(":") == 1:
            key.user_id_work[message.chat.id][-2], key.user_id_work[message.chat.id][-1] = list(
                map(int, command.args.split(':')))
            bot.set_new_user_jobs_morning(message.chat.id)
        else:
            print("incorrect time: ", command.args)


@router.message(Command("restart"))  # [2]
async def cmd_restart():
    for user_id in list(key.user_id_work.keys()):
        key.bot.send_message(chat_id=user_id, text="Бот уходит на тех.работы. Прошу прощения за неудобства")


@router.message(Command("end"))  # [2]
async def cmd_end(message: Message):
    pass


@router.message(Command("help"))  # [2]
async def cmd_help():
    key.scheduler.print_jobs()


@router.message(Text(text="Через 1 час", ignore_case=True))
async def answer_1_hour(message: Message):
    bot.set_new_job(message.chat.id, hour=1)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 1 час...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button(message.chat.id)


@router.message(Text(text="Через 2 часа", ignore_case=True))
async def answer_2_hour(message: Message):
    bot.set_new_job(message.chat.id, hour=2)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 2 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button(message.chat.id)


@router.message(Text(text="Через 3 часа", ignore_case=True))
async def answer_3_hour(message: Message):
    bot.set_new_job(message.chat.id, hour=3)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 3 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button(message.chat.id)


@router.message(Text(text="Через 4 часа", ignore_case=True))
async def answer_4_hour(message: Message):
    bot.set_new_job(message.chat.id, hour=4)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 4 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button(message.chat.id)


@router.message(Text(text="Сон", ignore_case=True))
async def answer_sleep(message: Message):
    await message.answer(
        random.choice(key.nignt_key),
        reply_markup=ReplyKeyboardRemove()
    )
    bot.end_of_day(message.chat.id)


@router.message(Text(text="Поела", ignore_case=True))
async def answer_eated(message: Message):
    key.user_id_work[message.chat.id][0].delete_job()
    key.user_id_work[message.chat.id][0].incr_var(n=1)

    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )
    await key.bot.send_message(chat_id=605850528, text=f"Поела {key.user_id_work[message.chat.id][0].eda}")
    await bot.set_button(message.chat.id)


@router.message(Text(text="Перекусила", ignore_case=True))
async def answer_eated_no(message: Message):
    key.user_id_work[message.chat.id][0].delete_job()
    key.user_id_work[message.chat.id][0].incr_var()

    await message.answer(
        "Хоть так)",
        reply_markup=ReplyKeyboardRemove()
    )
    await key.bot.send_message(chat_id=605850528, text=f"перекусила {key.user_id_work[message.chat.id][0].nedo_eda}")
    await bot.set_button(message.chat.id)


@router.message(Text(text="Статистика", ignore_case=True))
async def answer_stat(message: Message):
    await message.answer(
        "Вот твои данные"
    )
    await bot.set_button(message.chat.id, sett=True)


@router.message(Text(text="Назад", ignore_case=True))
async def answer_back(message: Message):
    await bot.set_button(message.chat.id)


@router.message(Text(text="Камень-ножницы-бумага", ignore_case=True))
async def answer_random(message: Message):
    await message.answer(
        random.choice(['камень', 'ножницы', 'бумага'])
    )


@router.message(Text(text="График", ignore_case=True))
async def answer_graph(message: Message):
    await message.answer(
        "Функционал кнопки находится в разработке"
    )


@router.message(Text(text="За день", ignore_case=True))
async def answer_day_today(message: Message):
    await message.answer(
        f"Сегодня ты поела: {key.user_id_work[message.chat.id][0].eda} раз\nПерекусила: {key.user_id_work[message.chat.id][0].nedo_eda} раз")


@router.message(Text(text="За неделю", ignore_case=True))
async def answer_week_today(message: Message):
    eda, nedo_eda, n = 0, 0, 0
    for ed, per in key.user_id_work[message.chat.id].data_out_table():
        n += 1
        eda += ed
        nedo_eda += per

    await message.answer(
        f"За неделю(или {n} дней) ты поела: {eda} раз\nПерекусила: {nedo_eda} раз"
    )
