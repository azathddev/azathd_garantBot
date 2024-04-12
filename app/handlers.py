import random
import time

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from app.database import Database
import app.keyboard as kb
from config import *

from icecream import ic


class Waiting(StatesGroup):
    password = State()
    choice = State()


db = Database('database.db')

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
    user_id = clbck.from_user.id
    chars = CHARS_LIST
    password = ''
    while True:
        for i in range(10):
            password += random.choice(chars)
        if password not in rooms:
            break
    buyer, seller = None, None
    if clbck.data == "seller":
        seller = user_id
    elif clbck.data == "buyer":
        buyer = user_id
    ic(clbck.data, user_id, password, buyer, seller)
    db.add_room(password, buyer, seller)
    answer = ROOM_CREATED.replace("%id%", password)
    await clbck.message.edit_text(answer)
    await clbck.answer("")


@router.message(Waiting.password)
async def join_password_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    ic(db.get_ids())
    if text in db.get_ids():
        room = db.get_room(text)
        ic(room)
        if room[0] and room[1]:
            await message.answer(ROOM_IS_FULL)
            return True
        if room[0]:
            room[1] = user_id
            answer = JOIN_SELLER.replace("%id%", text)
            await message.answer(answer)
            # рума готова
        elif room[1]:
            room[0] = user_id
            answer = JOIN_SELLER.replace("%id%", str(text))
            await message.answer(answer)
        db.update_room(text, room[0], room[1])
    else:
        await message.answer(ROOM_IS_NOT_FOUND)
