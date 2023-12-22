from collections import defaultdict
OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> tuple[dict[str, tuple[int, list[tuple[str, int]]]], defaultdict[str, set[str]]]:
    recipes: dict[str, tuple[int, list[tuple[str, int]]]] = {}
    requirements: defaultdict[str, set[str]] = defaultdict(lambda: set())

    for line in inp:
        line = line.strip()
        data: list[str] = line.split(" => ")
        products: list[str] = data[1].split(" ")
        ingredients: list[str] = data[0].split(", ")

        ingredients_parsed: list[tuple[str, int]] = []
        for ingredient in ingredients:
            amount: int = int(ingredient.split(" ")[0])
            item: str = ingredient.split(" ")[1]
            ingredients_parsed.append((item, amount))
            requirements[item].add(products[1])

        recipes[products[1]] = (int(products[0]), ingredients_parsed)

    return recipes, requirements


def compute_requirement(recipes: dict[str, tuple[int, list[tuple[str, int]]]], requirements: defaultdict[str, set[str]], goal: int):
    amounts_required: defaultdict[str, int] = defaultdict(lambda: 0)
    amounts_required["FUEL"] = goal
    remaining: set[str] = set(recipes.keys())

    while remaining:
        guess: str = remaining.pop()
        if len(set(remaining).intersection(requirements[guess])):
            remaining.add(guess)
            continue

        req: int = amounts_required[guess]

        gain: int
        ingredients: list[tuple[str, int]]
        gain, ingredients = recipes[guess]

        copies: int = -(-req // gain)
        for ingredient, amount in ingredients:
            amounts_required[ingredient] += amount * copies

    return amounts_required["ORE"]


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    recipes: dict[str, tuple[int, list[tuple[str, int]]]]
    requirements: defaultdict[str, set[str]]

    recipes, requirements = parse_inp(inp)
    return compute_requirement(recipes, requirements, 1)


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    recipes: dict[str, tuple[int, list[tuple[str, int]]]]
    requirements: defaultdict[str, set[str]]

    recipes, requirements = parse_inp(inp)

    low: int = 0
    high: int = 2 ** 64
    while low + 1 < high:
        mid: int = (low + high) // 2
        if compute_requirement(recipes, requirements, mid) > 10 ** 12:
            high = mid
        else:
            low = mid
    return low


def main() -> None:
    test_input: str = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 2210736
    test_output_part_2_expected: OUTPUT_TYPE = 460664

    file_location: str = "python/Advent of Code/2019/Day 14/input.txt"
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
