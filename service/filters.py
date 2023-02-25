from aiogram import types
from aiogram.dispatcher.filters import Filter
from models import User


class IsInfected(Filter):
    key = "is_infected"

    async def check(self, message: types.Message) -> bool:
        if not message.from_user.is_bot:
            user = User.get_or_none(User.tgid == message.from_user.id)
            if user:
                return user.is_infected
            else:
                return False
        return False
        

class IsReply(Filter):
    key = "is_reply"

    async def check(self, message: types.Message) -> bool:
        if not message.from_user.is_bot:
            if message.reply_to_message:
                return True
            else:
                return False
        else:
            return False