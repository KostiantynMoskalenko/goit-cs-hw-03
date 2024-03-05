import psycopg2


database_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

sql_commands = [
    # 1 Отримати всі завдання певного користувача. Використайте SELECT для
    # отримання завдань конкретного користувача за його user_id.
    """
    SELECT *
    FROM tasks
    WHERE user_id = 5;
    """,
    # 2 Вибрати завдання за певним статусом. Використайте підзапит для вибору
    # завдань з конкретним статусом, наприклад, 'new'.
    """
    SELECT *
    FROM tasks
    WHERE status_id = (SELECT id FROM status WHERE name = 'new');
    """,
    # 3 Оновити статус конкретного завдання. Змініть статус конкретного
    # завдання на 'in progress' або інший статус.
    """
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = 'in progress')
    WHERE id = 2;
    """,
    # 4 Отримати список користувачів, які не мають жодного завдання.
    # Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
    """
    SELECT *
    FROM users
    WHERE id NOT IN (SELECT user_id FROM tasks);
    """,
    # 5 Додати нове завдання для конкретного користувача. Використайте INSERT
    # для додавання нового завдання.
    """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES ('New task', 'New task added manually', (SELECT id FROM status WHERE name = 'new'), 3);
    """,
    # 6 Отримати всі завдання, які ще не завершено. Виберіть завдання, чий
    # статус не є 'завершено'.
    """
    SELECT *
    FROM tasks
    WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');
    """,
    # 7 Видалити конкретне завдання. Використайте DELETE для видалення
    # завдання за його id.
    """
    DELETE
    FROM tasks
    WHERE id = 5;
    """,
    # 8 Знайти користувачів з певною електронною поштою. Використайте SELECT
    # із умовою LIKE для фільтрації за електронною поштою.
    """
    SELECT *
    FROM users
    WHERE email LIKE '%.org';
    """,
    # 9 Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
    """
    UPDATE users
    SET fullname = 'Isaac Newton'
    WHERE id = 8;
    """,
    # 10 Отримати кількість завдань для кожного статусу. Використайте SELECT,
    # COUNT, GROUP BY для групування завдань за статусами.
    """
    SELECT status.name, COUNT(tasks.id)
    FROM status
    LEFT JOIN tasks ON status.id = tasks.status_id
    GROUP BY status.name;
    """,
    # 11 Отримати завдання, які призначені користувачам з певною доменною
    # частиною електронної пошти. Використайте SELECT з умовою LIKE в
    # поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия
    # електронна пошта містить певний домен (наприклад, '%@example.com').
    """
    SELECT tasks.*
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE users.email LIKE '%@example.com';
    """,
    # 12 Отримати список завдань, що не мають опису. Виберіть завдання, у яких
    # відсутній опис.
    """
    SELECT *
    FROM tasks
    WHERE description IS NULL
        OR description = '';
    """,
    # 13 Вибрати користувачів та їхні завдання, які є у статусі 'in progress'.
    # Використайте INNER JOIN для отримання списку користувачів та їхніх
    # завдань із певним статусом.
    """
    SELECT users.fullname, tasks.title
    FROM users
    INNER JOIN tasks ON users.id = tasks.user_id
    WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
    """,
    # 14 Отримати користувачів та кількість їхніх завдань. Використайте LEFT
    # JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
    """
    SELECT users.fullname, COUNT(tasks.id) AS task_count
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.fullname;
    """
]

try:
    with psycopg2.connect(**database_config) as conn:
        c = conn.cursor()
        i = 0
        for command in sql_commands:
            c.execute(command)
            i += 1
            print('Виконую запит номер ', i)
            try:
                for row in c:
                    print(row)
            except (Exception, psycopg2.DatabaseError):
                print('Додаємо/змінюємо/видаляємо дані')
        conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
