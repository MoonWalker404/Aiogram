import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Простое меню с кнопками
@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Привет", callback_data="greet")],
        [InlineKeyboardButton(text="Пока", callback_data="goodbye")]
    ])
    await message.answer(f"Приветики, {message.from_user.first_name}!", reply_markup=keyboard)

@dp.callback_query(F.data == "greet")
async def greet(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Привет, {callback_query.from_user.first_name}!")

@dp.callback_query(F.data == "goodbye")
async def goodbye(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"До свидания, {callback_query.from_user.first_name}!")

# Задание 2: Кнопки с URL-ссылками
@dp.message(Command('links'))
async def links(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://rutube.ru/search/?query=новости")],
        [InlineKeyboardButton(text="Музыка", url="https://rutube.ru/search/?query=музыка")],
        [InlineKeyboardButton(text="Видео", url="https://rutube.ru/video/ceebfe705a5a60dc0a1a778fa409b0dd/")]
    ])
    await message.answer("Выберите ссылку:", reply_markup=keyboard)

# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)

@dp.callback_query(F.data == "show_more")
async def show_more(callback_query):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await bot.send_message(callback_query.from_user.id, "Выберите опцию:", reply_markup=keyboard)

@dp.callback_query(F.data == "option_1")
async def option_1(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали Опцию 1!")

@dp.callback_query(F.data == "option_2")
async def option_2(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы выбрали Опцию 2!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
