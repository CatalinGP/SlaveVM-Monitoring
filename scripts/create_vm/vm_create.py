import subprocess
import sys
import config.vm_config
from config.vm_config import vm_config_param


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
    config.vm_config.create_vm_params_sh_file()
    if is_vm_exists(vm_directory):
        print(f"VM '{vm_directory}' already exists. Skipping creation.")
        return

    script_path = 'create_vm.sh'
    execute_shell_script(script_path)


vm_dir = vm_config_param['volumename']
vboxmanage_file = 'vboxmanage_addPath.sh'
execute_shell_script(vboxmanage_file)

# os.makedirs(vm_dir, exist_ok=True)

create_vm(vm_dir)
