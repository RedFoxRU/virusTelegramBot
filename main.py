from bot import dp, commandReger
import handlers
import models
import asyncio
from service import filters as fl

async def main():
    await commandReger()
    dp.bind_filter(fl.IsReply)
    dp.bind_filter(fl.IsInfected)
    await dp.start_polling()
    


if __name__ == '__main__':
    asyncio.run(main())