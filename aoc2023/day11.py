import collections.abc
import dataclasses
import itertools
import typing

import aoc2023


@dataclasses.dataclass(frozen=True)
class IJ:
    idx: int
    jdx: int


@dataclasses.dataclass
class Puzzle:
    galaxies: set[IJ]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as fp:
            return cls(
                galaxies={
                    IJ(idx=idx, jdx=jdx)
                    for idx, line in enumerate(fp)
                    for jdx, char in enumerate(line.strip())
                    if char == "#"
                }
            )

    def total_steps(self, expansion: int) -> int:
        idxs, jdxs = zip(*((ij.idx, ij.jdx) for ij in self.galaxies))

        def get_missings(present: tuple[int, ...]) -> set[int]:
            possible = range(max(present))
            return set(possible) - set(present)

        empty_idxs = get_missings(present=idxs)
        empty_jdxs = get_missings(present=jdxs)

        def get_steps(left: IJ, right: IJ) -> collections.abc.Iterator[int]:
            def iter_steps(
                attr: str, exclusion: set[int]
            ) -> collections.abc.Iterator[int]:
                for value in range(
                    min(getattr(left, attr), getattr(right, attr)),
                    max(getattr(left, attr), getattr(right, attr)),
                ):
                    if value in exclusion:
                        yield expansion
                    else:
                        yield 1

            yield from iter_steps(attr="idx", exclusion=empty_idxs)
            yield from iter_steps(attr="jdx", exclusion=empty_jdxs)

        return sum(
            step
            for stepper in itertools.starmap(
                get_steps, itertools.combinations(self.galaxies, r=2)
            )
            for step in stepper
        )


@aoc2023.expects(9742154)
def part_one(path_to_input: str) -> int:
    return Puzzle.from_path_to_input(path_to_input=path_to_input).total_steps(
        expansion=2
    )


@aoc2023.expects(411142919886)
def part_two(path_to_input: str) -> int:
    return Puzzle.from_path_to_input(path_to_input=path_to_input).total_steps(
        expansion=1_000_000
    )
