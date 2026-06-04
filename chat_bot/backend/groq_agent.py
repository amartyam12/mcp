import json
import os
from groq import Groq
from mcp_client import call_tool
from tool_registry import TOOLS


from dotenv import load_dotenv

load_dotenv()



client = Groq(api_key=os.getenv("GROQ_API_KEY"))
async def chat(message):
    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": """
You are a DevOps assistant.
You have access to MCP tools:
- get_servers
- get_pm2_processes
- get_pm2_list
- restart_process
- get_logs
When needed, call tools.
After receiving tool output, explain the result clearly.
""",
            },
            {"role": "user", "content": message},
        ],
        tools=TOOLS,
        tool_choice="auto",
    )
    msg = response.choices[0].message
    if not msg.tool_calls:
        return msg.content
    tool_call = msg.tool_calls[0]
    tool_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    tool_result = await call_tool(tool_name, args)

    if hasattr(tool_result, "content"):
        tool_content = "\n".join(
            item.text
            for item in tool_result.content
            if hasattr(item, "text")
        )
    else:
        tool_content = str(tool_result)

    print("SENDING TO GROQ:")
    print(tool_content)
    final_response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": """
            You are a DevOps assistant.

            Never explain JSON structures.
            Never say 'The JSON object contains'.
            Never describe the format of the tool output.

            When tool output contains servers:
            - Present them as a clean server list.

            When tool output contains PM2 processes:
            - Present them as a process table.

            When tool output contains logs:
            - Show the logs.

            When tool output contains a success message:
            - State the action succeeded.

            Respond like an operations engineer, not like a JSON analyst.
            """
            },
            {"role": "user", "content": message},
            {"role": "assistant", "tool_calls": [tool_call]},
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_content,
            },
        ],
    )
    return final_response.choices[0].message.content
