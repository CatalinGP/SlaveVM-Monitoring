import subprocess
import os
import sys
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException

def install_packages(packages):
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install package: {package}")
            sys.exit(1)

def check_and_install_dependencies():
    try:
        import paramiko
    except ImportError:
        print("Required library 'paramiko' not found. Installing it...")
        install_packages(["paramiko"])

def create_ssh_key(ssh_key_path):
    ssh_dir = os.path.dirname(ssh_key_path)
    if not os.path.exists(ssh_dir):
        print(f"Creating directory {ssh_dir}")
        os.makedirs(ssh_dir, exist_ok=True)

    if not os.path.exists(ssh_key_path):
        print("Generating SSH key...")
        try:
            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-N", "", "-f", ssh_key_path], check=True)
            print(f"SSH key generated at {ssh_key_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate SSH key: {e}")
            sys.exit(1)
    else:
        print(f"SSH key already exists at {ssh_key_path}")

def is_vm_reachable(ssh_host):
    try:
        response = subprocess.run(['ping', '-n', '1', ssh_host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return response.returncode == 0
    except subprocess.SubprocessError:
        return False

def copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, ssh_password, local_public_key_path):
    try:
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

            # Read the local public key
            with open(local_public_key_path, 'r') as local_public_key_file:
                public_key = local_public_key_file.read()

            # Append the public key to the authorized_keys file on the VM
            ssh_client.exec_command(f'echo "{public_key}" >> ~/.ssh/authorized_keys')

        return True
    except SSHException as e:
        print(f"SSH error while copying public key to VM: {e}")
        return False

# New function for SSH authentication
def authenticate_ssh(ssh_key_filepath, ssh_host, ssh_port, ssh_user):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)
        return ssh_client
    except SSHException as e:
        print(f"SSH authentication error: {e}")
        return None
