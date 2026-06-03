from tools.alias_parser import load_aliases
from tools.ssh_client import execute_remote


def get_environment(environment):
    aliases = load_aliases()
    if environment not in aliases:
        raise Exception(f"{environment} not found")
    return aliases[environment]


# ssh_client.py already wraps with `sudo -i bash -lc "..."`,
# so just try pm2 with common absolute paths — no extra sudo needed.
PM2_COMMAND_MODES = (
    # root with nvm (e.g. gps.agorae)
    "sudo env PATH=/root/.nvm/versions/node/v22.14.0/bin:$PATH /root/.nvm/versions/node/v22.14.0/bin/pm2 {cmd}",
    # ubuntu PM2 daemon started by root — connect via sudo with ubuntu's HOME (e.g. stage.agorae.web)
    "sudo env HOME=/home/ubuntu pm2 {cmd}",
)



def run_pm2(environment, cmd):
    env = get_environment(environment)

    for template in PM2_COMMAND_MODES:
        command = template.format(cmd=cmd)

        result = execute_remote(
            host=env["host"],
            username=env["user"],
            pem_file=env["pem"],
            command=command,
            port=env.get("port", 22),
        )

        output = result.get("output") or ""

        # accept ANY valid pm2 output
        if result["success"] and (
            "│" in output or "online" in output.lower() or "process" in output.lower()
        ):
            return {
                "mode": template,
                "output": output,
                "error": result.get("error", ""),
            }

    return {
        "mode": None,
        "error": f"PM2 not accessible on {environment}",
    }


def list_servers():
    aliases = load_aliases()
    return sorted(aliases.keys())


def pm2_list(environment):
    return run_pm2(environment, "jlist")


def restart_pm2(environment, process_id):
    return run_pm2(environment, f"restart {process_id}")


def pm2_logs(environment, process_id):
    return run_pm2(environment, f"logs {process_id} --lines 50 --nostream")
