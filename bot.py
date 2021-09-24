import logging

from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import categories
import tasks

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
USER_ID = os.getenv("TELEGRAM_USER_ID")



bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def extract_args(args):
    return args.split()[1:]


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=["new", "add"])
async def add_task(message: types.Message):
    args = extract_args(message.text)
    try:
        task = tasks.add_task(args)
    except tasks.NotCorrectMessage as e:
        await message.answer(str(e))
        return None
    await message.reply(f"Task {task.text} added")


@dp.message_handler(lambda message: message.text.startswith("/del"))
async def del_task(message: types.Message):
    row_id = int(message.text[4:])
    tasks.delete_task(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=["cat"])
async def show_category_info(message: types.Message):
    category_list = categories.get_category_list()

    all_category_message = [
        f"{category.name}  —  for show all {category.name} tasks type {' '.join([f'/{alias}' for alias in category.aliases])}"
        for category in category_list
    ]
    answer_message = "\n\n".join(all_category_message)

    await message.answer(answer_message)


@dp.message_handler(commands=["all"])
async def show_all_tasks(message: types.Message):
    all_tasks = tasks.get_all_tasks()
    all_tasks_message = [
        f"{task.text} — {task.category_id}. Type /del{task.id} for deleting"
        for task in all_tasks
    ]
    answer_message = "\n\n".join(all_tasks_message)

    await message.answer(answer_message)


@dp.message_handler(commands=["ali"])
async def _show_category_aliases(message: types.Message):
    answer_message = ", ".join(categories.get_category_aliases_list())

    await message.answer(answer_message)


@dp.message_handler(commands=categories.get_category_aliases_list())
async def show_category_tasks(message: types.Message):
    alias = message.text.split()[0]
    if alias in ["/daily", "/d"]:
        category_tasks = tasks.get_category_tasks("daily")
    elif alias in ["/hourly", "/h"]:
        category_tasks = tasks.get_category_tasks("hourly")
    elif alias in ["/single", "/s", "/one"]:
        category_tasks = tasks.get_category_tasks("single")
    elif alias in ["/alarm", "/a"]:
        category_tasks = tasks.get_category_tasks("alarm")
    tasks_message = [
        f"{task.text} — {task.category_id}. Type /del{task.id} for deleting"
        for task in category_tasks
    ]
    answer_message = "\n\n".join(tasks_message)

    await message.answer(answer_message)


@dp.message_handler(commands=["change"])
async def change_task_type(message: types.Message):
    args = extract_args(message.text)
    """
    To hourly or daily
    :param message: 
    :return: 
    """
    pass


@dp.message_handler(commands=["daily_freq"])
async def change_daily_frequency(message: types.Message):
    pass


@dp.message_handler(commands=["hourly_freq"])
async def change_hourly_frequency(message: types.Message):
    pass


@dp.message_handler(commands=["alarm_freq"])
async def change_alarm_frequency(message: types.Message):
    pass


async def remind_tasks(freq):
    reminder_tasks = tasks.get_category_tasks(freq)
    if reminder_tasks:
        tasks_message = [
            f"You need to do {task.category_id} {task.text}. Type /del{task.id} for deleting"
            for task in reminder_tasks
        ]
        answer_message = "\n\n".join(tasks_message)
        await bot.send_message(USER_ID, answer_message)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(remind_tasks, "interval", seconds=4, args=("alarm",))
    scheduler.add_job(remind_tasks, "interval", seconds=7, args=("hourly",))
    scheduler.add_job(remind_tasks, "interval", seconds=10, args=("daily",))
    scheduler.start()

    executor.start_polling(dp, skip_updates=True)
