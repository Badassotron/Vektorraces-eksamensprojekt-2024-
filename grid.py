from vector import Vec


class Tile:
    def __init__(self, active: bool = False, weight: int = 0):
        self.active: bool = active
        self.weight: int = weight


class Grid:
    def __init__(self, size: Vec = Vec()):
        self._tiles: list[list[Tile]] = []
        self._size: Vec = size

        self._populate_grid()

    def _populate_grid(self):
        pass

    def get_tile_weight(self, position: Vec) -> int:
        if not (0 < position.x < self._size.x and 0 < position.y < self._size.y):
            return -1

        if not self._tiles[position.x][position.y].active:
            return -1

        return self._tiles[position.x][position.y].weight
