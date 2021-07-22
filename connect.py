
# from mysql.connector import MySQLConnection

import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """

    conn = mysql.connector.connect(host='localhost', database='photodrome', user='user', password='password')
    try:

        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        conn.close()
    return True


if __name__ == '__main__':
    connect()
