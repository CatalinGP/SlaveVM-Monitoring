import json
import time
import logging
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException
from db.database_setup import Session, VMStatus
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

                status_output = stdout.read().decode('utf-8')

                if status_output:
                    logger.info("VM Status Report:")
                    organized_data = organize_vm_status(status_output)
                    for section, lines in organized_data.items():
                        logger.info(section)
                        for line in lines:
                            logger.info(line)

                    # status_json = json.dumps(organized_data, indent=4)
                    # logger.info(f"VM Status (JSON):\n{status_json}")
                    #
                    # with open(output_json_file, 'w') as json_file:
                    #     json.dump(organized_data, json_file, indent=4)

                    status_json = json.dumps(organized_data, indent=4)
                    logger.info(f"VM Status (JSON):\n{status_json}")

                    # Database insertion
                    session = Session()
                    new_vm_status = VMStatus(status_data=organized_data,
                                             vm_name=vm_config_dict["vmname"])  # Replace with actual VM name
                    session.add(new_vm_status)
                    session.commit()
                    session.close()


                else:
                    logger.warning("Unable to retrieve VM status.")
                time.sleep(10)  # Execute at {} seconds
    except SSHException as e:
        logger.error(f"SSH error while executing script on VM: {e}")
