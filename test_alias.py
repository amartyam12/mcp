from tools.alias_parser import load_aliases
from tools.ssh_client import execute_remote

server = load_aliases()["gps.agorae"]
PEM_DIR = "/home/amartya-mandal/Downloads/Amartya-001/Amartya/Pem_Files"

result = execute_remote(
    host=server["host"],
    username=server["user"],
    pem_file=server["pem"],
    port=server["port"],
    command="whoami"
)

print(result)