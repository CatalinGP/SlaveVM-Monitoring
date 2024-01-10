import subprocess
import time
import os
import sys
from scp import SCPClient
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException
from scripts import auth

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
                time.sleep(5)  # Update status every 5 seconds
    except SSHException as e:
        print(f"SSH error while executing script on VM: {e}")

def main():
    ssh_host = '127.0.0.1'
    ssh_port = 5050
    ssh_user = 'gabriel'
    status_script_name = 'vm_status.sh'
    local_status_script_path = 'vm_status.sh'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    ssh_key_filepath = os.path.join(script_dir, 'ssh_keys', 'id_rsa')
    remote_script_path = '/home/' + ssh_user
    auth.check_and_install_dependencies()  # Use auth module for dependency check

    while not auth.is_vm_reachable(ssh_host):  # Use auth module for reachability check
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
            time.sleep(5)  # Update status every 5 seconds
    else:
        print("Failed to transfer status script.")

if __name__ == "__main__":
    main()
