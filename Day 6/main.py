from collections import defaultdict

OUTPUT_TYPE = int


def generate_parents(orbits: dict[str, str], planet: str) -> set[str]:
    ret: set[str] = set()
    while planet != "COM":
        planet = orbits[planet]
        ret.add(planet)

    return ret


def parse_inp(inp: list[str]) -> defaultdict[str, list[str]]:
    orbits: defaultdict[str, list[str]] = defaultdict(lambda: [].copy())

    for line in inp:
        line = line.strip()
        planets: list[str] = line.split(")")
        orbits[planets[0]].append(planets[1])

    return orbits


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    orbits: dict[str, list[str]] = parse_inp(inp)
    orbit_count: dict[str, int] = {"COM": 0}
    seen: list[str] = ["COM"]

    while seen:
        current: str = seen.pop()
        current_depth: int = orbit_count[current]

        for planet in orbits[current]:
            orbit_count[planet] = current_depth + 1
            seen.append(planet)

    return sum(orbit_count.values())


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    orbits: dict[str, list[str]] = parse_inp(inp)
    orbit_count: dict[str, int] = {"COM": 0}

    orbits_reverse: dict[str, str] = {}
    seen: list[str] = ["COM"]

    while seen:
        current: str = seen.pop()
        current_depth: int = orbit_count[current]

        for planet in orbits[current]:
            orbit_count[planet] = current_depth + 1
            seen.append(planet)
            orbits_reverse[planet] = current

    you_parents: set[str] = generate_parents(orbits_reverse, "YOU")
    san_parents: set[str] = generate_parents(orbits_reverse, "SAN")

    common_parents: set[str] = you_parents.intersection(san_parents)
    intersection: str = common_parents.difference(
        {orbits_reverse[planet] for planet in common_parents if planet != "COM"}).pop()

    return orbit_count["YOU"] + orbit_count["SAN"] - 2 * orbit_count[intersection] - 2


def main() -> None:
    test_input: str = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 54
    test_output_part_2_expected: OUTPUT_TYPE = 4

    file_location: str = "python/Advent of Code/2019/Day 6/input.txt"
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
