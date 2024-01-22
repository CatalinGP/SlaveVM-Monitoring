import logging
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException
from db.db_manager import save_vm_status
from scripts.create.vm_config import vm_config_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def organize_vm_status(status_output):
    status_data = {}
    current_section = None
    lines = status_output.split('\n')

    for line in lines:
        line = line.strip()
        if line:
            if line.endswith(":"):
                current_section = line[:-1]
                status_data[current_section] = []
            elif current_section:
                status_data[current_section].append(line)

    return status_data


def get_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)

            command = f'bash {remote_script_path}/{status_script_name}'
            logger.info(f"Executing command on VM: {command}")
            stdin, stdout, stderr = ssh_client.exec_command(command)

            status_output = stdout.read().decode('utf-8')

            if status_output:
                organized_data = organize_vm_status(status_output)
                vm_name = vm_config_dict["vmname"]
                save_vm_status(vm_name, organized_data)

            else:
                logger.warning("Unable to retrieve VM status.")

    except SSHException as e:
        logger.error(f"SSH error: {e}")

