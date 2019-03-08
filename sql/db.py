import records
import os


def abosulte_path(filename, db_type='sqlite:///')
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = db_type + os.path.join(basedir, filename)

import sqlite3

#
# load sql scripts from the command line
# sqlite3 data.db --init tables.sql
#
def sqlite3_example():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cur = cursor.execute('select * from employees')
    print(cur.fetchall())

import psycopg2

# https://www.datacamp.com/community/tutorials/tutorial-postgresql-python
def postgres_example():
    conn = psycopg2.connect("dbname=dvdrental user=bcutrell")
    cur = conn.cursor()
    cur.execute("SELECT * FROM actor")
    print(cur.fetchall())

    # bulk insert
    # args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
    # cur.execute("INSERT INTO table VALUES " + args_str)

    # from psycopg2.extras import execute_values
    # execute_values(cur, "INSERT INTO test (id, v1, v2) VALUES %s", [(1, 2, 3), (4, 5, 6), (7, 8, 9)])

    cur.commit()
    cur.close()
    conn.close()

