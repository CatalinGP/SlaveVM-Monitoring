import os

current_directory = os.path.dirname(__file__)
target_two_levels_upper = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))


def generate_vm_config_sh():
    file_path = os.path.join(target_two_levels_upper, "config", "vm_params.sh")
    with open(file_path, "w") as f:
        for key, value in vm_config_dict.items():
            f.write(f"export {key}=\"{value}\"\n")
    return "Virtual machine params updated."


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

vm_config_dict = {
    "vmname": "VirtualMachine",
    "isopath": os.path.join(current_directory, "ubuntu-22.04.3-live-server-amd64.iso"),
    "vmdir": os.path.join(target_two_levels_upper, "VirtualMachines"),
    "hddname": os.path.join(target_two_levels_upper, "VirtualMachines", "VMVolume.vdi"),
    "volumename": "VMVolume.vdi",
}

