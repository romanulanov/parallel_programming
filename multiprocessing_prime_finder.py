"""
Задача 2 (ПРОЦЕССЫ) - Параллельный поиск простых чисел
Напишите программу, которая ищет все простые числа в диапазоне от 1 до 1_000_000, используя 4 процесса. Каждый процесс должен проверять свой диапазон чисел. Результаты от всех процессов собираются в основной процесс и выводятся количество найденных простых чисел и время выполнения.

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


def find_primes(ranges: tuple, q: Queue):
    start, end = ranges
    count = 0
    start_time = time.time()
    for num in range(start, end):
        if check_prime_num(num):
            count += 1
    elapsed = int((time.time() - start_time))
    q.put(f"Найдено {count} простых чисел за {elapsed} секунд")


ranges = [
        (1, 250_000),
        (250_001, 500_000),
        (500_001, 750_000),
        (750_001, 1_000_000),
    ]


def main():
    queue = Queue()
    processes = []

    for index in range(len(ranges)):
        processes.append(Process(target=find_primes, args=(ranges[index], queue)))
    for process in processes:
        process.start()
    for process in processes:
        print(queue.get())
    for process in processes:
        process.join()

    print(f"В одном потоке: \n{find_primes((1, 1_000_000))}")


if __name__ == '__main__':
    main()
