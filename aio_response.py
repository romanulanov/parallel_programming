"""
Задача 3 (АСИНХРОННОСТЬ) - Асинхронный ping серверов
Напишите программу, которая проверяет доступность списка веб-сайтов. Для
каждого URL программа должна асинхронно отправить HTTP-запрос и замерить время
ответа. Вывести результат в формате: "{url} - {status} - {time}ms".

Требования:

Использовать aiohttp или httpx

Список из 10 разных сайтов (например, google.com, github.com, yandex.ru)

Ограничить количество одновременных запросов до 3 с помощью семафора
(asyncio.Semaphore)

Все запросы должны выполняться конкурентно

Вывести время выполнения всей проверки

Цель: Понять базовые корутины, await, asyncio.gather, семафоры.
"""

from aiohttp import ClientSession
from asyncio import Semaphore, gather, run
import certifi
import ssl
import time


links = [
    "https://google.com",
    "https://github.com",
    "https://yandex.ru",
    "https://stackoverflow.com",
    "https://wikipedia.org",
    "https://python.org",
    "https://reddit.com",
    "https://openai.com",
    "https://habr.com",
    "https://vk.com"
]


async def check_site_status(url: str, session: ClientSession, sem: Semaphore):
    async with sem:
        start_time = time.time()
        try:
            async with session.head(
                url,
                ssl=ssl.create_default_context(cafile=certifi.where()),
            ) as response:
                response.raise_for_status()
                elapsed = int((time.time() - start_time) * 1000)
                print(f"{url} - {response.status} - {elapsed} ms")
        except Exception as e:
            print(f"{url} - ERROR - {e}")


async def main():
    sem = Semaphore(3)
    start_time = time.time()
    async with ClientSession() as session:
        tasks = [check_site_status(url, session, sem) for url in links]
        await gather(*tasks)
    elapsed = int((time.time() - start_time) * 1000)
    print(f"Справились за {elapsed} ms")


if __name__ == "__main__":
    run(main())
