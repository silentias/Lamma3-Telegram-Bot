import asyncio
from aiogram import Bot, Dispatcher
from config import token
from messages import router

async def main():
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('Бот отключен')