from collections import defaultdict


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.program: defaultdict[int, int] = defaultdict(lambda: 0)
        for key, value in enumerate(program):
            self.program[key] = value

        self.outputs: list[int] = []
        self.instruction_pointer: int = 0
        self.relative_base: int = 0

        self.parameter_types: dict[int, tuple[int, ...]] = {
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

    def read_input(self, input_value: int) -> bool:
        input_read: bool = False

        while self.program[self.instruction_pointer] != 99:
            prev_index: int = self.instruction_pointer

            opcode_unpared: int = self.program[self.instruction_pointer]
            opcode: int = opcode_unpared % 100
            parameter_type: tuple[int, ...] = self.parameter_types[opcode]
            parameter_count: int = len(self.parameter_types[opcode])

            modes: tuple[int, ...] = tuple([
                int(str(opcode_unpared)[
                    :-2].zfill(parameter_count)[::-1][parameter])
                for parameter in range(parameter_count)
            ])

            parameters_unparsed: list[int] = [
                self.program[self.instruction_pointer + i + 1]
                for i in range(parameter_count)
            ]

            params = [0 for _ in parameter_type]
            for i, param_type in enumerate(parameter_type):
                if param_type == 0:
                    if modes[i] == 0:
                        params[i] = parameters_unparsed[i]
                    elif modes[i] == 2:
                        params[i] = parameters_unparsed[i] + self.relative_base
                    else:
                        raise ValueError("Oh crap!")
                    continue

                if param_type == 1:
                    if modes[i] == 0:
                        params[i] = self.program[parameters_unparsed[i]]
                    elif modes[i] == 1:
                        params[i] = parameters_unparsed[i]
                    elif modes[i] == 2:
                        params[i] = self.program[parameters_unparsed[i] +
                                                 self.relative_base]
                    else:
                        raise ValueError("Oh crap!")
                    continue

                raise ValueError("Oh crap!")

            if opcode == 1:
                self.program[params[2]] = params[0] + params[1]
            elif opcode == 2:
                self.program[params[2]] = params[0] * params[1]
            elif opcode == 3:
                if input_read:
                    return False

                self.program[params[0]] = input_value
                input_read = True
            elif opcode == 4:
                self.outputs.append(params[0])
            elif opcode == 5:
                if params[0]:
                    self.instruction_pointer = params[1]
            elif opcode == 6:
                if not params[0]:
                    self.instruction_pointer = params[1]
            elif opcode == 7:
                self.program[params[2]] = int(params[0] < params[1])
            elif opcode == 8:
                self.program[params[2]] = int(params[0] == params[1])
            elif opcode == 9:
                self.relative_base += params[0]
            else:
                raise ValueError("Oh crap!")

            if self.instruction_pointer == prev_index:
                self.instruction_pointer += parameter_count + 1

        return True

    def read_output(self) -> int:
        return self.outputs.pop(0)


def str_assign(string: str, index: int, item: str) -> str:
    return string[:index] + item + string[index+1:]


def main_part_1(inp: list[str]) -> int:
    program: Intcode = Intcode(eval(f"[{inp[0].strip()}]"))

    location: tuple[int, int] = (0, 0)
    angle: int = 0
    painted: set[tuple[int, int]] = set()
    white: set[tuple[int, int]] = set()

    directions: list[tuple[int, int]] = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    while not program.read_input(int(location in white)):
        if program.read_output():
            white.add(location)
        elif location in white:
            white.remove(location)

        if program.read_output():
            angle -= 1
        else:
            angle += 1

        painted.add(location)
        location = (
            location[0] + directions[angle % 4][0],
            location[1] + directions[angle % 4][1]
        )

    return len(painted)


def main_part_2(inp: list[str]) -> str:
    program: Intcode = Intcode(eval(f"[{inp[0].strip()}]"))

    location: tuple[int, int] = (0, 0)
    angle: int = 0
    painted: set[tuple[int, int]] = set()
    white: set[tuple[int, int]] = {(0, 0)}

    directions: list[tuple[int, int]] = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    while not program.read_input(int(location in white)):
        if program.read_output():
            white.add(location)
        elif location in white:
            white.remove(location)

        if program.read_output():
            angle -= 1
        else:
            angle += 1

        painted.add(location)
        location = (
            location[0] + directions[angle % 4][0],
            location[1] + directions[angle % 4][1]
        )

    x_coords: list[int] = []
    y_coords: list[int] = []
    while white:
        x: int
        y: int

        x, y = white.pop()

        x_coords.append(x)
        y_coords.append(y)

    x_normalization: int = min(x_coords)
    y_normalization: int = min(y_coords)

    x_coords = [x - x_normalization for x in x_coords]
    y_coords = [y - y_normalization for y in y_coords]

    length: int = max(x_coords) + 1
    width: int = max(y_coords) + 1

    ret: str = ("\n" + "." * length) * width
    for x, y in zip(x_coords, y_coords):
        ret = str_assign(ret, x + (width - y - 1) * (length + 1) + 1, "#")

    return ret


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 11/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
