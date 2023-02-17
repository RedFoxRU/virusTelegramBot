from bot import dp
import handlers
import asyncio

async def main():
    dp.start_polling()
    


if __name__ == '__main__':
    asyncio.run(main)