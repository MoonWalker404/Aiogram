# 1. Создайте новую базу данных school_data.db.
# В этой базе данных создайте таблицу students с колонками:
# id (INTEGER, PRIMARY KEY, AUTOINCREMENT) name (TEXT) age (INTEGER) grade (TEXT)

# 2. Создайте Телеграм-бота, который запрашивает у пользователя имя,
# возраст и класс (grade), в котором он учится. Сделайте так чтоб бот
# сохранял введенные данные в таблицу students базы данных school_data.db.

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, WEATHER_API_KEY
import sqlite3
import aiohttp
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
	conn = sqlite3.connect('school_data.db')
	cur = conn.cursor()
	cur.execute('''
	CREATE TABLE IF NOT EXISTS students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	grade TEXT NOT NULL)
	''')
	conn.commit()
	conn.close()

init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Почет и слава учащимся! Напишите Ваше имя:')
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Напишите Ваш возраст:")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("На каком курсе проходите обучение?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    school_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',(school_data['name'], school_data['age'], school_data['grade']))
    conn.commit()
    conn.close()

    response_message = (
        f"Данные успешно сохранены!\n\n"
        f"Имя: {school_data['name']}\n"
        f"Возраст: {school_data['age']}\n"
        f"Класс: {school_data['grade']}"
    )

    await message.answer(response_message)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
