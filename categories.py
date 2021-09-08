from dataclasses import dataclass
import db_wrapper


@dataclass
class Category:
    id: int
    name: int
    aliases: tuple


def get_category_aliases():
    category_list = db_wrapper.select_category_aliases_list()

    return [Category(id=None, name=category[0], aliases=category[1].split()) for category in category_list]


def get_category_id(category_alias):
    category_id = db_wrapper.select_category



