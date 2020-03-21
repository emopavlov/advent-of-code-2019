# Utility functions


def read_input(file, separator="\n"):
    with open("../input/" + file, "r") as rd:
        out = []
        for line in rd:
            for elem in line.strip().split(separator):
                out.append(elem)

    return out


class Matrix:
    def __init__(self, width, height, elem=""):
        self.width = width
        self.height = height
        self.matrix = [elem] * (width * height)

    def set(self, x, y, value):
        self.matrix[x + y * self.width] = value

    def print_top_left(self):
        for i in range(0, len(self.matrix), self.width):
            print(*self.matrix[i:i + self.width])

    def print_bottom_left(self):
        for i in range(len(self.matrix), 0, -self.width):
            print(*self.matrix[i - self.width:i])
