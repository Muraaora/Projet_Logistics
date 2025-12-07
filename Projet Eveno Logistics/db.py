# db.py

import mysql.connector
from mysql.connector import MySQLConnection
from config import DB_CONFIG


def get_connection() -> MySQLConnection:
    """
    Retourne une connexion MySQL vers la base 'logistics'.
    """
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )
    return conn
