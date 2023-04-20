import asyncio
import datetime
import multiprocessing

from aiogram import Bot, Dispatcher
from aiogram import types

from handlers import questions, different_types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards import key

ADDRESS = 1404348569


async def morning(bot):  # утренние кнопки, отрабатывающиеся в 5 часов утра
    kb = [
        [
            types.KeyboardButton(text="Через 1 час"),
            types.KeyboardButton(text="Через 2 часа"),
            types.KeyboardButton(text="Поела")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Жду когда покушаешь..."
    )
    await bot.send_message(chat_id=ADDRESS, text="Напоминаю, надо кушать! Мяу", reply_markup=keyboard)


async def send_every_X_hour(hour):
    job = key.job
    bot = key.bot_g
    if hour == 1:
        await bot.send_message(chat_id=ADDRESS, text="Прошёл 1 час, пора кушать!")
    else:
        await bot.send_message(chat_id=ADDRESS, text=f"Прошло {hour} часа, пора кушать!")

    key.job.remove()
    key.job = None
    set_new_job(0, minute=15)


async def send_every_15_minute():
    bot = key.bot_g
    await bot.send_message(chat_id=ADDRESS, text="Поешь, прошло 15 минут!")


async def set_button():
    bot = key.bot_g
    if datetime.datetime.now().hour < 16:
        kb = [
            [
                types.KeyboardButton(text="Через 1 час"),
                types.KeyboardButton(text="Через 2 часа"),
                types.KeyboardButton(text="Через 3 часа"),
                types.KeyboardButton(text="Через 4 часа"),
                types.KeyboardButton(text="Поела")
            ],
        ]
    else:
        kb = [
            [
                types.KeyboardButton(text="Через 1 час"),
                types.KeyboardButton(text="Через 2 часа"),
                types.KeyboardButton(text="Через 3 часа"),
                types.KeyboardButton(text="Через 4 часа"),
                types.KeyboardButton(text="Сон"),
                types.KeyboardButton(text="Поела")
            ],
        ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Жду твой выбор =)"
    )
    await bot.send_message(chat_id=ADDRESS, text="Примите позу ожидания", reply_markup=keyboard)


def set_scheduled_jobs(scheduler, bot, *args, **kwargs):  # задание работы на каждое утро
    scheduler.add_job(morning, "cron", hour=1, minute=0, second=0, args=[bot])


def set_new_job(hour=0, minute=0, *args, **kwargs):
    if key.job != None:
        key.job.remove()
        key.job = None
    if hour != 0:
        key.job = key.scheduler_g.add_job(send_every_X_hour, "interval", hours=hour, args=[hour])
    else:
        key.job = key.scheduler_g.add_job(send_every_15_minute, "interval", minutes=minute, args=[])


# Запуск бота
async def my():
    bot = Bot(token=open("ass.txt").readline())
    key.bot_g = bot
    dp = Dispatcher()
    dp.include_routers(questions.router, different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler()
    scheduler.start()

    set_scheduled_jobs(scheduler, bot)
    key.scheduler_g = scheduler
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(my())
