import collections
import collections.abc
import dataclasses


import aoc2023


def iter_string(path_to_input: str) -> collections.abc.Iterator[str]:
    with open(file=path_to_input) as fp:
        raw = fp.read().strip()
    yield from raw.split(",")


def hasher(s: str) -> int:
    ret = 0
    for char in s:
        ret += ord(char)
        ret *= 17
        ret %= 256
    return ret


@aoc2023.expects(502139)
def part_one(path_to_input: str) -> int:
    return sum(map(hasher, iter_string(path_to_input=path_to_input)))


@dataclasses.dataclass
class Lense:
    label: str
    focal: int


@aoc2023.expects(0)
def part_two(path_to_input: str) -> int:
    boxes: dict[int, list[Lense]] = collections.defaultdict(list)
    for s in iter_string(path_to_input=path_to_input):
        if s.endswith("-"):
            label = s[:-1]
            box = boxes[hasher(s=label)]
            for idx, lense in enumerate(box):
                if lense.label == label:
                    box.pop(idx)
                    break
        else:
            label, focal = s.split("=")
            box = boxes[hasher(s=label)]
            for idx, lense in enumerate(box):
                if lense.label == label:
                    lense.focal = int(focal)
                    break
            else:
                box.append(Lense(label=label, focal=int(focal)))
    return sum(
        (1 + idx) * sum(jdx * lense.focal for jdx, lense in enumerate(box, start=1))
        for idx, box in sorted(boxes.items())
    )
