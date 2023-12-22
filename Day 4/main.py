OUTPUT_TYPE = int


def is_valid(num: int) -> bool:
    ret: bool = False
    for lower, higher in zip(str(num), str(num)[1:]):
        if higher < lower:
            return False
        elif higher == lower:
            ret = True

    return ret


def is_valid_2(num: int) -> bool:
    for lower, higher in zip(str(num), str(num)[1:]):
        if higher < lower:
            return False

    for i in "0123456789":
        if str(num).count(i) == 2:
            return True
    return False


def main_part_1(inp: str) -> OUTPUT_TYPE:
    low: int = int(inp.split("-")[0])
    high: int = int(inp.split("-")[1].strip())

    ret: int = 0
    for number in range(low, high + 1):
        if is_valid(number):
            ret += 1

    return ret


def main_part_2(inp: str) -> OUTPUT_TYPE:
    low: int = int(inp.split("-")[0])
    high: int = int(inp.split("-")[1].strip())

    ret: int = 0
    for number in range(low, high + 1):
        if is_valid_2(number):
            ret += 1

    return ret


def main() -> None:
    input_file: str = "246540-787419"

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
