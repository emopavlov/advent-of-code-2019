class Matrix:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.values = []

    def copy(self):
        m = Matrix()
        m.width = self.width
        m.height = self.height
        m.values = self.values.copy()
        return m

    def init_from_elem(self, width, height, elem=""):
        """
        Init all values of a matrix of the given sizes with the given element
        """
        self.width = width
        self.height = height
        self.values = [elem] * (width * height)

        return self

    def init_from_values(self, values):
        """
        Create a matrix from the given values

        :param values: array of arrays, where each array is a line in the matrix
        """
        self.width = len(values[0])
        self.height = len(values)
        self.values = [""] * (self.width * self.height)

        i = 0
        for line in values:
            for value in line:
                self.values[i] = value
                i += 1

        return self

    def set(self, x, y, value):
        self.values[x + y * self.width] = value

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.values[x + y * self.width]
        else:
            return None

    def index_range(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield x, y

    def print_top_left(self, print_headers=False):
        if print_headers:
            top = "  "
            for i in range(0, self.width):
                top += str(i % 10) + " "
            print(top)

        for i in range(0, len(self.values), self.width):
            if print_headers:
                print(str(i // self.width % 10), end=" ")
            print(*self.values[i:i + self.width])

    def print_bottom_left(self):
        for i in range(len(self.values), 0, -self.width):
            print(*self.values[i - self.width:i])
