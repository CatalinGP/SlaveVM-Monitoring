import json
import subprocess

from flask import Flask, render_template
from db.db_manager import get_all_vm_status
from scripts.monitor import monitor_vm
app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the VM Status Web App!"


@app.route('/status')
def status():
    raw_vm_status_data = get_all_vm_status()
    vm_status_data = []

    for vm in raw_vm_status_data:
        vm_dict = {
            "id": vm[0],
            "vm_name": vm[1],
            "status_data": json.loads(vm[2]) if vm[2] else {},  # Safely parse JSON
            "timestamp": vm[3]
        }
        vm_status_data.append(vm_dict)

    return render_template('status.html', vm_status=vm_status_data)


if __name__ == '__main__':
    subprocess.Popen(["python", "../scripts/monitor/monitor_vm.py"])
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
#