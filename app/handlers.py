import random
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

import app.keyboard as kb
from config import *


class Waiting(StatesGroup):
    password = State()
    choice = State()


rooms = {}
router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_MESSAGE, reply_markup=kb.start)


@router.callback_query(F.data == "create")
async def cmd_create(clbck: CallbackQuery):
    await clbck.message.edit_text(CREATE_MESSAGE, reply_markup=kb.choice)
    await clbck.answer("")


@router.callback_query(F.data == "join")
async def cmd_join(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Waiting.password)
    await clbck.message.edit_text(JOIN_MESSAGE)


@router.callback_query(F.data == "buyer")
@router.callback_query(F.data == "seller")
async def create_handler(clbck: CallbackQuery):
    user_id = clbck.message.from_user.id
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    while True:
        for i in range(10):
            password += random.choice(chars)
        if password not in rooms:
            break
    buyer = seller = None
    if F.data == "buyer":
        buyer = user_id
    elif F.data == "seller":
        seller = user_id
    rooms[password] = {"buyer": buyer,
                       "seller": seller}
    answer = ROOM_CREATED.replace("%id%", password)
    await clbck.message.edit_text(answer)
    await clbck.answer("")


@router.message(Waiting.password)
async def join_password_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    if rooms.get(text):
        if rooms[text]["buyer"] and rooms[text]["seller"]:
            await message.answer(ROOM_IS_FULL)
            return True
        if rooms[text]["buyer"]:
            rooms[text]["seller"] = user_id
            answer = JOIN_SELLER.replace("%id%", text)
            await message.answer(answer)
            # рума готова
        elif rooms[text]["seller"]:
            rooms[text]["buyer"] = user_id
            answer = JOIN_SELLER.replace("%id%", str(text))
            await message.answer(answer)
            # рума готова
    else:
        await message.answer(ROOM_IS_NOT_FOUND)
