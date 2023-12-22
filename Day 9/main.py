from collections import defaultdict


OUTPUT_TYPE = int


def run_program(program_list: list[int], inputs: list[int] = [].copy()) -> list[int]:
    program: defaultdict[int, int] = defaultdict(lambda: 0)
    for key, value in enumerate(program_list):
        program[key] = value

    parameter_types: dict[int, tuple[int, ...]] = {
        1: (1, 1, 0),
        2: (1, 1, 0),
        3: (0, ),
        4: (1, ),
        5: (1, 1),
        6: (1, 1),
        7: (1, 1, 0),
        8: (1, 1, 0),
        9: (1, )
    }

    outputs: list[int] = []
    inputs = inputs[::-1]

    instruction_pointer: int = 0
    relative_base: int = 0
    while program[instruction_pointer] != 99:
        prev_index: int = instruction_pointer

        opcode_unpared: int = program[instruction_pointer]
        opcode: int = opcode_unpared % 100
        parameter_type: tuple[int, ...] = parameter_types[opcode]
        parameter_count: int = len(parameter_types[opcode])

        modes: tuple[int, ...] = tuple([
            int(str(opcode_unpared)[
                :-2].zfill(parameter_count)[::-1][parameter])
            for parameter in range(parameter_count)
        ])

        parameters_unparsed: list[int] = [
            program[instruction_pointer + i + 1]
            for i in range(parameter_count)
        ]

        params = [0 for _ in parameter_type]
        for i, param_type in enumerate(parameter_type):
            if param_type == 0:
                if modes[i] == 0:
                    params[i] = parameters_unparsed[i]
                elif modes[i] == 2:
                    params[i] = parameters_unparsed[i] + relative_base
                else:
                    raise ValueError("Oh crap!")
                continue

            if param_type == 1:
                if modes[i] == 0:
                    params[i] = program[parameters_unparsed[i]]
                elif modes[i] == 1:
                    params[i] = parameters_unparsed[i]
                elif modes[i] == 2:
                    params[i] = program[parameters_unparsed[i] + relative_base]
                else:
                    raise ValueError("Oh crap!")
                continue

            raise ValueError("Oh crap!")

        if opcode == 1:
            program[params[2]] = params[0] + params[1]
        elif opcode == 2:
            program[params[2]] = params[0] * params[1]
        elif opcode == 3:
            program[params[0]] = inputs.pop()
        elif opcode == 4:
            outputs.append(params[0])
        elif opcode == 5:
            if params[0]:
                instruction_pointer = params[1]
        elif opcode == 6:
            if not params[0]:
                instruction_pointer = params[1]
        elif opcode == 7:
            program[params[2]] = int(params[0] < params[1])
        elif opcode == 8:
            program[params[2]] = int(params[0] == params[1])
        elif opcode == 9:
            relative_base += params[0]
        else:
            raise ValueError("Oh crap!")

        if instruction_pointer == prev_index:
            instruction_pointer += parameter_count + 1

    return outputs


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    return run_program(eval(f"[{inp[0].strip()}]"), [1])[0]


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    return run_program(eval(f"[{inp[0].strip()}]"), [2])[0]


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 9/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
