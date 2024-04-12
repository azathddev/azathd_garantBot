from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from config import *

start = [
    [InlineKeyboardButton(text=CREATE_BUTTON_TEXT, callback_data="create")],
    [InlineKeyboardButton(text=JOIN_BUTTON_TEXT, callback_data="join")]
]
start = InlineKeyboardMarkup(inline_keyboard=start)

choice = [
    [InlineKeyboardButton(text=BUYER_BUTTON_TEXT, callback_data="buyer")],
    [InlineKeyboardButton(text=SELLER_BUTTON_TEXT, callback_data="seller")]
]
choice = InlineKeyboardMarkup(inline_keyboard=choice)

