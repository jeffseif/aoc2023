import collections
import collections.abc
import dataclasses
import enum
import math

import aoc2023


LABEL_TO_RANK = {v: k for k, v in enumerate("23456789TJQKA")}
LABEL_TO_RANK_WITH_JOKERS = {v: k for k, v in enumerate("J23456789TQKA")}


class HandType(enum.Enum):
    HIGH = enum.auto()
    ONE = enum.auto()
    TWO = enum.auto()
    THREE = enum.auto()
    HOUSE = enum.auto()
    FOUR = enum.auto()
    FIVE = enum.auto()

    @classmethod
    def from_hand(cls, hand: str) -> HandType:
        assert len(hand) == 5
        if len(counts := collections.Counter(hand)) == 1:
            return cls.FIVE
        elif (matches := max(counts.values())) == 4:
            return cls.FOUR
        elif matches == 3 and len(counts) == 2:
            return cls.HOUSE
        elif matches == 3:
            return cls.THREE
        elif matches == 2 and len(counts) == 3:
            return cls.TWO
        elif matches == 2:
            return cls.ONE
        else:
            return cls.HIGH

    def __lt__(self, other: HandType) -> bool:
        return self.value < other.value


@dataclasses.dataclass
class Hand:
    hand: str
    with_jokers: bool

    @property
    def iter_joker_variants(self) -> collections.abc.Iterator[Hand]:
        if not self.with_jokers:
            yield self
        elif (jokers := self.hand.count("J")) == 0:
            yield self
        elif jokers == 5:
            yield dataclasses.replace(self, hand="AAAAA")
        else:
            for label in set(self.hand).difference("J"):
                yield dataclasses.replace(self, hand=self.hand.replace("J", label))

    @property
    def hand_type(self) -> HandType:
        if not self.with_jokers:
            return HandType.from_hand(hand=self.hand)
        elif (jokers := self.hand.count("J")) == 0:
            return HandType.from_hand(hand=self.hand)
        elif jokers == 5:
            return HandType.FIVE
        else:
            return max(
                HandType.from_hand(hand=self.hand.replace("J", label))
                for label in set(self.hand).difference("J")
            )

    @property
    def rank(self) -> tuple[int, ...]:
        label_to_rank = LABEL_TO_RANK_WITH_JOKERS if self.with_jokers else LABEL_TO_RANK
        return tuple(map(label_to_rank.__getitem__, self.hand))

    def __lt__(self, other: Hand) -> bool:
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self.rank < other.rank


def iter_hand_bid(
    path_to_input: str, with_jokers: bool
) -> collections.abc.Iterator[tuple[Hand, int]]:
    with open(file=path_to_input) as f:
        for line in map(str.strip, f):
            hand, bid = line.split()
            yield Hand(hand=hand, with_jokers=with_jokers), int(bid)


@aoc2023.expects(248179786)
def part_one(path_to_input: str) -> int:
    hand_bids = sorted(iter_hand_bid(path_to_input=path_to_input, with_jokers=False))
    rank_bids = enumerate((bid for _, bid in hand_bids), start=1)
    return int(math.sumprod(*zip(*rank_bids)))


@aoc2023.expects(247885995)
def part_two(path_to_input: str) -> int:
    hand_bids = sorted(iter_hand_bid(path_to_input=path_to_input, with_jokers=True))
    rank_bids = enumerate((bid for _, bid in hand_bids), start=1)
    return int(math.sumprod(*zip(*rank_bids)))
