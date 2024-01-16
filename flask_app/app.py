from flask import Flask, jsonify, render_template
import sqlite3
from scripts.monitor import monitor_vm

app = Flask(__name__)

# def display_data():
#     db_path = 'vm_status.db'
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, vm_name, status_data FROM vm_status")
#     rows = cursor.fetchall()
#     conn.close()
#     data = [{"ID": row[0], "VM Name": row[1], "Status Data": row[2]} for row in rows]
#     return data

@app.route('/')
def home():
    return "Welcome to the VM Status Web App!"

# @app.route('/status')
# def vm_status():
#     data = display_data()
#     return jsonify(data)
#
# @app.route('/status-table')
# def vm_status_table():
#     data = display_data()
#     return render_template('vm_status_table.html', data=data)


if __name__ == '__main__':
    # with app.app_context():
    #     monitor_vm.run()
    app.run(debug=True)




# from flask import Flask, jsonify, render_template
# import json
# import os
# from scripts.monitor import monitor_vm
#
# app = Flask(__name__)
#
# vm_status_file_path = '../scripts/monitor/vm_status.json'
#
#
# @app.route('/')
# def home():
#     return "Welcome to the VM Status Web App!"
#
#
# @app.route('/status', methods=['GET'])
# def get_vm_status():
#     if os.path.exists(vm_status_file_path):
#         with open(vm_status_file_path, 'r') as json_file:
#             vm_status_data = json.load(json_file)
#         return jsonify(vm_status_data), 200
#     else:
#         return jsonify({"error": "VM status data not available"}), 404
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
