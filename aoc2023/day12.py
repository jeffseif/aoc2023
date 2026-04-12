import collections.abc
import dataclasses
import enum
import functools
import typing

import aoc2023


class Condition(enum.Enum):
    OPERATIONAL = enum.auto()
    DAMAGED = enum.auto()
    UNKNOWN = enum.auto()


CHAR_TO_CONDITION = {
    ".": Condition.OPERATIONAL,
    "#": Condition.DAMAGED,
    "?": Condition.UNKNOWN,
}
assert set(Condition) == set(CHAR_TO_CONDITION.values())
CONDITION_TO_CHAR = {v: k for k, v in CHAR_TO_CONDITION.items()}


@functools.cache
def count_arrangements(groups: tuple[int, ...], slots: tuple[Condition, ...]) -> int:
    count = 0
    group, groups = groups[0], groups[1:]
    # Iterate over all possible spans
    for idx in range(len(slots) - group + 1):
        jdx = idx + group
        if any(slot == Condition.DAMAGED for slot in slots[:idx]):
            # Some preceding damaged aren't accounted for
            break
        elif any(slot == Condition.OPERATIONAL for slot in slots[idx:jdx]):
            # Some spanned are operational
            ...
        elif jdx < len(slots) and slots[jdx] == Condition.DAMAGED:
            # The following damaged isn't account for
            ...
        elif groups:
            count += count_arrangements(
                groups=groups,
                # Remove the spanned, plus the following
                slots=slots[jdx + 1 :],
            )
        elif any(slot == Condition.DAMAGED for slot in slots[jdx:]):
            # Some following damaged aren't account for
            ...
        else:
            count += 1
    return count


@dataclasses.dataclass
class Spring:
    groups: tuple[int, ...]
    slots: tuple[Condition, ...]

    def __repr__(self) -> str:
        return " ".join(
            (
                "".join(map(CONDITION_TO_CHAR.__getitem__, self.slots)),
                ",".join(map(str, self.groups)),
            )
        )

    @classmethod
    def from_line(cls, line: str) -> typing.Self:
        visual, numerical = line.strip().split(" ")
        return cls(
            groups=tuple(map(int, numerical.split(","))),
            slots=tuple(map(CHAR_TO_CONDITION.__getitem__, visual)),
        )

    @property
    def unfolded_slots(self) -> tuple[Condition, ...]:
        return tuple(
            (
                *self.slots,
                Condition.UNKNOWN,
                *self.slots,
                Condition.UNKNOWN,
                *self.slots,
                Condition.UNKNOWN,
                *self.slots,
                Condition.UNKNOWN,
                *self.slots,
            )
        )


def iter_spring(path_to_input: str) -> collections.abc.Iterator[Spring]:
    with open(file=path_to_input) as fp:
        yield from map(Spring.from_line, fp)


@aoc2023.expects(7653)
def part_one(path_to_input: str) -> int:
    return sum(
        count_arrangements(groups=spring.groups, slots=spring.slots)
        for spring in iter_spring(path_to_input=path_to_input)
    )


@aoc2023.expects(60681419004564)
def part_two(path_to_input: str) -> int:
    return sum(
        count_arrangements(groups=spring.groups * 5, slots=spring.unfolded_slots)
        for spring in iter_spring(path_to_input=path_to_input)
    )
