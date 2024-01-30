import asyncio

from aiogram import executor

from create_bot import dp
from handlers import setup_points, setup_registration
from functions import check_website_changes


def main():
    setup_points(dp)
    setup_registration(dp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_website_changes())
    main()
    executor.start_polling(dp, skip_updates=True)
