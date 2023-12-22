OUTPUT_TYPE = int


def main_part_1(inp: list[str]) -> int:
    ret: int = 0
    for line in inp:
        ret += int(line.strip()) // 3 - 2
    return ret


def get_fuel(mass: int) -> int:
    if mass < 9:
        return 0

    required: int = mass // 3 - 2

    return required + get_fuel(required)


def main_part_2(inp: list[str]) -> int:
    ret: int = 0
    for line in inp:
        ret += get_fuel(int(line.strip()))
    return ret


def main() -> None:
    test_input: str = """100756"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 33583
    test_output_part_2_expected: OUTPUT_TYPE = 50346

    file_location: str = "python/Advent of Code/2019/Day 1/input.txt"
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
