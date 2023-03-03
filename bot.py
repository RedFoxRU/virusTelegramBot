from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScope

from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode='Markdown')
dp = Dispatcher(bot,storage=storage)


async def commandReger():
    await dp.bot.set_my_commands(
        [
            BotCommand(command='profile', description='Профиль'),
            BotCommand(command='job', description='Работа'),
            BotCommand(command='shop', description='Магазин'),
            BotCommand(command='gdonate', description='Пожертвовать в казну чата'),
            BotCommand(command='gprofile', description='Профиль чата'),
            BotCommand(command='sv', description='Начать разработку вакцины.'),
            BotCommand(command='invent', description='Инвентарь.'),
            BotCommand(command='pay', description='Перевести пользователю монеты.'),
         ]
        )
    