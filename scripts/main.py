import subprocess
import sys
import os

def run_script(script_path, *args):
    try:
        subprocess.run([sys.executable, script_path, *args], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during script execution: {e}")
        return False
    return True

def main():
    # Adjust the relative paths according to your directory structure
    create_vm_script = "./create_vm/vm_create.py"
    monitor_vm_script = "./monitor_vm/monitor_vm.py"

    print("Running create_vm script...")
    if run_script(create_vm_script):
        print("create_vm script executed successfully.")

        print("Running monitor_vm script...")
        if run_script(monitor_vm_script):
            print("monitor_vm script executed successfully.")
        else:
            print("Failed to execute monitor_vm script.")
    else:
        print("Failed to execute create_vm script.")

if __name__ == "__main__":
    main()
