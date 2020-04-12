class Map:
    """
    A matrix backed by a dictionary that can expand as the map is explored
    """
    def __init__(self):
        self.elems = {}

    def set(self, x, y, value):
        self.elems[(x, y)] = value

    def get(self, x, y, default):
        return self.elems[(x, y)] if (x, y) in self.elems else default

    def print(self):
        xs = list(map(lambda l: l[0], self.elems.keys()))
        ys = list(map(lambda l: l[1], self.elems.keys()))
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        for i in range(max_y, min_y - 1, -1):
            for j in range(min_x, max_x + 1):
                print(self.get(j, i, " "), end="")
            print()


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_north(self):
        self.y += 1

    def move_south(self):
        self.y -= 1

    def move_east(self):
        self.x += 1

    def move_west(self):
        self.x -= 1
