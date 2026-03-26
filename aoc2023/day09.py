import collections.abc
import itertools

import aoc2023


def iter_history_from_path_to_input(
    path_to_input: str,
) -> collections.abc.Iterable[list[int]]:
    with open(file=path_to_input) as fp:
        for line in fp:
            yield list(map(int, line.split()))


def extrapolate(history: list[int]) -> int:
    if all(element == 0 for element in history):
        return 0
    else:
        return history[-1] + extrapolate(
            history=[right - left for left, right in itertools.pairwise(history)]
        )


@aoc2023.expects(1789635132)
def part_one(path_to_input: str) -> int:
    return sum(
        map(extrapolate, iter_history_from_path_to_input(path_to_input=path_to_input))
    )


@aoc2023.expects(913)
def part_two(path_to_input: str) -> int:
    iter_reverse_history = (
        list(reversed(history))
        for history in iter_history_from_path_to_input(path_to_input=path_to_input)
    )
    return sum(map(extrapolate, iter_reverse_history))
