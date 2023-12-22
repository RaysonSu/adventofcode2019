from itertools import permutations
OUTPUT_TYPE = int


def run_program_special(program: list[int], inputs: list[int], index: int = 0) -> tuple[list[int], list[int], int]:
    parameter_lengths: dict[int, int] = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3
    }
    outputs: list[int] = []
    inputs = inputs[::-1]

    while program[index] != 99 and outputs == []:
        prev_index: int = index

        opcode_unpared: int = program[index]
        opcode: int = opcode_unpared % 100
        parameter_count: int = parameter_lengths[opcode]

        modes: tuple[bool, ...] = tuple([
            str(opcode_unpared)[:-2].zfill(
                parameter_count)[::-1][parameter] == "1"
            for parameter in range(parameter_count)
        ])

        param: list[int] = [
            program[index + i + 1]
            for i in range(parameter_count)
        ]

        param_0: int
        param_1: int
        param_2: int
        if opcode == 1:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = param_0 + param_1
        elif opcode == 2:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = param_0 * param_1
        elif opcode == 3:
            param_0 = param[0]
            program[param_0] = inputs.pop()
        elif opcode == 4:
            param_0 = param[0]
            outputs.append(program[param_0])
        elif opcode == 5:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            if param_0:
                index = param_1
        elif opcode == 6:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            if not param_0:
                index = param_1
        elif opcode == 7:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = int(param_0 < param_1)
        elif opcode == 8:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = int(param_0 == param_1)
        else:
            raise ValueError("Oh crap")

        if index == prev_index:
            index += parameter_count + 1

    return program, outputs, index


def run_program(program: list[int], inputs: list[int]) -> list[int]:
    parameter_lengths: dict[int, int] = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3
    }
    outputs: list[int] = []
    inputs = inputs[::-1]

    index: int = 0
    while program[index] != 99:
        prev_index: int = index

        opcode_unpared: int = program[index]
        opcode: int = opcode_unpared % 100
        parameter_count: int = parameter_lengths[opcode]

        modes: tuple[bool, ...] = tuple([
            str(opcode_unpared)[:-2].zfill(
                parameter_count)[::-1][parameter] == "1"
            for parameter in range(parameter_count)
        ])

        param: list[int] = [
            program[index + i + 1]
            for i in range(parameter_count)
        ]

        param_0: int
        param_1: int
        param_2: int
        if opcode == 1:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = param_0 + param_1
        elif opcode == 2:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = param_0 * param_1
        elif opcode == 3:
            param_0 = param[0]
            program[param_0] = inputs.pop()
        elif opcode == 4:
            param_0 = param[0]
            outputs.append(program[param_0])
        elif opcode == 5:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            if param_0:
                index = param_1
        elif opcode == 6:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            if not param_0:
                index = param_1
        elif opcode == 7:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = int(param_0 < param_1)
        elif opcode == 8:
            param_0 = param[0] if modes[0] else program[param[0]]
            param_1 = param[1] if modes[1] else program[param[1]]
            param_2 = param[2]
            program[param_2] = int(param_0 == param_1)
        else:
            raise ValueError("Oh crap")

        if index == prev_index:
            index += parameter_count + 1

    return outputs


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    best: int = 0
    program: list[int] = eval(f"[{inp[0].strip()}]")

    for inputs in permutations(range(5)):
        signal: int = 0

        for value in inputs:
            signal = run_program(program, [value, signal])[0]

        best = max(best, signal)
    return best


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    best: int = 0
    program: list[int] = eval(f"[{inp[0].strip()}]")

    for inputs in permutations(range(5, 10)):
        states: list[list[int]] = [program.copy() for _ in range(5)]
        indexes: list[int] = [0 for _ in range(5)]
        outputs: list[int]

        signal: int = 0
        for i, value in enumerate(inputs):
            states[i], outputs, indexes[i] = run_program_special(
                states[i],
                [value, signal],
                indexes[i]
            )
            signal = outputs[0]

        while outputs:
            for i in range(5):
                states[i], outputs, indexes[i] = run_program_special(
                    states[i],
                    [signal],
                    indexes[i]
                )

                if not outputs:
                    break

                signal = outputs[0]

        best = max(best, signal)
    return best


def main() -> None:

    file_location: str = "python/Advent of Code/2019/Day 7/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()
    input_file = [x.replace("\n", "") for x in input_file]

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
