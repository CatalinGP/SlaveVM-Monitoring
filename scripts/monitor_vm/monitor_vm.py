import subprocess
import time
import os
import sys
import logging

from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_packages(packages):
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            logger.error(f"Failed to install package: {package}")
            sys.exit(1)

def check_and_install_dependencies():
    try:
        import paramiko
        import scp
    except ImportError:
        logger.info("Required libraries not found. Installing them...")
        install_packages(["paramiko", "scp"])

def create_ssh_key(ssh_key_path):
    ssh_dir = os.path.dirname(ssh_key_path)
    if not os.path.exists(ssh_dir):
        logger.info(f"Creating directory {ssh_dir}")
        os.makedirs(ssh_dir, exist_ok=True)

    if not os.path.exists(ssh_key_path):
        logger.info("Generating SSH key...")
        try:
            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-N", "", "-f", ssh_key_path], check=True)
            logger.info(f"SSH key generated at {ssh_key_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate SSH key: {e}")
            sys.exit(1)
    else:
        logger.info(f"SSH key already exists at {ssh_key_path}")

def is_vm_reachable(ssh_host):
    try:
        response = subprocess.run(['ping', '-n', '1', ssh_host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return response.returncode == 0
    except subprocess.SubprocessError:
        return False


def copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, local_public_key_path, ssh_key_filepath):
    try:
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())

            # Attempt to connect to the SSH server with key-based authentication
            try:
                ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
                ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)

                # If the connection was successful, proceed with copying the public key
                with open(local_public_key_path, 'r') as local_public_key_file:
                    public_key = local_public_key_file.read()

                ssh_client.exec_command(f'echo "{public_key}" >> ~/.ssh/authorized_keys')

                return True  # Authentication was successful using SSH keys
            except AuthenticationException as key_auth_error:
                logger.warning(f"SSH key-based authentication failed: {key_auth_error}")

            # If key-based authentication fails, prompt the user for the SSH password
            ssh_password = input("Enter the SSH password for the VM: ")

            # Attempt password-based authentication
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

            # If the connection was successful, proceed with copying the public key
            with open(local_public_key_path, 'r') as local_public_key_file:
                public_key = local_public_key_file.read()

            ssh_client.exec_command(f'echo "{public_key}" >> ~/.ssh/authorized_keys')

            return True  # Authentication was successful using password

    except SSHException as e:
        logger.error(f"SSH error while copying public key to VM: {e}")
    except Exception as e:
        logger.error(f"An error occurred while connecting to VM: {e}")

    return False  # Authentication failed



def transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)

            with SCPClient(ssh_client.get_transport()) as scp_client:
                scp_client.put(local_status_script_path, remote_script_path)
        return True
    except SSHException as e:
        logger.error(f"SSH error while transferring script: {e}")
        return False


def get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)

            while True:
                command = f'bash {remote_script_path}/{status_script_name}'
                logger.info(f"Executing command on VM: {command}")
                stdin, stdout, stderr = ssh_client.exec_command(command)

                # Read and decode the data from stdout
                status = stdout.read().decode().strip()

                if status:
                    logger.info(f"VM Status: \n{status}")
                else:
                    logger.warning("Unable to retrieve VM status.")
                time.sleep(5)  # Update status every 5 seconds
    except SSHException as e:
        logger.error(f"SSH error while executing script on VM: {e}")


def run():
    ssh_host = '127.0.0.1'
    ssh_port = 5050
    ssh_user = 'gabriel'

    local_status_script_path = 'vm_status.sh'

    current_directory = os.path.dirname(__file__)
    target_two_levels_upper = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))

    ssh_key_filepath = os.path.join(target_two_levels_upper, 'config', 'ssh_keys', 'id_rsa')
    local_public_key_path = os.path.join(target_two_levels_upper, 'config', 'ssh_keys', 'id_rsa.pub')

    remote_script_path = '/home/' + ssh_user

    check_and_install_dependencies()
    create_ssh_key(ssh_key_filepath)

    if copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, local_public_key_path, ssh_key_filepath):
        logger.info("Public key copied to VM.")
    else:
        logger.error("Failed to copy public key to VM.")

    while not is_vm_reachable(ssh_host):
        logger.info("Waiting for VM to become reachable...")
        time.sleep(30)

    # Transfer status script
    if transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
        logger.info("Script transferred. Starting monitoring...")
        while True:
            get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, local_status_script_path)
            time.sleep(60)
    else:
        logger.error("Failed to transfer status script.")

if __name__ == "__main__":
    run()
