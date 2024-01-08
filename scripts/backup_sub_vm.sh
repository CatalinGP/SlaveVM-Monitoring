#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <No argument provided>"
    exit 1
fi

if ! VBoxManage --version >/dev/null 2>&1; then
    echo "VirtualBox is not installed or not in your PATH. Please install VirtualBox first."
    exit 1
fi

vm_name="$1"
echo VM name provided as an argument
echo

export_dir="exported_files"
mkdir -p "$export_dir"

ovf_file="${export_dir}/${vm_name}.ovf"
VBoxManage export "$vm_name" --output "$ovf_file"

vmdk_file="${export_dir}/${vm_name}.vmdk"
VBoxManage clonehd "$(VBoxManage showvminfo --machinereadable "$vm_name" | grep "SATA Controller-0-0")" "$vmdk_file" --format VMDK

echo "Exported VM '$vm_name' to $ovf_file and $vmdk_file in the '$export_dir' sub-directory successfully."

set +x