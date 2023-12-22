OUTPUT_TYPE = int


def compute_wire(wire: list[str]) -> set[tuple[int, int]]:
    ret: set[tuple[int, int]] = set()
    current_pos: list[int] = [0, 0]
    for line in wire:
        direction: str = line[0]
        amount: int = int(line[1:])
        for _ in range(amount):
            current_pos[0] += {"U": 0, "D": 0, "R": 1, "L": -1}[direction]
            current_pos[1] += {"U": 1, "D": -1, "R": 0, "L": 0}[direction]
            ret.add((current_pos[0], current_pos[1]))
    return ret


def wire_path(wire: list[str]) -> list[tuple[int, int]]:
    ret: list[tuple[int, int]] = []
    current_pos: list[int] = [0, 0]
    for line in wire:
        direction: str = line[0]
        amount: int = int(line[1:])
        for _ in range(amount):
            current_pos[0] += {"U": 0, "D": 0, "R": 1, "L": -1}[direction]
            current_pos[1] += {"U": 1, "D": -1, "R": 0, "L": 0}[direction]
            ret.append((current_pos[0], current_pos[1]))
    return ret


def parse_inp(inp: list[str]) -> tuple[list[str], list[str]]:
    ret: tuple[list[str], list[str]] = ([], [])
    for index, wire in enumerate(inp):
        for instruction in wire.split(","):
            ret[index].append(instruction)

    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    wire_1: list[str]
    wire_2: list[str]

    wire_1, wire_2 = parse_inp(inp)
    intersections = compute_wire(wire_1).intersection(compute_wire(wire_2))

    ret = 10 ** 200
    for x, y in intersections:
        ret = min(ret, abs(x) + abs(y))

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    wire_1: list[str]
    wire_2: list[str]

    wire_1, wire_2 = parse_inp(inp)
    intersections = compute_wire(wire_1).intersection(compute_wire(wire_2))

    wire_1_path: list[tuple[int, int]] = wire_path(wire_1)
    wire_2_path: list[tuple[int, int]] = wire_path(wire_2)

    ret = 10 ** 200
    for point in intersections:
        ret = min(ret, wire_1_path.index(point) + wire_2_path.index(point) + 2)

    return ret


def main() -> None:
    test_input: str = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 135
    test_output_part_2_expected: OUTPUT_TYPE = 410

    file_location: str = "python/Advent of Code/2019/Day 3/input.txt"
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
