from datetime import datetime
import random
from aiogram.dispatcher import FSMContext
import aiogram
from texts import client as texts
from aiogram import types
from models import User, Inventory


async def outputInventory(msg: types.Message, user: User):
    inventory, _ = Inventory.get_or_create(user=user.id)
    if _:
        inventory.save()
    inkb = types.InlineKeyboardMarkup()
    inkb.add(types.InlineKeyboardButton(
        f"Шприц | {inventory.injector}", callback_data=f'inv_injector_{user.id}'))
    inkb.add(types.InlineKeyboardButton(
        f"Вата | {inventory.cotton}", callback_data=f'inv_cotton_{user.id}'))
    inkb.add(types.InlineKeyboardButton(
        f"Спирт | {inventory.spirit}", callback_data=f'inv_spirit_{user.id}'))
    if user.group.is_vaccine:
        inkb.add(types.InlineKeyboardButton(
            f"Вакцина | {inventory.vaccine}", callback_data=f'inv_vaccine_{user.id}'))
    try:
        await msg.bot.send_message(msg.from_user.id, texts.INVENTORY, reply_markup=inkb)
    except aiogram.utils.exceptions.CantInitiateConversation:
        await msg.reply(texts.I_CANT_WRITE_U)


async def use_spirit(msg: types.Message, user: User):
    inventory, _ = Inventory.get_or_create(user=user.id)
    if _:
        inventory.save()
    inkb = types.InlineKeyboardMarkup()
    inkb.add(types.InlineKeyboardButton(
        f"Выпить", callback_data=f'drink_spirit_{user.id}'))
    inkb.add(types.InlineKeyboardButton(
        f"Дезинфекция", callback_data=f'des_{user.id}'))
    try:
        await msg.bot.send_message(user.tgid, texts.SPIRIT_CHOOSE, reply_markup=inkb)
        await msg.delete()
    except aiogram.utils.exceptions.CantInitiateConversation:
        await msg.reply(texts.I_CANT_WRITE_U)


async def drink_spirit(msg: types.Message, user: User):
    inventory, _ = Inventory.get_or_create(user=user.id)
    if inventory.spirit >= 50:
        inventory.spirit -= 50
        if user.chances >= 15:
            user.chances -= 15
        else:
            user.chances = 0
        user.save()
        inventory.save()
        await msg.answer(texts.DRINK_SPIRIT)


async def des_spirit(msg: types.Message, user: User, state: FSMContext):
    inventory, _ = Inventory.get_or_create(user=user.id)
    if inventory.spirit >= 10 and inventory.cotton >= 1:
        inventory.spirit -= 10
        inventory.cotton -= 1
        inventory.save()
        await state.set_data({
            'des': True,
            'des_time': datetime.now()
        })
        await msg.answer(texts.DES_SUCCESS)


async def use_vaccine(msg: types.Message, user: User, state: FSMContext):
    inventory, _ = Inventory.get_or_create(user=user.id)
    if inventory.vaccine >= 1 and inventory.injector >= 1 and user.is_infected:
        data = await state.get_data()
        if 'des' in data and (datetime.now()-data['des_time']).secconds <= 60*2 and (datetime.now()-data['des_time']).days == 1:
            inventory.vaccine -= 1
            inventory.injector -= 1
            inventory.save()
            user.save()
            if random.choices([True, False], [3,97])[0]:
                user.is_imune = True
                user.is_infected = False
                user.infected_dt = None
                user.save()
                await msg.bot.send_message(user.group.tgid,texts.VACCINE_PLUS_IMUNE.format(name=user.full_name))
                await msg.answer(texts.VACCINE_PLUS_IMUNE.format(name=user.full_name))
            else:
                user.is_infected = False
                user.chances -= 200
                user.infected_dt = None
                user.save()
                await msg.bot.send_message(user.group.tgid,texts.VACCINE_USED.format(name=user.full_name))
                await msg.answer(texts.VACCINE_USED.format(name=user.full_name))
        else:
            inventory.vaccine -= 1
            inventory.injector -= 1
            inventory.save()
            user.chances += 200
            user.is_infected = False
            user.infected_dt = None
            user.save()
            await msg.bot.send_message(user.group.tgid,texts.VACCINE_BUT_NOT_DES.format(name=user.full_name))
            await msg.answer(texts.VACCINE_BUT_NOT_DES.format(name=user.full_name))
    elif user.is_infected:
        await msg.answer(texts.U_NOT_INFECTED)
    else:
        await msg.answer(texts.VACCINE_NOT_MUCH)

    await state.finish()