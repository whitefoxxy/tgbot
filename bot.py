import asyncio
import datetime
import random

from aiogram import Bot, Dispatcher
from aiogram import types

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
            types.KeyboardButton(text="Работа"),
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


async def send_every_5_minute(user_id):
    await key.bot.send_message(chat_id=user_id, text="Я не знаю когда запуститься")


def end_of_day(user_id):
    if key.user_id_work[user_id][0].flag_sleep:
        data_in_table(key.user_id_work[user_id][0])
        key.user_id_work[user_id][0].incr_var(2)
        key.user_id_work[user_id][0].flag_sleep = False

async def cure_for_N():
    await key.bot.send_message(chat_id=1404348569, text='Пришло время для лекарства')
def set_cure_job():
    key.scheduler.add_job(cure_for_N, 'cron', day_of_week='*/2', hour=16, minute=0)

def set_new_user_jobs_morning(user_id):  # задание работы на каждое утро
    user = key.user_id_work[user_id][0]
    h = (((key.user_id_work[user_id][-1] + 59) % 60) == 59)
    if h and (key.user_id_work[user_id][-2] - 1) == -1:
        job_pred = key.scheduler.add_job(end_of_day, "cron", hour=23,
                                         minute=((key.user_id_work[user_id][-1] + 59) % 60), second=50, args=[user_id])
    elif h:
        job_pred = key.scheduler.add_job(end_of_day, "cron", hour=key.user_id_work[user_id][-2] - 1,
                                         minute=((key.user_id_work[user_id][-1] + 59) % 60), second=50, args=[user_id])
    else:
        job_pred = key.scheduler.add_job(end_of_day, "cron", hour=key.user_id_work[user_id][-2],
                                         minute=((key.user_id_work[user_id][-1] + 59) % 60), second=50, args=[user_id])
    job0 = key.scheduler.add_job(morning, "cron", hour=key.user_id_work[user_id][-2],
                                 minute=key.user_id_work[user_id][-1], second=0, args=[key.bot, user_id])
    user.set_time_0(job_pred, job0, ch=key.user_id_work[user_id][-2], m=key.user_id_work[user_id][-1])


async def send_after_work():
    await key.bot.send_message(chat_id=1404348569, text='Время работы истекло, пора кушать)')
    key.user_id_work[1404348569][0].work = False
    set_new_job(1404348569, minute=5)


def set_new_job(user_id, hour=0, minute=0, work=False):
    if work:
        job = key.scheduler.add_job(send_after_work, "cron", hour=13)
    elif hour != 0:
        job = key.scheduler.add_job(send_every_X_hour, "interval", hours=hour,
                                    args=[user_id, hour])
    elif minute == 15:
        job = key.scheduler.add_job(send_every_15_minute, "interval", minutes=minute,
                                    args=[user_id])
    elif minute == 5 and not key.user_id_work[user_id][0].work:
        job = key.scheduler.add_job(send_every_5_minute, "interval", minutes=minute,
                                    args=[user_id])
    else:
        if datetime.datetime.now().hour > 12:
            key.user_id_work[user_id][0].work = False
            job = key.scheduler.add_job(send_every_5_minute, "interval", minutes=minute,
                                        args=[user_id])

    key.user_id_work[user_id][0].set_new_var_job(job)


def data_in_table(user: key.User):
    user.data_in_table()
    key.con.commit()


def save_csv():
    for k in key.user_id_work.keys:
        with open('/root/user_my.csv', 'w+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(
                [key.user_id_work[k][0].ADDRESS] + [key.user_id_work[k][0].t0_ch] + [key.user_id_work[k][0].t0_m] + [
                    key.user_id_work[k][0].eda] + [key.user_id_work[k][0].nedo_eda])


def read_csv():
    with open('/root/user_my.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            key.user_id_work[int(row[0])] = [key.User(int(row[0]), key.con.cursor()), int(row[0]), int(row[1]),
                                             int(row[2])]
            set_new_user_jobs_morning(int(row[0]))


# Запуск бота
async def my():
    bot = Bot(token=open("ass.txt").readline())
    key.bot = bot

    dp = Dispatcher()
    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)

    con = sqlite3.connect("stat_FBot.db", check_same_thread=False)
    # con = sqlite3.connect("/root/stat_FBot.db", check_same_thread=False)
    key.con = con

    scheduler = AsyncIOScheduler()
    scheduler.start()

    key.scheduler = scheduler
    await dp.start_polling(bot)
    read_csv()


if __name__ == "__main__":
    asyncio.run(my())
