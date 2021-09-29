from dataclasses import dataclass
from typing import List

import db_wrapper


@dataclass
class Category:
    id: int
    name: int
    aliases: tuple


def get_category_list() -> List[Category]:
    category_list = db_wrapper.select_category_aliases_list()

    return [
        Category(id=int(category[0]), name=category[1], aliases=category[2].split())
        for category in category_list
    ]


def get_category_id(checking_alias: str) -> int:
    category_list = get_category_list()
    for category in category_list:
        if checking_alias in category.aliases:
            return category.id


def get_category_aliases_list() -> List[str]:
    category_list = get_category_list()
    return [alias for category in category_list for alias in category.aliases]
