'''
#### **Задача 2 (сложная) - WebSocket чат-сервер c комнатами**

Реализуйте асинхронный WebSocket сервер, который:

1. Поддерживает несколько "комнат" (чатов)
2. Каждый клиент при подключении указывает имя и комнату
3. Сервер рассылает сообщения от клиента всем другим клиентам в той же комнате
4. При входе/выходе клиента отправляет уведомление в комнату
5. Хранит историю последних 100 сообщений в каждой комнате
6. Имеет команду `/users` для получения списка пользователей в комнате

**Требования:**

- Использовать `websockets` библиотеку
- Разные комнаты изолированы
- Обработка отключений клиентов (cleanup)
- Graceful shutdown сервера
- Поддержка 3+ одновременных подключений
- Логирование событий подключения/отключения/сообщений

**Цель:** Понять долгоживущие асинхронные соединения, управление состоянием в
asyncio, broadcast сообщений.

'''
from json import dumps
from websockets.sync.client import connect


ROOMS = [f"room{num}" for num in range(1, 6)]


def hello():
    user = {}
    name = input("Введите имя:")
    room = ""
    user["name"] = name
    while room not in ROOMS:
        room = input(
            f"Введите комнату {[f'room{num}' for num in range(1, 6)]}: "
        )
    user["room"] = room
    uri = f"ws://localhost:8765/{room}"
    with connect(uri) as websocket:
        websocket.send(dumps(user))
        print(f">>> На сервер заходит {name}.")
        greeting = websocket.recv()
        print(f"<<< {greeting}")


if __name__ == "__main__":
    hello()
