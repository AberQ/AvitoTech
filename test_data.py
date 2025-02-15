import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  
django.setup()


from api.models import Merch


items = [
    ("t-shirt", 80),
    ("cup", 20),
    ("book", 50),
    ("pen", 10),
    ("powerbank", 200),
    ("hoody", 300),
    ("umbrella", 200),
    ("socks", 10),
    ("wallet", 50),
    ("pink-hoody", 500),
]


for name, price in items:
    Merch.objects.create(name=name, price=price)

print("Объекты созданы успешно!")
