import os

# vm_name = "VM"
# iso_file = "ubuntu-22.04.3-live-server-amd64.iso"
project_dir = os.getcwd()
# iso_path = os.path.join(project_dir, iso_file)
# vm_dir = os.path.join(project_dir, "VirtualMachines")
# hdd_path = os.path.join(vm_dir, vm_name, f"{vm_name}.vdi")

ssh_config_param = {
    "vm_name": "VirtualMachine",
    "iso_path": "./scripts/create_vm/ubuntu-22.04.3-live-server-amd64.iso",
    "vm_dir": "/scripts/create_vm/VirtualMachines",
    "hdd_path": "scripts/create_VM/VirtualMachines/VM/MyVM.vdi",
    "ssh_host": "127.0.0.1",
    "ssh_port": "5050",
    "ssh_user": "gabriel"
}
