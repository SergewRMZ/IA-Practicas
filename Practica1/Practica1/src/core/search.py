from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Generic, Hashable, Iterable, List, Optional, Set, Tuple, TypeVar

S = TypeVar("S", bound=Hashable)

@dataclass
class SearchResult(Generic[S]):
    found: bool
    path: List[S]
    expanded: int
    frontier_max: int
    visited_count: int

def reconstruct_path(parent: Dict[S, Optional[S]], goal: S) -> List[S]:
    path = []
    cur: Optional[S] = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def bfs(start: S, is_goal: Callable[[S], bool], neighbors: Callable[[S], Iterable[S]]) -> SearchResult[S]:
    q: Deque[S] = deque([start])
    visited: Set[S] = {start}
    parent: Dict[S, Optional[S]] = {start: None}
    expanded = 0
    frontier_max = 1

    exploration_order = []

    while q:
        frontier_max = max(frontier_max, len(q))
        state = q.popleft()
        expanded += 1

        exploration_order.append(state)

        if is_goal(state):
            result = SearchResult(True, reconstruct_path(parent, state), expanded, frontier_max, len(visited))
            result.exploration = exploration_order
            return result

        for nxt in neighbors(state):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = state
                q.append(nxt)

    result = SearchResult(False, [], expanded, frontier_max, len(visited))
    result.exploration = exploration_order
    return result

def dfs(start: S, is_goal: Callable[[S], bool], neighbors: Callable[[S], Iterable[S]], depth_limit: Optional[int] = None) -> SearchResult[S]:
    stack: List[Tuple[S, int]] = [(start, 0)]
    visited: Set[S] = {start}
    parent: Dict[S, Optional[S]] = {start: None}
    expanded = 0
    frontier_max = 1

    while stack:
        frontier_max = max(frontier_max, len(stack))
        state, depth = stack.pop()
        expanded += 1

        if is_goal(state):
            return SearchResult(True, reconstruct_path(parent, state), expanded, frontier_max, len(visited))

        if depth_limit is not None and depth >= depth_limit:
            continue

        for nxt in neighbors(state):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = state
                stack.append((nxt, depth + 1))

    return SearchResult(False, [], expanded, frontier_max, len(visited))