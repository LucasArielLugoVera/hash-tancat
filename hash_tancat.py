LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash tancat amb adreçament obert i sondeig lineal."""

    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)

    def _find(self, key):
        inici = self._hash_function(key)

        for i in range(len(self._table)):
            j = (inici + i) % len(self._table)
            clau, _, estat = self._table[j]

            if estat == LLIURE:
                return None
            if estat == OCUPAT and clau == key:
                return j

        return None

    def put(self, key: int, value: int) -> None:
        inici = self._hash_function(key)
        primer_esborrat = None

        for i in range(len(self._table)):
            j = (inici + i) % len(self._table)
            clau, _, estat = self._table[j]

            if estat == OCUPAT and clau == key:
                self._table[j][1] = value
                return

            if estat == ESBORRAT and primer_esborrat is None:
                primer_esborrat = j

            if estat == LLIURE:
                if primer_esborrat is not None:
                    j = primer_esborrat
                self._table[j] = [key, value, OCUPAT]
                self._n += 1
                break
        else:
            if primer_esborrat is None:
                raise RuntimeError("La taula de hash és plena")
            self._table[primer_esborrat] = [key, value, OCUPAT]
            self._n += 1

        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._find(key)
        if j is None:
            return -1
        return self._table[j][1]

    def remove(self, key: int) -> None:
        j = self._find(key)
        if j is not None:
            self._table[j] = [None, None, ESBORRAT]
            self._n -= 1

    def __len__(self):
        return self._n

    def _resize(self, c):
        taula_antiga = self._table
        self._table = [[None, None, LLIURE] for _ in range(c)]
        self._n = 0

        for clau, valor, estat in taula_antiga:
            if estat == OCUPAT:
                self.put(clau, valor)
