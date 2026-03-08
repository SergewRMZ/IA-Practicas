from typing import Iterable, Tuple

State = Tuple[int, int]

def jug_neighbors(a_cap: int, b_cap: int, state: State) -> Iterable[State]:
    a, b = state

    # llenar jarra A
    yield (a_cap, b)

    # llenar jarra B
    yield (a, b_cap)

    # vaciar jarra A
    yield (0, b)

    # vaciar jarra B
    yield (a, 0)

    # verter A -> B
    pour = min(a, b_cap - b)
    yield (a - pour, b + pour)

    # verter B -> A
    pour = min(b, a_cap - a)
    yield (a + pour, b - pour)


def goal_state(target: int, state: State) -> bool:
    a, b = state
    return a == target or b == target