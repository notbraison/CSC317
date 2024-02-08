from typing import TypeVar, Generic, List

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self.stack: List[T] = []

    def push(self, value: T) -> None:
        self.stack.append(value)

    def isEmpty(self) -> bool:
        return len(self.stack) == 0

    def size(self) -> int:
        return len(self.stack)

    def pop(self) -> T | None:
        if self.isEmpty():
            print("Empty stack when trying to pop")
        else:
            return self.stack.pop()
