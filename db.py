import os
from typing import Dict, List, Tuple

import sqlite3

from datetime import datetime

conn = sqlite3.connect(os.path.join( "database.db"))
cursor = conn.cursor()

def _init_db():
    with open("create_db.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()

def insert_sumbols(values):
    table=cursor.execute("SELECT MAX(id) FROM exchange").fetchone()[0]
    for val in values:
        table_val=[table]
        table_val.append(val)
        table_val.append(values[val]) 
        cursor.executemany(
            f"INSERT INTO sumbols"
            f"(exchange, name, price)  "
            f"VALUES (?,?,?)",
            (table_val,))
    conn.commit()

def insert_exchange(open_time):
    cursor.execute( f"INSERT INTO exchange(open_time) VALUES (?)",(float(open_time),) )
    conn.commit()
    

def inset_values(time,values):
    insert_exchange(time)
    insert_sumbols(values)

def fetch_time():
    time=cursor.execute("SELECT open_time FROM exchange ORDER BY id DESC LIMIT 1").fetchone()[0]
    return time

def fetch_val():
    table=cursor.execute("SELECT MAX(id) FROM exchange").fetchone()[0]
    data=cursor.execute("SELECT name, price FROM sumbols WHERE exchange=={}".format(table))
    return data.fetchall()

def check_db_exists():
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='exchange'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


