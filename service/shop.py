from aiogram import types
from loguru import logger
from models import User, Inventory, Price, Group
import random
import utils
from texts import templates, client

async def getShop(msg: types.Message):
    prices = Price.get_by_id(1)
    inkb = types.InlineKeyboardMarkup()

    inkb.add(types.InlineKeyboardButton(f'Шприц | {prices.injector}',callback_data=f'buy_injector_{msg.chat.id}'))
    inkb.add(types.InlineKeyboardButton(f'Вата на 5 раз | {prices.cotton}',callback_data=f'buy_cotton_{msg.chat.id}'))
    inkb.add(types.InlineKeyboardButton(f'Спирт 200 мл | {prices.spirit}',callback_data=f'buy_spirit_{msg.chat.id}'))

    group = Group.get(Group.tgid == msg.chat.id)
    if group.is_vaccine:
        inkb.add(types.InlineKeyboardButton(f'Вакцина | {prices.vaccine}',callback_data=f'buy_vaccine_{msg.chat.id}'))
    await msg.bot.send_message(msg.from_user.id, client.SHOP, reply_markup=inkb)

async def buyInjector(cb: types.CallbackQuery):
    groupId = cb.data.replace('buy_injector_', '')
    user = User.get( (User.tgid == cb.from_user.id) & (User.group == int(groupId)) )
    prices = Price.get_by_id(1)
    if user.money >= prices.injector:
        logger.info(prices.injector)
        logger.info(user.money)
        user.money -= prices.injector
        inventory, _ = Inventory.get_or_create(user=user.id)
        inventory.injector += 1
        inventory.save()
        await cb.message.answer(client.SUCCESS_BUY.format(item='шприц', price=prices.injector))
    else:
        await cb.message.answer(client.NOT_HAVE_MONEY)

async def buyCotton(cb: types.CallbackQuery):
    groupId = cb.data.replace('buy_cotton_', '')
    user = User.get( (User.tgid == cb.from_user.id) & (User.group == int(groupId)) )
    prices = Price.get_by_id(1)
    if user.money >= prices.cotton:
        user.money -= prices.cotton
        inventory, _ = Inventory.get_or_create(user=user.id)
        inventory.cotton += 1
        inventory.save()
        await cb.message.answer(client.SUCCESS_BUY.format(item='шприц', price=prices.cotton))
    else:
        await cb.message.answer(client.NOT_HAVE_MONEY)

async def buyspirit(cb: types.CallbackQuery):
    groupId = cb.data.replace('buy_spirit_', '')
    user = User.get( (User.tgid == cb.from_user.id) & (User.group == int(groupId)) )
    prices = Price.get_by_id(1)
    if user.money >= prices.spirit:
        user.money -= prices.spirit
        inventory, _ = Inventory.get_or_create(user=user.id)
        inventory.spirit += 1
        inventory.save()
        await cb.message.answer(client.SUCCESS_BUY.format(item='шприц', price=prices.spirit))
    else:
        await cb.message.answer(client.NOT_HAVE_MONEY)