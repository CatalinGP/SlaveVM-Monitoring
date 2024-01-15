import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_vm_config_sh():
    current_directory = os.path.dirname(__file__)
    target_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    file_path = os.path.join(target_directory, "config", "vm_params.sh")

    with open(file_path, "w") as f:
        for key, value in vm_config_dict.items():
            f.write(f"export {key}=\"{value}\"\n")
    return "Virtual machine params updated."

vm_config_dict = {
    "vmname": "VirtualMachine",
    "isopath": os.path.join(project_dir, "scripts", "create_vm", "ubuntu-22.04.3-live-server-amd64.iso"),
    "vmdir": os.path.join(project_dir, "VirtualMachines"),
    "hddname": os.path.join(project_dir, "VirtualMachines", "VMVolume.vdi"),
    "volumename": "VMVolume.vdi",
}

