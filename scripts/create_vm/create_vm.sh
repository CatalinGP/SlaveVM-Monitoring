#!/bin/bash

source ssh_config.py

vm_name="${ssh_config["vm_name"]}"
iso_path="${ssh_config["iso_path"]}"
vm_dir="${ssh_config["vm_dir"]}"
hdd_path="${ssh_config["hdd_path"]}"
ssh_host="${ssh_config["ssh_host"]}"
ssh_port="${ssh_config["ssh_port"]}"
ssh_user="${ssh_config["ssh_user"]}"

# Quick test param
#vm_name="MyVM"
#iso_file="ubuntu-22.04.3-live-server-amd64.iso"  # Replace with your Ubuntu ISO file name
#project_dir=$(pwd)
#iso_path="${project_dir}/${iso_file}"
#vm_dir="${project_dir}/VirtualMachines"
#hdd_path="${vm_dir}/${vm_name}/${vm_name}.vdi"


find_vboxmanage() {
    local potential_paths=(
        "/usr/bin"
        "/usr/local/bin"
        "/usr/sbin"
        "/sbin"
        "/bin"
        "/snap/bin"
        "/c/Program Files/Oracle/VirtualBox"
        "/c/Program Files (x86)/Oracle/VirtualBox"
    )

    for path in "${potential_paths[@]}"; do
        vboxmanage_path="${path}/VBoxManage"
        if [ -x "$vboxmanage_path" ] || [ -f "${vboxmanage_path}.exe" ]; then
            echo "$vboxmanage_path"
            return 0
        fi
    done

    echo "VBoxManage not found. Please ensure VirtualBox is installed." >&2
    return 1
}

run_command() {
    command=("$@")
    "${command[@]}"
    if [ $? -ne 0 ]; then
        echo "Error executing command: ${command[*]}" >&2
        exit 1
    fi
}

vboxmanage=$(find_vboxmanage)
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Creating VM: ${vm_name}"
vboxmanage_cmd=("${vboxmanage}" createvm --name "${vm_name}" --ostype Ubuntu_64 --register --basefolder "${vm_dir}")
run_command "${vboxmanage_cmd[@]}"

echo "Setting VM hardware requirements..."
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --memory 4048 --cpus 4 --vram 128 --ioapic on)
run_command "${vboxmanage_cmd[@]}"

echo "Creating virtual hard disk..."
mkdir -p "${vm_dir}"
if [ ! -f "${hdd_path}" ]; then
    vboxmanage_cmd=("${vboxmanage}" createhd --filename "${hdd_path}" --size 50000)  # Size in MB
    run_command "${vboxmanage_cmd[@]}"
else
    echo "Virtual hard disk already exists. Skipping creation."
fi

echo "Attaching hard disk and ISO..."
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'SATA Controller' --add sata --controller IntelAhci)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'SATA Controller' --port 0 --device 0 --type hdd --medium "${hdd_path}")
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'IDE Controller' --add ide)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'IDE Controller' --port 0 --device 0 --type dvddrive --medium "${iso_path}")
run_command "${vboxmanage_cmd[@]}"

echo "Configuring NAT Network Adapter with Port Forwarding..."
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --nic1 nat)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --natpf1 'guestssh,$ssh_host,,$ssh_port,,22')
run_command "${vboxmanage_cmd[@]}"

echo "VM created successfully."
echo "Starting VM"
vboxmanage_cmd=("${vboxmanage}" startvm "${vm_name}")
run_command "${vboxmanage_cmd[@]}"

