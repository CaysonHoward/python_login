import login as lg
import sqlite3 as sl

def test_db_creation():
    con = sl.connect('login.db')
    assert lg.db_initialization == con