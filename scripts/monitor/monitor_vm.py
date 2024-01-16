import os
import time
import logging
from . import ssh_vm_config
from . import vm_status_monitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    ssh_host = '127.0.0.1'
    ssh_port = 5050
    ssh_user = 'gabriel'

    current_directory = os.path.dirname(os.path.abspath(__file__))
    script_filename = "vm_status.sh"
    local_status_script_path = os.path.join(current_directory, script_filename)

    current_directory = os.path.dirname(__file__)
    target_two_levels_upper = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))

    ssh_key_filepath = os.path.join(target_two_levels_upper, 'config', 'ssh_keys', 'id_rsa')
    local_public_key_path = os.path.join(target_two_levels_upper, 'config', 'ssh_keys', 'id_rsa.pub')

    remote_script_path = '/home/' + ssh_user

    ssh_vm_config.create_ssh_key(ssh_key_filepath)

    if ssh_vm_config.copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, local_public_key_path, ssh_key_filepath):
        logger.info("Public key copied to VM.")
    else:
        logger.error("Failed to copy the public key to VM.")

    while not ssh_vm_config.is_vm_reachable(ssh_host):
        logger.info("Waiting for VM to become reachable...")
        time.sleep(30)

    if not os.path.exists(os.path.join(remote_script_path, local_status_script_path)):
        if ssh_vm_config.transfer_status_script(ssh_key_filepath,
                                                ssh_host,
                                                ssh_port,
                                                ssh_user,
                                                local_status_script_path,
                                                remote_script_path):
            logger.info("Script transferred. Starting monitoring...")
        else:
            logger.error("Failed to transfer the status script.")

    output_json_filename = 'vm_status.json'
    output_json_file = os.path.join(current_directory, output_json_filename)
    logger.info(f"Json containing VM data successfully saved at {output_json_file}")
    vm_status_monitor.get_vm_status(ssh_key_filepath,
                                    ssh_host,
                                    ssh_port,
                                    ssh_user,
                                    remote_script_path,
                                    script_filename,
                                    output_json_file)


if __name__ == "__main__":
    run()
