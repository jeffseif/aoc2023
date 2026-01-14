import dataclasses
import typing

import aoc2023


@dataclasses.dataclass
class Card:
    idx: int
    numbers: set[int]
    winning: set[int]

    @classmethod
    def from_line(cls, line: str) -> typing.Self:
        card_id, _, winning_numbers = line.partition(": ")
        _, _, id_str = card_id.partition(" ")
        winning_str, _, number_str = winning_numbers.partition("|")
        return cls(
            idx=int(id_str),
            numbers=set(map(int, number_str.split())),
            winning=set(map(int, winning_str.split())),
        )

    @property
    def matches(self) -> int:
        return len(self.numbers.intersection(self.winning))

    @property
    def points(self) -> int:
        return 1 << (self.matches - 1) if self.matches > 0 else 0


@aoc2023.expects(17782)
def part_one(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        return sum(card.points for card in map(Card.from_line, f))


@aoc2023.expects(8477787)
def part_two(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        idx_to_card = {card.idx: card for card in map(Card.from_line, f)}
    idx_to_counts = {idx: 1 for idx in idx_to_card}
    for idx, card in idx_to_card.items():
        count = idx_to_counts[idx]
        for jdx in range(idx + 1, idx + 1 + card.matches):
            if jdx in idx_to_counts:
                idx_to_counts[jdx] += count * 1
    return sum(idx_to_counts.values())
