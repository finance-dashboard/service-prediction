import time


def job(limit: int = 10) -> int:
    counter = 0

    for i in range(limit):
        counter += i
        time.sleep(1)

    return counter
