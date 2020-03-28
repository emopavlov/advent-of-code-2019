from enum import Enum

black = "."
white = "#"


class EmergencyHullPaintingRobot:
    def __init__(self, computer, tile_colour=black):
        self.location = (0, 0)
        self.hull = _Hull()
        self.hull.paint((0, 0), tile_colour)
        self.computer = computer
        self.direction = _Direction.NORTH

    def run(self):
        self.computer.run()
        while self.computer.is_running():
            tile_colour = self._read_colour()
            command = self._run_computer(0 if tile_colour == black else 1)
            self._paint_and_move(command[0], command[1])

    def count_painter_tiles(self):
        return len(self.hull.path)

    def print(self):
        min_x = min(map(lambda x: x[0], self.hull.path))
        max_x = max(map(lambda x: x[0], self.hull.path))
        min_y = min(map(lambda x: x[1], self.hull.path))
        max_y = max(map(lambda x: x[1], self.hull.path))

        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                print(self.hull.colour((x, y)), end=" ")
            print()

    def _run_computer(self, input):
        self.computer.output_list.clear()
        self.computer.continue_run([input])
        return self.computer.output_list

    def _read_colour(self):
        return self.hull.colour(self.location)

    def _paint_and_move(self, new_colour, turn):
        self.hull.paint(self.location, white if new_colour == 1 else black)

        if turn == 0:
            self.direction = self.direction.turn_left()
        else:
            self.direction = self.direction.turn_right()

        if self.direction == _Direction.NORTH:
            self.location = self.location[0], self.location[1] + 1
        elif self.direction == _Direction.EAST:
            self.location = self.location[0] + 1, self.location[1]
        elif self.direction == _Direction.SOUTH:
            self.location = self.location[0], self.location[1] - 1
        elif self.direction == _Direction.WEST:
            self.location = self.location[0] - 1, self.location[1]


class _Hull:
    def __init__(self):
        self.path = {}

    def colour(self, location):
        return self.path[location] if location in self.path else black

    def paint(self, location, colour):
        self.path[location] = colour


class _Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_right(self):
        return _Direction((self.value + 1) % 4)

    def turn_left(self):
        return _Direction((self.value + 4 - 1) % 4)
