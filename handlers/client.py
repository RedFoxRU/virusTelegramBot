import aiogram
from bot import dp
from aiogram import types, filters
from models import User, Group, Equation
from service import filters as fl, qVirus, shop, inventory
from texts import client as texts, templates
from loguru import logger
import random
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Job(StatesGroup):
    work = State()


@dp.message_handler(fl.IsReply(), state='*')
async def changeChance(msg: types.Message, state: FSMContext):
    group, g_ = Group.get_or_create(tgid=msg.chat.id)
    if g_:
        group.save()
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.chances += 1
    user.save()


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['sv'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['sv'], state='*')
async def gdonateHandler(msg: types.Message, state: FSMContext):
    group, g_ = Group.get_or_create(tgid=msg.chat.id)
    if g_:
        group.save()
    if group.treas >= 5000 and not group.vaccine_start_dt and not group.is_vaccine:
        group.vaccine_start_dt = datetime.datetime.now()
        group.treas -= 5000
        group.save()
        await msg.answer(texts.VACCINE_START_DEVELOP)
    else:
        await msg.answer(texts.TREAS_NOT_HAVE_MONEY)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['gprofile'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['gprofile'], state='*')
async def gdonateHandler(msg: types.Message, state: FSMContext):
    group, g_ = Group.get_or_create(tgid=msg.chat.id)
    zeroInfectedName = ""
    if group.zero_infected:
        user = User.get_by_id(group.zero_infected)
        zeroInfectedName = user.full_name
    else:
        zeroInfectedName = '✖️'
    is_vaccine = ''
    if group.is_vaccine:
        is_vaccine = '✅'
    else:
        is_vaccine = '✖️'

    await msg.answer(templates.G_PROFILE.format(chat=msg.chat.title, zero_pac=zeroInfectedName, ifecteds=group.infected_users, vaccine=is_vaccine, money=group.treas))


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['gdonate'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['gdonate'], state='*')
async def gdonateHandler(msg: types.Message, state: FSMContext):
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    argvs = msg.text.split(' ')
    if len(argvs) > 1:
        hmDonate = int(argvs[1])
        if user.money < hmDonate or hmDonate <= 0:
            await msg.answer(texts.U_NOT_HAVE_THIS_MONEY.format(money=user.money))
            return None
        group, g_ = Group.get_or_create(tgid=msg.chat.id)
        group.treas += hmDonate
        group.save()
        user.money -= hmDonate
        user.save()
        await msg.answer(texts.USER_DONATE.format(name=msg.from_user.full_name, money=hmDonate))
    else:
        await msg.answer(texts.GDONATE_WRONG_ARGV)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['money'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['money'], state='*')
