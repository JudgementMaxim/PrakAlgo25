# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary


class SetNode:
    """
    TODO for students: die Klasse user.User erbt von SetNode. diese Klasse wird eigentlich erst in Praktikum 3 benötigt.
    für Praktikum 1 und 2 müsste User nicht von dieser Klasse erben
    Class representing a node in a disjoint set (union-find) structure.

    Attributes:
        _parent (SetNode): The parent node in the union-find structure.
        _weight (int): The weight (number of nodes) of the (sub-)tree rooted in the current node.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new SetNode.
        """
        super().__init__()
        self._groups = {}
        # TODO: werden nur für Praktikum 3 benötigt
        self._parent = self  # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist

        # SetNode erweiterung
        self._praktikumsgruppe = None

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden


class Praktikumsgruppen(dict):
    """
    In Praktikum 1 und 2: Dictionary containing all students. Die Klasse user.Users erbt von dieser Klasse.
    In Praktikum 3: Class representing a collection of disjoint sets for grouping users into practical groups.

    Methods:
        find(node): Finds the root of the set containing the node, with path compression.
        find_byid(user_id, return_id=False): Finds the root of the set containing the user by ID.
        union(user_id1, user_id2): Unions the sets containing the two users.
        create_groups(user_ids, groupnumbers): Creates groups from the provided user IDs and group numbers.
        get_groupmembers(user_id): Gets the members of the group containing the user.
        print_ds(): Prints the disjoint set structure.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new Praktikumsgruppen object.
        """
        super().__init__()
        self._groups = {}
        self._groupnumbers = []

    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)

    def find(self, node):
        """
        Finds the root of the set containing the node, with path compression.

        Args:
            node (SetNode): node whose root should be found

        Returns:
            SetNode: root node
        """
        if node._parent != node:
            node._parent = self.find(node._parent)  # Pfadverkürzung
        return node._parent

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    def find_byid(self, user_id, return_id=False):
        """
        Finds the root of the set (Praktikumsgruppe) containing the user by ID.

        Args:
            user_id (str): The ID of the user.
            return_id (bool): Whether to return the ID of the root node (True) or the root node itself (False, default).

        Returns:
            SetNode or str: The root node or its ID, depending on return_id.
        """
        if user_id not in self:
            return None

        root = self.find(self[user_id])

        if return_id:
            # root id ist der Schlüssel, dessen Objekt root ist
            for uid, node in self.items():
                if node is root:
                    return uid
            return None

        return root

    def union(self, user_id1, user_id2):
        """
        Unions the sets containing the two users. Uses weighted union.

        Args:
            user_id1 (str): user id of first user
            user_id2 (str): user id of second user
        """
        if user_id1 not in self or user_id2 not in self:
            return

        root1 = self.find(self[user_id1])
        root2 = self.find(self[user_id2])

        if root1 == root2:
            return

        # Weighted Quick-Union: kleinerer Baum hängt sich an größeren Baum
        if root1._weight < root2._weight:
            root1._parent = root2
            root2._weight += root1._weight
        else:
            root2._parent = root1
            root1._weight += root2._weight

    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.

        Args:
            user_ids (list): A list of user IDs.
            groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """
        # TODO: implement in Praktikum 3 (neu)
        self._groups = {}
        self._groupnumbers = list(set(groupnumbers))

        # 1) Alle User als einzelne Mengen anlegen (jeder ist erstmal eigene Wurzel)
        for user_id in user_ids:
            if user_id not in self:
                self[user_id] = SetNode()

        # 2) Gruppen-IDs merken (wie im Praktikum 1), damit get_groupmembers schnell filtern kann
        for user_id, groupnumber in zip(user_ids, groupnumbers):
            self._groups[user_id] = groupnumber
            self[user_id]._praktikumsgruppe = groupnumber

        # 3) Alle User mit gleicher Gruppennummer unionen
        reps = {}  # groupnumber -> repräsentant (erste user_id dieser Gruppe)
        for user_id, groupnumber in zip(user_ids, groupnumbers):
            if groupnumber not in reps:
                reps[groupnumber] = user_id
            else:
                self.union(user_id, reps[groupnumber])

    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id):
        """
        Gets the members of the group containing the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of user IDs in the same group.
        """
        # TODO: implement in Praktikum 3 (neu)
        if user_id not in self:
            return []

        root = self.find(self[user_id])

        members = []
        for uid in self:
            if self.find(self[uid]) is root:
                members.append(uid)

        return members

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods **

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***

