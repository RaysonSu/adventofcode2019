from math import lcm
from functools import reduce
OUTPUT_TYPE = int


def sign(num: int) -> int:
    if num:
        return num // abs(num)
    else:
        return 0


def tick(positions: list[list[int]], velocities: list[list[int]]) -> None:
    for index_1, body_1 in enumerate(positions):
        for body_2 in positions:
            for axis in range(3):
                velocities[index_1][axis] -= sign(body_1[axis] - body_2[axis])

    for index in range(len(velocities)):
        for axis in range(3):
            positions[index][axis] += velocities[index][axis]


def parse_inp(inp: list[str]) -> list[list[int]]:
    ret: list[list[int]] = []
    for line in inp:
        ret.append(
            eval(f"[{''.join([x for x in line if x in '1234567890-,'])}]"))
    return ret


def determine_period(data: list[int]) -> int:
    ret: int = 1
    while ret + 10 < len(data):
        if data[:50] == data[ret:ret+50]:
            return ret
        ret += 1
    raise ValueError("Oh crap!")


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    positions: list[list[int]] = parse_inp(inp)
    velocities: list[list[int]] = [[0, 0, 0] for _ in range(len(positions))]

    for _ in range(1000):
        tick(positions, velocities)

    ret: int = 0
    for position, velocity in zip(positions, velocities):
        ret += sum(map(abs, position)) * sum(map(abs, velocity))

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    positions: list[list[int]] = parse_inp(inp)
    velocities: list[list[int]] = [[0, 0, 0] for _ in range(len(positions))]
    velocity_data: list[list[list[int]]] = [[], [], [], []]

    repetitions: int = 10 ** 6
    for _ in range(repetitions):
        for body, velocity in enumerate(velocities):
            velocity_data[body].append(velocity.copy())
        tick(positions, velocities)

    ret: int = 1
    for body in range(4):
        for axis in range(3):
            ret = lcm(ret,
                      determine_period([
                          velocity_data[body][time][axis]
                          for time in range(repetitions)
                      ]))

    return ret


def main() -> None:
    test_input: str = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 14645
    test_output_part_2_expected: OUTPUT_TYPE = 4686774924

    file_location: str = "python/Advent of Code/2019/Day 12/input.txt"
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
