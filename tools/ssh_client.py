import paramiko


def execute_remote(
    host: str,
    username: str,
    pem_file: str,
    command: str,
    port: int = 2223,
    timeout: int = 10,
):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            key_filename=pem_file,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
        )

        wrapped_command = command

        stdin, stdout, stderr = ssh.exec_command(wrapped_command)

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        return {
            "success": True,
            "output": output,
            "error": error,
        }

    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
        }

    finally:
        ssh.close()
