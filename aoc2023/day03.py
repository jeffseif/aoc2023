import collections
import collections.abc
import dataclasses
import re
import typing

import aoc2023


@dataclasses.dataclass
class Number:
    row: int
    span: tuple[int, int]
    value: int


CoordType = tuple[int, int]


@dataclasses.dataclass
class Puzzle:
    gears: set[CoordType]
    numbers: list[Number]
    symbols: set[CoordType]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        numbers: list[Number] = []
        symbols: set[CoordType] = set()
        gears: set[CoordType] = set()
        with open(file=path_to_input) as f:
            for row, line in enumerate(map(str.strip, f)):
                numbers.extend(
                    Number(row=row, span=match.span(), value=int(match.group()))
                    for match in re.finditer(pattern=r"\d+", string=line)
                )
                symbols.update(
                    (symbol_row, col)
                    for match in re.finditer(pattern=r"[^.\d]+", string=line)
                    for symbol_row in range(row - 1, row + 2)
                    for col in range(match.start() - 1, match.start() + 2)
                )
                gears.update(
                    (row, match.start())
                    for match in re.finditer(pattern=r"\*", string=line)
                )
        return cls(gears=gears, numbers=numbers, symbols=symbols)

    @property
    def iter_part_number(self) -> collections.abc.Iterator[int]:
        for number in self.numbers:
            if any((number.row, col) in self.symbols for col in range(*number.span)):
                yield number.value

    @property
    def iter_gear_ratio(self) -> collections.abc.Iterator[int]:
        gear_to_numbers: dict[tuple[int, int], list[int]] = collections.defaultdict(
            list
        )
        for number in self.numbers:
            left, right = number.span
            aura = {
                (row, col)
                for row in range(number.row - 1, number.row + 2)
                for col in range(left - 1, right + 1)
            }
            for gear in aura.intersection(self.gears):
                gear_to_numbers[gear].append(number.value)
        for numbers in gear_to_numbers.values():
            if len(numbers) == 2:
                left, right = numbers
                yield left * right


@aoc2023.expects(537732)
def part_one(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return sum(puzzle.iter_part_number)


@aoc2023.expects(84883664)
def part_two(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return sum(puzzle.iter_gear_ratio)
