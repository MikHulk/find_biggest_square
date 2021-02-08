import sys
from functools import reduce


class Board:
    def __init__(self, area, obstacle_repr='o',
                 plain_repr='x', empty_repr='.'):
        self.raw_area = area
        self.area = [
            [cell for cell in row]
            for row in (
                self.raw_area
                .strip('\n')
                .strip()
                .split('\n')
            )
        ]
        self.obstacle_repr = obstacle_repr
        self.plain_repr = plain_repr
        self.empty_repr = empty_repr
        self._biggest_square = None

    def get_cell(self, x, y):
        return self.area[x][y]

    def get_square_sides(self, x, y, side):
        if x + side >= len(self.area) or y + side >= len(self.area[0]):
            return None
        return (
            [row[y + side] for row in (self.area[x : x + side + 1])]
            + self.area[x + side][y : y + side + 1]
        )

    @property
    def is_valid(self):
        lines = self.area
        return (
            lines
            and len(lines[0]) >= 1
            and reduce(
                lambda prev, new: (prev[0] and prev[1] == len(new), prev[1]),
                lines[1:],
                (True, len(lines[0]))
            )[0]
            and all(c in [self.plain_repr, self.empty_repr, self.obstacle_repr, '\n']
                    for c in self.raw_area)
        )

    def get_biggest_square_from(self, x, y):
        cell = self.get_cell(x, y)
        if cell == self.obstacle_repr:
            return 0
        side = 1
        while True:
            sides = self.get_square_sides(x, y, side)
            if not sides or self.obstacle_repr in sides:
                break
            side += 1
        return side

    @property
    def biggest_square(self):
        if self._biggest_square is None:
            side_length = len(self.area[0])
            for x in range(0, len(self.area)):
                if self._biggest_square and self._biggest_square[2] == side_length:
                    break
                for y in range(0, len(self.area[0])):
                    side = self.get_biggest_square_from(x, y)
                    if self._biggest_square is None or side > self._biggest_square[0]:
                        self._biggest_square = side, x, y
                side_length -= 1
        return self._biggest_square

    def draw(self):
        biggest_side, biggest_sq_x, biggest_sq_y = self.biggest_square
        lines = []
        for x in range(0, len(self.area)):
            line = []
            for y in range(0, len(self.area[0])):
                cell = self.get_cell(x, y)
                if (
                        cell == self.empty_repr
                        and biggest_sq_x <= x < biggest_sq_x + biggest_side
                        and biggest_sq_y <= y < biggest_sq_y + biggest_side
                ):
                    line.append(self.plain_repr)
                else:
                    line.append(cell)
            lines.append(''.join(line))
        return '\n'.join(lines)


if __name__ == "__main__":

    for filename in sys.argv[1:]:
        print("===")
        print(filename)
        with open(filename) as f:
            header = f.readline().strip()
            empty_repr = header[-3]
            obstacle_repr = header[-2]
            plain_repr = header[-1]
            b = Board(
                f.read(),
                empty_repr=empty_repr,
                plain_repr=plain_repr,
                obstacle_repr=obstacle_repr
            )
        if not b.is_valid:
            sys.stderr.write("map error\n")
            continue
        print(f"Biggest square with {b.biggest_square[0]} units side "
              f"at ({b.biggest_square[1]}, {b.biggest_square[2]})")
        print(b.draw())
