#!/bin/bash

# Variables from arguments
vm_name=$1
iso_path=$2
vm_dir=$3
hdd_path=$4

#vm_name="MyVM"
#iso_file="ubuntu-22.04.3-live-server-amd64.iso"  # Replace with your Ubuntu ISO file name
#project_dir=$(pwd)
#iso_path="${project_dir}/${iso_file}"
#vm_dir="${project_dir}/VirtualMachines"
#hdd_path="${vm_dir}/${vm_name}/${vm_name}.vdi"


# Function to find VBoxManage executable
find_vboxmanage() {
    local potential_paths=(
        "/usr/bin"  # Typical path on Unix/Linux
        "/usr/local/bin"  # Another possible path on Unix/Linux
        "/usr/sbin"  # Another potential path
        "/sbin"  # Additional path
        "/bin"  # Additional path
        "/snap/bin"   # Snap installation path
        "/c/Program Files/Oracle/VirtualBox"  # Typical path on Windows with Git Bash
        "/c/Program Files (x86)/Oracle/VirtualBox"
    )

    # Check each path
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

# Function to run a command and check if it was successful
run_command() {
    command=("$@")  # Store all arguments in an array
    "${command[@]}"  # Execute the command array
    if [ $? -ne 0 ]; then
        echo "Error executing command: ${command[*]}" >&2
        exit 1
    fi
}


# Find VBoxManage
vboxmanage=$(find_vboxmanage)
if [ $? -ne 0 ]; then
    exit 1
fi


# Creating VM
echo "Creating VM: ${vm_name}"
vboxmanage_cmd=("${vboxmanage}" createvm --name "${vm_name}" --ostype Ubuntu_64 --register --basefolder "${vm_dir}")
run_command "${vboxmanage_cmd[@]}"

# Setting VM hardware requirements
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

# Attaching hard disk and ISO
echo "Attaching hard disk and ISO..."
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'SATA Controller' --add sata --controller IntelAhci)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'SATA Controller' --port 0 --device 0 --type hdd --medium "${hdd_path}")
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'IDE Controller' --add ide)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'IDE Controller' --port 0 --device 0 --type dvddrive --medium "${iso_path}")
run_command "${vboxmanage_cmd[@]}"

# Configuring NAT Network Adapter with Port Forwarding
echo "Configuring NAT Network Adapter with Port Forwarding..."
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --nic1 nat)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --natpf1 'guestssh,tcp,,5050,,22')
run_command "${vboxmanage_cmd[@]}"

echo "VM created successfully."