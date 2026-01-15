import dataclasses
import itertools
import typing

import aoc2023


@dataclasses.dataclass
class SparseMap:
    counts: list[int]
    domains: list[int]
    ranges: list[int]

    @classmethod
    def from_block(cls, block: str) -> typing.Self:
        range_domain_counts = []
        for line in block.splitlines()[1:]:
            range_domain_counts.append(map(int, line.split()))
        ranges, domains, counts = map(list, zip(*range_domain_counts))
        return cls(counts=counts, domains=domains, ranges=ranges)

    def __contains__(self, other: int) -> bool:
        return any(
            domain <= other < domain + count
            for domain, count in zip(self.domains, self.counts)
        )

    def __getitem__(self, other: int) -> int:
        return next(
            range + (other - domain)
            for domain, count, range in zip(self.domains, self.counts, self.ranges)
            if domain <= other < domain + count
        )


@dataclasses.dataclass
class Puzzle:
    seeds: list[int]
    maps: list[SparseMap]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as f:
            seeds, *blocks = f.read().split("\n\n")
        return cls(
            seeds=list(map(int, seeds.split(" ")[1:])),
            maps=list(map(SparseMap.from_block, blocks)),
        )

    @property
    def lowest_seed_location(self) -> int:
        def get_location_for_seed(idx: int) -> int:
            for mapper in self.maps:
                if idx in mapper:
                    idx = mapper[idx]
            return idx

        return min(map(get_location_for_seed, self.seeds))

    @property
    def lowest_seed_range_location(self) -> int:
        def get_location_for_seed(idx: int) -> int:
            for mapper in self.maps:
                if idx in mapper:
                    idx = mapper[idx]
            return idx

        iter_seeds = (
            seed
            for start, count in itertools.batched(self.seeds, n=2)
            for seed in range(start, start + count)
        )
        return min(map(get_location_for_seed, iter_seeds))


@aoc2023.expects(196167384)
def part_one(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return puzzle.lowest_seed_location


@aoc2023.skip_slow
@aoc2023.expects(125742456)
def part_two(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return puzzle.lowest_seed_range_location
