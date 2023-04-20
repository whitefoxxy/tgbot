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
        "Это здорово! Жду 1 час...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 2 часа", ignore_case=True))
async def answer_2_hour(message: Message):
    bot.set_new_job(hour=2)
    await message.answer(
        "Это здорово! Жду 2 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 3 часа", ignore_case=True))
async def answer_3_hour(message: Message):
    bot.set_new_job(hour=3)
    await message.answer(
        "Это здорово! Жду 3 часа...",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()


@router.message(Text(text="Через 4 часа", ignore_case=True))
async def answer_4_hour(message: Message):
    bot.set_new_job(hour=4)
    await message.answer(
        "Это здорово! Жду 4 часа...",
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


@router.message(Text(text="Поела", ignore_case=True))
async def answer_eated(message: Message):
    key.job.remove()
    key.job = None
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()

@router.message(Text(text="Поела", ignore_case=True))
async def answer_eated(message: Message):
    key.job.remove()
    key.job = None
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.set_button()