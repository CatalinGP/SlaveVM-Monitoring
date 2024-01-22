import sqlite3
import json
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(base_dir, 'vm_status.db')


def create_db_table():
    with sqlite3.connect(db_file) as conn:
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
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vm_status (vm_name, status_data) VALUES (?, ?)",
                       (vm_name, json.dumps(status_data)))
        conn.commit()


def get_all_vm_status():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vm_status ORDER BY timestamp DESC")
        return cursor.fetchall()


