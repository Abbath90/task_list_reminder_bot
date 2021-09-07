import sqlite3
import logging
import os
from typing import List, NamedTuple, Optional
import tasks
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
#API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def extract_args(args):
    return args.split()[1:]


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['new'])
async def add_task(message: types.Message):
    args = extract_args(message.text)
    try:
        task = tasks.add_task(args)
    except tasks.NotCorrectMessage as e:
        await message.answer(str(e))
        return None
    await message.reply(f'Task {task.text} added')


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_task(message: types.Message):
    row_id = int(message.text[4:])
    tasks.delete_task(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['all'])
async def show_all_tasks(message: types.Message):
    all_tasks = tasks.get_all_tasks()
    all_tasks_message = [f"{task.text} — {task.category}. Type /del{task.id} for deleting" for task in all_tasks]
    answer_message = "\n\n".join(all_tasks_message)

    await message.answer(answer_message)


@dp.message_handler(commands=['daily'])
async def show_daily_tasks(message: types.Message):
    pass


@dp.message_handler(commands=['hourly'])
async def show_hourly_tasks(message: types.Message):
    pass


@dp.message_handler(commands=['single'])
async def show_single_tasks(message: types.Message):
    pass


@dp.message_handler(commands=['alarm'])
async def show_alarm_tasks(message: types.Message):
    pass


@dp.message_handler(commands=['change'])
async def change_task_type(message: types.Message):
    args = extract_args(message.text)
    """
    To hourly or daily
    :param message: 
    :return: 
    """
    pass


@dp.message_handler(commands=['daily_freq'])
async def change_daily_frequency(message: types.Message):
    pass


@dp.message_handler(commands=['hourly_freq'])
async def change_hourly_frequency(message: types.Message):
    pass


@dp.message_handler(commands=['alarm_freq'])
async def change_alarm_frequency(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
