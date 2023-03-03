from aiogram import types
from models import User, Group
import random
import datetime
import aiogram
import utils
from texts import templates, client


async def virusGen1(msg: types.Message, user: User):
    k = (datetime.datetime.now() - user.infected_dt).days*2
    if k <= 10:
        k = 10

    if random.choices([True, False], [k, 150])[0]:
        text = msg.text.split(' ')
        outputWord = ""
        outputText = ""
        if len(text) != 1:
            rInt = random.randint(0, len(text)-1)
            for i in range(0, len(text[rInt])):
                try:
                    outputWord += utils.symbolDict[text[rInt][i]]
                except:
                    pass
            text[rInt] = outputWord
            rInt = random.randint(0, len(text)-1)
            word = list(text[rInt])
            random.shuffle(word)
            text[rInt] = "".join(word)
            outputText = ' '.join(text)
        else:
            for i in range(0, len(text[0])):
                try:
                    outputWord += utils.symbolDict[text[0][i]]
                except:
                    pass
            text[0] = outputWord
            outputText = ' '.join(text)

        try:
            await msg.delete()
        except aiogram.utils.exceptions.MessageCantBeDeleted:
            await msg.answer(client.CANT_DELETE)
            return None
        await msg.answer(templates.QVIRUS.format(fullname=msg.from_user.full_name, message=outputText))


async def virusGen2(msg: types.Message, user: User):
    k = (datetime.datetime.now() - user.infected_dt).days
    if k <= 4:
        k = 5
    if random.choices([True, False], [k, 100])[0]:
        await msg.answer(client.SNAP.format(name=msg.from_user.full_name))
        await msg.delete()


async def mutate(msg: types.Message, user: User):
    if random.choices([True, False], [user.chances, 15000])[0]:
        user.gen += 1
        user.save()
        await msg.answer(client.MUTATE.format(name=msg.from_user.full_name))

async def vaccine_done(msg):
    group, g_ = Group.get_or_create(tgid=msg.chat.id)
    if group.vaccine_start_dt and (datetime.datetime.now() - group.vaccine_start_dt).days >= 2:
        group.is_vaccine = True
        group.vaccine_start_dt = None
        group.save()
        await msg.answer(client.DEVELOP_VACCINE_IS_DONE)
