import aiohttp
import asyncio
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

async def fetch_url(url, session, sem):
    start_time = time.time()
    try:
        async with sem, session.get(url) as response:
            elapsed = int((time.time() - start_time) * 1000)
            print(f"{url} - {response.status} - {elapsed} ms")
    except Exception as e:
        print(f"{url} - ERROR - {e}")


async def main():
    sem = asyncio.Semaphore(3)
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(url, session, sem) for url in links]
        await asyncio.gather(*tasks)
    elapsed = int((time.time() - start_time) * 1000)
    print(f"Справились за {elapsed} ms")

asyncio.run(main())
