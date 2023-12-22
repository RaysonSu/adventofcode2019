OUTPUT_TYPE = int


def mod_inv(base: int, num: int) -> int:
    r_0: int = num
    r_1: int = base

    s_0: int = 1
    s_1: int = 0

    t_0: int = 0
    t_1: int = 1

    while r_1:
        quotient: int = r_0 // r_1
        r_0, r_1 = r_1, r_0 % r_1
        s_0, s_1 = s_1, s_0 - quotient * s_1
        t_0, t_1 = t_1, t_0 - quotient * t_1

    return s_0 % base


def mod_exp(base: int, exp: int, mod: int) -> int:
    base = base % mod
    ret: int = base
    extra: int = 1
    while exp > 1:
        if exp % 2 == 0:
            ret = (ret * ret) % mod
        else:
            extra = (extra * ret) % mod
            exp -= 1
            ret = (ret * ret) % mod
        exp = exp >> 1
    ret = (ret * extra) % mod
    return ret


print(mod_exp(2345, 4535, 2034))


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    initial: int = 2019
    cards: int = 10007
    for line in inp:
        line = line.strip()
        if line == "deal into new stack":
            initial = -initial - 1
        elif line.startswith("deal with increment"):
            initial *= int(line[20:])
        elif line.startswith("cut"):
            initial -= int(line[4:])

        initial %= cards
    return initial


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    goal: int = 2020
    cards: int = 119315717514047
    multiplier: int = 1
    diffrence: int = 0
    for line in inp:
        line = line.strip()
        if line == "deal into new stack":
            multiplier *= -1
            diffrence = -diffrence - 1
        elif line.startswith("deal with increment"):
            amount: int = int(line[20:])
            multiplier *= amount
            diffrence *= amount
        elif line.startswith("cut"):
            diffrence -= int(line[4:])

        multiplier %= cards
        diffrence %= cards

    times: int = 101741582076661
    a: int = mod_exp(multiplier, times, cards)
    b: int = ((a - 1) * mod_inv(cards, multiplier - 1) * diffrence) % cards

    return (mod_inv(cards, a) * (goal - b)) % cards


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 22/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
