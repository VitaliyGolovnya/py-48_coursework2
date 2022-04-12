import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        con = psycopg2.connect(user='postgres',
                               password='1234',
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
                               password='1234',
                               host='localhost',
                               port='5432',
                               database='vkinder_db'
                               )
        print(con.get_dsn_parameters())
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

create_table()