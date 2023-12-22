def main_part_1(inp: list[str]) -> int:
    width: int = 25
    length: int = 6

    image_layers: list[str] = [
        inp[0][width * length * i: width * length * (i + 1)] for i in range(len(inp[0]) // (width * length))
    ]
    best: tuple[int, int, int] = (width * length, 0, 0)
    for layer in image_layers:
        counts: tuple[int, int, int] = (
            layer.count("0"),
            layer.count("1"),
            layer.count("2")
        )
        best = min(best, counts)

    return best[1] * best[2]


def main_part_2(inp: list[str]) -> str:
    width: int = 25
    length: int = 6

    image_layers: list[str] = [
        inp[0][width * length * i: width * length * (i + 1)] for i in range(len(inp[0]) // (width * length))
    ]

    image: int = 0
    mask: int = (1 << (width * length)) - 1

    for layer in image_layers:
        image_layer: int = int(layer.replace("2", "0"), 2)
        mask_layer: int = int(layer.replace("1", "0").replace("2", "1"), 2)

        image_layer &= mask
        mask &= mask_layer
        image |= image_layer

    image_decoded: str = bin(image)[2:].zfill(width * length)
    ret: str = ""
    for row in range(length):
        ret += "\n" + image_decoded[width * row: width * (row + 1)]

    ret = ret.replace("1", "#").replace("0", " ")

    return ret


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 8/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
