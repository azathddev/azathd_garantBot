import asyncio
import logging
import time

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.handlers import router, db
from aiogram import Bot, Dispatcher
from config import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.DEBUG)


async def timeout_rooms():
    for room_id, ctime in db.get_times():
        if int(time.time()) - ctime > ROOM_EXPIRE_TIME:
            room = db.get_room(room_id)
            answer = ROOM_TIMEOUT_DELETED.replace("%id%", room_id)
            if room[0]:
                await bot.send_message(int(room[0]), answer)
            if room[1]:
                await bot.send_message(int(room[1]), answer)
            db.del_room(room_id)


async def main():
    dp.include_router(router)
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
    scheduler.add_job(timeout_rooms, 'cron', hour="*", minute="*")
    scheduler.start()
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Bot off already")


if __name__ == "__main__":
    asyncio.run(main())
