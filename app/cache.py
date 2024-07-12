from cachetools import TTLCache
from typing import Dict

cache: Dict[int, TTLCache] = {}

def get_cache(user_id: int) -> TTLCache:
    if user_id not in cache:
        cache[user_id] = TTLCache(maxsize=100, ttl=300)
    return cache[user_id]
