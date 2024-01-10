import subprocess
import os
import sys
from config.ssh_config import ssh_config_param

def execute_shell_script(script_path, *args):
    try:
        subprocess.check_output([script_path, *args], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {e.output.decode().strip()}", file=sys.stderr)
        sys.exit(1)


def is_vm_exists(vm_name):
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
    try:
        existing_vms = subprocess.check_output([vboxmanage_path, "list", "vms"], shell=True).decode()
        return vm_name in existing_vms
    except subprocess.CalledProcessError as e:
        print(f"Error checking existing VMs: {e.output.decode().strip()}", file=sys.stderr)
        return False


def create_vm(vm_name, iso_path, vm_dir, hdd_path):
    if is_vm_exists(vm_name):
        print(f"VM '{vm_name}' already exists. Skipping creation.")
        return

    script_path = 'create_vm.sh'
    execute_shell_script(script_path, vm_name, iso_path, vm_dir, hdd_path)


vm_name = ssh_config_param["vm_name"]
iso_path = ssh_config_param["iso_path"]
vm_dir = ssh_config_param["vm_dir"]
hdd_path = ssh_config_param["hdd_path"]

vboxmanage_path = 'vboxmanage_addPath.sh'
execute_shell_script(vboxmanage_path)

if not os.path.exists(iso_path):
    print(f"ISO file not found: {iso_path}", file=sys.stderr)
    sys.exit(1)

os.makedirs(vm_dir, exist_ok=True)

create_vm(vm_name, iso_path, vm_dir, hdd_path)
