# Chap 5 - Object-Oriented Design


# 8.10
# Implement a hash table which uses lists to handle collisions.
# The values should be accessed in a LRU fashion.
class HashTable(object):
    def __init__(self, size=100):
        self._items = [[]] * size

    def __len__(self):
        return len(self._items)

    def _iter_for_key(self, key):
        for key, value in self._items[self._hash(key)]:
            yield key, value

    def _hash(self, key):
        return hash(key) % len(self)

    def _insert(self, key, value, remove=True):
        item, key_hash = (key, value), self._hash(key)
        if item in self._items[key_hash]:
            self._items[key_hash].remove(item)
        self._items[key_hash].insert(0, item)
        return value

    def put(self, key, value):
        self._insert(key, value, False)

    def get(self, key):
        for key_, value in self._iter_for_key(key):
            if key_ == key:
                return self._insert(key, value)

t = HashTable()
t.put("first", "alex")
t.put("second", "bob")
t.put("third", "roger")
t.put("first", "xela")
t.put("second", "tim")
assert t.get("first") == "xela"
assert t.get("second") == "tim"
assert t.get("third") == "roger"
assert not t.get("fourth")

