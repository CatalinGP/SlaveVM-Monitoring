import sqlite3
import json


def create_db_table():
    with sqlite3.connect('vm_status.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vm_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vm_name TEXT NOT NULL,
                status_data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_vm_status(vm_name, status_data):
    with sqlite3.connect('vm_status.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vm_status (vm_name, status_data) VALUES (?, ?)",
                       (vm_name, json.dumps(status_data)))
        conn.commit()


def get_all_vm_status():
    with sqlite3.connect('vm_status.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vm_status ORDER BY timestamp DESC")
        return cursor.fetchall()


# Ensure the database table is created when this script is imported
create_db_table()
