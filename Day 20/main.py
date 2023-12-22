from __future__ import annotations
from collections import defaultdict, deque
from re import match
from time import sleep
OUTPUT_TYPE = int
labels: dict[tuple[int, int], str]


class State_part_1:
    def __init__(
        self,
        grid: list[str],
        teleports: dict[tuple[int, int], tuple[int, int]],
        location: tuple[int, int],
        time: int = 0,
        prev: tuple[int, int] = (-1, -1),
        telepoted: tuple[tuple[int, int], ...] = ()
    ) -> None:

        self.grid: list[str] = grid
        self.teleports: dict[tuple[int, int], tuple[int, int]] = teleports
        self.location: tuple[int, int] = location
        self.time: int = time
        self.prev: tuple[int, int] = prev
        self.teleported: tuple[tuple[int, int], ...] = telepoted

    def __str__(self) -> str:
        return f"location: {self.location}, time: {self.time}, previous: {self.prev}, teleports: {self.teleported}"

    def neighbours(self) -> list[State_part_1]:
        ret: list[State_part_1] = []
        for direction in range(4):
            new_location: tuple[int, int] = (
                self.location[0] + [1, 0, -1, 0][direction],
                self.location[1] + [0, -1, 0, 1][direction]
            )

            tile: str = self.grid[new_location[1]][new_location[0]]
            if tile == "#":
                continue

            new_teleported: tuple[tuple[int, int], ...] = self.teleported
            if tile.isalpha():
                if new_location in self.teleports.keys():
                    new_location = self.teleports[new_location]
                    new_teleported += (new_location,)
                else:
                    continue

            if new_location == self.prev:
                continue

            ret.append(State_part_1(
                self.grid,
                self.teleports,
                new_location,
                self.time + 1,
                self.location,
                new_teleported
            ))

        return ret

    def copy(self) -> State_part_1:
        return State_part_1(
            self.grid,
            self.teleports,
            self.location,
            self.time,
            self.prev
        )

    def __hash__(self) -> int:
        return hash(str(self.location) + str(self.prev))


class State_part_2:
    def __init__(
        self,
        grid: list[str],
        teleports: dict[tuple[int, int], tuple[int, int]],
        location: tuple[int, int],
        prev: tuple[int, int] = (-1, -1),
        time: int = 0,
        telepoted: tuple[str, ...] = ("",),
        layer: int = 0
    ) -> None:

        self.grid: list[str] = grid
        self.teleports: dict[tuple[int, int], tuple[int, int]] = teleports
        self.location: tuple[int, int] = location
        self.time: int = time
        self.teleported: tuple[str, ...] = telepoted
        self.layer: int = layer
        self.prev: tuple[int, int] = prev

    def __str__(self) -> str:
        return f"location: {self.location}, time: {self.time}, layer: {self.layer}"

    def neighbours(self) -> list[State_part_2]:
        ret: list[State_part_2] = []
        for direction in range(4):
            new_location: tuple[int, int] = (
                self.location[0] + [1, 0, -1, 0][direction],
                self.location[1] + [0, -1, 0, 1][direction]
            )
            if new_location == self.prev:
                continue

            tile: str = self.grid[new_location[1]][new_location[0]]
            if tile == "#":
                continue

            new_teleported: tuple[str, ...] = self.teleported
            new_layer: int = self.layer
            if tile.isalpha():
                if new_location in self.teleports.keys():
                    tele_tile: str = labels[new_location]
                    if self.is_outer(new_location):
                        new_layer -= 1
                    else:
                        new_layer += 1

                    if new_layer < 0 or new_layer > len(self.teleports) // 2:
                        continue

                    if tele_tile == self.teleported[-1]:
                        continue

                    new_teleported += (tele_tile,)
                    new_location = self.teleports[new_location]
                else:
                    continue

            ret.append(State_part_2(
                self.grid,
                self.teleports,
                new_location,
                self.location,
                self.time + 1,
                new_teleported,
                new_layer
            ))

        return ret

    def is_outer(self, location: tuple[int, int]) -> bool:
        if location[0] < 2:
            return True

        if location[0] > len(self.grid[0]) - 4:
            return True

        if location[1] < 2:
            return True

        if location[1] > len(self.grid) - 4:
            return True

        return False

    def copy(self) -> State_part_2:
        return State_part_2(
            self.grid,
            self.teleports,
            self.location,
            self.prev,
            self.time
        )

    def __hash__(self) -> int:
        return hash(str(self.location) + "//" + str(self.layer) + "//" + str(self.teleports) + "//" + str(self.prev))


