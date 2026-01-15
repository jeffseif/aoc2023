import collections.abc
import dataclasses
import functools
import math
import operator

import aoc2023

eps = 1e-12


@dataclasses.dataclass
class Race:
    duration: int
    distance: int

    @property
    def margin(self) -> int:
        roots = (
            op(
                self.duration,
                (self.duration * self.duration - 4 * self.distance) ** 0.5,
            )
            / 2
            for op in (operator.add, operator.sub)
        )
        low, high = sorted(roots)
        return int(math.floor(high - eps) - math.ceil(low + eps)) + 1


def iter_race_one(path_to_input: str) -> collections.abc.Iterator[Race]:
    with open(file=path_to_input) as f:
        duration_line, distance_line = f
    for duration_str, distance_str in zip(
        duration_line.split()[1:], distance_line.split()[1:]
    ):
        yield Race(duration=int(duration_str), distance=int(distance_str))


def get_race_two(path_to_input: str) -> Race:
    with open(file=path_to_input) as f:
        duration_line, distance_line = f
    _, _, duration_str = duration_line.partition(":")
    _, _, distance_str = distance_line.partition(":")
    return Race(
        duration=int(duration_str.replace(" ", "")),
        distance=int(distance_str.replace(" ", "")),
    )


@aoc2023.expects(5133600)
def part_one(path_to_input: str) -> int:
    return functools.reduce(
        operator.mul,
        (race.margin for race in iter_race_one(path_to_input=path_to_input)),
    )


@aoc2023.expects(40651271)
def part_two(path_to_input: str) -> int:
    race = get_race_two(path_to_input=path_to_input)
    return race.margin
