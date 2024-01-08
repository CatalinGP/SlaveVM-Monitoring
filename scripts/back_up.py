import os
import subprocess
import shlex


def back_up():
    default_vm_name = "SubVM"
    export_script_path = "./backup_sub_vm.sh"
    export_dir = "exported_files"
    ovf_file = os.path.join(export_dir, f"{default_vm_name}.ovf")
    vmdk_file = os.path.join(export_dir, f"{default_vm_name}.vmdk")

    if os.path.exists(ovf_file) and os.path.exists(vmdk_file):
        print("Main: OVF and VMDK files already exist. Skipping export.")
    else:
        try:
            cmd = f"{export_script_path} {default_vm_name}"
            subprocess.run(shlex.split(cmd), check=True)
            print("Sub-VM export script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during sub-VM export: {e}")


if __name__ == "__main__":
    back_up()
