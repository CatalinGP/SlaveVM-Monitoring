import subprocess
import time
import os
import sys
from scp import SCPClient
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
        import scp
    except ImportError:
        print("Required libraries not found. Installing them...")
        install_packages(["paramiko", "scp"])

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
        # Adjust the command for Windows compatibility
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
        print(f"SSH error while transferring script: {e}")
        return False

def get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)

            while True:
                stdin, stdout, stderr = ssh_client.exec_command(f'bash {remote_script_path}/{status_script_name}')
                status = stdout.read().decode()
                if status:
                    print(f"VM Status: \n{status}")
                else:
                    print("Unable to retrieve VM status.")
                time.sleep(5)  # Update status every 1 second
    except SSHException as e:
        print(f"SSH error while executing script on VM: {e}")

def main():
    # SSH Configuration
    ssh_host = '127.0.0.1'
    ssh_port = 5050
    ssh_user = 'gabriel'
    status_script_name = 'vm_status.sh'
    local_status_script_path = 'vm_status.sh'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    ssh_key_filepath = os.path.join(script_dir, 'ssh_keys', 'id_rsa')
    local_public_key_path = os.path.join(script_dir, 'ssh_keys', 'id_rsa.pub')
    remote_script_path = '/home/' + ssh_user

    check_and_install_dependencies()

    create_ssh_key(ssh_key_filepath)

    ssh_password = input("Enter the SSH password for the VM: ")

    if copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, ssh_password, local_public_key_path):
        print("Public key copied to VM.")
    else:
        print("Failed to copy public key to VM.")

    # if verify_key_based_auth(ssh_key_filepath, ssh_user, ssh_host, ssh_port):
    #     print("Key-based authentication successful.")
    # else:
    #     print("Key-based authentication failed.")

    while not is_vm_reachable(ssh_host):
        print("Waiting for VM to become reachable...")
        time.sleep(30)

    # Transfer status script
    if transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
        print("Script transferred. Starting monitoring...")
        while True:
            status = get_vm_status(ssh_key_filepath, ssh_host, ssh_port, ssh_user, remote_script_path, status_script_name)
            if status:
                print(f"VM Status: \n{status}")
            else:
                print("Unable to retrieve VM status.")
            time.sleep(60)
    else:
        print("Failed to transfer status script.")

if __name__ == "__main__":
    main()
