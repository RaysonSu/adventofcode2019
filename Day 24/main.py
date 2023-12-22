OUTPUT_TYPE = int


class CellularAutomata1:
    def __init__(self) -> None:
        self.points: set[tuple[int, int]] = set()

    def add_point(self, points: tuple[int, int] | list[tuple[int, int]]) -> None:
        if isinstance(points, list):
            for point in points:
                self.points.add(point)
        else:
            self.points.add(points)

    def generate_neighbours(self, point: tuple[int, int]) -> list[tuple[int, int]]:
        neighbours: list[tuple[int, int]] = []
        for x_diff, y_diff in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x: int = point[0] + x_diff
            y: int = point[1] + y_diff

            if x < 0 or x >= 5:
                continue

            if y < 0 or y >= 5:
                continue

            neighbours.append((x, y))

        return neighbours

    def count_neighbours(self, point: tuple[int, int]) -> int:
        lookup: int = 0
        for point in self.generate_neighbours(point):
            if point in self.points:
                lookup += 1

        return lookup

    def tick(self) -> None:
        new_points: set[tuple[int, int]] = set()
        for point in self.points:
            if self.count_neighbours(point) == 1:
                new_points.add(point)

            for neighbour in self.generate_neighbours(point):
                count: int = self.count_neighbours(neighbour)
                if neighbour not in self.points and count in [1, 2]:
                    new_points.add(neighbour)

        self.points = new_points

    def __hash__(self) -> int:
        ret: int = 0
        for y in range(5):
            for x in range(5):
                if (x, y) in self.points:
                    ret += 1 << (5 * y + x)

        return ret

    def __str__(self) -> str:
        ret: str = ""
        for y in range(5):
            for x in range(5):
                if (x, y) in self.points:
                    ret += "#"
                else:
                    ret += "."
            ret += "\n"

        return ret


class CellularAutomata2:
    def __init__(self) -> None:
        self.points: set[tuple[int, int, int]] = set()

    def add_point(self, points: tuple[int, int, int] | list[tuple[int, int, int]]) -> None:
        if isinstance(points, list):
            for point in points:
                self.points.add(point)
        else:
            self.points.add(points)

    def generate_neighbours(self, point: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        neighbours: list[tuple[int, int, int]] = []
        for x_diff, y_diff in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x: int = point[0] + x_diff
            y: int = point[1] + y_diff

            if x < 0 or x >= 5:
                continue

            if y < 0 or y >= 5:
                continue

            if (x, y) == (2, 2):
                continue

            neighbours.append((x, y, point[2]))

        if point[1] == 0:
            neighbours.append((2, 1, point[2] + 1))
        if point[0] == 0:
            neighbours.append((1, 2, point[2] + 1))
        if point[1] == 4:
            neighbours.append((2, 3, point[2] + 1))
        if point[0] == 4:
            neighbours.append((3, 2, point[2] + 1))

        if point[:2] == (2, 1):
            for i in range(5):
                neighbours.append((i, 0, point[2] - 1))
        if point[:2] == (2, 3):
            for i in range(5):
                neighbours.append((i, 4, point[2] - 1))
        if point[:2] == (1, 2):
            for i in range(5):
                neighbours.append((0, i, point[2] - 1))
        if point[:2] == (3, 2):
            for i in range(5):
                neighbours.append((4, i, point[2] - 1))

        return neighbours

    def count_neighbours(self, point: tuple[int, int, int]) -> int:
        lookup: int = 0
        for point in self.generate_neighbours(point):
            if point in self.points:
                lookup += 1

        return lookup

    def tick(self) -> None:
        new_points: set[tuple[int, int, int]] = set()
        for point in self.points:
            if self.count_neighbours(point) == 1:
                new_points.add(point)

            for neighbour in self.generate_neighbours(point):
                count: int = self.count_neighbours(neighbour)
                if neighbour not in self.points and count in [1, 2]:
                    new_points.add(neighbour)

        self.points = new_points

    def __str__(self) -> str:
        ret: str = ""
        for i in range(-100, 101):
            cur: str = f"Depth: {i}\n"
            tmp: str = ""
            for y in range(5):
                for x in range(5):
                    if (x, y) == (2, 2):
                        tmp += "?"
                    elif (x, y, i) in self.points:
                        tmp += "#"
                    else:
                        tmp += "."
                tmp += "\n"
            if "#" in tmp:
                ret += cur + tmp

        return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    points: list[tuple[int, int]] = []
    for row_index, row in enumerate(inp):
        for col_index, char in enumerate(row):
            if char == "#":
                points.append((col_index, row_index))

    automata: CellularAutomata1 = CellularAutomata1()
    automata.add_point(points)

    hashes_seen: set[int] = set()
    hashed: int = hash(automata)
    while hashed not in hashes_seen:
        hashes_seen.add(hashed)
        automata.tick()
        hashed = hash(automata)

    return hashed


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    points: list[tuple[int, int, int]] = []
    for row_index, row in enumerate(inp):
        for col_index, char in enumerate(row):
            if char == "#":
                points.append((col_index, row_index, 0))

    automata: CellularAutomata2 = CellularAutomata2()
    automata.add_point(points)

    for _ in range(200):
        automata.tick()

    return len(automata.points)


def main() -> None:
    test_input: str = """....#
#..#.
#..##
..#..
#...."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 2129920
    test_output_part_2_expected: OUTPUT_TYPE = 1922

    file_location: str = "python/Advent of Code/2019/Day 24/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = main_part_2(test_input_parsed)

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
    else:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()

    if test_output_part_2_expected == test_output_part_2:
        print(f"Part 2: {main_part_2(input_file)}")
    else:
        print(f"Part 2 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_2_expected}")
        print(f"Got: {test_output_part_2}")


if __name__ == "__main__":
    main()
