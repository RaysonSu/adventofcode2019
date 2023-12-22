from collections import defaultdict
from time import sleep


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

    def read_output_all(self) -> list[int]:
        ret: list[int] = self.outputs.copy()
        self.outputs = []
        return ret

    def set_memory(self, index: int, value: int) -> None:
        self.program[index] = value


def str_assign(string: str, index: int, item: str) -> str:
    return string[:index] + item + string[index+1:]


def sign(num: int) -> int:
    if num:
        return num // abs(num)
    else:
        return 0


def main_part_1(inp: list[str]) -> int:
    program: Intcode = Intcode(eval(f"[{inp[0].strip()}]"))
    program.read_input(0)
    output: list[int] = program.read_output_all()
    ret: int = 0
    for x, y, tile_id in zip(output[::3], output[1::3], output[2::3]):
        if tile_id == 2:
            ret += 1
    return ret


def main_part_2(inp: list[str]) -> int:
    program: Intcode = Intcode(eval(f"[{inp[0].strip()}]"))
    program.set_memory(0, 2)
    program.read_input(0)
    output: list[int] = program.read_output_all()
    ret: int = 0

    x_coords = output[::3]
    y_coords = output[1::3]
    tile_ids = output[2::3]
    grid_width: int = max(x_coords)
    grid_length: int = max(y_coords)
    score: int = 0
    grid: list[str] = ["." * (grid_width + 1) for _ in range(grid_length + 1)]
    ball: int = -1
    paddle: int = -1

    for x, y, tile_id in zip(x_coords, y_coords, tile_ids):
        if x == -1 and y == 0:
            score = tile_id
        else:
            block: str = [" ", "#", "X", "-", "o"][tile_id]
            grid[y] = str_assign(grid[y], x, block)
            if tile_id == 3:
                paddle = x
            elif tile_id == 4:
                ball = x

    for row in grid:
        print(row)
    print(f"Score: {score}")
    sleep(1 / 60)

    while len(output) > 3:
        program.read_input(sign(ball - paddle))
        output = program.read_output_all()
        x_coords = output[::3]
        y_coords = output[1::3]
        tile_ids = output[2::3]
        for x, y, tile_id in zip(x_coords, y_coords, tile_ids):
            if x == -1 and y == 0:
                score = tile_id
            else:
                block = [" ", "#", "X", "-", "o"][tile_id]
                grid[y] = str_assign(grid[y], x, block)
                if tile_id == 3:
                    paddle = x
                elif tile_id == 4:
                    ball = x
        print("\033[A" * (grid_length + 3))
        for row in grid:
            print(row)
        print(f"Score: {score}")
        sleep(1 / 60)
    return score


def main() -> None:
    file_location: str = "python/Advent of Code/2019/Day 13/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    print(f"Part 1: {main_part_1(input_file)}")
    print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
