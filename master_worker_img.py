"""Система обработки изображений c master-worker архитектурой

Реализуйте систему, где:
1. Master-процесс сканирует директорию c изображениями (jpg/png)
2. Для каждого изображения создает "задачу" (путь к файлу и операцию: resize,
grayscale, rotate)
3. Задачи распределяются между N worker-процессами (по количеству ядер CPU)
4. Каждый worker:
- Берет задачу из общей очереди
- Обрабатывает изображение (библиотека Pillow)
- Сохраняет результат в выходную директорию
- Отправляет статистику (размер файла, время обработки) в master
5. Master собирает статистику и по завершении выводит отчет

**Требования:**
- Использовать`multiprocessing.Queue`для очереди задач
- Использовать`multiprocessing.Manager`для общей статистики
- Обработка минимум 3 разных операций над изображениями
- Graceful завершение при получении сигнала Ctrl+C
- Ограничение на использование памяти (не более 2GB на процесс)
- Вывод отчета: обработано файлов, общее время, среднее время на файл

**Цель:**Понять межпроцессное взаимодействие, управление пулом процессов,
обработку shared state.
"""

from multiprocessing import Queue, Manager, Process
from os import listdir, makedirs
from os.path import basename, isfile, join, exists
from PIL import Image
from typing import Callable

q1: Queue = Queue()


def apply_pipeline(file_path: str, functions: list[Callable]) -> None:
    for func in functions:
        func(file_path)


def master_process(path: str) -> None:
    file_paths = [
        full_path for file in listdir(path) if isfile(
            full_path := join(path, file)
        )
    ]
    operations = [resize_image, grayscale_image, rotate_image]
    worker_processes = [Process(target=apply_pipeline, args=(file_path, operations)) for file_path in file_paths]


def resize_image(file_name: str) -> None:
    size = (500, 500)
    image = Image.open(file_name).resize(size, resample=Image.BILINEAR)
    if not exists('output'):
        makedirs('output')
    file_name = basename(file_name)
    image.save(f'output/resized_{file_name}')


def grayscale_image(file_name: str) -> None:
    image = Image.open(file_name).convert('L')
    if not exists('output'):
        makedirs('output')
    file_name = basename(file_name)
    image.save(f'output/grayscaled_{file_name}')


def rotate_image(file_name: str) -> None:
    if not exists('output'):
        makedirs('output')
    image = Image.open(file_name).rotate(45)
    file_name = basename(file_name)
    image.save(f'output/rotate_{file_name}')
