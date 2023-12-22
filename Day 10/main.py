from math import atan2

OUTPUT_TYPE = int


def count_seen(asteroids: list[tuple[int, int]], base: tuple[int, int]) -> int:
    seen: set[float] = set()
    for asteriod in asteroids:
        if asteriod == base:
            continue

        delta_x: int = asteriod[0] - base[0]
        delta_y: int = asteriod[1] - base[1]

        seen.add(atan2(delta_y, delta_x))

    return len(seen)


def distance(point_1: tuple[int, ...], point_2: tuple[int, ...]) -> int:
    return sum([abs(i_1 - i_2) for i_1, i_2 in zip(point_1, point_2)])


def determine_seen(asteroids: list[tuple[int, int]], base: tuple[int, int]) -> dict[float, tuple[int, int]]:
    seen: dict[float, tuple[int, int]] = {}
    for asteriod in asteroids:
        if asteriod == base:
            continue

        delta_x: int = asteriod[0] - base[0]
        delta_y: int = asteriod[1] - base[1]

        angle: float = -atan2(delta_x, delta_y)

        if angle in seen.keys():
            prev: tuple[int, int] = seen[angle]

            if distance(asteriod, base) < distance(prev, base):
                seen[angle] = asteriod
        else:
            seen[angle] = asteriod

    return seen


def parse_inp(inp: list[str]) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for row_index, row in enumerate(inp):
        for col_index, char in enumerate(row.strip()):
            if char != "#":
                continue

            points.append((col_index, row_index))

    return points


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    asteroids: list[tuple[int, int]] = parse_inp(inp)
    best: int = 0

    for base in asteroids:
        best = max(best, count_seen(asteroids, base))

    return best


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    asteroids: list[tuple[int, int]] = parse_inp(inp)
    best: int = 0
    best_base: tuple[int, int] = (-1, -1)

    for base in asteroids:
        count: int = count_seen(asteroids, base)
        if count > best:
            best = count
            best_base = base

    asteroids.remove(best_base)

    asteroids_exploded: int = 0
    while True:
        asteroids_seen: dict[float, tuple[int, int]]

        asteroids_seen = determine_seen(asteroids, best_base)
        order: list[float] = sorted(asteroids_seen.keys())

        for angle in order:
            asteroids_exploded += 1
            asteroids.remove(asteroids_seen[angle])

            if asteroids_exploded == 200:
                asteroid_x: int
                asteroid_y: int

                asteroid_x, asteroid_y = asteroids_seen[angle]
                return 100 * asteroid_x + asteroid_y


def main() -> None:
    test_input: str = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 210
    test_output_part_2_expected: OUTPUT_TYPE = 802

    file_location: str = "python/Advent of Code/2019/Day 10/input.txt"
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
