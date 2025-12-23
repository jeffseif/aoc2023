import collections.abc
import re


import aoc2023


def iter_digit_numbers(path_to_input: str) -> collections.abc.Iterator[int]:
    with open(file=path_to_input) as f:
        for line in f:
            groups = re.findall(pattern=r"\d", string=line)
            yield int(groups[0]) * 10 + int(groups[-1])


NUMBER_NAMES = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def iter_all_numbers(path_to_input: str) -> collections.abc.Iterator[int]:
    with open(file=path_to_input) as f:
        for line in f:
            groups = sorted(
                (idx, pattern)
                for item in NUMBER_NAMES.items()
                for pattern in map(str, item)
                for idx in range(len(line))
                if line[idx:].startswith(pattern)
            )
            tens, ones = (
                int(group) if len(group) == 1 else NUMBER_NAMES[group]
                for _, group in (groups[0], groups[-1])
            )
            yield tens * 10 + ones


@aoc2023.expects(56042)
def part_one(path_to_input: str) -> int:
    return sum(iter_digit_numbers(path_to_input=path_to_input))


@aoc2023.expects(55358)
def part_two(path_to_input: str) -> int:
    return sum(iter_all_numbers(path_to_input=path_to_input))
