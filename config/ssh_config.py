import os


ssh_config_dict = {
    "host": "127.0.0.1",
    "port": "5050",
    "user": "gabriel",
}


def generate_ssh_config_sh():
    current_directory = os.path.dirname(__file__)
    target_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    file_path = os.path.join(target_directory, "config", "ssh_params.sh")

    with open(file_path, "w") as f:
        for key, value in ssh_config_dict.items():
            f.write(f"export {key}=\"{value}\"\n")
    return "SSH config parameters updated."
