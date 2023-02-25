from bot import dp
from aiogram import filters, types
from models import Equation

@dp.message_handler(filters.IDFilter(chat_id=[848150113]),commands=['addQ'])
async def addQ(msg:types.Message):
    argvs = msg.text.replace('/addQ', '').split(' ')
    argvs[0] = argvs[1].split('=')
    equat = Equation.create(equat=argvs[0][0],answer=argvs[0][1], money=argvs[2])
    equat.save()
    await msg.reply('Пример был добавлен')