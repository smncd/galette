from typing import TypedDict


class PageCacheItem(TypedDict):
    ttl: int
    timestamp: float
    body: str

class PageCache:
    _store: dict[str, PageCacheItem] = {}

    def set(self, id: str, **item: PageCacheItem):
        self._store[id] = item
        
    def get(self, id: str) -> PageCacheItem|None:
        return self._store[id] if id in self._store else None
