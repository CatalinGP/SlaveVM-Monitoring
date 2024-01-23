import os
import logging

from scripts.monitoring import ssh_vm_utils
from scripts.monitoring import data_fetch_manager
from scripts.create.ssh_config import ssh_config_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    while True:
        ssh_host = ssh_config_dict["host"]
        ssh_port = ssh_config_dict["port"]
        ssh_user = ssh_config_dict["user"]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        status_report_script_filename = "status_report.sh"
        local_status_report_script_path = os.path.join(base_dir, status_report_script_filename)

        config_dir = os.path.abspath(os.path.join(base_dir, os.pardir, os.pardir, 'config'))
        ssh_key_filepath = os.path.join(config_dir, 'ssh_keys', 'id_rsa')
        local_public_key_path = os.path.join(config_dir, 'ssh_keys', 'id_rsa.pub')

        remote_script_path = f'/home/{ssh_user}'

        try:
            ssh_vm_utils.create_ssh_key(ssh_key_filepath)
            if not ssh_vm_utils.copy_public_key_to_vm(ssh_host,
                                                      ssh_port,
                                                      ssh_user,
                                                      local_public_key_path,
                                                      ssh_key_filepath):
                logger.error("Failed to transfer the status script.")
                return {}

            if not ssh_vm_utils.transfer_script(ssh_host,
                                                ssh_key_filepath,
                                                ssh_port,
                                                ssh_user,
                                                local_status_report_script_path,
                                                remote_script_path,
                                                status_report_script_filename):
                logger.error("Failed to transfer the status script.")
                return {}

            if not data_fetch_manager.get_status(ssh_key_filepath,
                                                 ssh_host,
                                                 ssh_port,
                                                 ssh_user,
                                                 remote_script_path,
                                                 status_report_script_filename):
                logger.error("Failed to retrieve VM status")
                return {}

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {}


run()
