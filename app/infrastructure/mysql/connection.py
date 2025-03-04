import pymysql


def get_mysql_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        database='agrocontrol',
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection