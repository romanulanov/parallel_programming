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
from random import randint
from time import time, sleep
from threading import Event

q = Queue()

def task_generator(work_time:int = 10):
    start_time = time()
    while True:
        q.put(randint(1, 100))
        sleep(0.5)
        elapsed = int((time.time() - start_time))
        if elapsed >= 10:
            break
    q.put(None)
    q.shutdown()
    #TODO остановка из-за статуса событий Event
    

def task_logger():
    while True:
        task = q.get()
        if not task:
            break
        with open("file.txt", "a", encoding="utf-8") as f:
            f.write(task)
    #TODO для остановки использовать статус событий Event 


def task_worker(worker_id: int):
    #TODO бесконечный цикл берёт задачи из очереди.queue.get
    #TODO завершение при получении None-задачи
    #TODO для остановки использовать статус событий Event 
    #TODO помечать завершённые задачи в очереди task_done


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
