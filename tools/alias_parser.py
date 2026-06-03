import os
import re

ALIAS_FILE = os.path.expanduser("~/.bashrc")
PEM_BASE_DIR = os.path.expanduser("~/Downloads/Amartya-001/Amartya/Pem_Files")


def load_aliases():
    aliases = {}
    with open(ALIAS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("alias "):
                continue
            alias_match = re.match(r'alias\s+([^\s=]+)=["\'](.*?)["\']$', line)
            if not alias_match:
                continue
            alias_name, command = alias_match.groups()
            ssh_match = re.search(
                r"ssh.*?-i\s+(\S+).*?(?:-p\s+(\d+)\s+)?([^@\s]+)@([\d\.]+)", command
            )
            if not ssh_match:
                continue
            pem, port, user, host = ssh_match.groups()

            # Resolve relative PEM paths to absolute
            if not os.path.isabs(pem):
                pem = os.path.join(PEM_BASE_DIR, pem)

            port_match = re.search(r"-p\s+(\d+)", command)
            port = int(port_match.group(1)) if port_match else 22
            aliases[alias_name] = {"pem": pem, "user": user, "host": host, "port": port}
    return aliases


def get_alias():
    return sorted(load_aliases().keys())