async def moneyHandler(msg: types.Message, state: FSMContext):
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    await msg.answer(texts.BALANCE.format(name=msg.from_user.full_name, balance=user.money))


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['shop'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['shop'], state='*')
async def shopHandler(msg: types.Message, state: FSMContext):
    await shop.getShop(msg)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['invent'])
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['invent'])
async def inventoryHandler(msg: types.Message, state: FSMContext):
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    await inventory.outputInventory(msg, user)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['profile'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['profile'], state='*')
async def profileHandler(msg: types.Message, state: FSMContext):
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    is_infect = ''
    if user.is_infected:
        is_infect = '✅'
    else:
        is_infect = '✖️'

    await msg.answer(templates.PROFILE.format(name=msg.from_user.full_name, is_infect=is_infect, money=user.money, infect_dt=user.infected_dt.strftime("%Y-%m-%d %H:%M:%S") if user.infected_dt != None else '✖️', chances=round(user.chances/(5000+user.chances)*100, 2), chances_mute=round(user.chances/(15000+user.chances)*100, 2)))


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['pay'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['pay'], state='*')
async def jobHandler(msg: types.Message, state: FSMContext):
    user_from, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    argvs = msg.text.split(' ')
    if len(argvs) > 2 and int(argvs[2]) > 0 and user_from.money >= int(argvs[2]):
        user_to = User.get_or_none((User.username == argvs[1].replace('@', '')) & (User.group == msg.chat.id))
        user_from.money -= int(argvs[2])
        user_to.money += int(argvs[2])
        user_from.save()
        user_to.save()
        await msg.answer(texts.PAYMENT_TO_PLAYER.format(from_user=user_from.full_name, to_user=user_to.full_name, hm=argvs[2]))
    elif user_from.money < int(argvs[2]):
        await msg.answer(texts.PAYMENT_NOT_HAVE_MUCH_MONEY)
    else:
        await msg.answer(texts.PAYMENT_WRONG_ARGVS)

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), commands=['job'], state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), commands=['job'], state='*')
async def jobHandler(msg: types.Message, state: FSMContext):
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)

    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    if not user.job_dt or (datetime.datetime.now() - user.job_dt).seconds >= 4*60*60:
        equatLen = Equation.select().count()
        equat = Equation.get_by_id(random.randint(1, equatLen))
        try:
            await msg.bot.send_message(msg.from_user.id, text=equat.equat, parse_mode='html')
        except aiogram.utils.exceptions.CantInitiateConversation:
            await msg.reply('Вы должны первыми написать мне.')
            return None
        user.job_dt = datetime.datetime.now()
        user.save()
        state = dp.current_state(chat=msg.from_user.id, user=msg.from_user.id)
        await state.set_data({'chatid': msg.chat.id, 'eqID': equat.id})
        await state.set_state(Job.work)
    else:
        await msg.reply('У вас уже есть работа, если выполнили, то ожидайте.')


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), state=Job.work)
async def jobPrivateHandler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    equat = Equation.get_by_id(data['eqID'])
    if float(msg.text) == float(equat.answer):
        logger.info(msg.from_user)
        user = User.get((User.tgid == msg.from_user.id)
                        & (User.group == data['chatid']))
        logger.info(user.full_name)
        user.money += equat.money
        user.save()
        await msg.reply(f'Верно, вам начисленно {equat.money} монет')

        await state.finish()
    else:
        await msg.reply('Не верно')


@dp.message_handler(fl.IsInfected(), filters.ChatTypeFilter(types.ChatType.SUPERGROUP), state='*')
@dp.message_handler(fl.IsInfected(), filters.ChatTypeFilter(types.ChatType.GROUP), state='*')
async def useGen(msg: types.Message, state: FSMContext):
    await qVirus.vaccine_done(msg)

    right = await msg.bot.get_my_default_administrator_rights()
    if right['can_delete_messages']:
        user = User.get(
            (User.tgid == msg.from_user.id) & (User.group == msg.chat.id))
        await qVirus.mutate(msg, user)
        if user.gen >= 1:
            await qVirus.virusGen1(msg, user)
        if user.gen >= 2:
            await qVirus.virusGen2(msg, user)
    else:
        await msg.answer(texts.CANT_DELETE)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), state='*')
async def messageHandler(msg: types.Message, state: FSMContext):
    group, g_ = Group.get_or_create(tgid=msg.chat.id)
    await qVirus.vaccine_done(msg)
    user, _ = User.get_or_create(tgid=msg.from_user.id, group=msg.chat.id)
    user.username = msg.from_user.username
    user.full_name = msg.from_user.full_name
    user.save()
    if not user.is_infected and not user.is_imune:
        if not user.try_infect or (datetime.datetime.now() - user.try_infect).seconds >= 4*60*60:
            user.try_infect = datetime.datetime.now()
            user.save()
            if random.choices([True, False], [user.chances, 5000])[0]:
                if group.infected_users == 0:
                    group.zero_infected = msg.from_user.id
                group.infected_users += 1
                user.gen = 1
                user.is_infected = True
                user.infected_dt = datetime.datetime.now()
                user.save()
                group.save()
                await msg.answer(texts.INFECTED.format(name=msg.from_user.full_name))
