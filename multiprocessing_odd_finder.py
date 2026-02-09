import threading
import time

from multiprocessing import Pool

def odd(num):
    for i in range(2, num):
        if num % i == 0:
            return False
    else:
        return True


def find_odds(range_limits):
    start, end = range_limits
    count = 0
    start_time = time.time()
    for num in range(start, end):
        if odd(num):
            count += 1
    elapsed = int((time.time() - start_time))
    return f"Найдено {count} простых чисел за {elapsed} секунд"


ranges = [
        (1, 250_000),
        (250_001, 500_000),
        (500_001, 750_000),
        (750_001, 1_000_000),
    ]
with Pool(4) as p:
    results = p.starmap(find_odds, ranges)
for result in results:
    print(result)

print(f"В одном потоке: \n{find_odds((1, 1_000_000))}")
