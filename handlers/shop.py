from bot import dp
from aiogram import filters, types
from service import shop


@dp.callback_query_handler(filters.Text(startswith='buy_injector_'))
async def buy_injector(cb: types.CallbackQuery):
    await shop.buyInjector(cb)


@dp.callback_query_handler(filters.Text(startswith='buy_cotton_'))
async def buy_cotton(cb: types.CallbackQuery):
    await shop.buyCotton(cb)


@dp.callback_query_handler(filters.Text(startswith='buy_spirit_'))
async def buy_spirit(cb: types.CallbackQuery):
    await shop.buyspirit(cb)


@dp.callback_query_handler(filters.Text(startswith='buy_vaccine_'))
async def buy_spirit(cb: types.CallbackQuery):
    await shop.buy_vaccine(cb)
