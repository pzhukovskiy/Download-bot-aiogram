from aiogram import Bot, types, asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#---------------Функция старт------------------------------
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    first_name = message.from_user['first_name']#Получение имени
    last_name = message.from_user['last_name']#Получение фамилии
    user_id = message.from_user['username']#Получение имени пользователя
    author = f'{user_id}'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=file1, callback_data="file1"))
    keyboard.add(types.InlineKeyboardButton(text=file2, callback_data="file2"))
    await message.answer(f"{first_name} {last_name} @{author}")
    await message.answer("Выберите файл, который хотите скачать", reply_markup=keyboard)
    file = open("File_info.txt", "a+")
    file.write(f"Файл скачал {first_name} {last_name}, @{author}\n")
    file.close()
#---------------Логика скачивания файла------------------
    @dp.callback_query_handler(text=['file1'])#README.txt
    async def command_file1(call: types.CallbackQuery):
        await asyncio.sleep(1)
        await call.message.answer_document(open(file1, 'rb'))
        await call.message.edit_reply_markup(reply_markup=None)
    @dp.callback_query_handler(text=['file2'])#config.py
    async def command_file2(call: types.CallbackQuery):
        await asyncio.sleep(1)
        await call.message.answer_document(open(file2, 'rb'))
        await call.message.edit_reply_markup(reply_markup=None)

#---------------Панель администратора------------------
@dp.message_handler(commands=['admin_panel'])
async def admin_panel(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Пользователи", callback_data="users"))
    await message.answer("Выберите действие", reply_markup=keyboard)

#---------------Показать пользователей------------------
    @dp.callback_query_handler(text=['users'])
    async def command_users(call: types.CallbackQuery):
        await asyncio.sleep(1)
        await call.message.edit_reply_markup(reply_markup=None)
        user_id = message.from_user['username']
        author = f'{user_id}'
        with open("File_info.txt", "r") as f:
            for line in f: 
                first_part = f.read()
                await message.answer(line)       

if __name__ == '__main__':
    executor.start_polling(dp)