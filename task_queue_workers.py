'''
#### **Задача 2 (сложная) - Thread-safe очередь задач с обработчиками**

Реализуйте систему обработки задач с пулом потоков, где:
1. Есть поток-генератор задач, который каждые 0.5 секунды создает новую
"задачу" (просто случайное число от 1 до 100).
2. Есть поток-логирующий результаты в файл.
3. Есть N worker-потоков (3-5), которые берут задачи из общей очереди и
"обрабатывают" (возводят число в квадрат, добавляют задержку
`random.uniform(0.1, 0.5)`).
4. Результаты обработки складываются в другую очередь, откуда их забирает
логгер.
**Требования:**- Использовать `queue.Queue` для обеих очередей
- Защитить доступ к очередям через механизмы threading
(Lock, RLock или сами Queue)
- Генератор должен работать 10 секунд, затем остановиться
- После завершения генератора, воркеры должны завершиться, когда обработают
все задачи
- Логгер должен записывать в файл: `{timestamp} | {number} -> {result}`
- Реализовать graceful shutdown всех потоков (корректное завершение работы)
**Цель:** Понять взаимодействие потоков через очереди,
thread-safe структуры, координацию потоков.'''

from queue import Queue
from random import randint, uniform
from time import time, sleep
from threading import Thread, Event
from typing import List

q1: Queue = Queue()
q2: Queue = Queue()
stop_event = Event()


def task_generator():
    start_time = time()
    while True:
        elapsed = int((time() - start_time))
        if elapsed >= 10 or stop_event.is_set():
            break
        q1.put(randint(1, 100))
        sleep(0.5)
    q1.put(None)
    stop_event.set()


def task_logger():
    with open("file.txt", "w", encoding="utf-8"):
        pass
    while True:
        task = q2.get()
        if not task or stop_event.is_set():
            stop_event.set()
            break
        with open("file.txt", "a", encoding="utf-8") as f:
            f.write(f"{str(task)}\n")


def task_worker():
    while True:
        task = q1.get()
        if not task or stop_event.is_set():
            q2.put(None)
            q1.task_done()
            stop_event.set()
            break
        q2.put(task**2)
        q1.task_done()
        sleep(uniform(0.1, 0.5))


def print_info():
    with open("file.txt", "r", encoding="utf-8") as file:
        print(file.read())


def main_tasks_run(threads: List[Thread]):
    for thread in threads:
        thread.start()


def main_tasks_stop(threads: List[Thread]):
    for thread in threads:
        thread.join()
    print_info()


def main():
    thread1 = Thread(target=task_generator)
    thread2 = Thread(target=task_logger)
    thread3 = Thread(target=task_worker)
    threads = [thread1, thread2, thread3]
    main_tasks_run(threads)
    main_tasks_stop(threads)


if __name__ == '__main__':
    main()
