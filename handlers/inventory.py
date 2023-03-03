from aiogram.dispatcher import FSMContext
from bot import dp
from aiogram import filters, types
from models import User
from service import inventory


@dp.callback_query_handler(filters.Text(startswith='inv_spirit'), state='*')
async def inv_injector(cb: types.CallbackQuery):
    user_id = int(cb.data.replace('inv_spirit_', ''))
    user = User.get_by_id(user_id)
    await inventory.use_spirit(cb.message, user)


@dp.callback_query_handler(filters.Text(startswith='drink_spirit_'), state='*')
async def drink_spirit(cb: types.CallbackQuery):
    user_id = int(cb.data.replace('drink_spirit_', ''))
    user = User.get_by_id(user_id)
    await inventory.drink_spirit(cb.message, user)


@dp.callback_query_handler(filters.Text(startswith='des_'), state='*')
async def des_spirit(cb: types.CallbackQuery, state: FSMContext):
    user_id = int(cb.data.replace('des_', ''))
    user = User.get_by_id(user_id)
    await inventory.des_spirit(cb.message, user, state)


@dp.callback_query_handler(filters.Text(startswith='inv_vaccine_'), state='*')
async def des_spirit(cb: types.CallbackQuery, state: FSMContext):
    user_id = int(cb.data.replace('inv_vaccine_', ''))
    user = User.get_by_id(user_id)
    await inventory.use_vaccine(cb.message, user, state)
