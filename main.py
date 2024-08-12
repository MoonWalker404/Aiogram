import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
from gtts import gTTS
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound2.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.mp3")
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.mp3")

@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
    list = [
        'https://img.desktopwallpapers.ru/animals/pics/wide/1920x1080/3de2df8acf4496612b25bf70e91f61f3.jpg',
        'https://amiel.club/uploads/posts/2022-03/1647608290_11-amiel-club-p-milie-kartinki-s-kotikom-15.jpg',
        "https://koshka.top/uploads/posts/2021-12/1638847770_82-koshka-top-p-ochen-khoroshie-kotiki-87.jpg"
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого какая фотка', 'Непонятно что это такое', "Не отправляй мне это больше!"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект (ИИ) — это отдельное направление компьютерных наук, которое занимается разработкой систем, способных анализировать информацию и решать задачи аналогично человеку.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /photo \n /help')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветики, {message.from_user.first_name}")

@dp.message()
async def start(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тестируем')

async def main():
    await dp.start_polling(bot)


