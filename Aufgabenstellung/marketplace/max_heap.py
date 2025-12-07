# Die Klasse MaxHeap implementiert einen Max-Heap
# TODO: Diese Klasse implementieren Sie in Praktikum 2

class MaxHeap:
    def __init__(self):
        """ Initialisierung des Max-Heaps. """

        self.heap = []
        self.auction_map = {}

    # *** PUBLIC methods ***

    def add_auction(self, auction_id, bid_count):
        """ Fügt eine neue Auktion zum Max-Heap hinzu. """

        if auction_id in self.auction_map:
            raise ValueError("Auktion existiert bereits")

        # Hinten anfügen
        self.heap.append((bid_count, auction_id))
        index = len(self.heap) - 1

        # HashMap aktualisieren
        self.auction_map[auction_id] = (bid_count, index)

        # nach oben heapifizieren
        self._heapify_up(index)

    def update_bidders(self, auction_id, new_bid_count):
        """ Aktualisiert die Anzahl der Bieter für eine Auktion. """

        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        old_bid_count, index = self.auction_map[auction_id]

        # neuen Wert eintragen
        self.heap[index] = (new_bid_count, auction_id)
        self.auction_map[auction_id] = (new_bid_count, index)

        # entscheiden ob hoch oder runter
        if new_bid_count > old_bid_count:
            self._heapify_up(index)
        else:
            self._heapify_down(index)

    def remove(self, auction_id):
        """ Entfernt eine Auktion aus dem Max-Heap. """

        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        _, index = self.auction_map[auction_id]
        last_index = len(self.heap) - 1

        # letzter Eintrag → direkt löschen
        if index == last_index:
            self.heap.pop()
            del self.auction_map[auction_id]
            return

        # letztes Element an Stelle des zu löschenden Elements setzen
        last_item = self.heap[last_index]
        self.heap[index] = last_item
        self.heap.pop()

        moved_bid_count, moved_id = last_item

        # HashMap aktualisieren
        self.auction_map[moved_id] = (moved_bid_count, index)
        del self.auction_map[auction_id]

        # korrekt einsortieren
        self._heapify_down(index)
        self._heapify_up(index)

    # *** PUBLIC GET methods ***

    def get_auction_with_max_bidders(self):
        if not self.heap:
            return None
        return self.heap[0]

    def get_auction_bidders(self, auction_id):
        if auction_id in self.auction_map:
            return self.auction_map[auction_id][0]
        return None

    # *** PRIVATE methods ***

    def _swap(self, i, j):
        """ Tauscht zwei Elemente im Heap und aktualisiert die HashMap. """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        b1, id1 = self.heap[i]
        b2, id2 = self.heap[j]

        self.auction_map[id1] = (b1, i)
        self.auction_map[id2] = (b2, j)

    def _heapify_up(self, index):
        """ Element nach oben verschieben. """

        while index > 0:
            parent = (index - 1) // 2

            if self.heap[parent][0] >= self.heap[index][0]:
                break

            self._swap(parent, index)
            index = parent

    def _heapify_down(self, index):
        """ Element nach unten verschieben. """

        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left

            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest == index:
                break

            self._swap(index, largest)
            index = largest
