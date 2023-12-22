def parse_inp(inp: str) -> list[int]:
    return [int(digit) for digit in inp if digit.isnumeric()]


def fft(signal: list[int]) -> list[int]:
    ret: list[int] = []
    for index in range(1, len(signal) + 1):
        current: int = sum([digit * [0, 1, 0, -1][(i + 1) // index % 4]
                           for i, digit in enumerate(signal)])
        ret.append(abs(current) % 10)
    return ret


def main_part_1(inp: list[str]) -> str:
    signal: list[int] = parse_inp(inp[0])

    for _ in range(100):
        signal = fft(signal)
    return "".join(map(str, signal[:8]))


def main_part_2(inp: list[str]) -> str:
    offset: int = int(inp[0][:7])
    signal: list[int] = parse_inp(inp[0] * 10000)

    signal_data: str = ""
    for i in range(offset - 1, offset + 7):
        ret: int = 0
        for index in range(len(signal) - i):
            ret += signal[i + index] * nCr(index + 99, 99) % 10
        signal_data += str(ret % 10)
    return signal_data


def nCr(n: int, r: int) -> int:
    ret: int = 1
    for i in range(1, r + 1):
        ret *= n - i
        ret //= i
    return ret


def main() -> None:
    test_input: str = "03036732577212944063491565474664"
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: str = "24465799"
    test_output_part_2_expected: str = "84462026"

    file_location: str = "python/Advent of Code/2019/Day 16/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: str = main_part_1(test_input_parsed)
    test_output_part_2: str = main_part_2(test_input_parsed)

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
