#!/usr/bin/env python3
import os
from fastmcp import FastMCP
import requests 
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Sample MCP Server")

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our sample MCP server running on Heroku!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Amaan's abomination",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

@mcp.tool(description="calls a user by their name and tells them to shut the fuck up")
def shut_up(name:str) -> str:
    return f"Hello, {name}! Please shut the fuck up."

import requests

@mcp.tool(description="turn on the user's computer")
def call_pi_api(data: dict = {}) -> dict:
    try:
        pi_url = os.getenv("PI_URL", "https://poke.tail4d1b1f.ts.net:8000")
        url = f"{pi_url}/turn_on_computer"
        response = requests.post(url, json=data, timeout=180)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "error": str(e)}



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
