from typing import Iterable, Tuple

State = Tuple[int, ...]

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)


def is_goal(state: State) -> bool:
    return state == GOAL_STATE


def puzzle_neighbors(state: State) -> Iterable[State]:

    zero_index = state.index(0)

    row = zero_index // 3
    col = zero_index % 3

    def swap(i, j):
        new_state = list(state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return tuple(new_state)

    neighbors = []

    if row > 0:
        neighbors.append(swap(zero_index, zero_index - 3))

    if row < 2:
        neighbors.append(swap(zero_index, zero_index + 3))

    if col > 0:
        neighbors.append(swap(zero_index, zero_index - 1))

    if col < 2:
        neighbors.append(swap(zero_index, zero_index + 1))

    return neighbors