import sqlite3
import json
import os

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


def display_all_vm_status():
    vm_statuses = get_all_vm_status()
    if not vm_statuses:
        print("No VM status data available")
        return

    print("VM statuses:")
    for id, vm_name, status_data, timestamp in vm_statuses:
        print(f"\nID: {id}, VM Name: {vm_name}, Timestamp: {timestamp}")
        print("Status Data:")
        pretty_status = json.dumps(json.loads(status_data), indent=4, sort_keys=True)
        print(pretty_status)


def get_latest_vm_status():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, vm_name, status_data, timestamp
            FROM vm_status
            WHERE id IN (
                SELECT MAX(id)
                FROM vm_status
                GROUP BY vm_name
            )
            ORDER BY timestamp DESC
        """)
        return cursor.fetchall()


def display_latest_vm_status():
    vm_statuses = get_latest_vm_status()
    if not vm_statuses:
        print("No latest VM status data available.")
        return

    print("Latest VM Statuses:")
    for id, vm_name, status_data, timestamp in vm_statuses:
        print(f"\nID: {id}, VM Name: {vm_name}, Timestamp: {timestamp}")
        print("Status Data:")
        pretty_status = json.dumps(json.loads(status_data), indent=4, sort_keys=True)
        print(pretty_status)


