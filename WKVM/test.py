import paramiko
import threading
import time
import logging
import select

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_commands(shell, commands, timeout=5):
    for command in commands:
        logging.info(f"Executing command: {command}")
        shell.send(command + "\n")
        # Wait for the command to complete or timeout
        end_time = time.time() + timeout
        while time.time() < end_time:
            if shell.exit_status_ready():
                break
            time.sleep(0.5)  # Check every 0.5 seconds
        else:
            logging.warning(f"Command timeout reached: {command}")
        time.sleep(1)  # Buffer time before next command
    shell.send("exit\n")
    logging.info("Sent exit command.")

def read_output(shell):
    output_buffer = ""
    try:
        while not shell.exit_status_ready():
            ready, _, _ = select.select([shell], [], [], 5)
            if ready:
                output = shell.recv(1024).decode('utf-8')
                output_buffer += output
                print(output, end='')
            else:
                logging.info("No output received in the last 5 seconds.")
    finally:
        if output_buffer:
            logging.info("Final output captured from the session.")

def main(hostname, username, password, commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        logging.info("SSH connection established.")
        shell = client.invoke_shell(term='xterm')
        logging.info("Interactive SSH session started.")

        thread_executor = threading.Thread(target=execute_commands, args=(shell, commands))
        thread_reader = threading.Thread(target=read_output, args=(shell,))

        thread_executor.start()
        thread_reader.start()

        thread_executor.join()
        thread_reader.join()

    except paramiko.AuthenticationException:
        logging.error("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        logging.error(f"SSH connection failed: {str(e)}")
    finally:
        client.close()
        logging.info("SSH connection closed.")

if __name__ == "__main__":
    commands = ["ls --color=auto", "uname -a", "echo -e '\e[1;33mYellow Text\e[0m'", "uname -a"]
    main('192.168.8.103', 'kvm', 'kvm', commands)
