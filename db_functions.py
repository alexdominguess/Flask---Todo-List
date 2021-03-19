import sqlite3


def db_connection():
    conn = sqlite3.connect('data_base.db')  # Connect to db. If it does not exist it will create a new one
    return conn


def get_data(sql):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def update_data(sql):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return


if __name__ == '__main__':
    # tables - accounts - tarefas
    sql = "SELECT * FROM tarefas"
    data = get_data(sql)
    print(data)
