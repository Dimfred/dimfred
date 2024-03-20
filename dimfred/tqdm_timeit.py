"""TQDM timeit wrapper by Eusmilis <3"""
import gc
import itertools
import time
import timeit
from typing import Any, Callable

from tqdm import tqdm


class ProgressTimer(timeit.Timer):
    def __init__(
        self,
        stmt: str | Callable[[], object] = "pass",
        setup: str | Callable[[], object] = "pass",
        timer: Callable[[], float] = time.perf_counter,
        globals: dict[str, Any] | None = None,
        *,
        description: str | None = None,
    ) -> None:
        super().__init__(stmt, setup, timer, globals)
        self.description = description

    def timeit(self, number: int = 1000000) -> float:
        # wrap the iterator in tqdm
        it = tqdm(itertools.repeat(None, number), total=number, desc=self.description)
        gcold = gc.isenabled()
        gc.disable()
        try:
            timing = self.inner(it, self.timer)
        finally:
            if gcold:
                gc.enable()
        # the tqdm bar sometimes doesn't flush on short timers, so print an empty line
        print()
        return timing
