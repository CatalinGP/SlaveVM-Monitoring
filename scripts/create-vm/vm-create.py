import subprocess
import os
import sys


def execute_shell_script(script_path, *args):
    try:
        subprocess.check_output([script_path, *args], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {e.output.decode().strip()}", file=sys.stderr)
        sys.exit(1)


def create_vm(vm_name, iso_path, vm_dir, hdd_path):
    script_path = 'create_vm.sh'
    execute_shell_script(script_path, vm_name, iso_path, vm_dir, hdd_path)


def main():
    vm_name = "MyVM"
    iso_file = "ubuntu-22.04.3-live-server-amd64.iso"  # Replace with your Ubuntu ISO file name
    project_dir = os.getcwd()
    iso_path = os.path.join(project_dir, iso_file)
    vm_dir = os.path.join(project_dir, "VirtualMachines")  # Directory to store VMs
    hdd_path = os.path.join(vm_dir, vm_name, f"{vm_name}.vdi")  # Path for the virtual hard disk

    if not os.path.exists(iso_path):
        print(f"ISO file not found: {iso_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(vm_dir, exist_ok=True)

    create_vm(vm_name, iso_path, vm_dir, hdd_path)


if __name__ == "__main__":
    main()
