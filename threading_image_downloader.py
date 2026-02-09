import requests
import threading

def fetch_image(url, filename):
    print(f"Начало загрузки {url}")
    img = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(img)
    print(f"Завершено: {url}")


urls = [
    "https://images.unsplash.com/photo-1575936123452-b67c3203c357?fm=jpg&q=60&w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
    "https://static.vecteezy.com/vite/assets/photo-masthead-375-BoK_p8LG.webp",
    "https://media.istockphoto.com/id/1550071750/photo/green-tea-tree-leaves-camellia-sinensis-in-organic-farm-sunlight-fresh-young-tender-bud.jpg?s=612x612&w=0&k=20&c=RC_xD5DY5qPH_hpqeOY1g1pM6bJgGJSssWYjVIvvoLw=",
    "https://img.freepik.com/free-photo/closeup-scarlet-macaw-from-side-view-scarlet-macaw-closeup-head_488145-3540.jpg?semt=ais_hybrid&w=740&q=80",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFYqoKTu_o3Zns2yExbst2Co84Gpc2Q1RJbA&s",
    ]

threads = []

for index, url in enumerate(urls):
    t = threading.Thread(target=fetch_image, args=(url, f"image_{index+1}.jpg"))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Все файлы загружены")