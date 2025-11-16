from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass(frozen=True)
class Transaction:
    seller: str
    buyer: str
    price: float
    timestamp: datetime
    product_name: str

    def __repr__(self) -> str:
        # Compact representation for printing
        ts = self.timestamp.isoformat(timespec="seconds")
        return (f"Transaction(seller={self.seller!r}, buyer={self.buyer!r}, "
                f"price={self.price}, timestamp={ts}, product_name={self.product_name!r})")


class Transactions:
    """
    Intentionally naive hash table
    - Uses a deliberately bad hash function (default: first letter of product name).
    - Counts total collisions since creation.
    """

    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity = capacity
        self._buckets: List[List[Transaction]] = [[] for _ in range(capacity)]
        self._size = 0
        self._collisions = 0

     # *** PUBLIC METHODS ***

    def insert(self, tx: Transaction) -> None:
        """Insert a transaction, count a collision if the target bucket is non-empty."""
        idx = self._hash_fn(tx)
        bucket = self._buckets[idx]
        if len(bucket) > 0:
            self._collisions += 1
        bucket.append(tx)
        self._size += 1

    # *** PUBLIC GET METHODS ***

    def get_collisions(self) -> int:
        """Total number of collisions since table creation."""
        return self._collisions

    def get_capacity(self) -> int:
        return self._capacity
    
    def get_size(self) -> int:
        return self._size
    
    # *** PRIVATE METHODS ***
    
    # TODO: Erstellt eine bessere Hashfunktion, welche möglichst wenig Kollisionen generiert
    def _hash_fn(self, tx: Transaction) -> int:
        """
        Deliberately bad key function:
        Use ONLY the first character of the product name.
        """
        if not tx.product_name:
            return 0
        first = tx.product_name[0].lower()
        # Map 'a'..'z' to 0..25, everything else also squeezed into the table
        return (ord(first) - ord('a')) % self._capacity

