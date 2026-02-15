"""
Задача 2 (ПРОЦЕССЫ) - Параллельный поиск простых чисел
Напишите программу, которая ищет все простые числа в диапазоне от 1 до
1_000_000, используя 4 процесса. Каждый процесс должен проверять свой
диапазон чисел. Результаты от всех процессов собираются в основной
процесс и выводятся количество найденных простых чисел и время выполнения.

Требования:

Разделить диапазон на 4 примерно равные части

Каждый процесс возвращает список простых чисел своего диапазона

Использовать multiprocessing.Pool или Process

Вывести: "Найдено {N} простых чисел за {time} секунд"

Сравнить время с однопроцессной версией

Цель: Понять базовое создание процессов, передачу данных между процессами.
"""

import time

from multiprocessing import Process, Queue


def check_prime_num(num: int):
    for div in range(2, num):
        if num % div == 0:
            return False
    else:
        return True


def find_primes(ranges: tuple, q: Queue | None = None):
    start, end = ranges
    primes = []

    for num in range(start, end):
        if check_prime_num(num):
            primes.append(num)
    if q is not None:
        q.put(primes)
    else:
        return primes


ranges = [
        (1, 250_000),
        (250_001, 500_000),
        (500_001, 750_000),
        (750_001, 1_000_000),
    ]


def main():
    start_time = time.time()
    all_primes = []
    queue = Queue()
    processes = []

    for interval in ranges:
        process = Process(
            target=find_primes,
            args=(interval, queue),
        )
        processes.append(process)
        process.start()
    for process in processes:
        all_primes += queue.get()
    for process in processes:
        process.join()
    elapsed = int((time.time() - start_time))
    print(f"Найдено {len(all_primes)} простых чисел за {elapsed} секунд")
    start_time = time.time()
    single_count = len(find_primes((1, 1_000_000)))
    elapsed = int((time.time() - start_time))
    print(f"В одном потоке:\n{single_count} простых чисел за {elapsed} секунд")


if __name__ == '__main__':
    main()
