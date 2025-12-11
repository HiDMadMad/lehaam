import paramiko

# ---------------- CONFIG ----------------
hostname = "IP"
username = "USER"
password = "PASS"
port = 22

files_to_upload = [
    (r"from_PATH", "to_PATH"),
]

commands = [
    "COMMAND_1",
    "COMMAND_2"
]


# ---------------------------------------
def upload_files(client, files):
    try:
        sftp = client.open_sftp()
        for local_path, remote_path in files:
            print(f"📤 uploading {local_path} → {remote_path}")
            sftp.put(local_path, remote_path)
        sftp.close()
        print("✅ all files uploaded successfully")
    except Exception as e:
        print("❌ upload error:", e)

def run_commands(client, cmds):
    try:
        for cmd in cmds:
            print(f"\n▶ running: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()

            if out:
                print("📤 output:")
                print(out)
            if err:
                print("⚠️ error:")
                print(err)
    except Exception as e:
        print("❌ command execution error:", e)

def kill_python_processes(client, user):
    try:
        cmd = f"ps -u {user} | grep python3 | awk '{{print $1}}'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        pids = stdout.read().decode().split()
        err = stderr.read().decode()
        
        if err:
            print("⚠️ error while getting python3 PIDs:")
            print(err)
            return
        
        if not pids:
            print("ℹ️ no python3 processes found")
            return
        
        for pid in pids:
            kill_cmd = f"kill -9 {pid}"
            client.exec_command(kill_cmd)
            print(f"✅ killed python3 process with PID: {pid}")
            
    except Exception as e:
        print("❌ error in kill_python_processes:", e)

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("🔌 connecting to server...")
        client.connect(hostname, port=port, username=username, password=password, timeout=30)
        print("✅ connected successfully")

        upload_files(client, files_to_upload)

        kill_python_processes(client, username)

        run_commands(client, commands)

    except Exception as e:
        print("❌ connection error:", e)

    finally:
        client.close()
        print("🔒 connection closed")


if __name__ == "__main__":
    main()
#MadMad_98