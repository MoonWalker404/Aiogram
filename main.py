import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание inline-клавиатуры
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
    [InlineKeyboardButton(text="Новости", callback_data='news')],
    [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /minitraining')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=inline_keyboard_test)

@dp.callback_query(F.data == 'news')
async def news(callback_query: CallbackQuery):
    await callback_query.answer("Новости подгружаются", show_alert=True)
    await callback_query.message.edit_text('Вот свежие новости!', reply_markup=inline_keyboard_test)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
