# -*- coding: utf8 -*-
from mysql.connector import MySQLConnection
from mysql.connector import Error
from modules.python_mysql_dbconfig import read_db_config


class MysqlConnect:

    query = ""
    row = ""
    args = ""

    def query_with_fetchone(self):
        result = None
        if self.query != "":
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            try:
                cursor.execute(self.query)
                row = cursor.fetchone()

                while row is not None:
                    field_name = [field[0] for field in cursor.description]
                    result = dict(zip(field_name, row))
                    row = cursor.fetchone()

            except Error as e:
                print(e)

            finally:
                cursor.close()
                conn.close()

        return result

    def query_with_insert(self):

        result = None

        if self.query != "" and self.args != "":

            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            try:
                # print(self.args)
                cursor.execute(self.query, self.args)
                conn.commit()
                result = True

            except Error as e:
                print(e)

            finally:
                cursor.close()
                conn.close()

        return result

