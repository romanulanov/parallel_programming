'''
#### **Задача 2 (сложная) - Thread-safe очередь задач с обработчиками**

Реализуйте систему обработки задач с пулом потоков, где:
1. Есть поток-генератор задач, который каждые 0.5 секунды создает новую "задачу" (просто случайное число от 1 до 100).    
2. Есть поток-логирующий результаты в файл.    
3. Есть N worker-потоков (3-5), которые берут задачи из общей очереди и "обрабатывают" (возводят число в квадрат, добавляют задержку `random.uniform(0.1, 0.5)`).    
4. Результаты обработки складываются в другую очередь, откуда их забирает логгер.    
**Требования:**- Использовать `queue.Queue` для обеих очередей    
- Защитить доступ к очередям через механизмы threading (Lock, RLock или сами Queue)    
- Генератор должен работать 10 секунд, затем остановиться    
- После завершения генератора, воркеры должны завершиться, когда обработают все задачи    
- Логгер должен записывать в файл: `{timestamp} | {number} -> {result}`    
- Реализовать graceful shutdown всех потоков (корректное завершение работы)    
**Цель:** Понять взаимодействие потоков через очереди, thread-safe структуры, координацию потоков.'''
from queue import Queue
from random import randint, uniform
from time import time, sleep
from threading import Event

q1 = Queue()
q2 = Queue()
stop_event = Event()

def task_generator(work_time:int = 10):
    start_time = time()
    while True:
        if elapsed >= 10 or stop_event.is_set():
            break
        q1.put(randint(1, 100))
        sleep(0.5)
        elapsed = int((time.time() - start_time))
    q1.put(None)
    q1.shutdown()
    #TODO остановка из-за статуса событий Event
    

def task_logger():
    while True:
        task = q2.get()
        if not task or stop_event.is_set():
            break
        with open("file.txt", "a", encoding="utf-8") as f:
            f.write(task)


def task_worker(worker_id: int):
    while True:
        task = q1.get()
        q1.task_done()
        if not task or stop_event.is_set():
            break
        q2.put(task**2)
        sleep(uniform(0.1, 0.5))


def print_info():
    #TODO прочитать файл и вывести статистику


def main_tasks_run():
    #TODO запустить task_generator, task_logger и task_worker


def main_tasks_stop():
    #TODO передаёт сигнал стоп task_generator и дождаться его заверщения (join)
    #TODO передаёт сигнал стоп task_worker и дождаться его заверщения (join)
    #TODO передаёт сигнал стоп task_logger и дождаться его заверщения (join)
    #TODO дождаться завершения задачи в очередях и дождаться его заверщения (join)
    #TODO вывести статистику (print_info)
