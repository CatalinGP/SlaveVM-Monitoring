import subprocess
import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import ssh_config, vm_config
from config.vm_config import vm_config_dict

def execute_shell_script(script_path, *args):
    try:
        subprocess.check_output([script_path, *args], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {e.output.decode().strip()}", file=sys.stderr)
        sys.exit(1)


def is_vm_exists(vm_directory):
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
    try:
        existing_vms = subprocess.check_output([vboxmanage_path, "list", "vms"], shell=True).decode()
        return vm_directory in existing_vms
    except subprocess.CalledProcessError as e:
        print(f"Error checking existing VMs: {e.output.decode().strip()}", file=sys.stderr)
        return False


def create_vm(vm_directory):
    if is_vm_exists(vm_directory):
        print(f"VM '{vm_directory}' already exists. Skipping creation.")
        return

    # script_path = 'create_vm.sh'
    # execute_shell_script(script_path)


vm_dir = vm_config_dict['vmname']
vboxmanage_file = 'vboxmanage_addPath.sh'
execute_shell_script(vboxmanage_file)

# os.makedirs(vm_dir, exist_ok=True)

vm_config.generate_vm_config_sh()
ssh_config.generate_ssh_config_sh()
create_vm(vm_dir)
