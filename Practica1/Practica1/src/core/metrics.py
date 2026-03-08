import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

@dataclass
class Perf(Generic[T]):
    result: T
    seconds: float
    peak_kb: float

def measure(fn: Callable[[], T]) -> Perf[T]:
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn()
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return Perf(result=result, seconds=(t1 - t0), peak_kb=(peak / 1024.0))