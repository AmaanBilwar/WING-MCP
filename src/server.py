#!/usr/bin/env python3
import os
from fastmcp import FastMCP
import requests 
from dotenv import load_dotenv
from fastmcp.server.auth.providers.github import GitHubProvider


load_dotenv()


# Debug: Check if environment variables are set
client_id = os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID")
client_secret = os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET")
base_url = os.getenv("FASTMCP_SERVER_AUTH_GITHUB_BASE_URL")

print(f"GitHub OAuth Config:")
print(f"  Client ID: {'SET' if client_id else 'NOT SET'}")
print(f"  Client Secret: {'SET' if client_secret else 'NOT SET'}")
print(f"  Base URL: {base_url or 'NOT SET'}")
print(f"  Expected Callback URL: {base_url}/auth/callback" if base_url else "  Expected Callback URL: NOT SET")

auth_provider = GitHubProvider(
    client_id=client_id,
    client_secret=client_secret,
    base_url=base_url,
)


mcp = FastMCP("Sample MCP Server", auth=auth_provider)


# @mcp.tool(description="Login to the MCP server using Github")
# async def get_user_info() -> dict:
#     """Returns information about the authenticated GitHub user."""
#     from fastmcp.server.dependencies import get_access_token
    
#     token = get_access_token()
#     # The GitHubProvider stores user data in token claims
#     return {
#         "github_user": token.claims.get("login"),
#         "name": token.claims.get("name"),
#         "email": token.claims.get("email")
#     }

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
