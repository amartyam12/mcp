from mcp.server.fastmcp import FastMCP
from tools.pm2_tools import pm2_list, restart_pm2, pm2_logs
from tools.alias_parser import get_alias

mcp = FastMCP("AWS PM2 Manager")


@mcp.tool()
def get_servers():
    servers = get_alias()
    return {
        "total": len(servers),
        "servers": servers
    }


@mcp.tool()
def get_pm2_processes(server: str):
    return pm2_list(server)

@mcp.tool()
def get_pm2_list(environment: str):
    return pm2_list(environment)


@mcp.tool()
def restart_process(environment: str, process_id: int):
    return restart_pm2(environment, process_id)


@mcp.tool()
def get_logs(environment: str, process_id: int):
    return pm2_logs(environment, process_id)


@mcp.tool()
def get_test():
    return ["AAA", "BBB", "CCC"]


if __name__ == "__main__":
    if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )