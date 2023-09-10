import subprocess
import time
import os

CONFIG_FILE = 'D:/jvb.txt'
FINAL_FILE = 'D:/final.txt'

def run_v2ray_process(config):
    start_info = subprocess.STARTUPINFO()
    start_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    start_info.wShowWindow = subprocess.SW_HIDE

    try:
        process = subprocess.Popen(["v2ray.exe", "run", f"-config={config}"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   startupinfo=start_info)
        time.sleep(1.5)
        process.wait()  # Wait for the process to finish

        if process.returncode == 0:
            return True
        else:
            stderr = process.communicate()[1]
            print(f"v2ray stderr: {stderr}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error starting v2ray process: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file '{CONFIG_FILE}' not found.")
        return

    with open(CONFIG_FILE) as f:
        configs = f.readlines()

    for config in configs:
        config = config.strip()
        success = run_v2ray_process(config)

        if success:
            with open(FINAL_FILE, 'a') as f:
                f.write(config + '\n')

if __name__ == "__main__":
    main()
