import os
import time
import logging

from paramiko.ssh_exception import SSHException

import auth
import scp

# Setup logging
logging.basicConfig(level=logging.INFO)

def transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
    try:
        ssh_client = auth.authenticate_ssh(ssh_key_filepath, ssh_host, ssh_port, ssh_user)
        if ssh_client is None:
            return False

        with scp.SCPClient(ssh_client.get_transport()) as scp_client:
            scp_client.put(local_status_script_path, remote_script_path)

        ssh_client.close()
        return True
    except SSHException as e:
        logging.error(f"SSH error while transferring script: {e}")
        return False

def get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name):
    try:
        ssh_client = auth.authenticate_ssh(ssh_key_filepath, ssh_host, ssh_port, ssh_user)
        if ssh_client is None:
            return False

        while True:
            stdin, stdout, stderr = ssh_client.exec_command(f'bash {remote_script_path}/{status_script_name}')
            status = stdout.read().decode()
            if status:
                logging.info(f"VM Status: \n{status}")
            else:
                logging.warning("Unable to retrieve VM status.")
            time.sleep(5)  # Update status every 5 seconds

        ssh_client.close()
    except SSHException as e:
        logging.error(f"SSH error while executing script on VM: {e}")

def main():
    ssh_host = os.getenv('SSH_HOST', '127.0.0.1')
    ssh_port = int(os.getenv('SSH_PORT', '5050'))
    ssh_user = os.getenv('SSH_USER', 'gabriel')
    status_script_name = 'vm_status.sh'
    local_status_script_path = 'vm_status.sh'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    ssh_key_filepath = os.path.join(script_dir, 'ssh_keys', 'id_rsa')
    remote_script_path = '/home/' + ssh_user

    auth.check_and_install_dependencies()

    while not auth.is_vm_reachable(ssh_host):
        logging.info("Waiting for VM to become reachable...")
        time.sleep(30)

    if transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
        logging.info("Script transferred. Starting monitoring...")
        get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name)
    else:
        logging.error("Failed to transfer status script.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
