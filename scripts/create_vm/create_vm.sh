#!/usr/bin/env bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
config_dir="$(dirname $(dirname "$script_dir"))"
cd "$config_dir/config" || exit 1

source "ssh_params.sh"
ssh_host=$host
ssh_port=$port
ssh_user=$user

source "vm_params.sh"
vm_name=$vmname
iso_path=$isopath
vm_dir=$vmdir
hdd_name=$hddname

cd "$script_dir" || exit 1

is_not_empty() {
    local var="$1"
    local message="$2"
    if [ -n "$var" ]; then
        echo "$message: Variable is not empty."
        return 0  # Variable is not empty
    else
        echo "$message: Variable is empty."
        return 1  # Variable is empty
    fi
}

is_not_empty "$vm_name" "Checking my_variable"
is_not_empty "$iso_path" "Checking my_variable"
is_not_empty "$vm_dir" "Checking my_variable"
is_not_empty "$hdd_name" "Checking my_variable"

is_not_empty "$ssh_host" "Checking my_variable"
is_not_empty "$ssh_port" "Checking my_variable"
is_not_empty "$ssh_user" "Checking my_variable"


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
if [ ! -f "${hdd_name}" ]; then
    vboxmanage_cmd=("${vboxmanage}" createhd --filename "${hdd_name}" --size 50000)  # Size in MB
    run_command "${vboxmanage_cmd[@]}"
else
    echo "Virtual hard disk already exists. Skipping creation."
fi

echo "Attaching hard disk and ISO..."
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'SATA Controller' --add sata --controller IntelAhci)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'SATA Controller' --port 0 --device 0 --type hdd --medium "${hdd_name}")
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storagectl "${vm_name}" --name 'IDE Controller' --add ide)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" storageattach "${vm_name}" --storagectl 'IDE Controller' --port 0 --device 0 --type dvddrive --medium "${iso_path}")
run_command "${vboxmanage_cmd[@]}"

echo "Configuring VM graphics controller to VMSVGA..."
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --graphicscontroller vmsvga)
run_command "${vboxmanage_cmd[@]}"

echo "Configuring NAT Network Adapter with Port Forwarding..."
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --nic1 nat)
run_command "${vboxmanage_cmd[@]}"
vboxmanage_cmd=("${vboxmanage}" modifyvm "${vm_name}" --natpf1 "guestssh,tcp,$ssh_host,$ssh_port,,22")
run_command "${vboxmanage_cmd[@]}"

echo "VM created successfully."
echo "Starting VM"
vboxmanage_cmd=("${vboxmanage}" startvm "${vm_name}")
run_command "${vboxmanage_cmd[@]}"

