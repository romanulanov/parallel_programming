"""Задача 1 (ПОТОКИ) - Скачивание файлов с прогрессом
Создайте программу, которая скачивает 5 разных изображений с заданных URL.
Каждое скачивание должно выполняться в отдельном потоке.
Во время скачивания каждый поток должен выводить сообщение о начале и
завершении загрузки. Основной поток должен ждать завершения всех загрузок и
вывести итоговое сообщение.

Требования:

Использовать библиотеку requests или urllib

Каждый поток загружает свой URL

Вывод в консоль: "Начало загрузки {url}" и "Завершено: {url}"

После всех загрузок: "Все файлы загружены!"

Цель: Понять базовый запуск потоков и join().

"""

import os
import requests
import threading

urls = [
    "https://images.unsplash.com/photo-1575936123452-b67c3203c357?fm=jpg&q=60&\
    w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mn\
    x8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
    "https://static.vecteezy.com/vite/assets/photo-masthead-375-BoK_p8LG.webp",
    "https://media.istockphoto.com/id/1550071750/photo/green-tea-tree-leaves-c\
        amellia-sinensis-in-organic-farm-sunlight-fresh-young-tender-bud.jpg?s=\
        612x612&w=0&k=20&c=RC_xD5DY5qPH_hpqeOY1g1pM6bJgGJSssWYjVIvvoLw=",
    "https://img.freepik.com/free-photo/closeup-scarlet-macaw-from-side-view-\
        scarlet-macaw-closeup-head_488145-3540.jpg?semt=ais_hybrid&w=740&q=80",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFYqoKTu_o3Zns2yEx\
        bst2Co84Gpc2Q1RJbA&s",
    ]


def write_image_to_file(url: str, filename: str):
    print(f"Начало загрузки {url}")
    img = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(img)
    print(f"Завершено: {url}")


def main():
    threads = []
    if not os.path.exists("images"):
        os.makedirs("images")
    for index, url in enumerate(urls):
        thread = threading.Thread(
            target=write_image_to_file,
            args=(url, f"images/image_{index+1}.jpg"),
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Все файлы загружены")


if __name__ == '__main__':
    main()
