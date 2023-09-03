from aiogram import Router, F
from aiogram.types import Message
from keyboards import key

router = Router()

@router.message(F.text)
async def message_with_text(message: Message):
    if message.chat.id == 1404348569:
        await key.bot.send_message(chat_id=605850528, text=message.text)
    elif message.chat.id == 1906153307:
        await key.bot.send_message(chat_id=1117720980, text=message.text)
    else:
        await message.answer("Это текстовое сообщение!")

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("Это GIF!")