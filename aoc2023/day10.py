import collections
import collections.abc
import dataclasses
import itertools
import typing

import aoc2023


CHAR_TO_DI_DJ = {
    "|": ((-1, 0), (+1, 0)),
    "-": ((0, -1), (0, +1)),
    "L": ((-1, 0), (0, +1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((0, -1), (+1, 0)),
    "F": ((+1, 0), (0, +1)),
    "S": (),
}


@dataclasses.dataclass(frozen=True, order=True)
class IJ:
    idx: int
    jdx: int

    def iter_neighbor_for_char(self, char: str) -> collections.abc.Iterator[IJ]:
        for di, dj in CHAR_TO_DI_DJ[char]:
            yield IJ(idx=self.idx + di, jdx=self.jdx + dj)

    def __repr__(self) -> str:
        return f"{self.idx:d}/{self.jdx:d}"

    def tangent(self, other: IJ) -> IJ:
        # 0 1 -> -1 0
        #
        return IJ(
            # 90 degree rotation
            # idx=other.jdx - self.jdx,
            # jdx=self.idx - other.idx,
            idx=self.jdx - other.jdx,
            jdx=other.idx - self.idx,
        )

    def __add__(self, other: IJ) -> IJ:
        return IJ(idx=self.idx + other.idx, jdx=self.jdx + other.jdx)


@dataclasses.dataclass
class Graph:
    edges: dict[IJ, set[IJ]]
    shape: tuple[int, int]
    start: IJ

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        candidates = collections.defaultdict(list)
        start: IJ | None = None
        with open(file=path_to_input) as fp:
            for idx, line in enumerate(fp):
                for jdx, char in enumerate(line.strip()):
                    if char in CHAR_TO_DI_DJ:
                        ij = IJ(idx=idx, jdx=jdx)
                        if char == "S":
                            start = ij
                        for neighbor in ij.iter_neighbor_for_char(char=char):
                            candidates[ij].append(neighbor)
        assert start is not None
        candidates[start].extend(
            xy for xy, neighbors in candidates.items() if start in neighbors
        )

        edges = {}
        queue = collections.deque((start,))
        while queue:
            ij = queue.popleft()
            if ij in edges:
                continue
            else:
                edges[ij] = set(candidates[ij])
                queue.extend(edges[ij])
        return cls(edges=edges, shape=(idx, jdx), start=start)

    @property
    def furthest_steps(self) -> int:
        return len(self.edges) // 2

    @property
    def iter_node_inclusive(self) -> collections.abc.Iterator[IJ]:
        previous = self.start
        current = next(iter(sorted(self.edges[previous])))
        yield previous
        while current != self.start:
            yield current
            candidates = self.edges[current]
            previous, (current,) = current, candidates - {previous}
        yield current

    @property
    def enclosed_squares(self) -> int:
        # Shoelace formula
        area = abs(
            sum(
                previous.idx * current.jdx - previous.jdx * current.idx
                for previous, current in itertools.pairwise(self.iter_node_inclusive)
            )
        )
        # Pick's theorem
        return (area - len(self.edges)) // 2 + 1


@aoc2023.expects(6860)
def part_one(path_to_input: str) -> int:
    return Graph.from_path_to_input(path_to_input=path_to_input).furthest_steps


@aoc2023.expects(343)
def part_two(path_to_input: str) -> int:
    return Graph.from_path_to_input(path_to_input=path_to_input).enclosed_squares
