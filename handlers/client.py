from bot import dp
from aiogram import types, filters
from models import User, Group

import random, datetime


@dp.message_handler(commands=['start'])
async def start_func(msg: types.Message):
    pass


@dp.message_handler()
async def messageHandler(msg: types.Message):
    user, _ = User.get_or_create(tgid=msg.from_user.id)
    if _:
        user.save()
    if datetime.datetime.now().hour in [12,13,14,15]:
        pass