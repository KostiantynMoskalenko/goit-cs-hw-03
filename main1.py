"""
Команди для виконання операцій з базою даних:
Считати всю базу даних:
py .\main.py --action read

Отримати відомості про кота за його іменем, де <Name> це ім'я існуючого кота,
дані про якого ми виводимо:
py .\main.py --action read_by_name --name <Name>

Створити нового кота, де <Name> це ім'я кота, <Age> його вік цифрами
і <Features> - його особливості вказані кожна в окремих лапках через кому:
py .\main.py --action create --name <Name> --age <Age> --features <Features>

Оновити дані про вже існуючого кота, де <ID> - це ідентифікатор кота, дані про
якого ми хочемо оновити, <Name> - його нове ім'я, <Age> - його новий вік і
<Features> - нові його особливості вказані кожна в окремих лапках через кому:
py .\main.py --action update --id <ID> --name <Name> --age <Age> --features <Features>

Додати особливості до вже існуючого кота, де <ID> - це ідентифікатор кота,
особливості якого ми хочемо додати, <Features> - нові його особливості вказані
кожна в окремих лапках через кому, яких в нього ще немає у базі даних:
py .\main.py --action update_features --id <ID> --features <Features>

Видалення даних про обраного кота з бази, де <ID> - це ідентифікатор кота,
якого ми хочему видалити:
py .\main.py --action delete --id <ID>
"""


import argparse

# from bson.objectid import ObjectId
#from pymongo import MongoClient
import pymongo
from pymongo.errors import PyMongoError, ConnectionFailure
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values('.env')
try:
    uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@cluster1.z0xs4cu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
except ConnectionFailure:
    print('Щось пішло не так. Не вдалося підключитися до бази даних.')

# Create a new client and connect to the server
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client.mds

# Робимо парсер для аргументів
parser = argparse.ArgumentParser(description="Application cats")
parser.add_argument("--action", help="create, read, update, delete")
parser.add_argument("--id", help="id")
parser.add_argument("--name", help="name")
parser.add_argument("--age", help="age")
parser.add_argument("--features", help="features", nargs="+")

# Перетворюємо отримані аргументи в словникові ключі
args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]


# Читання всієї бази котів
def read():
    return db.cats.find()


# Пошук і виведення даних про кота за ім'ям
def read_by_name(name):
    #name = input("Enter name: ")
    document = db.cats.find_one({"name": name})
    if document is not None:
        print(document)
    else:
        print("Not found")


# Створення нового кота
def create(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.insert_one(cat)


# Оновлюємо дані для існуючого кота, замінюючи частину або всі поля
def update(name, age, features):
    new_cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.update_one({"name": name}, {"$set": new_cat})


# Додаємо особливості до конкретного кота
def update_features(name, features):
    new_cat = {
        "features": {"$addToSet": features}
    }
    return db.cats.update_one({"name": name}, {"$push": new_cat})


# Видаляємо існуючого кота
def delete(pk):
    return db.cats.delete_one({"_id": ObjectId(pk)})


if __name__ == "__main__":
    match action:
        case "read":
            results = read()
            [print(cat) for cat in results]
        case "create":
            result = create(name, age, features)
            print(result)
        case "update":
            result = update(pk, name, age, features)
            print(result)
        case "update_features":
            result = update_features(name, features)
            print(result)
        case "delete":
            result = delete(pk)
            print(result)
        case "read_by_name":
            read_by_name(name)
        case _:
            print("Unknown action")
