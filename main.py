from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations
import threading
import time


@dataclass(frozen=True)
class State:
    count: Counter[float]
    path: str = field(default_factory=str)


cache = {}


def step(cards: State) -> bool:
    key = tuple(cards.count.elements())
    if key in cache:
        return cache[key]

    # {2: 2, 3: 1, 6: 1}
    # {3: 1, 4: 1, 6: 1} (2+2)
    # {0: 1, 3: 1, 6: 1} (2-2) ...
    # ...
    # {24: 1}

    if len(key) == 1:
        if key[0] == 24:
            print(cards.path)
            return True
        return False

    next_nodes: list[State] = []
    # pick all combinations x,y and y,x
    for ix, x in enumerate(cards.count.keys()):
        for iy, y in enumerate(cards.count.keys()):
            # we don't need to enumerate all of the options, skip half of the triangle
            if ix <= iy:
                next_nodes.extend(new_func(cards, x, y))

    cache[key] = any(map(step, next_nodes))
    return cache[key]


def new_func(orig_cards: State, x, y) -> list[State]:
    cards = orig_cards.count.copy()
    if not ((x != y and cards[x] >= 1 and cards[y] >= 1) or (x == y and cards[x] >= 2)):
        return []

    cards[x] -= 1
    cards[y] -= 1

    operations = [x + y, x - y, y - x, x * y]
    operations += [x / y] if y != 0 else []
    operations += [y / x] if x != 0 else []

    next_states: list[State] = []
    for new_v in operations:
        cards_copy = Counter(cards)
        cards_copy[new_v] += 1
        next_states.append(
            State(
                count=cards_copy,
                path=f"{orig_cards.path}[({x}, {y})->{new_v}]",
            )
        )

    return next_states


def monitor(stop_event: threading.Event):
    global cache
    while not stop_event.is_set():
        time.sleep(1)
        print(cache)


test_case_1 = State(count=Counter({2: 2, 3: 1, 6: 1}))
test_case_1a = State(count=Counter({3: 1, 2: 2, 6: 1}))
test_case_2 = State(count=Counter({10: 4}))

monitor_stop = threading.Event()
# threading.Thread(target=monitor, args=(monitor_stop,)).start()

try:
    assert step(test_case_1)
    # assert step(test_case_1a)
    # assert not step(test_case_2)
except KeyboardInterrupt:
    pass
finally:
    monitor_stop.set()
