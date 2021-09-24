import os
import sqlite3
from typing import Dict, List, Tuple

conn = sqlite3.connect(os.path.join("tasks.db"))
cursor = conn.cursor()


def insert_to_db(table: str, column_values: Dict):
    columns = ", ".join(column_values.keys())
    values = tuple(column_values.values())
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
    conn.commit()


def delete_from_db(table: str, row_id: int) -> None:
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def select_all():
    cursor.execute(
        "SELECT t.id, c.name, t.text FROM tasks t LEFT JOIN category c ON t.category_id=c.id;"
    )
    rows = cursor.fetchall()
    return rows


def select_category(category_id):
    cursor.execute(
        f"SELECT t.id, c.name, t.text FROM tasks t LEFT JOIN category c ON t.category_id=c.id WHERE t.category_id={category_id};"
    )
    rows = cursor.fetchall()
    return rows


def select_category_aliases_list():
    cursor.execute("SELECT id, name, aliases FROM category;")
    rows = cursor.fetchall()
    return rows
