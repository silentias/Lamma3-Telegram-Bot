import sqlite3
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from groq import *
from config import api_lamma3

con = sqlite3.connect('database/users.db')
cursor = con.cursor()

router = Router()

dialog_history = []

client = Groq(
   api_key=api_lamma3
)

models = ["gemma-7b-it", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]

class Reg(StatesGroup):
    search = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Reg.search)
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    cursor.execute(f"SELECT name FROM users WHERE id = '{user_id}'")
    if not(cursor.fetchall()):
        cursor.execute(f"INSERT INTO users (id, name) VALUES ('{user_id}', '{user_name}')")
    cursor.execute(f"SELECT name FROM users WHERE id = '{user_id}'")
    result_select = cursor.fetchall()
    print(result_select)
    await message.answer(f'Привет {result_select[0][0]}, я нейросеть c бесплатным API, мною можно пользоваться без VPN, благодаря тому, что бот размещен на сервере в Нидерландах\n\nБот помнит историю сообщений, вы можете задавать наводящие вопросы, если ответ был не полным.\n\nНапиши мне запрос и я быстро на него отвечу.\n\n<i>Сделано 419 группой</i>', parse_mode="HTML")

@router.message(Reg.search)
async def cmd_reg(message: Message, state: FSMContext):
    await state.update_data(search=message.text)
    data = await state.get_data()
    search = data["search"]
    dialog_history.append({
        "role": "user",
        "content": search,
    })

    chat_completion = client.chat.completions.create(
        messages=dialog_history,
        model=models[1],
    )

    response = chat_completion.choices[0].message.content
    await state.set_state(Reg.search)
    await message.answer(response)

@router.message(F.photo)
async def message_photo(message: Message):
    await message.answer('Бот не обрабатывает фотографии')
