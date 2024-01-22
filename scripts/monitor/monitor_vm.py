import json
import os
import time
import logging

# from . import ssh_vm_config
# from . import get_vm_status
# from ..create.ssh_config import ssh_config_dict

from scripts.monitor import ssh_vm_config
from scripts.monitor import get_vm_status
from scripts.create.ssh_config import ssh_config_dict

# import ssh_vm_config
# import get_vm_status
# from scripts.create.ssh_config import ssh_config_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    while True:
        ssh_host = ssh_config_dict["host"]
        ssh_port = ssh_config_dict["port"]
        ssh_user = ssh_config_dict["user"]

        # Define file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_filename = "vm_status.sh"
        local_status_script_path = os.path.join(base_dir, script_filename)

        config_dir = os.path.abspath(os.path.join(base_dir, os.pardir, os.pardir, 'config'))
        ssh_key_filepath = os.path.join(config_dir, 'ssh_keys', 'id_rsa')
        local_public_key_path = os.path.join(config_dir, 'ssh_keys', 'id_rsa.pub')

        remote_script_path = f'/home/{ssh_user}'

        try:
            ssh_vm_config.create_ssh_key(ssh_key_filepath)
            if not ssh_vm_config.copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, local_public_key_path,
                                                       ssh_key_filepath):
                logger.error("Failed to copy the public key to VM.")
                return {}

            while not ssh_vm_config.is_vm_reachable(ssh_host):
                logger.info("Waiting for VM to become reachable...")
                time.sleep(30)

            if not ssh_vm_config.transfer_status_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user,
                                                        local_status_script_path, remote_script_path):
                logger.error("Failed to transfer the status script.")
                return {}

            get_vm_status.get_status(ssh_key_filepath,
                                     ssh_host,
                                     ssh_port,
                                     ssh_user,
                                     remote_script_path,
                                     script_filename)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {}


# run()
