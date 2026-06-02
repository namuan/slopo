from typing import Protocol


class ProgressReporter(Protocol):
    def __call__(self, message: str) -> None: ...
