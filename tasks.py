from dataclasses import dataclass
from typing import List, NamedTuple, Optional
import db_wrapper
import categories

import pytz
import datetime


class NotCorrectMessage(Exception):
    pass


@dataclass
class Message:
    category_id: int
    text: str


@dataclass
class Task:
    id: int
    category_id: int
    text: str


_category_aliases_list = categories.get_category_aliases_list()


def add_task(raw_message_elements):
    parsed_message = _parse_message(raw_message_elements)
    category_id = parsed_message.category_id
    text = parsed_message.text
    db_wrapper.insert_to_db('tasks', {'created': _get_now_formatted(), 'category_id': category_id, 'text': text})
    return Task(id=None, category_id=category_id, text=text)


def delete_task(row_id: int) -> None:
    db_wrapper.delete_from_db("tasks", row_id)


def get_all_tasks():
    rows = db_wrapper.select_all()

    return [Task(id=row[0], category_id=row[1], text=row[2]) for row in rows]


def get_category_tasks(category):
    category_id = categories.get_category_id(category)
    rows = db_wrapper.select_category(category_id)

    return [Task(id=row[0], category_id=row[1], text=row[2]) for row in rows]


def _parse_message(raw_message_elements: list) -> Message:
    category = raw_message_elements[0]
    text = ' '.join(raw_message_elements[1:])
    if category not in _category_aliases_list or not text:
        raise NotCorrectMessage("Incorrect task")
    category_id = categories.get_category_id(category)

    return Message(category_id=category_id, text=text)


def _get_now_formatted() -> str:

    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)

    return now
