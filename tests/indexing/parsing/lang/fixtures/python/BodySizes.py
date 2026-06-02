from functools import cache


def stub(): ...


def empty_body():
    pass


@cache
def fibonacci(n):
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current
