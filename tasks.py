from dataclasses import dataclass
from typing import List, NamedTuple, Optional
import db_wrapper

import pytz
import datetime

daily_aliases = ("daily", "d")
hourly_aliases = ("hourly", "h")
singe_aliases = ("single", "s", "one")
alarm_aliases = ("alarm", "a")
aliases = daily_aliases + hourly_aliases + singe_aliases + alarm_aliases


class NotCorrectMessage(Exception):
    pass


@dataclass
class Message:
    category_id: str
    text: str


@dataclass
class Task:
    id: int
    category: int
    text: str


def add_task(raw_message_elements):
    parsed_message = _parse_message(raw_message_elements)
    category = parsed_message.category
    text = parsed_message.text
    db_wrapper.insert_to_db('tasks', {'created': _get_now_formatted(), 'category': category, 'text': text})
    return Task(id=None, category=category, text=text)


def delete_task(row_id: int) -> None:
    db_wrapper.delete_from_db("tasks", row_id)


def get_all_tasks():
    rows = db_wrapper.select_all()
    return [Task(id=row[0], category=row[1], text=row[2]) for row in rows]

def _parse_message(raw_message_elements: list) -> Message:
    category = raw_message_elements[0]
    text = ' '.join(raw_message_elements[1:])
    if category not in aliases or not text:
        raise NotCorrectMessage("Incorrect task")
    category_id = _get_category_id(category)
    return Message(category_id=category_id, text=text)


def _get_category_id(category):
    if category in daily_aliases:
        return 0
    if category in hourly_aliases:
        return 1
    if category in singe_aliases:
        return 2
    if category in alarm_aliases:
        return 3


def _get_now_formatted() -> str:

    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:

    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now