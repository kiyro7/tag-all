from collections import defaultdict
from typing import Dict, Set

# chat_id -> set(user_id)
chat_users: Dict[int, Set[int]] = defaultdict(set)


def add_user(chat_id: int, user_id: int):
    chat_users[chat_id].add(user_id)


def get_users(chat_id: int) -> Set[int]:
    return chat_users.get(chat_id, set())
