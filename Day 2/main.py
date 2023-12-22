OUTPUT_TYPE = int


def run_program(program: list[int]) -> int:
    index: int = 0

    while program[index] != 99:
        opcode: int = program[index]
        inp_1: int = program[program[index + 1]]
        inp_2: int = program[program[index + 2]]
        dest: int = program[index + 3]

        if opcode == 1:
            program[dest] = inp_1 + inp_2
        elif opcode == 2:
            program[dest] = inp_1 * inp_2
        else:
            raise ValueError("Oh crap")

        index += 4

    return program[0]


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    data: list[int] = eval(f"[{inp[0].strip()}]")

    data[1] = 12
    data[2] = 2

    return run_program(data)


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    data: list[int] = eval(f"[{inp[0].strip()}]")

    for noun in range(100):
        for verb in range(100):
            data[1] = noun
            data[2] = verb

            if run_program(data.copy()) == 19690720:
                return 100 * noun + verb

    return -1


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 2/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()


5
7
8
10
11
13
17
18
20
23
24
29
31
33
34
35
40
42
44
46
47
48
51
52
54
55
56
59
60
61
65
66
67
70
71
72
73
74
77
80
81
82
83
85
86
91
93
96
100
