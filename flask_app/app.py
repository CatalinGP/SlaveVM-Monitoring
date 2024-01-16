from flask import Flask, jsonify, render_template
import json
import os
from scripts.monitor import monitor_vm
app = Flask(__name__)

vm_status_file = '../scripts/monitor_vm/vm_status.json'


@app.route('/')
def home():
    return "Welcome to the VM Status Web App!"


@app.route('/status', methods=['GET'])
def get_vm_status():
    if os.path.exists(vm_status_file):
        with open(vm_status_file, 'r') as json_file:
            vm_status_data = json.load(json_file)
        return jsonify(vm_status_data), 200
    else:
        return jsonify({"error": "VM status data not available"}), 404


if __name__ == '__main__':
    monitor_vm.run()
    app.run(debug=False)
