from copy import deepcopy
from datetime import datetime, timedelta
from time import sleep
import threading

import schedule

from src.core.helpers.interfaces.chace_service import CacheService


class InMemoryCacheService(CacheService):
    def __init__(self, start_cleaner_deamon: bool = True, cleaner_interval: int = 10):
        self.cache = {}
        self.exit_event: threading.Event = None
        if start_cleaner_deamon:
            self.start_cleaner(cleaner_interval)

    def set(self, key: str, value: any, ttl: int = 300) -> None:
        expiration = datetime.now() + timedelta(seconds=ttl) if ttl else None
        self.cache[key] = (value, expiration)

    def get(self, key: str) -> any:
        value, expiration = self.cache.get(key, (None, None))
        if expiration and datetime.now() > expiration:
            self.delete(key)
            return None
        return deepcopy(value)

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        self.cache.clear()

    def start_cleaner(self, interval: int = 10):
        self._start_cache_cleaner(interval)

    def stop_cleaner(self):
        self.exit_event.set()
        schedule.clear()

    def _start_cache_cleaner(self, interval: int):
        """Starts the background thread for cache cleanup using schedule."""
        schedule.every(interval).seconds.do(self._clean_expired_entries)
        self.exit_event = threading.Event()

        def run_schedule():
            while True:
                schedule.run_pending()
                sleep(1)

        threading.Thread(target=run_schedule, daemon=True)

    def _clean_expired_entries(self):
        """Remove expired cache entries."""
        now = datetime.now()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items() if expiry and now > expiry
        ]
        for key in expired_keys:
            self.delete(key)
