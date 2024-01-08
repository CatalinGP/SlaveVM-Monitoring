import subprocess


def main():
    try:
        # Call create_sub_vm.py script
        subprocess.run(["python3", "./create.py"], check=True)
        print("Main: create_sub_vm.py script executed successfully.")

        # Call backup_sub_vm.py script
        # subprocess.run(["python3", "./back_up.py"], check=True)
        # print("Main: backup_sub_vm.py script executed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Main: Error during script execution: {e}")


if __name__ == "__main__":
    main()
