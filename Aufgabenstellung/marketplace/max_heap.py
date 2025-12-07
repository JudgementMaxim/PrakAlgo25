# Die Klasse MaxHeap implementiert einen Max-Heap

# TODO: Diese Klasse implementieren Sie in Praktikum 2

class MaxHeap:
    def __init__(self):
        """ Initialisierung des Max-Heaps.
            Ein Knoten speichert die Anzahl der Bieter für eine Auktion sowie die ID-Nummer der Auktion.
            Die Auktion mit den meisten Bietern soll an der Spitze des Max-Heaps stehen.

        heap: Eine Liste zur Speicherung des Heaps, bestehend aus Tupeln in der Form (bid_count, auction_id).
        auction_map: Eine Hash-Map, welche die Position der Auktionen im Max-Heap speichert.
                     (key = auction_id, value = (bid_count, heap_index))
        """
        self.heap = []
        self.auction_map = {}

        # TODO: wenn Sie die anderen Methoden implementiert haben, können Sie diese Zeile auskommentieren
        raise NotImplementedError

    # *** PUBLIC methods ***

    def add_auction(self, auction_id, bid_count):
           """ Fügt eine neue Auktion zum Max-Heap hinzu.
            Wenn die Auktion schon im heap ist, wird die Auktion nicht hinzugefügt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            bid_count: Die Anzahl der Bieter für diese Auktion.
        """

        if auction_id in self.auction_map:
            raise ValueError("Auktion existiert bereits")

        # hinten anhängen
        self.heap.append((bid_count, auction_id))
        index = len(self.heap) - 1

        # in HashMap eintragen
        self.auction_map[auction_id] = (bid_count, index)

         # korrekt einordnen
        self._heapify_up(index)

        

    def update_bidders(self, auction_id, new_bid_count):
        """ Aktualisiert die Anzahl der Bieter für eine Auktion.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion geändert.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            new_bid_count: Die neue Anzahl der Bieter für diese Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        old_bid_count, index = self.auction_map[auction_id]

        # neuen Wert in heap eintragen
        self.heap[index] = (new_bid_count, auction_id)

        # HashMap aktualisieren
        self.auction_map[auction_id] = (new_bid_count, index)

        # Entscheiden: hoch oder runter heapify
        if new_bid_count > old_bid_count:
            self._heapify_up(index)
        else:
            self._heapify_down(index)
        

    def remove(self, auction_id):
        """ Entfernt die Auktion aus dem Max-Heap.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion entfernt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        _, index = self.auction_map[auction_id]
        last_index = len(self.heap) - 1

        # letzter Eintrag → einfach löschen
        if index == last_index:
            self.heap.pop()
            del self.auction_map[auction_id]
            return

        # letztes Element nach vorne holen
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
        """ Gibt die Auktion mit der höchsten Anzahl an Bietern zurück.

        Returns:
            Tuple[int, int]: (bid_count, auction_id)
        """
        if not self.heap:
            return None
        return self.heap[0][0], self.heap[0][1]

    def get_auction_bidders(self, auction_id):
        """ Gibt die Anzahl der Bieter für eine Auktion zurück.
            Wenn die Auktion nicht im Max-Heap ist, wird None zurückgegeben.

        Args:
            auction_id: Die ID-Nummer der Auktion.

        Returns:
            Optional[int]: bid_count
        """
        if auction_id in self.auction_map:
            return self.auction_map[auction_id][0]
        return None

    # *** PRIVATE methods ***

    def _swap(self, i, j):
        """ Hilfsfunktion zum Tauschen von zwei Auktionen im Max-Heap.
            Aktualisiert ebenfalls die Position der Auktionen in der auction_map.

        Args:
            i: Index der ersten Auktion im Max-Heap.
            j: Index der zweiten Auktion im Max-Heap.
        """
        # TODO:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        bid_i, id_i = self.heap[i]
        bid_j, id_j = self.heap[j]

        self.auction_map[id_i] = (bid_i, i)
        self.auction_map[id_j] = (bid_j, j)


    def _heapify_up(self, index):
        """ Führt das Heapify-Up-Verfahren durch, um die Heap-Eigenschaft nach oben hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach oben "heapified" werden soll.
        """
        # TODO:
         while index > 0:
            parent = (index - 1) // 2

            # wenn Elternknoten größer → fertig
            if self.heap[parent][0] >= self.heap[index][0]:
                break

            # tauschen
            self._swap(parent, index)
            index = parent


    def _heapify_down(self, index):
        """ Führt das Heapify-Down-Verfahren durch, um die Heap-Eigenschaft nach unten hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach unten "heapified" werden soll.
        """
        # TODO:
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left

            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            # schon richtig
            if largest == index:
                break

            self._swap(index, largest)
            index = largest


