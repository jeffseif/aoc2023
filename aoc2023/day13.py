import collections.abc
import dataclasses
import itertools
import operator
import typing
import aoc2023


def int_from_bits(bits: collections.abc.Iterable[bool]) -> int:
    return sum((base) << bit for bit, base in enumerate(bits))


@dataclasses.dataclass
class Block:
    grid: list[list[bool]]

    def __repr__(self) -> str:
        return "\n".join(
            "".join("#" if bit else "." for bit in row) for row in self.grid
        )

    @classmethod
    def from_lines(cls, lines: collections.abc.Iterable[str]) -> typing.Self:
        return cls(grid=[list(map("#".__eq__, line)) for line in lines if line.strip()])

    @property
    def rows(self) -> list[int]:
        return list(map(int_from_bits, self.grid))

    @property
    def cols(self) -> list[int]:
        return list(map(int_from_bits, zip(*self.grid, strict=True)))

    def score(self, compare_func: typing.Callable[[tuple[int, int]], bool]) -> int:
        for is_horizontal in (False, True):
            multiplier = 100 if is_horizontal else 1
            grid = self.rows if is_horizontal else self.cols
            for split in range(1, len(grid)):
                left_rights = zip(*(reversed(grid[:split]), grid[split:]))
                if compare_func(*left_rights):
                    return split * multiplier
        else:
            raise ValueError


def iter_block(path_to_input: str) -> collections.abc.Iterator[Block]:
    with open(file=path_to_input) as fp:
        for block in fp.read().split("\n\n"):
            yield Block.from_lines(lines=map(str.strip, block.split("\n")))


def all_equal(*pairs: tuple[int, int]) -> bool:
    return all(itertools.starmap(operator.eq, pairs))


@aoc2023.expects(35232)
def part_one(path_to_input: str) -> int:
    return sum(
        block.score(compare_func=all_equal)
        for block in iter_block(path_to_input=path_to_input)
    )


def off_by_one_rest_equal(*pairs: tuple[int, int]) -> bool:
    unequals = [(left, right) for left, right in pairs if left != right]
    try:
        ((left, right),) = unequals
    except ValueError:
        return False
    else:
        xor = left ^ right
        return (xor & (xor - 1)) == 0


@aoc2023.expects(37982)
def part_two(path_to_input: str) -> int:
    return sum(
        block.score(compare_func=off_by_one_rest_equal)
        for block in iter_block(path_to_input=path_to_input)
    )
