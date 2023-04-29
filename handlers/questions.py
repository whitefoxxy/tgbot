import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
import bot
from keyboards import key

router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        text=str(message.chat.id)
    )


@router.message(Command("help"))  # [2]
async def cmd_help(message: Message):
    key.scheduler_g.print_jobs()


@router.message(Text(text="Через 1 час", ignore_case=True))
async def answer_1_hour(message: Message):
    bot.set_new_job(hour=1)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 1 час...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 2 часа", ignore_case=True))
async def answer_2_hour(message: Message):
    bot.set_new_job(hour=2)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 2 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 3 часа", ignore_case=True))
async def answer_3_hour(message: Message):
    bot.set_new_job(hour=3)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 3 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 4 часа", ignore_case=True))
async def answer_4_hour(message: Message):
    bot.set_new_job(hour=4)
    await message.answer(
        f"{random.choice(key.waiting_key)} Жду 4 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Сон", ignore_case=True))
async def answer_sleep(message: Message):
    if key.job != None:
        key.job.remove()
        key.job = None
    await message.answer(
        "Доброй ночи",
        reply_markup=ReplyKeyboardRemove()
    )
    key.chet = 0
    key.perec = 0


@router.message(Text(text="Поела", ignore_case=True))
async def answer_eated(message: Message):
    key.job.remove()
    key.job = None
    key.chet += 1

    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )
    await key.bot_g.send_message(chat_id=605850528, text=f"Поела {key.chet}")
    await bot.set_button()


@router.message(Text(text="Перекусила", ignore_case=True))
async def answer_eated_no(message: Message):
    key.job.remove()
    key.job = None
    key.perec += 1

    await message.answer(
        "Хоть так)",
        reply_markup=ReplyKeyboardRemove()
    )
    await key.bot_g.send_message(chat_id=605850528, text=f"перекусила {key.perec}")
    await bot.set_button()


@router.message(Text(text="Статистика", ignore_case=True))
async def answer_stat(message: Message):
    await message.answer(
        "Вот твои данные, Лиса"
    )
    await bot.set_button(sett=True)


@router.message(Text(text="Назад", ignore_case=True))
async def answer_back(message: Message):
    await message.answer(
        "Ня"
    )
    await bot.set_button()


@router.message(Text(text="Камень-ножницы-бумага", ignore_case=True))
async def answer_random(message: Message):
    await message.answer(
        random.choice(['камень', 'ножницы', 'бумага'])
    )
