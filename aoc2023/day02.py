import collections.abc
import dataclasses
import functools
import operator
import typing

import aoc2023


@dataclasses.dataclass
class Game:
    draws: list[dict[str, int]]
    id: int

    @classmethod
    def from_string(cls, s: str) -> typing.Self:
        game_id, _, draw_list = s.partition(": ")
        _, id_str = game_id.split()
        return cls(
            draws=[
                {
                    color: int(count)
                    for count_color_str in draw_str.split(", ")
                    for count, color in [count_color_str.split()]
                }
                for draw_str in draw_list.strip().split("; ")
            ],
            id=int(id_str),
        )

    def accommodates(self, counts: dict[str, int]) -> bool:
        for draw in self.draws:
            for color, count in draw.items():
                if color not in counts:
                    return False
                elif counts[color] < count:
                    return False
        else:
            return True

    @property
    def minimal(self) -> dict[str, int]:
        colors = {color for draw in self.draws for color in draw}
        return {
            color: max(draw.get(color, 0) for draw in self.draws) for color in colors
        }


def iter_game(path_to_input: str) -> collections.abc.Iterator[Game]:
    with open(file=path_to_input) as f:
        yield from map(Game.from_string, f)


@aoc2023.expects(2348)
def part_one(path_to_input: str) -> int:
    counts = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    return sum(
        game.id
        for game in iter_game(path_to_input=path_to_input)
        if game.accommodates(counts=counts)
    )


@aoc2023.expects(76008)
def part_two(path_to_input: str) -> int:
    return sum(
        functools.reduce(operator.mul, game.minimal.values())
        for game in iter_game(path_to_input=path_to_input)
    )
