from collections import Counter
from dataclasses import dataclass, field
import time
from loguru import logger

Path = str


@dataclass(frozen=True)
class State:
    count: Counter[float]
    path: Path = field(default_factory=str)


cache = {}


def solve_24(cards: list[int]) -> list[Path]:
    explored_nodes = 0
    cache_hits = 0

    def solve(node: State) -> list[Path]:
        nonlocal explored_nodes, cache_hits
        explored_nodes += 1
        key = tuple(node.count.elements())
        if key in cache:
            cache_hits += 1
            return cache[key]

        if len(key) == 1:
            if key[0] == 24:
                return [node.path]

            return []

        next_nodes: list[State] = []
        # pick all combinations x,y and y,x
        for ix, x in enumerate(node.count.keys()):
            for iy, y in enumerate(node.count.keys()):
                # we don't need to enumerate all of the options, skip half of the triangle
                if ix <= iy:
                    next_nodes.extend(_get_next_states(node, x, y))

        cache[key] = [path for next_node in next_nodes for path in solve(next_node)]
        return cache[key]

    start_time = time.time()
    paths = solve(State(count=Counter(cards)))
    logger.info(
        f"took {1000 * (time.time() - start_time):.2f}ms to search {explored_nodes} nodes."
    )
    logger.debug(
        f"{cache_hits / explored_nodes * 100:.1f}% = ({cache_hits}/{explored_nodes}) were cache hits!"
    )
    return paths


def _get_next_states(orig_cards: State, x, y) -> list[State]:
    cards = orig_cards.count.copy()
    if not ((x != y and cards[x] >= 1 and cards[y] >= 1) or (x == y and cards[x] >= 2)):
        return []

    cards[x] -= 1
    cards[y] -= 1

    operations = [
        (x + y, f"{x}+{y}"),
        (x - y, f"{x}-{y}"),
        (y - x, f"{y}-{x}"),
        (x * y, f"{x}*{y}"),
    ]
    operations += [(x / y, f"{x}/{y}")] if y != 0 else []
    operations += [(y / x, f"{y}/{x}")] if x != 0 else []

    next_states: list[State] = []
    for new_v, op_strp in operations:
        cards_copy = Counter(cards)
        cards_copy[new_v] += 1
        next_states.append(
            State(
                count=cards_copy,
                path=f"{orig_cards.path}[{op_strp}={new_v}] ",
            )
        )

    return next_states


test_case_1 = [2, 2, 3, 6]
test_case_1a = [3, 2, 2, 6]
test_case_2 = [10, 10, 10, 10]
test_case_3 = [6, 6, 6, 6]
test_case_4 = [1, 2, 2, 6]
test_case_5 = [1, 5, 7, 13]
test_case_6 = [2, 8, 8, 9]
test_case_7 = [1, 2, 5, 13]
test_case_8 = [4, 4, 11, 11]
test_case_9 = [1, 4, 5, 6]

if __name__ == "__main":
    assert solve_24(test_case_1)
    assert solve_24(test_case_1a)
    assert not solve_24(test_case_2)
    assert solve_24(test_case_3)
    assert solve_24(test_case_4)
    assert solve_24(test_case_5)
    assert solve_24(test_case_6)
    assert solve_24(test_case_7)
    assert not solve_24(test_case_8)
    assert solve_24(test_case_9)
