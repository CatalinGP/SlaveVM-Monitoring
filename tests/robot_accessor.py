
from scripts.create.ssh_config import ssh_config_dict

def get_config_value(key):
    if key in ssh_config_dict:
        return config_dict_1[key]
    else:
        raise KeyError(f"Config key {key} not found.")