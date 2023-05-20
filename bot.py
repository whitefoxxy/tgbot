import asyncio
import datetime
import random

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from handlers import questions, different_types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards import key
import sqlite3
import csv


# ADDRESS = 1404348569  #


async def morning(bot, address):
    key.user_id_work[address][0].flag_sleep = True
    kb = [
        [
            types.KeyboardButton(text="Через 1 час"),
            types.KeyboardButton(text="Через 2 часа"),
            types.KeyboardButton(text="Перекусила"),
            types.KeyboardButton(text="Поела")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Жду когда покушаешь..."
    )
    await bot.send_message(chat_id=address, text=random.choice(key.morning_key), reply_markup=keyboard)


async def send_every_X_hour(user_id, hour):
    if hour == 1:
        await key.bot.send_message(chat_id=user_id, text="Прошёл 1 час, пора кушать!")
    else:
        await key.bot.send_message(chat_id=user_id, text=f"Прошло {hour} часа, пора кушать!")

    set_new_job(user_id, hour=0, minute=15)


async def send_every_15_minute(user_id):
    await key.bot.send_message(chat_id=user_id, text="Поешь, прошло 15 минут!")


async def set_button(user_id, sett=False):
    if sett:
        kb = [
            [
                types.KeyboardButton(text="Камень-ножницы-бумага"),
                types.KeyboardButton(text="График"),
                types.KeyboardButton(text="За день"),
                types.KeyboardButton(text="За неделю"),
                types.KeyboardButton(text="Назад")
            ],
        ]
    else:
        kb = [
            [
                types.KeyboardButton(text="Через 1 час"),
                types.KeyboardButton(text="Через 2 часа"),
                types.KeyboardButton(text="Через 3 часа"),
                types.KeyboardButton(text="Через 4 часа"),
                types.KeyboardButton(text="Перекусила"),
                types.KeyboardButton(text="Поела"),
                types.KeyboardButton(text="Статистика")
            ],
        ]
        if datetime.datetime.now().hour > 15:
            kb[0].append(types.KeyboardButton(text="Сон"))

    builder = ReplyKeyboardBuilder()
    for i in kb[0]:
        builder.add(i)
    builder.adjust(3)

    await key.bot.send_message(chat_id=user_id, text="Примите позу ожидания",
                               reply_markup=builder.as_markup(resize_keyboard=True,
                                                              input_field_placeholder="Жду твой выбор =)"))


def end_of_day(user_id):
    if key.user_id_work[user_id][0].flag_sleep:
        data_in_table(key.user_id_work[user_id][0])
        key.user_id_work[user_id][0].incr_var(n=2)
        key.user_id_work[user_id][0].flag_sleep = False


def set_new_user_jobs_morning(user_id):  # задание работы на каждое утро
    user = key.user_id_work[user_id][0]
    user.set_time_0(key.scheduler.add_job(end_of_day, "cron", hour=key.user_id_work[user_id][-2] * (
            ((key.user_id_work[user_id][-1] + 59) % 60) != 59) + (key.user_id_work[user_id][-2] - 1) * (((
                                                                                                                 key.user_id_work[
                                                                                                                     user_id][
                                                                                                                     -1] + 59) % 60) == 59),
                                          minute=(key.user_id_work[user_id][-1] + 59) % 60, second=50),
                    key.scheduler.add_job(morning, "cron", hour=key.user_id_work[user_id][-2],
                                          minute=key.user_id_work[user_id][-1], second=0, args=[key.bot]),
                    ch=key.user_id_work[user_id][-2], m=key.user_id_work[user_id][-1])


def set_new_job(user_id, hour=0, minute=0):
    if hour != 0:
        job = key.user_id_work[user_id][0].job = key.scheduler.add_job(send_every_X_hour, "interval", hours=hour,
                                                                       args=[user_id, hour])
    else:
        job = key.user_id_work[user_id][0].job = key.scheduler.add_job(send_every_15_minute, "interval", minutes=minute,
                                                                       args=[user_id])
    key.user_id_work[user_id][0].set_new_var_job(job)


def data_in_table(user: key.User):
    user.data_in_table()
    key.con.commit()


# Запуск бота
async def my():  # TODO: create save's
    bot = Bot(token=open("ass.txt").readline())
    key.bot = bot

    dp = Dispatcher()
    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)

    con = sqlite3.connect("/root/stat_FBot.db")
    key.con = con

    scheduler = AsyncIOScheduler()
    scheduler.start()

    key.scheduler = scheduler
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(my())
