from vector import Vec


class Tile:
    def __init__(self, active: bool = False, weight: int = 0):
        self.active: bool = active
        self.weight: int = weight


class Grid:
    def __init__(self, size: Vec):
        self._tiles: list[list[Tile]] = []
        self._size = size

        self._populate_grid()


    def _populate_grid(self):
        for y in range(0, self._size.y):
            self._tiles.append([])
            for x in range(0, self._size.x):
                self._tiles[y].append(Tile())


    def setTile(self, position: Vec, tile: Tile):
        self._tiles[position.x][position.y] = tile


    def get_tile_weight(self, position: Vec) -> int:
        if not (-1 < position.x < self._size.x and -1 < position.y < self._size.y):
            return -1

        if not self._tiles[position.x][position.y].active:
            return -2

        return self._tiles[position.x][position.y].weight



''' 
-- Mega sej test grid --

matrix = Grid(Vec(3, 3))

matrix.setTile(Vec(1, 1), Tile(True, 3))

for i in range(0, 3):
    print("---")
    for j in range(0, 3):
        print(matrix.get_tile_weight(Vec(i, j)))
'''
