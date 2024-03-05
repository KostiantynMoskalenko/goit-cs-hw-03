import psycopg2

# Задаємо параметри для підключення до бази даних
database_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}


# Функція для підключеня до бази даних і створення таблиць
def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn = psycopg2.connect(**database_config)
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    # Задаємо параметри для створення таблиць

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
     id SERIAL PRIMARY KEY,
     fullname VARCHAR(100) NOT NULL,
     email VARCHAR(100) UNIQUE
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
     id SERIAL PRIMARY KEY,
     name VARCHAR(50) UNIQUE
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
     id SERIAL PRIMARY KEY,
     title VARCHAR(100) NOT NULL,
     description TEXT,
     status_id INTEGER,
     user_id INTEGER,
     FOREIGN KEY (status_id) REFERENCES status (id),
     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """
    # Створюємо таблицю users
    create_table(sql_create_users_table)
    # Створюємо таблицю status
    create_table(sql_create_status_table)
    # Створюємо таблицю tasks
    create_table(sql_create_tasks_table)
