import dataclasses
import itertools
import math
import re
import typing

import aoc2023


@dataclasses.dataclass
class Puzzle:
    directions: list[int]
    edges: dict[str, tuple[str, str]]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as fp:
            directions_line = fp.readline().strip()
            fp.readline()
            edge_lines = map(str.strip, fp.readlines())
        ALPHANUM = "([0-9A-Z]{3})"
        regex = re.compile(f"{ALPHANUM:s} = \\({ALPHANUM:s}, {ALPHANUM:s}\\)")
        return cls(
            directions=[0 if direction == "L" else 1 for direction in directions_line],
            edges={
                match.group(1): (match.group(2), match.group(3))
                for edge_line in edge_lines
                if (match := regex.search(string=edge_line)) is not None
            },
        )

    def get_cycle_length(self, node: str, ends: set[str]) -> int:
        count = 0
        for direction in itertools.cycle(self.directions):
            node = self.edges[node][direction]
            count += 1
            if node in ends:
                return count
        else:
            raise ValueError(node)

    @property
    def multi_cycle_length(self) -> int:
        ends = {node for node in self.edges if node.endswith("Z")}
        return math.lcm(
            *(
                self.get_cycle_length(node=node, ends=ends)
                for node in self.edges
                if node.endswith("A")
            )
        )


@aoc2023.expects(16697)
def part_one(path_to_input: str) -> int:
    return Puzzle.from_path_to_input(path_to_input=path_to_input).get_cycle_length(
        node="AAA",
        ends={"ZZZ"},
    )


@aoc2023.expects(10668805667831)
def part_two(path_to_input: str) -> int:
    return Puzzle.from_path_to_input(path_to_input=path_to_input).multi_cycle_length
