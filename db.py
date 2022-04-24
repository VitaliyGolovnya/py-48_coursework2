import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        con = psycopg2.connect(user='postgres',
                               password='admin',
                               host='localhost',
                               port='5432')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        sql_create_database = 'CREATE DATABASE vkinder_db;'
        cursor.execute(sql_create_database)
    except (Exception, psycopg2.Error) as error:
        print('Ошибка при работе с PostgreSQL', error)



def create_table():
    try:
        con = psycopg2.connect(user='postgres',
                               password='admin',
                               host='localhost',
                               port='5432',
                               database='vkinder_db'
                               )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        sql_create_table = '''CREATE TABLE IF NOT EXISTS matches (
                            id SERIAL, 
                            name CHAR(255) NOT NULL,
                            match CHAR(255) NOT NULL,
                            PRIMARY KEY (name, match)
                            );'''
        cursor.execute(sql_create_table)

    except (Exception, psycopg2.Error) as error:
        print('Ошибка при работе с PostgreSQL', error)


def insert_db(user, match):
    try:
        con = psycopg2.connect(user='postgres',
                               password='admin',
                               host='localhost',
                               port='5432',
                               database='vkinder_db')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        insert_query = '''INSERT INTO matches (name, match)
            VALUES (%s, %s)'''
        insert_tuple = (user, match)
        cursor.execute(insert_query, insert_tuple)
    except (Exception, psycopg2.Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
        return 'db_error'


def select_db(user, match):
    try:
        con = psycopg2.connect(user='postgres',
                               password='admin',
                               host='localhost',
                               port='5432',
                               database='vkinder_db')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        select_query = '''SELECT name, match FROM matches
            WHERE name = %s AND match = %s'''
        select_tuple = (user, match)
        cursor.execute(select_query, select_tuple)
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False
    except (Exception, psycopg2.Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
        return 'db_error'
