import asyncio
import logging
import handlers
from config import BOT_API_TOKEN
from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(BOT_API_TOKEN)
    dp = Dispatcher()

    dp.include_routers(handlers.router)

    dp['bot'] = bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
