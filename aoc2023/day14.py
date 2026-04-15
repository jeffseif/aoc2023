import collections
import dataclasses
import functools
import typing

import aoc2023


@dataclasses.dataclass(frozen=True)
class IJ:
    idx: int
    jdx: int

    @property
    def shifted(self) -> typing.Self:
        return dataclasses.replace(self, idx=self.idx - 1)


@dataclasses.dataclass(frozen=True)
class Puzzle:
    cubes: tuple[IJ, ...]
    rounds: tuple[IJ, ...]
    size: int

    def __repr__(self) -> str:
        return "\n".join(
            "".join(
                "O"
                if (ij := IJ(idx=idx, jdx=jdx)) in self.rounds
                else "#"
                if ij in self.cubes
                else "."
                for jdx in range(self.size)
            )
            for idx in range(self.size)
        )

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as fp:
            cubes: list[IJ,] = []
            rounds: list[IJ] = []
            for idx, line in enumerate(fp):
                for jdx, char in enumerate(line.strip()):
                    match char:
                        case "#":
                            cubes.append(IJ(idx=idx, jdx=jdx))
                        case "O":
                            rounds.append(IJ(idx=idx, jdx=jdx))
                        case _:
                            ...

        return cls(
            cubes=tuple(cubes),
            rounds=tuple(rounds),
            size=max(ij.idx for ij in cubes) + 1,
        )

    @property
    def shifted(self) -> typing.Self:
        queue = collections.deque(self.rounds)
        queue_as_set = set(queue)
        cubes = set(self.cubes)
        rounds: set[IJ] = set()
        while queue:
            unshifted = queue.popleft()
            queue_as_set.remove(unshifted)
            if (shifted := unshifted.shifted).idx < 0:
                # At the edge, cannot shift
                rounds.add(unshifted)
            elif shifted in cubes:
                # Stopped by cube, cannot shift
                rounds.add(unshifted)
            elif shifted in rounds:
                # Stopped by shifted, cannot shift
                rounds.add(unshifted)
            elif shifted in queue_as_set:
                # Stopped by queued, re-queue in case that one shifts
                queue.append(unshifted)
                queue_as_set.add(unshifted)
            else:
                # Shift and then re-queue
                queue.append(shifted)
                queue_as_set.add(shifted)
        return dataclasses.replace(self, rounds=tuple(rounds))

    @property
    def rotated(self) -> typing.Self:
        def rotate(ij: IJ) -> IJ:
            return dataclasses.replace(ij, idx=ij.jdx, jdx=self.size - 1 - ij.idx)

        return dataclasses.replace(
            self,
            cubes=tuple(map(rotate, self.cubes)),
            rounds=tuple(map(rotate, self.rounds)),
        )

    @property
    def load(self) -> int:
        return sum(self.size - round.idx for round in self.rounds)


@aoc2023.expects(110090)
def part_one(path_to_input: str) -> int:
    return Puzzle.from_path_to_input(path_to_input=path_to_input).shifted.load


REPEATS = 10


@functools.cache
def cycled_puzzle(puzzle: Puzzle, count: int) -> Puzzle:
    if count == 1:
        return puzzle.shifted.rotated.shifted.rotated.shifted.rotated.shifted.rotated
    else:
        if (count % REPEATS) == 0:
            ret = puzzle
            for _ in range(REPEATS):
                ret = cycled_puzzle(puzzle=ret, count=count // REPEATS)
            return ret
        else:
            raise ValueError()


@aoc2023.expects(95254)
def part_two(path_to_input: str) -> int:
    return cycled_puzzle(
        puzzle=Puzzle.from_path_to_input(path_to_input=path_to_input),
        count=1_000_000_000,
    ).load
