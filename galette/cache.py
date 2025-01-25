from typing import TypedDict


class PageCacheItem(TypedDict):
    ttl: int
    timestamp: float
    body: str


class PageCache:
    _maxsize: int
    _store: dict[str, PageCacheItem] = {}

    def __init__(self, maxsize: int = 0) -> None:
        self._maxsize = maxsize

    def set(self, id: str, **item: PageCacheItem) -> None:
        if self._maxsize > 0 and len(self._store) > self._maxsize:
            oldest = min(self._store, key=lambda item: item['timestamp'])
            self.delete(oldest)

        self._store[id] = item
        
    def get(self, id: str) -> PageCacheItem|None:
        return self._store[id] if id in self._store else None

    def delete(self, id: str) -> None:
        del self._store[id]
