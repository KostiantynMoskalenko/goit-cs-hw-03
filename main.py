from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values('.env')
try:
    uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@cluster1.z0xs4cu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1" # noqa
except ConnectionFailure:
    print('Щось пішло не так. Не вдалося підключитися до бази даних.')

# Створюємо нового клієнта і підключаємось до сервера
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mds


# Виводимо всю базу котів (1)
def read():
    try:
        results = db.cats.find({})
        i = 0
        for result in results:
            print(result)
            i += 1
        if i == 0:
            print("В базі немає записів")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")


# Виводимо інформацію про кота за його ім'ям (2)
def read_cat():
    try:
        name = input("Введіть ім'я кота: ")
        result = None
        result = db.cats.find_one({"name": name})
        if result:
            print(result)
        else:
            print("Кіт за таким ім'ям не знайдений")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Створюємо нового кота (3)
def create():
    try:
        features = ()
        name = input("Введіть ім'я кота: ")
        result = None
        result = db.cats.find_one({"name": name})
        if result:
            print("Кіт за таким ім'ям вже є в базі")
            return
        age = int(input("Введіть вік кота цифрами: "))
        features_input = input("Введіть особливості кота через кому з крапкою ';' ")
        features = features_input.split("; ")
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        print(cat)
        db.cats.insert_one(cat)
        print(f"Кота {name} додано у базу даних")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Оновлюємо ім'я для існуючого кота (4)
def update_name():
    try:
        name = input("Введіть ім'я кота: ")
        new_name = input("Введіть нове ім'я кота: ")
        result = None
        result = db.cats.find_one({"name": new_name})
        if result:
            print("Кіт за таким ім'ям вже є в базі")
            return
        result = db.cats.update_one({"name": name},
                                    {"$set": {"name": new_name}})
        if result.modified_count > 0:
            print(f"Ім'я кота {name} змінено на {new_name}")
        else:
            print("Ім'я кота не змінено")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Змінюємо вік існуючого кота (5)
def update_age():
    try:
        name = input("Введіть ім'я кота: ")
        new_age = int(input("Введіть новмй вік кота цифрами: "))
        result = db.cats.update_one({"name": name},
                                    {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота {name} змінено на {new_age}")
        else:
            print("Вік кота не змінено")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Додаємо особливості до конкретного кота (6)
def add_features():
    try:
        name = input("Введіть ім'я кота: ")
        new_features = ()
        features_input = input("Введіть особливості кота через крапку з комою ';' ")
        new_features = features_input.split("; ")
        result = db.cats.update_one({"name": name},
                                    {"$push": {"features": {"$each": new_features}}})
        if result.modified_count > 0:
            print(f"Особливості кота {name} додано")
        else:
            print("Особливості кота не змінено")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Замінюємо особливості конкретного кота на нові (7)
def replace_feature():
    try:
        name = input("Введіть ім'я кота: ")
        features_input = input("Введіть нові особливості кота замість старих через крапку з комою ';' ")
        new_features = features_input.split("; ")
        result = db.cats.update_one({"name": name}, {"$set": {"features": new_features}})
        if result.modified_count > 0:
            print(f"Особливості кота {name} змінено на нові")
        else:
            print("Особливості кота не змінено")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Видаляємо існуючого кота за ім'ям (8)
def delete_cat():
    try:
        name = input("Введіть ім'я кота для видалення: ")
        result = db.cats.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота {name} видалено")
        else:
            print(f"Кота {name} не видалено")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")
    except ValueError as e:
        print(f"Помилка вводеня даних: {e}")


# Видаляємо всіх котів з бази (9)
def delete_all():
    try:
        result = db.cats.delete_many({})
        if result.modified_count > 0:
            print("Усіх котів видалено за бази")
        else:
            print("Не всіх котів видалено з бази")
    except PyMongoError as e:
        print(f"Помилка при роботі за базою даних: {e}")


def main():
    while True:
        try:
            print("Введіть цифру від 1 до 9 для виконання однієї з команд:")
            print("1 - вивести всі дані про котів з бази")
            print("2 - вивести інформацію про кота за його ім'ям")
            print("3 - ввести нового кота в базу")
            print("4 - замінити ім'я вже існуючого в базі кота на інше")
            print("5 - замінити вік вже існуючого в базі кота на інший")
            print("6 - додати особливості вже існуючого в базі кота")
            print("7 - замінити особливості вже існуючого в базі кота на інші")
            print("8 - видалити кота з бази за його ім'ям")
            print("9 - видалити всіх котів з бази даних")
            print("або 'exit' для виходу: ")
            command = input()
            if command.lower() == 'exit':
                print("Вихід із програми.")
                break
            match command:
                case "1":
                    read()
                case "2":
                    read_cat()
                case "3":
                    create()
                case "4":
                    update_name()
                case "5":
                    update_age()
                case "6":
                    add_features()
                case "7":
                    replace_feature()
                case "8":
                    delete_cat()
                case "9":
                    delete_all()
                case _:
                    print("Невідома команда. Введіть цифру від 1 до 9 або 'exit' виходу:")
        except Exception as e:
            print(e)


if __name__ == "__main__":

    main()
