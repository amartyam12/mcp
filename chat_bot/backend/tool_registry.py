TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_servers",
            "description": "List all servers",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pm2_processes",
            "description": "Get PM2 process list",
            "parameters": {
                "type": "object",
                "properties": {"server": {"type": "string"}},
                "required": ["server"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restart_process",
            "description": "Restart PM2 process",
            "parameters": {
                "type": "object",
                "properties": {
                    "environment": {"type": "string"},
                    "process_id": {"type": "integer"},
                },
                "required": ["environment", "process_id"],
            },
        },
    },
]
