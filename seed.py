import faker
import random
import psycopg2

# Задаємо параметри для заповнення таблиць
NUMBER_USERS = 20
NUMBER_TASKS = 30


database_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}


def generate_fake_data(number_users, number_tasks):
    # Задаємо статуси задач вручну
    fake_status = [('new',), ('in progress',), ('completed',)]
    # Також задаємо змінні для збережння інших даних
    fake_users = []  # Тут зберігатимемо користувачів
    fake_tasks = []  # Тут зберігатимемо завдання
    # І заповнюємо таблиці даними
    fake = faker.Faker()

# Створюємо набір користувачів у кількості NUMBER_USERS
    for _ in range(number_users):
        fake_users.append((fake.name(), fake.unique.email()))

# А також набір тасок у кількості NUMBER_TASKS
    for _ in range(number_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        status_id = random.randint(1, 3)
        user_id = random.randint(1, 20)
        fake_tasks.append((title, description, status_id, user_id))

    return fake_users, fake_status, fake_tasks


def prepare_data(users, status, tasks):

    # Готуємо дані у списках кортежів
    for_users = []
    for user in users:
        for_users.append(user, )

    for_status = []
    for stage in status:
        for_status.append(stage, )

    for_tasks = []
    for task in tasks:
        for_tasks.append(task, )

    return for_users, for_status, for_tasks


def insert_data_to_db(users, status, tasks) -> None:
    # Створюємо з'єднання з нашою БД та отримаємо об'єкт курсора для
    # маніпуляцій з даними
    con = None
    try:
        con = psycopg2.connect(**database_config)
        cur = con.cursor()
        # Вводимо підготовані дані до таблиць users, status та tasks
        cur.executemany('INSERT INTO users(fullname, email) VALUES (%s, %s)',
                        users)
        cur.executemany('INSERT INTO status(name) VALUES (%s)', status)
        cur.executemany('INSERT INTO tasks(title, description, status_id, user_id) VALUES (%s, %s, %s, %s)', tasks) # noqa

        # Фіксуємо наші зміни в БД
        con.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con is not None:
            con.close()


if __name__ == '__main__':
    users, status, tasks = prepare_data(*generate_fake_data(NUMBER_USERS,
                                                            NUMBER_TASKS))
    insert_data_to_db(users, status, tasks)
