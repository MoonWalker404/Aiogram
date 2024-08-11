import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://img.desktopwallpapers.ru/animals/pics/wide/1920x1080/3de2df8acf4496612b25bf70e91f61f3.jpg', 'https://amiel.club/uploads/posts/2022-03/1647608290_11-amiel-club-p-milie-kartinki-s-kotikom-15.jpg', "https://koshka.top/uploads/posts/2021-12/1638847770_82-koshka-top-p-ochen-khoroshie-kotiki-87.jpg"]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого какая фотка', 'Непонятно что это такое', "Не отправляй мне это больше!"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект (ИИ) — это отдельное направление компьютерных наук, которое занимается разработкой систем, способных анализировать информацию и решать задачи аналогично человеку.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())