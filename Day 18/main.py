from __future__ import annotations
from collections import deque, defaultdict

OUTPUT_TYPE = int


class State_single:
    def __init__(self, grid: list[str], location: tuple[int, int] | None = None, time: int = 0, prev: int = -1, keys: str = "") -> None:
        self.grid: list[str] = grid
        if location:
            self.location: tuple[int, int] = location
        else:
            for row_index, row in enumerate(grid):
                if "@" in row:
                    self.location = (row.index("@"), row_index)
                    break
        self.time: int = time
        self.keys: str = keys
        self.prev: int = prev

    def neighbours(self) -> list[State_single]:
        ret: list[State_single] = []
        for direction in range(4):
            if self.prev == (direction + 2) % 4:
                continue

            new_location: tuple[int, int] = (
                self.location[0] + [1, 0, -1, 0][direction],
                self.location[1] + [0, -1, 0, 1][direction]
            )

            tile: str = self.grid[new_location[1]][new_location[0]]
            if tile == "#":
                continue

            if tile.islower() and tile not in self.keys:
                ret.append(State_single(
                    self.grid,
                    new_location,
                    self.time + 1,
                    -1,
                    self.keys + tile
                ))
                continue

            if tile.isupper() and tile.lower() not in self.keys:
                continue

            ret.append(State_single(
                self.grid,
                new_location,
                self.time + 1,
                direction,
                self.keys
            ))

        if ret == []:
            ret.append(State_single(
                self.grid,
                self.location,
                self.time + 1,
                self.prev,
                self.keys
            ))

        return ret

    def copy(self) -> State_single:
        return State_single(
            self.grid,
            self.location,
            self.time,
            self.prev,
            self.keys
        )

    def __hash__(self) -> int:
        return hash(str(self.location)) + sum([(23 + ord(x)) ** 6 for x in self.keys])


class State_multiple:
    def __init__(self, sub_states: list[State_single], control: int = -1) -> None:
        self.sub_states: list[State_single] = sub_states
        self.control: int = control

    def __hash__(self) -> int:
        ret: int = 0
        for state in self.sub_states:
            ret += hash(str(state.location))
        ret += sum([(23 + ord(x)) ** 6 for x in self.sub_states[0].keys])

        return ret

    def __str__(self) -> str:
        ret: str = ""
        ret += "locations: "
        for sub_state in self.sub_states:
            ret += str(sub_state.location + (sub_state.prev, ))
            ret += ", "
        ret = ret[:-2]
        ret += " time: "
        ret += str(self.sub_states[0].time)
        ret += " control: "
        ret += str(self.control)
        ret += " keys: "
        ret += str(self.sub_states[0].keys)

        return ret

    def neighbours(self) -> list[State_multiple]:
        ret: list[tuple[bool, State_multiple]] = []

        if self.control == -1:
            for i in range(len(self.sub_states)):
                ret.extend(self.move_bot([(False, self)], i))
        else:
            ret.extend(self.move_bot([(False, self)], self.control))

        new_states: list[State_multiple] = []
        for x, state in ret:
            new_states.append(state.synchronise_states(x))

        return new_states

    def move_bot(self, states: list[tuple[bool, State_multiple]], robot: int) -> list[tuple[bool, State_multiple]]:
        ret: list[tuple[bool, State_multiple]] = []
        for su, state in states:
            old_keys: str = state.sub_states[robot].keys
            for neighbour in state.sub_states[robot].neighbours():
                new_state: State_multiple = state.copy()
                new_state.sub_states[robot] = neighbour
                su = su or (old_keys != neighbour.keys)
                new_state.control = robot
                ret.append((su, new_state))

        return ret

    def synchronise_states(self, key_options: bool = False) -> State_multiple:
        keys: set[str] = set()
        time: int = 0
        for state in self.sub_states:
            keys = keys.union(set(state.keys))
            time = max(time, state.time)

        new_keys: str = "".join(keys)
        for i in range(len(self.sub_states)):
            self.sub_states[i].keys = new_keys
            self.sub_states[i].time = time
            if key_options:
                self.sub_states[i].prev = -1

        if key_options:
            self.control = -1

        return self

    def copy(self) -> State_multiple:
        return State_multiple([sub_state.copy() for sub_state in self.sub_states])

    def time(self) -> int:
        return self.sub_states[0].time

    def keys(self) -> str:
        return self.sub_states[0].keys


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    states: deque[State_single] = deque()
    best: defaultdict[int, int] = defaultdict(lambda: 10 ** 6)
    states.append(State_single(list(map(str.strip, inp))))
    count: int = 0
    for i in set("".join(inp)):
        if i.islower():
            count += 1

    while states:
        active: State_single = states.popleft()
        neighbours: list[State_single] = active.neighbours()
        for neighbour in neighbours:
            if len(neighbour.keys) == count:
                print()
                return neighbour.time

            hashed: int = hash(neighbour)
            if best[hashed] <= neighbour.time:
                continue

            best[hashed] = neighbour.time

            states.append(neighbour)

        del active
    return -1


def str_assign(string: str, index: int, item: str) -> str:
    return string[:index] + item + string[index+1:]


def initial_state(inp: list[str]) -> tuple[list[str], list[State_single]]:
    inp = list(map(str.strip, inp))
    center_x: int = len(inp[0]) // 2
    center_y: int = len(inp) // 2

    inp[center_y - 1] = str_assign(inp[center_y - 1], center_x - 1, "@")
    inp[center_y - 1] = str_assign(inp[center_y - 1], center_x, "#")
    inp[center_y - 1] = str_assign(inp[center_y - 1], center_x + 1, "@")
    inp[center_y] = str_assign(inp[center_y], center_x - 1, "#")
    inp[center_y] = str_assign(inp[center_y], center_x, "#")
    inp[center_y] = str_assign(inp[center_y], center_x + 1, "#")
    inp[center_y + 1] = str_assign(inp[center_y + 1], center_x - 1, "@")
    inp[center_y + 1] = str_assign(inp[center_y + 1], center_x, "#")
    inp[center_y + 1] = str_assign(inp[center_y + 1], center_x + 1, "@")

    states: list[State_single] = []
    for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        states.append(State_single(
            inp,
            (center_x + x, center_y + y),
        ))

    return inp, states


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    states: deque[State_multiple] = deque()
    best: defaultdict[int, int] = defaultdict(lambda: 10 ** 6)

    sub_states: list[State_single]
    inp, sub_states = initial_state(inp)
    states.append(State_multiple(sub_states))
    count: int = 0
    for i in set("".join(inp)):
        if i.islower():
            count += 1

    while states:
        active: State_multiple = states.popleft()
        neighbours: list[State_multiple] = active.neighbours()
        for neighbour in neighbours:
            if len(neighbour.keys()) == count:
                return neighbour.time()

            hashed: int = hash(neighbour)
            if best[hashed] <= neighbour.time():
                continue

            best[hashed] = neighbour.time()

            states.append(neighbour)

        del active

    return -1


def main() -> None:
    test_input: str = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 127
    test_output_part_2_expected: OUTPUT_TYPE = 32

    file_location: str = "python/Advent of Code/2019/Day 18/input.txt"
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
