import os

ssh_config_dict = {
    "host": "127.0.0.1",
    "port": "5050",
    "user": "gabriel",
}

current_directory = os.path.dirname(__file__)
target_two_levels_upper = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))

def generate_ssh_config_sh():
    file_path = os.path.join(target_two_levels_upper, "config", "ssh_params.sh")

    with open(file_path, "w") as f:
        for key, value in ssh_config_dict.items():
            f.write(f"export {key}=\"{value}\"\n")
    return "SSH config parameters updated."
