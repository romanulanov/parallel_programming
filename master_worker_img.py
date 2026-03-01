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
import os
from multiprocessing import Queue, Manager
from PIL import Image

q1: Queue = Queue()


def resize_img(filename):
    size = (500, 500)
    img = Image.open(filename).resize(size, resample=Image.BILINEAR)
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = os.path.basename(filename)
    img.save(f'output/resized_{filename}')


def grayscale_img(filename):
    img = Image.open(filename).convert('L')
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = os.path.basename(filename)
    img.save(f'output/grayscaled_{filename}')


def rotate_img(filename):
    if not os.path.exists('output'):
        os.makedirs('output')
    img = Image.open(filename).rotate(45)
    filename = os.path.basename(filename)
    img.save(f'output/rotate_{filename}')