def transpose(grid: list[str]) -> list[str]:
    return ["".join([grid[j][i] for j in range(len(grid))]) for i in range(len(grid[0]))]


def parse_inp(inp: list[str]) -> tuple[dict[tuple[int, int], tuple[int, int]], tuple[int, int], tuple[int, int], dict[tuple[int, int], str]]:
    inp = [row.replace("\n", "") for row in inp]

    locations: defaultdict[str, list[tuple[tuple[int, int], tuple[int, int]]]]
    locations = defaultdict(lambda: [].copy())

    window: str
    for row_index, row in enumerate(inp):
        for index in range(len(inp[0]) - 2):
            window = row[index:index+3]

            if match("[A-Z][A-Z]\.", window):
                locations[window[:2]].append((
                    (index + 1, row_index),
                    (index + 2, row_index)
                ))

            if match("\.[A-Z][A-Z]", window):
                locations[window[1:]].append((
                    (index + 1, row_index),
                    (index, row_index)
                ))

    for col_index, col in enumerate(transpose(inp)):
        for index in range(len(inp) - 2):
            window = col[index:index+3]
            if match("[A-Z][A-Z]\.", window):
                locations[window[:2]].append((
                    (col_index, index + 1),
                    (col_index, index + 2)
                ))

            if match("\.[A-Z][A-Z]", window):
                locations[window[1:]].append((
                    (col_index, index + 1),
                    (col_index, index)
                ))

    teleports: dict[tuple[int, int], tuple[int, int]] = {}
    start: tuple[int, int]
    end: tuple[int, int]
    labels: dict[tuple[int, int], str] = {}

    for key, value in locations.items():
        if key == "AA":
            start = value[0][1]
            continue

        if key == "ZZ":
            end = value[0][1]
            continue

        teleports[value[0][0]] = value[1][1]
        teleports[value[1][0]] = value[0][1]
        labels[value[0][0]] = key
        labels[value[1][0]] = key

    return teleports, start, end, labels


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    teleports: dict[tuple[int, int], tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    teleports, start, end, _ = parse_inp(inp)

    State_part_1s: deque[State_part_1] = deque()
    best: defaultdict[int, int] = defaultdict(lambda: 10 ** 6)
    State_part_1s.append(State_part_1(inp, teleports, start))

    while State_part_1s:
        active: State_part_1 = State_part_1s.popleft()
        neighbours: list[State_part_1] = active.neighbours()
        for neighbour in neighbours:
            if neighbour.location == end:
                return neighbour.time

            hashed: int = hash(neighbour)
            if best[hashed] <= neighbour.time:
                continue

            best[hashed] = neighbour.time

            State_part_1s.append(neighbour)

        del active
    return -1


def str_assign(string: str, index: int, item: str) -> str:
    return string[:index] + item + string[index+1:]


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    global labels
    teleports: dict[tuple[int, int], tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    teleports, start, end, labels = parse_inp(inp)

    State_part_2s: deque[State_part_2] = deque()
    best: defaultdict[int, int] = defaultdict(lambda: 10 ** 6)
    State_part_2s.append(State_part_2(inp, teleports, start))
    prev: int = 0

    while State_part_2s:
        if State_part_2s[0].time != prev:
            cur = inp.copy()
            for state in State_part_2s:
                loc = state.location
                dep = state.layer
                cur[loc[1]] = str_assign(
                    cur[loc[1]], loc[0], "0123456789abcdefghijklmnopqurtuvwxyz"[dep])

            for i in cur:
                print(i.replace("\n", "").replace(".", " "))
            print(f"Time: {prev}")
            sleep(0.01)
            prev = State_part_2s[0].time
        active: State_part_2 = State_part_2s.popleft()
        neighbours: list[State_part_2] = active.neighbours()

        for neighbour in neighbours:
            if neighbour.location == end and neighbour.layer == 0:
                return neighbour.time

            hashed: int = hash(neighbour)
            if best[hashed] <= neighbour.time:
                continue

            best[hashed] = neighbour.time

            State_part_2s.append(neighbour)

        del active
    return -1


def main() -> None:
    test_input: str = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 77
    test_output_part_2_expected: OUTPUT_TYPE = 396

    file_location: str = "python/Advent of Code/2019/Day 20/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = 396

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
