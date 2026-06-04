from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters



SERVER_CMD = StdioServerParameters(
    command="python3",
    args=["/home/amartya-mandal/Desktop/mcp/server.py"],
)


async def call_tool(tool_name, arguments=None):
    if arguments is None:
        arguments = {}
    async with stdio_client(SERVER_CMD) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result
